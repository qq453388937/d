# -*- coding:utf-8 -*-
from haystack import indexes
from .models import *


class GoodsSKUIndex(indexes.SearchIndex, indexes.Indexable):
    """建立索引时被使用的类"""
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        """从哪个表中查询"""
        return GoodsSKU

    def index_queryset(self, using=None):
        """返回要建立索引的数据"""  # 本质就是数据库中的数据建立索引放在本地文件中，直接索引本地文件
        return self.get_model().objects.all()  # filter这里可以过滤检索数据
