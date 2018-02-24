# -*- coding:utf-8 -*-
from django.conf.urls import url
from users.views import *  # 导包路径限制的 from apps.users.views import * 是错的

# from users import view
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # 函数视图注册
    # url(r"^register$", views.register, name="register")
    # 类视图注册  如何在正则表达式中调用类视图，用类名.as_view()函数
    url(r"^register$", RegisterView.as_view(), name="register"),
    url(r"^active/(?P<token>.+)$", ActiveView.as_view(), name="active"),
    url(r"^login$", Login.as_view(), name="login"),
    url(r"^logout$", Logout.as_view(), name="logout"),
    # url(r"^address$", Address.as_view(), name="address"),
    # url(r"^address$", login_required(Address.as_view()), name="address"),
    url(r"^address$", login_required(Address.as_view()), name="address"),
    # LoginoutView
]
