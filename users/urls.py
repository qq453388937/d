# -*- coding:utf-8 -*-
from django.conf.urls import url
from users import views  # 导包路径限制的 from apps.users.views import * 是错的

urlpatterns = [
    url(r"^register$", views.register, name="register")

]
