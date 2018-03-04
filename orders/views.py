from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse  # 反向解析

# 如何区分立即购买进入的订单确认页面和购物车进入的订单确认页面(count参数)
#  立即购买传sku_id 和 count ;购物车 只传sku_id  也可以参数名不同来区分
from utils.views import MyLoginBaseViewMixin
# django_redis
from django_redis import get_redis_connection
from goods.models import *
from users.models import *


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
                temp_skus.append(sku)  # 循环记录sku


        else:
            # 如果是从详情页立即购买过来的

            # 查询商品数据

            # 商品的数量从request中获取,并且try校验

            # 判断库存 ,立即购买没有判断库存

            pass
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
        }
        return render(request, 'place_order.html', context)
        # 响应结果 渲染html页面

        pass
