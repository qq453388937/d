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
    url(r"^address$", AddressView.as_view(), name="address"),
    url(r"^userinfo$", UserInfoView.as_view(), name="userinfo"),

    # 装饰器原理 @login_required === >  login_required(Addresss.as_view())
    # url(r"^address$", login_required(Address.as_view()), name="address"),
]

"""
login_required([redirect_field_name=REDIRECT_FIELD_NAME, login_url=None])
第一个参数是next = ？ next的名字 默认next
第二个参数是登陆失败校验不通过情况下跳转的页面，
第二个参数如果都不设置的话 可以仅仅设置settings.py 中 
LOGIN_URL = '/users/login' 即可！
"""