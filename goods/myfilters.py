# -*- coding:utf-8 -*-
from rest_framework import generics
from django_filters import rest_framework as filters
from .models import *


class MyGoodsSKUFilter(filters.FilterSet):
    """goodsSKU 自定义过滤类 """
    min_price = filters.NumberFilter(name="price", lookup_expr="gte")  # name 表的字段名
    max_price = filters.NumberFilter(name="price", lookup_expr="lte")  # name 表的字段名

    class Meta:
        model = GoodsSKU
        fields = ['name', 'min_price', 'max_price']
