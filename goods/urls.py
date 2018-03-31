# -*- coding:utf-8 -*-
from django.conf.urls import include, url
# from goods import views
# from goods.views import *
# from . import views
from .views import *
# drf
from rest_framework.documentation import include_docs_urls

# 1. router 的使用导入包
from rest_framework.routers import DefaultRouter
# 2. 导入views里面的viewsets 视图
from .views import GoodApiViewsetsView

# 3. 创建router对象
router = DefaultRouter()  # 默认get 绑list post 绑定create
# 4.注册路由 绑定viewsets,viewsets 重写了as_view并且给request绑定了.action
router.register(r"^apiaa", GoodApiViewsetsView, base_name="apiaa")
router.register(r'^apicat', GoodCategoryViewset, base_name="category")

# apigg 结果直接放进到url填坑就可以了 非router注册
apigg = GoodApiViewsetsView.as_view({
    "get": "list",  # 自己绑定
    "post": "create",
})

urlpatterns = [
    # 5. 把注册好的路由包含进来
    url(r'^', include(router.urls)),
    url(r'^$|^index$', IndexView.as_view(), name='index'),  # 神马都没有
    url(r'^detail/(?P<sku_id>\d+)$', DetailView.as_view(), name='detail'),  # DetailView /id 才能url让别人看到
    # list/category_id/page_num?.
    url(r'^list/(?P<category_id>\d+)/(?P<page_num>\d+)$', ListView.as_view(), name='list'),
    # DetailView /id 才能url让别人看到
    url(r'^mysearch/$', MySearchView.as_view(), name='list'),  # DetailView /id 才能url让别人看到

    url(r'^apigoodold/', GoodViewOld.as_view(), name="learn1"),
    url(r'^apigood/', GoodAPIView.as_view(), name="learn2"),
    url(r'^apig/', GoodApiMiXinView.as_view(), name="learn3"),
    # url(r'^apigg/', GoodApiViewsetsView.as_view(), name="learn4"),
    url(r'^apigg/', apigg, name="learn5"),
    url(r'docs/', include_docs_urls(title='pxd')),

]
