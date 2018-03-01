from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from django.views.generic import View
from django.core.urlresolvers import reverse
from django_redis import get_redis_connection

from goods.models import *
# django 缓存工具包导入 cache
from django.core.cache import cache


# 主页无需登陆即可访问添加购物车


class IndexView(View):

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
        if request.user.is_authenticated():
            """需求是：用户登陆了才会计算购物车信息"""
            # 创建redis
            redis_client = get_redis_connection('default')  # alt+enter 自动导入
            # hgetall() 读取购物车数据 hset key field value    key带上用户id用于主键区分每个用户的购物车
            # 每个用户都有自己的哈希对象，每个用户自己特有的购物车
            # %s 占位后面可以直接填数字
            # cart_dict = redis_client.hgetall('cart_%s' % request.user.id)  # 获取所有字段:value键值对组合
            cart_dict = redis_client.hgetall('cart_%s' % 666)  # 获取所有字段:value键值对组合
            cart_num = 0
            for val in cart_dict.values():  # 遍历值
                # print(type(val))
                # print(val)  # b'3'
                # print(int(val))  # 3
                # print(type(int(val)))  # <class 'int'>
                cart_num += int(val)  # 计算购物车的商品总数量 byte类型，只有数字和字母可以直接转int，如果是汉子必须decode()一下先
            # cart_num = 777777777  # 测试假数据,假设查出来了
            context['cart_num'] = cart_num
            # context.update({'cart_num': 777777777})
            # context.update(cart_num=777777777)

        # 渲染模板
        return render(request, 'index.html', context)

    def post(self, request):
        pass


class DetailView(View):
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
        # 查询购物车信息 redis
        if request.user.is_authenticated():
            """需求是：用户登陆了才会计算购物车信息
            这么写方便上面缓存，如果不需要缓存，一次构造完上下文即可
            """
            # 创建redis
            redis_client = get_redis_connection('default')  # alt+enter 自动导入
            # hgetall() 读取购物车数据 hset key field value    key带上用户id用于主键区分每个用户的购物车
            # 每个用户都有自己的哈希对象，每个用户自己特有的购物车
            # %s 占位后面可以直接填数字
            # cart_dict = redis_client.hgetall('cart_%s' % request.user.id)  # 获取所有字段:value键值对组合
            cart_dict = redis_client.hgetall('cart_%s' % 666)  # 获取所有字段:value键值对组合
            cart_num = 0
            for val in cart_dict.values():  # 遍历值
                # print(type(val))
                # print(val)  # b'3'
                # print(int(val))  # 3
                # print(type(int(val)))  # <class 'int'>
                cart_num += int(val)  # 计算购物车的商品总数量 byte类型，只有数字和字母可以直接转int，如果是汉子必须decode()一下先
            # cart_num = 777777777  # 测试假数据,假设查出来了
            context['cart_num'] = cart_num
            # context.update({'cart_num': 777777777})
            # context.update(cart_num=777777777)

        # 记录最近浏览信息(redis)
        redis_client.lrem('history_%s' % request.user.id, 0,
                          sku_id)  # count=0 删除所有value 是sku_id值的,count>0 从左往右删除count个,count<0从右往左删除count个
        redis_client.lpush('history_%s' % request.user.id, sku_id)
        # 最多保存５个
        redis_client.ltrim('history_%s', 0, 4)

        # 渲染模板
        return render(request, 'detail.html', context)

    def post(self, request):
        pass
