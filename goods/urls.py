# -*- coding:utf-8 -*-
from django.conf.urls import url
# from goods import views
# from goods.views import *
# from . import views
from .views import *

urlpatterns = [

    url(r'^$|^index$', IndexView.as_view(), name='index'),  # 神马都没有
    url(r'^detail/(?P<sku_id>\d+)$', DetailView.as_view(), name='detail'),  # DetailView /id 才能url让别人看到

]
