from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse  # 反向解析
from django.http import *
# 如何区分立即购买进入的订单确认页面和购物车进入的订单确认页面(count参数)
#  立即购买传sku_id 和 count ;购物车 只传sku_id  也可以参数名不同来区分
from utils.views import MyLoginBaseViewMixin, MyLoginRequiredJSONMixin, TransactionAtomicMixin
# django_redis
from django_redis import get_redis_connection
from goods.models import *
from users.models import *
from orders.models import *  # OrderInfo OrderGoods
# django提供的时间格式化工具
from django.utils import timezone
# django 事务
from django.db import transaction
import time
# 分页需要导包
from django.core.paginator import Paginator, Page, EmptyPage
# settings用到的需要导的包
from django.conf import settings
import alipay


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
                    return redirect(reverse('goods:detail', args=(sku_id,)))  # 一个元素必须有逗号
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

                # 直接购买=>将sku_id 和count写入redis 方便提交订单时从redis取出,从而不用区分count的来源
                redis_con.hset('cart_%s' % request.user.id, sku_id, sku_count)
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
            'sku_ids': ','.join(sku_ids),  # [1,2,3,] ==> '1,2,3' # 转换成字符串 贯穿过去不渲染
        }
        return render(request, 'place_order.html', context)
        # 响应结果 渲染html页面

        pass


# 自定义JSON 装饰器来处理ajax请求,前端来跳转
class CommitOrderView(MyLoginRequiredJSONMixin, TransactionAtomicMixin, View):
    """订单确认form表单提交"""

    def post(self, request):
        # 接受用户提交订单的参数,保存到orderinfo 和 ordergoods
        user = request.user  # 登陆用户
        address_id = request.POST.get('address_id')
        pay_method = request.POST.get('pay_method')
        sku_ids = request.POST.get('sku_ids')  # 贯穿回来

        # 校验参数：all([address_id, pay_method, sku_ids])
        if not all([address_id, pay_method, sku_ids]):
            return JsonResponse({'code': 2, 'message': '缺少参数'})
        # 判断地址
        try:
            address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            return JsonResponse({'code': 3, 'message': '地址不存在'})

        # 判断支付方式
        if pay_method not in OrderInfo.PAY_METHOD:  # 避免魔法属性 in ['1','2']  枚举一个道理
            return JsonResponse({'code': 4, 'message': '支付方式错误!'})

        # 从截取sku_ids列表 开始一对多 多的存储
        sku_ids = sku_ids.split(',')  # return列表
        redis_con = get_redis_connection('default')

        sid = transaction.savepoint()  # 事务安全保存点
        try:  # 暴力回滚
            # 创建订单OrderInfo # 先创建商品订单信息
            from django.utils import timezone
            # django提供的时间格式化工具
            order_id = timezone.now().strftime('%Y%m%d%H%M%S') + str(user.id)
            order = OrderInfo.objects.create(
                order_id=timezone.now().strftime('%Y%m%d%H%M%S') + str(user.id),
                user=user,
                address=address,
                total_count=0,
                # total_count  # 后面计算出来修改属性 update
                total_amount=0,  # 后面计算出来修改属性 update
                trans_cost=10,
                pay_method=pay_method,
                status=1,  # 默认是1可以不谢,待支付状态
                trade_id=None
            )

            # 遍历sku_ids
            total_count = 0
            total_sku_amount = 0
            for sku_id in sku_ids:
                for x in range(3):
                    # 循环取出sku，判断商品是否存在
                    try:
                        sku = GoodsSKU.objects.get(id=sku_id)
                    except GoodsSKU.DoesNotExist:
                        transaction.savepoint_rollback(sid)  # 异常回滚
                        return JsonResponse({'code': 5, 'message': '商品不存在!'})

                    # 获取商品数量，判断库存 (redis)
                    sku_count = redis_con.hget('cart_%s' % request.user.id, sku_id)  # bytes
                    sku_count = int(sku_count)
                    # 循环订单每个商品判断库存是否充足  最终判断验证库存
                    if sku_count > sku.stock:
                        transaction.savepoint_rollback(sid)
                        return JsonResponse({'code': 6, 'message': '库存不足!'})

                    time.sleep(1)

                    origin_stock = sku.stock  # 上一次查询的库存
                    new_stock = origin_stock - sku_count  # 计算剩余库存量new_stock
                    new_sales = sku_count + sku.sales  # 顺带更新一下少连一次数据库
                    # 乐观锁的原理是更改库存的时候判断是否是上一次查询出来的库存并到and以后,如果是就更新
                    result = GoodsSKU.objects.filter(id=sku_id, stock=origin_stock).update(stock=new_stock,
                                                                                           sales=new_sales)
                    if 0 == result and x < 2:
                        continue
                    if 0 == result and x == 2:
                        transaction.savepoint_rollback(sid)
                        return JsonResponse({'code': 8, 'message': '下单失败,库存不足乐观锁'})
                    # 减少sku库存
                    # sku.stock -= sku_count
                    # 增加sku销量,保存修改的信息save()
                    # sku.sales += sku_count
                    # sku.save()  # update

                    # 保存订单商品数据OrderGoods(能执行到这里说明无异常)
                    OrderGoods.objects.create(
                        order=order,
                        sku=sku,
                        count=sku_count,
                        price=sku.price,
                        comment='',
                    )
                    # 计算总数和总金额
                    total_count += sku_count
                    # 小计 数量 x 单价 用于计算总金额的桥梁
                    amount = sku_count * sku.price
                    total_sku_amount += amount
                    # 成功就break
                    break

            # 修改订单信息里面的总数和总金额(OrderInfo)
            order.total_count = total_count
            order.total_amount = total_sku_amount + 10  # order.trans_cost
            order.save()
        except Exception as e:
            print(e)
            transaction.savepoint_rollback(sid)
            return JsonResponse({'code': 7, 'message': '下单失败!!'})  # 记得响应
        # 没有异常
        transaction.savepoint_commit(sid)
        # 订单生成后删除购物车(hdel)
        # for sku_id in sku_ids:
        #     redis_con.hdel('cart_%s' % request.user.id, sku_id)
        # redis_con.hdel('cart_%s'%request.user.id,*sku_ids) # 1,2,3 列表｜元祖自动解包

        # 响应结果
        return JsonResponse({'code': 0, 'message': '提交订单成功!'})

    def get(self, request):
        pass


class UserOrderView(MyLoginBaseViewMixin, View):
    def get(self, request, page):
        """提供订单详情"""
        # 查询该登陆所有订单
        orders = request.user.orderinfo_set.all()
        # 遍历所有订单
        for o in orders:
            # 给订单动态绑定属性:订单状态 前台展示需要
            o.status_name = OrderInfo.ORDER_STATUS[o.status]
            # 给订单动态绑定支付方式 前台展示需要
            temp = o.pay_method
            try:
                o.pay_method_name = OrderInfo.PAY_METHOD[temp]
            except Exception as e:
                o.pay_method_name = 2
            # 给订单所关联的sku商品定义容器
            o.skus = []
            # 查询订单中的所有商品
            order_skus = o.ordergoods_set.all()  # 一对多关联
            for order_sku in order_skus:
                sku = order_sku.sku  # 一对一关联
                # 给每个sku商品动态的绑定count对应订单中的总数量字段count前台使用
                sku.count = order_sku.count
                # 给每个sku商品动态的绑定小计,每个sku商品的单价 X 数量
                sku.amount = sku.count * sku.price  # 动态属性*本身属性
                o.skus.append(sku)  # 这里给order_sku绑也可以但是就不能叫做count了因为有这个字段 ,用于前台双重遍历订单并且遍历

        # 分页
        page = int(page)
        try:
            paginator = Paginator(orders, 2)  # 每页两条
            page_orders = paginator.page(page)  # 选第几页
        except EmptyPage:
            # 如果传入的页数不存在 默认给第一页
            page_orders = paginator.page(1)
            page = 1  # 重新赋值为1

        # 页码条
        page_list = paginator.page_range
        context = {
            'orders': page_orders,  # 给分页后的
            'page': page,
            'page_list': page_list,  # 给页码条
        }

        return render(request, 'user_center_order.html', context)


class PayView(MyLoginRequiredJSONMixin, View):
    """对接支付宝支付接口"""

    def post(self, request):
        """接受订单信息order_id 查询订单 创建alipay 调用接口 返回url(json) 跳转"""
        order_id = request.POST.get('order_id')
        if not order_id:
            return JsonResponse({'code': 3, 'message': '缺少订单id'})
        # 校验订单id
        try:
            # 查询该用户提交的该订单号订单,确认是该登陆用户的订单,状态并且是待支付状态,&&支付方式是支付宝
            order = OrderInfo.objects.get(order_id=order_id,
                                          user=request.user,
                                          status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'],  # 类似枚举
                                          pay_method=OrderInfo.PAY_METHODS_ENUM['ALIPAY']
                                          )
        except OrderInfo.DoesNotExist as e:
            return JsonResponse({'code': 2, 'message': '订单不存在'})
        # 创建alipay 对象对接支付宝
        my_alipay = alipay.AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url  测试不要写成空字符串
            # 自己生产的私钥
            app_private_key_path=settings.APP_PRIVATE_KEY_PATH,  # 路径也是能读取出来的
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
            alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2=>2048 openssl
            debug=True  # 默认False  True 是沙箱模式
        )
        # 电脑网站支付，需要跳转到https://openapi.alipay[dev].com/gateway.do? + order_string
        order_string = my_alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount),  # 将浮点数转成字符串
            subject='头条天天生鲜',  # 标题无关太紧要
            return_url=None,
            notify_url=None  # 可选, 不填则使用默认notify url
        )
        # 生成打开支付宝的url
        url = settings.ALIPAY_URL + '?' + order_string

        # 响应url给前台(JsonResponse)
        return JsonResponse({'code': 0, 'message': '支付成功', 'url': url})


"""支付宝相关 私钥加密 公钥解密 填写网站公钥"""
"""returnurl 同步阻塞式 需要公网IP"""
"""notifyurl 异步非阻塞 成本高,天天生鲜需要公网IP"""
"""主动查询订单状态alipay.trade.query,前端轮询"""


class CheckPayView(MyLoginRequiredJSONMixin, View):
    """支付宝查询订单,返回支付宝维护的订单id 并且修改订单的状态为待评价"""

    def get(self, request):
        # 接受订单id
        order_id = request.GET.get('order_id')
        if not order_id:
            return JsonResponse({'code': 2, 'message': '缺少订单id'})
            # 校验订单id
        try:
            # 查询该用户提交的该订单号订单,确认是该登陆用户的订单,状态并且是待支付状态,&&支付方式是支付宝
            order = OrderInfo.objects.get(order_id=order_id,
                                          user=request.user,
                                          # 点带支付去查询待支付,还没支付成功
                                          status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'],  # 类似枚举
                                          pay_method=OrderInfo.PAY_METHODS_ENUM['ALIPAY']
                                          )
        except OrderInfo.DoesNotExist as e:
            return JsonResponse({'code': 2, 'message': '订单不存在'})
        # 创建alipay 对象对接支付宝
        my_alipay = alipay.AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url  测试不要写成空字符串
            # 自己生产的私钥
            app_private_key_path=settings.APP_PRIVATE_KEY_PATH,  # 路径也是能读取出来的
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
            alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2=>2048 openssl
            debug=True  # 默认False  True 是沙箱模式
        )
        # 循环查询,直到成功|失败
        while True:
            # 调用查询接口,读取code 和trade_status 判断订单状态
            response_dict = my_alipay.api_alipay_trade_query(order_id)  # 一种接受商家维护的订单id去查 | 也可以接受支付宝维护的订单id去查
            # 上面的返回值一个字典,包含了支付宝相应给调用者的参数信息 包括 code 和trade_status 和trade_no(支付宝维护的订单id)
            code = response_dict.get('code')
            trade_status = response_dict.get('trade_status')
            if code == '10000' and trade_status == 'TRADE_SUCCESS':
                order.trade_id = response_dict.get('trade_no')
                order.status = OrderInfo.ORDER_STATUS_ENUM['UNCOMMENT']
                order.save()
                return JsonResponse({'code': 0, 'message': '支付ok'})
            elif code == '40004' or (code == '10000' and trade_status == 'WAIT_BUYER_PAY'):
                # 有待商量,继续等待继续查询
                continue
            else:
                # 失败
                return JsonResponse({'code': 4, 'message': '支付失败'})


class OrderCommentView(MyLoginRequiredJSONMixin, View):
    def get(self, request, order_id):
        """提供评论页面"""
        try:
            order = OrderInfo.objects.get(order_id=order_id, user=request.user)
        except OrderInfo.DoesNotExist:
            return redirect(reverse("order:info", args=(1,)))

        order.status_name = OrderInfo.ORDER_STATUS[order.status]
        order.skus = []
        # 获取订单关联的所有商品
        order_skus = order.ordergoods_set.all()
        for order_sku in order_skus:
            sku = order_sku.sku  # 找到sku
            sku.count = order_sku.count  # 数量
            sku.amount = sku.price * sku.count  # 小计
            order.skus.append(sku)
        return render(request, "order_comment.html", {'order': order})

    def post(self, request, order_id):  # post 请求自己会把get中的url中的参数也会传过来,一个url限制2个请求
        """处理提交评论的post请求"""
        user = request.user
        try:
            order = OrderInfo.objects.get(user=user, order_id=order_id)
        except OrderInfo.DoesNotExist:
            return redirect(reverse('order:info', args=(1,)))
        # 接受total_count的目的是前台知道前台有多少个sku,也可以是认为获取评论条数
        total_count = request.POST.get('total_count')  # str
        total_count = int(total_count)
        for i in range(1, total_count + 1):
            sku_id = request.POST.get('sku_%d' % i)
            content = request.POST.get('content_%d' % i)
            try:
                # 后台校验每个商品是不是该订单中的
                order_goods = OrderGoods.objects.get(order=order, sku_id=sku_id)
            except OrderGoods.DoesNotExist:
                continue
            order_goods.comment = content  # 保存每个评论
            order_goods.save()

            # 清除商品详情缓存
            # cache.delete("detail_%s" % sku_id)
        order.status = OrderInfo.ORDER_STATUS_ENUM['FINISHED']
        order.save()
        # return redirect(reverse('order:info', kwargs={'page': 1}))
        return redirect(reverse('order:info',  kwargs={'page': 1}))
