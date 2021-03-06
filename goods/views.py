from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
# django 的view
from django.views.generic import View
from django.core.urlresolvers import reverse
from django_redis import get_redis_connection

from goods.models import *
# django 缓存工具包导入 cache
from django.core.cache import cache

# 分页需要导包
from django.core.paginator import *

import json


# 主页无需登陆即可访问添加购物车


class BaseCartView(View):
    """查询未登陆和登陆时购物车的数据"""

    def get_cart_num(self, request):
        cart_num = 0
        if request.user.is_authenticated():
            """需求是：用户登陆了才会计算购物车信息"""
            # 创建redis
            redis_client = get_redis_connection('default')  # alt+enter 自动导入
            # hgetall() 读取购物车数据 hset key field value    key带上用户id用于主键区分每个用户的购物车
            # 每个用户都有自己的哈希对象，每个用户自己特有的购物车
            # %s 占位后面可以直接填数字
            cart_dict = redis_client.hgetall('cart_%s' % request.user.id)  # 获取所有字段:value键值对组合
            # cart_dict = redis_client.hgetall('cart_%s' % 666)  # 获取所有字段:value键值对组合
            cart_num = 0
            for val in cart_dict.values():  # 遍历值
                # print(type(val))
                # print(val)  # b'3'
                # print(int(val))  # 3
                # print(type(int(val)))  # <class 'int'>
                cart_num += int(val)  # 计算购物车的商品总数量 byte类型，只有字符串可以直接转int，如果是汉子必须decode()一下先
            # cart_num = 777777777  # 测试假数据,假设查出来了
            # context['cart_num'] = cart_num # 放到外面去
            # context.update({'cart_num': 777777777})
            # context.update(cart_num=777777777)
        else:
            cookie_str = request.COOKIES.get('cart')
            if cookie_str:
                cart_dict = json.loads(cookie_str)
            else:
                cart_dict = {}
            # 遍历cart_dict 求和
            for value in cart_dict.values():
                cart_num += value  # int 类型不用转换 表里如一  + int可以做优化提取到if 外面

        return cart_num


class IndexView(BaseCartView):

    def get(self, request):
        """查询主页商品数据"""
        # 上来先去读取缓存的数据
        context = cache.get('index_page_data')  # 存进去是什么取出来就是什么.不需要转换
        # 没有缓存 去查询
        if context is None:
            print('没有缓存查询数据库')
            # 查询用户ｕｓｅｒ信息 ,不需要 在request中,视图中也不需要通过request点出来直接user

            # 查询商品分类信息
            categorys = GoodsCategory.objects.all()
            # 查询图片轮播信息
            goods_banners = IndexGoodsBanner.objects.all().order_by('index')
            # 查询商品活动信息
            promotion_banners = IndexPromotionBanner.objects.all().order_by('index')
            # 查询主页分类商品列表信息,动态的绑定属性绑定到六大分类中
            for category in categorys:
                # 分组查询出来 ,六大分类
                title_banners = IndexCategoryGoodsBanner.objects.filter(category=category).filter(display_type=0)
                category.title_banners = title_banners  # 动态的添加对象的属性 ,for 循环一次每个对象动态的添加一个属性
                image_banners = IndexCategoryGoodsBanner.objects.filter(category=category).filter(display_type=1)
                category.image_banners = image_banners  # 动态的添加对象的属性 ,for 循环一次每个对象动态的添加一个属性

            # 构造上下文
            context = {
                'categorys': categorys,
                'goods_banners': goods_banners,
                'promotion_banners': promotion_banners,
                # 'cart_num': cart_num,
            }
            # 设置缓存contexnt 一个小时过期,无论是否缓存,其中购物车的信息是单独查询的
            cache.set('index_page_data', context, 3600)

        else:  # 有缓存
            print('取redis缓存的context')
        # 查询购物车信息(购物车和缓存毛线关系都没有) ,购物车的信息不能放在缓存当中,要单独查询构造到原来已有的上下文中
        cart_num = 88  # 原先假数据,测试数据
        context.update(cart_num=cart_num)  # 传入一个字典变量解包,或者{},或者命名参数
        # 获得购物车数量
        cart_num = self.get_cart_num(request)  # 封装到方法里去了
        context['cart_num'] = cart_num

        # 渲染模板
        return render(request, 'index.html', context)

    def post(self, request):
        pass


class DetailView(BaseCartView):
    """商品详情页，不需要用户登陆也可以访问
        # 测试redis是否存取一个类型
        # g = Goods()
        # g.name = 'goods666'
        # dict_test = {'name': 'pxd', 'age': 18}
        # cache.set('dict_test', g, 3600)
        # ret = cache.get('dict_test')
        # print(type(ret))  # <class 'dict'>
        # print(ret)  # {'name': 'pxd', 'age': 18}
        # print(ret.name)  # goods666
        # print(ret['name'])  # pxd
        """

    def get(self, request, sku_id):

        # return HttpResponse('testok')
        # 查询用户，不用查

        # 查询商品ＳＫＵ信息
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:  # 用户手动传过来的
            return redirect(reverse('goods:index'))

        # 查询商品分类信息
        categorys = GoodsCategory.objects.all()
        # 查询商品详情介绍信息
        desc = sku.goods.desc
        # 查询商品评价信息  订单商品表中的comment，一对多
        sku_orders = sku.ordergoods_set.all().order_by('-create_time')[:30]  # 前30条最近的评论
        if sku_orders:
            for x in sku_orders:  # 订单商品信息扩展2个字段ctime,username, 要用这2个字段没有在其他表中融合导一起
                """strftime将一个tm结构格式化为一个字符串，strptime则是将一个字符串格式化为一个tm结构。"""
                x.ctime = sku_orders.ctime = x.create_time.strftime('%Y-%m-%d %H:%M:%S')  # str
                x.username = x.order.user.username  # 方便模板使用
        else:
            sku_orders = []
        # 查询最新推荐信息 从数据库中获取最新发布的两件商品
        new_skus = GoodsSKU.objects.filter(category=sku.category).order_by('-create_time')[:2]

        # 补充需求： 查询相同SPU商品其他规格商品信息
        others_skus_my = GoodsSKU.objects.filter(goods__name=sku.goods.name).exclude(id=sku.id)
        # other_skus = sku.goods.goodssku_set.exclude(id=sku.id)
        other_skus = sku.goods.goodssku_set.filter(~Q(id=sku.id))
        # 上下文
        context = {
            'sku': sku,
            'categorys': categorys,
            'orders': sku_orders,
            'new_skus': new_skus,
            'others_skus_my': others_skus_my,
            'other_skus': other_skus,
        }
        cart_num = self.get_cart_num(request)
        context['cart_num'] = cart_num
        # 查询购物车信息 redis
        if request.user.is_authenticated():  # 购物车最全注释
            """需求是：用户登陆了才会计算购物车信息
            这么写方便上面缓存，如果不需要缓存，一次构造完上下文即可
            """
            # 创建redis
            redis_client = get_redis_connection('default')  # alt+enter 自动导入
            # hgetall() 读取购物车数据 hset key field value    key带上用户id用于主键区分每个用户的购物车
            # 每个用户都有自己的哈希对象，每个用户自己特有的购物车
            # %s 占位后面可以直接填数字
            # cart_dict = redis_client.hgetall('cart_%s' % request.user.id)  # 获取所有字段:value键值对组合
            # cart_dict = redis_client.hgetall('cart_%s' % 666)  # 获取所有字段:value键值对组合
            # cart_num = 0
            # for val in cart_dict.values():  # 遍历值
            # print(type(val))
            # print(val)  # b'3'
            # print(int(val))  # 3
            # print(type(int(val)))  # <class 'int'>
            # cart_num += int(val)  # 计算购物车的商品总数量 byte类型，只有数字和字母可以直接转int，如果是汉子必须decode()一下先
            # cart_num = 777777777  # 测试假数据,假设查出来了
            # context['cart_num'] = cart_num
            # context.update({'cart_num': 777777777})
            # context.update(cart_num=777777777)

            # 记录最近浏览信息(redis) 添加前先去重
            redis_client.lrem('history_%s' % request.user.id, 0,
                              sku_id)  # count=0 删除所有value 是sku_id值的,count>0 从左往右删除count个,count<0从右往左删除count个
            # 添加
            redis_client.lpush('history_%s' % request.user.id, sku_id)
            # 最多保存５个
            redis_client.ltrim('history_%s', 0, 4)

        # 渲染模板
        return render(request, 'detail.html', context)

    def post(self, request):
        pass


class ListView(BaseCartView):
    def get(self, request, category_id, page_num):
        """渲染模板,查询分页,排序"""
        # 查询用户要看的商品分类,category_id 对应的
        # /list/category_id/page_num?sort=default
        try:
            category = GoodsCategory.objects.get(id=category_id)  # url传参可能非法输入
        except GoodsCategory.DoesNotExist:
            return redirect(reverse('goods:index'))
        # 查询所有商品分类
        categorys = GoodsCategory.objects.all()  # 6条 6大分类
        # 查询新品推荐 2个
        new_skus = GoodsSKU.objects.filter(category=category).order_by('-create_time')[:2]

        # 查询category_id 对应的所有分类sku信息，根据URL GET传递过来的参数
        sort = request.GET.get('sort', 'default')
        # 根据排序来查询过滤skus 信息
        if sort == 'price':
            skus = GoodsSKU.objects.filter(category=category).order_by('price')  # 价格正序
        elif sort == 'hot':
            skus = GoodsSKU.objects.filter(category=category).order_by('-sales')  # 销量倒叙
        else:  # list/1/1?sort=dwadwa 非法操作或者  # 不传|第一次请求
            skus = GoodsSKU.objects.filter(category=category)
            # 用户非法输入，重置sort 校正传给模板（前端URL参数重置使用），后端已经default
            sort = 'default'
        # 构造上下文
        context = {}
        # 查询购物车信息 redis
        cart_num = self.get_cart_num(request)  # 直接放到上下文中ok
        # if request.user.is_authenticated():
        #     redis_client = get_redis_connection('default')  # alt+enter 自动导入
        #     # hgetall => Return a Python dict of the hash’s name/value pairs
        #     cart_dict = redis_client.hgetall('cart_%s' % request.user.id)  # ('cart_%s' % 666 获取所有字段:value键值对组合
        #     cart_num = 0
        #     for val in cart_dict.values():  # 遍历值
        #         cart_num += int(val)  # 计算购物车的商品总数量 byte类型，只有数字和字母可以直接转int，如果是汉子必须decode()一下先
        #     # context.update({'cart_num': 77}|cart_num=77|dict(cart_num=77))
        #     context['cart_num'] = cart_num
        # 分页
        paginator = Paginator(skus, 2)  # 每页2条 ,惰性加载，懒加载，只有模板用到该数据的时候查询数据库
        page_num = int(page_num)  # url 传参过来的是字符串
        try:
            # 获取用户要看的那一页
            page_skus = paginator.page(
                page_num)  # paginator.page(1) Returns a Page object for the given 1-based page number.
        except EmptyPage as e:
            page_skus = paginator.page(1)
        # 获取页码列表
        page_list = paginator.page_range

        # 构造上下文
        context = {
            'category': category,
            'categorys': categorys,
            'new_skus': new_skus,
            # 'skus':skus, # 只传分页的skus 不传所有的skus
            'page_skus': page_skus,  # 传分页的skus
            'page_list': page_list,
            'sort': sort,  # 前端URL参数重置使用(非法操作),前台分页使用=> 分页保证排序
            'cart_num': cart_num,
        }

        # 渲染模板
        return render(request, 'list.html', context)


class MySearchView(View):
    def get(self, request):
        return render(request, 'mysearch.html')


class GoodViewOld(View):
    """from django.views.generic import View
    django.guardian 对象级别的权限

F:\pythonjieshiqi2\Lib\site-packages\pip\compat\__init__.py
if sys.version_info >= (3,):
    def console_to_str(s):
        try:
            return s.decode(sys.__stdout__.encoding)
        except UnicodeDecodeError:
            return s.decode('utf_8') ==> gbk

    """
    from django.views.generic.base import View
    from django.views.generic import ListView

    def get(self, request):
        goods_list = GoodsSKU.objects.all()
        container = []
        # for good in goods_list: # image 和datetime 会出错的!!!!!
        #     container.append({
        #         "name": good.name,
        #         "desc": good.desc,
        #         "create_time": good.create_time,
        #         "update_time": good.update_time,
        #     })
        # return JsonResponse({"data": container}, safe=False)

        # from django.forms.models import model_to_dict
        # """model_to_dict 的缺点是不能序列化图片Image_file"""
        # for good in goods_list:
        #     container.append(model_to_dict(good))
        # return JsonResponse({"data": container}, safe=False)

        from django.core.serializers import serialize
        ret = serialize("json", goods_list)  # 可以序列化所有类型
        # return JsonResponse(ret,safe=False) # serialize不能使用json返回
        return HttpResponse(ret, content_type="application/json")

    # return HttpResponse(json.dumps(container), content_type="application/json") # datetime.datetime(2017, 10, 16, 3, 3, 5, 257969, tzinfo=<UTC>) is not JSON serializable


from rest_framework.views import APIView

from .myserializer import *
from rest_framework.response import Response
from rest_framework import status


class GoodAPIView(APIView):
    def get(self, request, format=None):
        from django.core.serializers import serialize
        # goods_list = GoodsSKU.objects.all()
        goods_list = GoodsSKU.objects.all()[:100]
        serializer = GoodsSKUSerializer(goods_list, many=True)  # list 多个对象需传many = true ,路径序列化后是完整路径
        return Response(serializer.data)  # goods_json.data 数据

    def post(self, request):
        # request.data DRF统一取数据
        serializer = GoodsSKUSerializer(data=request.data)  # 源码
        if serializer.is_valid():
            serializer.save()  # GoodsSKUSerializer  => create
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import mixins
from rest_framework import generics


# GenericAPIView 源码
class GoodApiMiXinView_old(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = GoodsSKU.objects.all()[:10]
    serializer_class = GoodsSKUSerializer

    # 重载get 方法
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)  # list 是迷信的

    # 重载post方法
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)  # create 是迷信的


from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination  # settings 里面


class MySetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20
    page_query_param = "ppp"


#  ListAPIView = mixins.ListModelMixin  +  GenericAPIView
class GoodApiMiXinView(ListAPIView):  # GenericAPIView 源码
    queryset = GoodsSKU.objects.all()  # generic.py
    serializer_class = GoodsSKUSerializer  # 分页后结果放到了result里面,域名也加了
    pagination_class = MySetPagination


#  ListAPIView = mixins.ListModelMixin  +  GenericAPIView
class GoodApiMiXinView(ListAPIView):  # GenericAPIView 源码
    queryset = GoodsSKU.objects.all()  # generic.py
    serializer_class = GoodsSKUSerializer  # 分页后结果放到了result里面,域名也加了
    pagination_class = MySetPagination  # 分页类


"""
viewsets只是一种基于类的观点，不提供
任何方法处理，如` get() `，` post() `，等等。而是有方法， 
如` list() `，` retrieve() `，` create() `，等等。
user_list = UserViewSet.as_view({'get': 'list'})
user_detail = UserViewSet.as_view({'get': 'retrieve'})

因为基于类的视图创建了一个闭包
实例化视图，我们需要完全重新实现` as_view `，
并稍微修改创建和返回的视图函数



Set the `.action` attribute on the view,
depending on the request method.
 Set the `.action` attribute on the view,
  depending on the request method.
在视图上设置“动作”属性，
根据请求方法。
"""

"""
GenericViewSet(viewset) -drf
GenericAPIView  + mixin -drf
    APIView             -drf
      View              -django
主要是 和mixin搭配的 区别 扮演了的角色,无法享受到过滤,分页等功能
    ListModelMixin
    CreateModelMixin
    RetrieveModelMixin
    UpdateModelMixin
    DestroyModelMixin
"""
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend # django filter
from rest_framework.filters import SearchFilter,OrderingFilter

# 0.0 router
class GoodApiViewsetsView(mixins.ListModelMixin, viewsets.GenericViewSet):  # GenericAPIView 源码
    """viewsets 和 routes 配套使用"""
    queryset = GoodsSKU.objects.all()  # generic.py
    serializer_class = GoodsSKUSerializer  # 分页后结果放到了result里面,域名也加了
    pagination_class = MySetPagination  # 分页类
    # django-filter需要在view里面设置djangofilterbackend
    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter) #有filter 就不需要get_queryset手写了
    ordering_fields = ('price', 'sales') # 排序

    # django-filter 配置条件字段
    # filter_fields = ('name', 'price')

    # 自定义配置
    from .myfilters import MyGoodsSKUFilter
    # 配置fitler_class
    filter_class = MyGoodsSKUFilter
    search_fields = ('^name','title')


    # def get_queryset(self):
    #     """优先级最高"""
    #     id_gte = self.request.query_params.get("id_gte", 3)
    #     query_set = GoodsSKU.objects.filter(id__gte=id_gte)
    #     return query_set


class GoodCategoryViewset(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin, # http://127.0.0.1:8000/apicat/2/ RESTFUL 规范不用配置 drf 不用配置url
                          viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.all()
    serializer_class =GoodsCatorySerializer
"""
github  django cors headers
pip install django-cors-headers

"""
