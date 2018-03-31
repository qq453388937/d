# -*- coding:utf-8 -*-
from django.db.models import Q
from rest_framework import generics
from django_filters import rest_framework as filters
from .models import *


class MyGoodsSKUFilter(filters.FilterSet):
    """goodsSKU 自定义过滤类 """  # lookup_expr == django 的过滤器
    min_price_zidingyi = filters.NumberFilter(name="price", lookup_expr="gte")  # name 表的字段名
    max_price_zidingyi = filters.NumberFilter(name="price", lookup_expr="lte")  # name 表的字段名
    name_zidingyi = filters.CharFilter(name="name", lookup_expr="icontains")

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(sales__gt=1)

    class Meta:
        model = GoodsSKU  # 指明是给哪个类过滤
        fields = ['name_zidingyi', 'min_price_zidingyi', 'max_price_zidingyi']
