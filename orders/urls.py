# -*- coding:utf-8 -*-
from django.conf.urls import url
# from goods import views
# from goods.views import *
# from . import views
from .views import *

urlpatterns = [
    # /orders/place
    url(r'^place$', PlaceOrderView.as_view(), name='place'),

]
