# -*- coding:utf-8 -*-
from django.conf.urls import url
# from goods import views
# from goods.views import *
# from . import views
from .views import *

urlpatterns = [

    url(r'^$', IndexView.as_view(), name='index'),  # 神马都没有

]
