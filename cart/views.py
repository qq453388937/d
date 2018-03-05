from django.shortcuts import render
from django.views.generic import View
from django.http import *
from goods.models import *
from django_redis import get_redis_connection
import json

# 商品详情页面,添加购物车 ==> 入口,登陆和非登陆都可以添加
#  购物车存储到redis 用 hash 哈希存储
#  hmset cart_userid1 草莓(sku_id)=>2 芒果(sku_id) 3
# eg: cart_1 1:3 2:2 3:1 ...... 字段名是sku_id value是个数
# 读取方法 cart_dict = redis_coon.hgetall('cart_userid')
# cart_dict={ sku_id:count1, sku_id2:count2 }
# 注意:如果涉及到比较和计算注意统一转换对应的类型
#  for val in cart_dict.values():
#       pass
#
# ############################################################# #

# 加入购物车
# 收集 user_id  sku_id count 3个信息
# hset cart_userid sku_id count
# ajax post 请求!
"""
{
'code':0,
'message':'添加购物车成功'
}
{
'code':1,
'message':'用户未登录'
}
{
'code':1,
'message':'库存不足'
}
"""


class AddCart(View):
    def post(self, request):
        """接受购物车参数,校验,保存"""
        """(django_redis为什么要保存bytes字节的,读取和写入速度是最快的)"""
        '''"cart:{'sku_id1':count1,'sku_id2':count2}" cookie使用json字符串
                  因为浏览器的同源策略,每个用户的cookie是自己的所以键可以是重复的,
                  用户每次请求只会带上自己的cookie,不会带上别人的可以区分每个人,所以key可以是一样的cart可以这么使用
                  json 模块 技术支持
                  json.dumps   字典转json字符串
                  json.loads   json字符串转字典
                  注: 转换过程中value的类型不变,进入如一'''
        # 判断用户是否登陆
        # if not request.user.is_authenticated():
        #     return JsonResponse({'code': 1, 'message': '用户未登陆'})  # 先做登陆的
        # 接受购物车参数,user_id,sku_id count  ,信息

        sku_id = request.POST.get('sku_id')  # 字符串
        count = request.POST.get('count')  # 字符串

        # 校验参数all() user_id 不需要校验 因为购物车不需要登陆,登陆里面直接通过request.user.idd 取就可以了
        if not all([sku_id, count]):
            return JsonResponse({'code': 2, 'message': '缺少参数'})
        # 校验sku_id 是否合法
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'code': 3, 'message': '缺少参数'})
        # 校验count 是否合法
        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'code': 4, 'message': '商品数量错误'})

        # 判断库存是否超出,加入购物车的数量和库存比较
        if count > sku.stock:
            return JsonResponse({'code': 5, 'message': '库存不足'})
        if request.user.is_authenticated():
            # 保存购物车数据到redis
            redis_con = get_redis_connection('default')
            # 需要查询该用户保存到购物车的sku_id数据是否存在,如果存在的话累加,不存在的话直接赋值OK!
            origin_count = redis_con.hget('cart_%s' % request.user.id, sku_id)
            if origin_count is not None:  # 存在累加
                count += int(origin_count.decode())  # django_redis保存的是bytes字节类型需要转换
            # 累加完毕以后再次判断库存
            """问题?每个用户都能添加98个逻辑是否正确"""
            if count > sku.stock:
                return JsonResponse({'code': 5, 'message': '库存不足'})
            redis_con.hset('cart_%s' % request.user.id, sku_id, count)  # 有问题!重复的会被覆盖,应该先查询一下判断是否累加

            # 前台需要展示购物车的总数量这里需要查询redis 计算总数量
            cart_dict = redis_con.hgetall('cart_%s' % request.user.id)
            cart_num = 0
            for v in cart_dict.values():
                cart_num += int(v.decode())
            # 相应JsonResponse 根据情况不同code不同json不同
            return JsonResponse({'code': 0, 'message': '添加购物车成功', 'cart_num': cart_num})
        else:  # 用户未登陆
            # cookie =>'cart' : '{'1':1,'2':3}'
            cookies_str = request.COOKIES.get('cart')  # '{'1':1,'2':3}'
            if cookies_str:  # 和redis一样存在累加
                cart_dict = json.loads(cookies_str)  # {'1':1,'2':3}
            else:
                cart_dict = {}
            # 需要保证sku_id=》 cart_dict 的key的类型一致才能in
            if sku_id in cart_dict:  # {'1':1,'2':3} 刚好sku_id 是字符串类型ｏｋ
                number = cart_dict[sku_id]  # 转换过程中value的类型不变
                count += number  # 走到这里count肯定是数字转换过了
            if count > sku.stock:  # cookie 也要再次判断累加后的库存
                return JsonResponse({'code': 5, 'message': '库存不足'})
            # 更新最新的（累加过或者全新的）字典
            cart_dict[sku_id] = count
            cart_num = 0
            # 计算cookie中的购物车总数
            for value in cart_dict.values():
                cart_num += value  # 这里不需要转换 存的时候是int
            cart_str = json.dumps(cart_dict)
            # 创建response => render JsonResponse HttpResponse HttpRedirect Redirect 五大类都可以返回response
            response = JsonResponse({'code': 0, 'message': '添加购物车成功', 'cart_num': cart_num})
            response.set_cookie('cart', cart_str)
            return response

            # 伪代码
            # response.set_cookie('cart','cart_json')


class UpdateCart(View):
    def post(self, request):
        """+ -  手动输入购物车"""
        # 获取参数 sku_id count
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        # 校验参数all
        if not all([sku_id, count]):
            return JsonResponse({'code': 1, 'messsage': '缺少参数'})
        # 判断商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'code': 2, 'messsage': '商品不存在'})
        # 判断count是否是int
        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'code': 3, 'messsage': '商品数量错误'})
        # 判断库存
        if count > sku.stock:
            return JsonResponse({'code': 3, 'messsage': '库存不足'})
        # 判断用户是否登陆
        if request.user.is_authenticated():
            # 如果用户登陆,将修改的购物车信息存储导redis中
            redis_con = get_redis_connection('default')
            # 幂等做法
            redis_con.hset('cart_%s' % request.user.id, sku_id, count)
            return JsonResponse({'code': 0, 'messsage': 'ok!'})
            # # 非幂等做法
            # cart_dict = redis_con.hgetall()
            # if sku_id.encode() in cart_dict:
            #     origin_count = cart_dict[sku_id.encode()]
            #     count += int(origin_count.decode())
            # cart_dict[sku_id.encode()] = count
        else:
            # 如果用户没有登陆 存储用户修改的购物车信息到cookie中
            cookies_str = request.COOKIES.get('cart')
            if cookies_str:
                cart_dict = json.loads(cookies_str)
            else:
                cart_dict = {}
            cart_dict[sku_id] = count
            cookies_str = json.dumps(cart_dict)
            # 响应对应的JsonResponse
            http_response = JsonResponse({'code': 0, 'messsage': 'ok!'})
            http_response.set_cookie('cart', cookies_str)
            return http_response


class DeleteCart(View):
    def post(self, request):
        # 接受参数
        sku_id = request.POST.get('sku_id')
        # 校验参数all
        if not sku_id:
            return JsonResponse({'code': 1, 'message': '参数sku_id不能为空'})
        # 判断sku_id是否合法
        try:
            GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'code': 1, 'message': '删除的商品sku_id不存在'})
        # 判断用户是否登陆  # 响应对应的JsonResponse
        if request.user.is_authenticated():
            # 登陆删除redis
            redis_conn = get_redis_connection('default')
            redis_conn.hdel('cart_%s' % request.user.id, sku_id)  # hdel(userinfo,name)删除一个字段
            return JsonResponse({'code': 0, 'message': '删除ok!'})
        else:
            # 未登录删除cookie
            cookies_str = request.COOKIES.get('cart')
            if cookies_str:
                cart_dict = json.loads(cookies_str)
                del cart_dict[sku_id]
                cookies_str = json.dumps(cart_dict)
                response = JsonResponse({'code': 0, 'message': '删除ok!'})
                response.set_cookie('cart', cookies_str)
                return response
            else:
                return JsonResponse({'code': 1, 'message': '购物车为空不能删除!'}) # 恶意调用删除


class CartInfo(View):
    """用户不用登陆就可以看购物车信息"""

    def get(self, request):
        """用户登陆和未登录时，查询购物车信息，并且渲染页面==> 购物车列表"""
        if request.user.is_authenticated():
            redis_client = get_redis_connection('default')
            user_id = request.user.id
            # redis读取出来的是bytes类型，读写速度最快
            cart_dict = redis_client.hgetall('cart_%s' % request.user.id)
        else:
            cookie_str = request.COOKIES.get('cart')
            if cookie_str:
                # 字典类型 {'1':1,'2':2}
                cart_dict = json.loads(cookie_str)
            else:
                cart_dict = {}
        total_money_amount = 0
        totol_count = 0
        temp_arr = []
        for sku_id, count in cart_dict.items():
            try:
                sku = GoodsSKU.objects.get(id=sku_id)
            except GoodsSKU.DoesNotExist:
                continue

            sku.count = int(count)  # 统一处理redis和cookie  动态属性 数量
            # 小计 商品的价格 X 数量
            sku.amount = sku.count * sku.price  # 动态属性 小计
            total_money_amount += sku.amount  # 只有cart_dict 字典是不够的，还要把小计传过去,所以记录，需要列表嵌套多个GoodsSKU对象
            # 并且多个GoodsSKU对象动态的添加小计和总数，动态语言的特性
            totol_count += sku.count
            temp_arr.append(sku)
        # 构造上下文
        context = {
            'total_amount': total_money_amount,  # 总金额
            'totol_count': totol_count,  # 总个数
            'skus': temp_arr,
        }
        # 渲染模板
        return render(request, 'cart.html', context)
