from django.contrib import admin

# Register your models here.
from django.contrib import admin
from goods.models import GoodsCategory, Goods, GoodsSKU, IndexPromotionBanner
from celery_tasks.tasks import generic_static_index_html # 这一行决定了python manage.py celery worker --loglevel=info去哪里找异步
# from .task import generic_static_index_html
# django 缓存工具包导入 cache
from django.core.cache import cache


# -----------celery服务器无需改写admin因为是django调用该模块的代码--------------------------

class BaseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        """重写保存数据的方法"""
        generic_static_index_html.delay()
        obj.save()
        # 运维增删改了涉及到保存主页相关的东西,删除缓存
        cache.delete('index_page_data')

    def delete_model(self, request, obj):
        """重写删除数据的方法"""
        generic_static_index_html.delay()
        obj.save()
        # 运维增删改了涉及到保存主页相关的东西,删除缓存
        cache.delete('index_page_data')


class IndexPromotionBannerAdmin(BaseAdmin):
    pass


class GoodsCategoryAdmin(BaseAdmin):
    pass


class GoodsAdmin(BaseAdmin):
    pass


class GoodsSKUAdmin(BaseAdmin):
    pass


class IndexCategoryGoodsBannerAdmin(BaseAdmin):
    pass


# Register your models here.
admin.site.register(GoodsCategory, GoodsCategoryAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(GoodsSKU,GoodsSKUAdmin)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)
