# -*- coding:utf-8 -*-
from django.conf.urls import url
# from goods import views
# from goods.views import *
# from . import views
from .views import *

urlpatterns = [
    # ajax post  ajax post 请求必须有csrf 验证
    url(r'^add/$', AddCart.as_view(), name='add'),

]
