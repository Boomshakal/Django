from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import SKU, Goods, GoodsCategory


class SKUSerializer(ModelSerializer):
    """
    序列化器输出商品SKU信息
    """

    class Meta:
        model = SKU
        # 输出：序列化的字段
        fields = ('id', 'name', 'price', 'default_image_url', 'comments')


class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"  # 全部


class CategorySerializer2(serializers.ModelSerializer):
    parent = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"  # 全部


class CategorySerializer(serializers.ModelSerializer):
    """
    商品类别序列化
    """
    parent = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"  # 全部


class GoodsSerializer(ModelSerializer):
    """
    序列化器输出商品Goods信息
    """

    # category1 = CategorySerializer()  # 外键
    # category2 = CategorySerializer()  # 外键
    # category3 = CategorySerializer3()  # 外键

    class Meta:
        model = Goods
        # fields = '__all__'
        exclude = ['create_time', 'update_time']
