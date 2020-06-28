from rest_framework import serializers

from .models import Area


class AreaSerializer(serializers.ModelSerializer):
    """
    list
    省级行政区划信息序列化器，只做序列化
    """

    class Meta:
        model = Area
        fields = ('id', 'name')


class SubsAreaSerializer(serializers.ModelSerializer):
    """
    retrieve
    子行政区划信息序列化器，只做序列化
    """

    # 关联AreaSerializer，subs得到序列化之后的结果
    subs = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ('id', 'name', 'subs')
