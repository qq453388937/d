# -*- coding:utf-8 -*-
from django.conf.urls import url
# from goods import views
# from goods.views import *
# from . import views
from .views import *
# drf
from rest_framework.documentation import include_docs_urls

urlpatterns = [

    url(r'^$|^index$', IndexView.as_view(), name='index'),  # 神马都没有
    url(r'^detail/(?P<sku_id>\d+)$', DetailView.as_view(), name='detail'),  # DetailView /id 才能url让别人看到
    # list/category_id/page_num?.
    url(r'^list/(?P<category_id>\d+)/(?P<page_num>\d+)$', ListView.as_view(), name='list'),  # DetailView /id 才能url让别人看到
    url(r'^mysearch/$', MySearchView.as_view(), name='list'),  # DetailView /id 才能url让别人看到

    url(r'^apigoodold/', GoodViewOld.as_view(), name="learn1"),
    url(r'^apigood/', GoodAPIView.as_view(), name="learn2"),
    url(r'^apig/', GoodApiMiXinView.as_view(), name="learn3"),

    url(r'docs/', include_docs_urls(title='pxd')),

]
