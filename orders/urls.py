# -*- coding:utf-8 -*-
from django.conf.urls import url
# from goods import views
# from goods.views import *
# from . import views
from .views import *

urlpatterns = [
    # /order/place
    url(r'^place$', PlaceOrderView.as_view(), name='place'),
    # /order/commit POST
    url(r'^commit$', CommitOrderView.as_view(), name='commit'),
    # /order/1   page 第几页
    url(r'^(?P<page>\d+)$', UserOrderView.as_view(), name='info'),

]
