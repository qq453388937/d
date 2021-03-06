# -*- coding:utf-8 -*-

from .models import *
from rest_framework import serializers


# 它序列化的方式很类似于Django的forms
# class GoodsSKUSerializer(serializers.Serializer):#
#     """model.CharFiled 替换为 serializers.CharFiled
#      def 可以直接保存导数据库通过接口
#      """
#     name = serializers.CharField(required=True, max_length=100)
#     title = serializers.CharField(max_length=200)
#     stock = serializers.IntegerField(default=0)
#     unit = serializers.CharField(max_length=10)
#     price = serializers.DecimalField(max_digits=10, decimal_places=2)
#     sales = serializers.IntegerField(default=0)
#     default_image = serializers.ImageField()
#     status = serializers.BooleanField(default=True)
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return GoodsSKU.objects.create(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    """ModelSerializer"""

    class Meta:
        model = GoodsCategory  # 映射GoodsCategory
        # fields = ('id', 'title', 'code', 'linenos', 'language', 'style')
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    """ModelSerializer"""

    class Meta:
        model = Goods
        # fields = ('id', 'title', 'code', 'linenos', 'language', 'style')
        fields = "__all__"


class GoodsSKUSerializer(serializers.ModelSerializer):
    """ModelSerializer"""
    category = CategorySerializer()  # 映射GoodsCategory,覆盖外键字段
    goods = GoodsSerializer()  # 覆盖外键字段

    class Meta:
        model = GoodsSKU
        # fields = ('name', 'title', 'unit', 'price', 'stock', 'default_image')
        fields = "__all__"


class GoodsCatorySerializer(serializers.ModelSerializer):
    """商品类别序列化"""
    # 自链接关注related_name="sub_cate"
    # sub_cat = GoodsCatorySerializer2lei(many=True) # 不要漏了many=True
    class Meta:
        model = GoodsCategory
        fields = "__all__"



class GoodsCatorySerializer2lei(serializers.ModelSerializer):
    """商品类别序列化"""
    # 自链接关注related_name="sub_cate"
    # sub_cat =  GoodsCatorySerializer3lei(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"



class GoodsCatorySerializer3lei(serializers.ModelSerializer):
    """商品类别序列化"""
    # 自链接关注related_name="sub_cate"
    # sub_cat =
    class Meta:
        model = GoodsCategory
        fields = "__all__"