from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from goods.models import *


# 主页无需登陆即可访问添加购物车
class IndexView(View):

    def get(self, request):
        """查询主页商品数据"""

        # 查询用户ｕｓｅｒ信息 ,不需要 在request中

        # 查询商品分类信息
        categorys = GoodsCategory.objects.all()
        # 查询图片轮播信息
        goods_banners = IndexGoodsBanner.objects.all().order_by('index')
        # 查询商品活动信息
        promotion_banners = IndexPromotionBanner.objects.all().order_by('index')
        # 查询主页分类商品列表信息
        for category in categorys:
            # 分组查询出来 ,六大分类
            title_banners = IndexCategoryGoodsBanner.objects.filter(category=category).filter(display_type=0)
            category.title_banners = title_banners  # 动态的添加对象的属性 ,for 循环一次每个对象动态的添加一个属性
            image_banners = IndexCategoryGoodsBanner.objects.filter(category=category).filter(display_type=1)
            category.image_banners = image_banners  # 动态的添加对象的属性 ,for 循环一次每个对象动态的添加一个属性
        # 查询购物车信息
        cart_num = 88
        # 构造上下文
        context = {
            'categorys': categorys,
            'goods_banners': goods_banners,
            'promotion_banners': promotion_banners,
            'cart_num': cart_num,
        }

        # 渲染模板
        return render(request, 'index.html', context)

    def post(self, request):
        pass
