from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse  # 反向解析

# 如何区分立即购买进入的订单确认页面和购物车进入的订单确认页面(count参数)
#  立即购买传sku_id 和 count ;购物车 只传sku_id  也可以参数名不同来区分
from utils.views import MyLoginBaseViewMixin, MyLoginRequiredJSONMixin, JsonResponse
# django_redis
from django_redis import get_redis_connection
from goods.models import *
from users.models import *
from orders.models import *  # OrderInfo OrderGoods
# django提供的时间格式化工具
from django.utils import timezone


# 订单确认展示问题
# 用户需要登陆才能结算,进入确认页面,所以需要第一个父类继承MyLoginBaseViewMixin
class PlaceOrderView(MyLoginBaseViewMixin, View):
    """订单确认"""

    def post(self, request):
        """购物车去结算|和|详情页立即购买进入订单确认页面"""

        # 获取参数 sku_ids,count
        sku_ids = request.POST.getlist('sku_ids')
        count = request.POST.get('count')
        # 校验sku_ids 参数 not
        if not sku_ids:
            return redirect(reverse('cart:info'))
        redis_con = get_redis_connection('default')
        # 校验count 参数 用于区分用户是从立即购买还是购物车进入的
        temp_skus = []  # 需要容器存下传导前台
        total_sku_amount = 0
        total_money_amount = 0
        total_amount = 0
        trans_cost = 10  # 邮费
        if count is None:
            # 购物车里过来的不用判断库存是因为已经判断过了通过增删改
            # 如果是购物车过来的 redis
            # c查询商品数量
            cart_dict = redis_con.hgetall('cart_%s' % request.user.id)
            for sku_id in sku_ids:  # sku_id ===> string 字符串类型的
                # 查询商品数据
                try:
                    sku = GoodsSKU.objects.get(id=sku_id)
                except GoodsSKU.DoesNotExist:
                    return redirect(reverse('cart:info'))
                #  redis_con.hget('cart_%s'%request.user.id,sku_id)  ???
                # 查询redis得到商品数量 sku_count 是bytes类型
                # sku_count = redis_con.hget('cart_%s'%request.user.id,sku_id) 也可以
                sku_count = cart_dict[sku_id.encode()]  # cart_dict是bytes类型的需要转换
                sku_count = int(sku_count)
                # 小计 = mysql中的price * redis中的sku_count
                amount = sku.price * sku_count
                # 数量
                sku.sku_count = sku_count  # 动态添加属性
                # 总数量
                total_sku_amount += sku_count
                # 总金额
                total_money_amount += amount
                sku.amount = amount
                sku.count = sku_count
                temp_skus.append(sku)  # 循环记录sku
        else:
            # 如果是从详情页点立即购买过来的
            # 查询商品数据
            for sku_id in sku_ids:
                try:
                    sku = GoodsSKU.objects.get(id=sku_id)
                except GoodsSKU.DoesNotExist:
                    return redirect(reverse('goods:index'))

                # 商品的数量从request中获取,并且try校验
                try:
                    sku_count = int(count)
                except Exception as e:
                    return redirect(reverse('cart:info'))

                # 判断库存 ,立即购买没有判断库存
                if sku_count > sku.stock:
                    return redirect(reverse('goods:detail', args=(sku_id,))) # 一个元素必须有逗号
                amount = sku_count * sku.price
                # 数量
                sku.sku_count = sku_count  # 动态添加属性
                # 总数量
                total_sku_amount += sku_count
                # 总金额
                total_money_amount += amount
                sku.amount = amount
                sku.count = sku_count
                temp_skus.append(sku)  # 循环记录sku

                # 将sku_id 和count写入redis 方便提交订单时从redis取出
                redis_con.hset('cart_%s' % request.user.is_authenticated(), sku_id, sku_count)
        # 实付款
        total_amount = total_money_amount + trans_cost  # 循环完加上邮费,统一加在if else外面  实付款
        # 查询用户地址信息
        try:
            address = Address.objects.filter(user=request.user).latest('create_time')
        except Address.DoesNotExist:
            address = None  # 页面可以没有地址,点提交订单的时候可以判断
        # request.user.address_set.latest('create_time')
        # 构造上下文
        context = {
            'skus': temp_skus,
            'total_amount': total_amount,
            'total_count': total_sku_amount,
            'total_sku_amount': total_money_amount,
            'trans_cost': trans_cost,
            # '': total_money_amount,
            'address': address,
            'sku_ids': ','.join(sku_ids),  # [1,2,3,] ==> '1,2,3'
        }
        return render(request, 'place_order.html', context)
        # 响应结果 渲染html页面

        pass


class CommitOrderView(MyLoginRequiredJSONMixin, View):
    """订单确认form表单提交"""
    def post(self, request):
        # 接受用户提交订单的参数,保存到orderinfo 和 ordergoods
        user = request.user # 登陆用户
        address_id = request.POST.get('address_id')
        pay_method = request.POST.get('pay_method')
        sku_ids = request.POST.get('sku_ids')

        # 校验参数：all([address_id, pay_method, sku_ids])
        if not all([address_id, pay_method, sku_ids]):
            return JsonResponse({'code': 2, 'message': '缺少参数'})
        # 判断地址
        try:
            address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            return JsonResponse({'code': 3, 'message': '地址不存在'})

        # 判断支付方式
        if pay_method not in OrderInfo.PAY_METHOD:
            return JsonResponse({'code': 4, 'message': '支付方式错误!'})

        # 截取出sku_ids列表
        sku_ids = sku_ids.split(',')  # return列表
        redis_con = get_redis_connection('default')
        # 创建订单OrderInfo # 先创建商品订单信息
        order = OrderInfo.objects.create(
            order_id=timezone.now().strftime('%Y%m%d%H%M%S')+str(user.id),
            user=user,
            address=address,
            # total_count  # 后面计算出来修改属性
            total_amount=0,
            trans_cost=10,
            pay_method=pay_method,
            trade_id=None
        )

        # 遍历sku_ids
        total_count = 0
        total_sku_amount = 0
        for sku_id in sku_ids:
            # 循环取出sku，判断商品是否存在
            try:
                sku = GoodsSKU.objects.get(id=sku_id)
            except GoodsSKU.DoesNotExist:
                return JsonResponse({'code': 5, 'message': '商品不存在!'})
            # 获取商品数量，判断库存 (redis)
            sku_count = redis_con.hget('cart_%s' % request.user.id, sku_id)
            sku_count = int(sku_count)
            # 循环订单每个商品判断库存是否充足
            if sku_count > sku.stock:
                return JsonResponse({'code': 6, 'message': '库存不足!'})

            # 小计 数量 x 单价
            amount = sku_count * sku.price
            # 减少sku库存
            sku.stock -= sku_count
            # 增加sku销量,保存修改的信息save()
            sku.sales += sku_count
            sku.save()

            # 保存订单商品数据OrderGoods(能执行到这里说明无异常)
            OrderGoods.objects.create(
                order=order,
                sku=sku,
                count=sku_count,
                price=sku.price
            )
            # 计算总数和总金额
            total_count += sku_count
            total_sku_amount += amount

        # 修改订单信息里面的总数和总金额(OrderInfo)
        order.total_count = total_count
        order.total_amount = total_sku_amount + 10
        # 订单生成后删除购物车(hdel)

        # 响应结果
        return JsonResponse({'code': 0, 'message': '提交订单成功!'})

    def get(self, request):
        pass
