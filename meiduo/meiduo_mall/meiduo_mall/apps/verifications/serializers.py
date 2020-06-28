from rest_framework import serializers
from django_redis import get_redis_connection
from redis import exceptions

import logging

# 日志记录器
logger = logging.getLogger('django')


class ImageCodeCheckSerializer(serializers.Serializer):
    """校验图形验证码的序列化器"""

    # 定义校验字段：定义的校验字段要么和模型类一样，要么和参数的key一样
    image_code_id = serializers.UUIDField()
    text = serializers.CharField(max_length=4, min_length=4)

    def validate(self, attrs):
        """
        对image_code_id和text联合校验
        :param attrs: validate_data
        :return: 如果校验成功返回attrs，否则抛出异常
        """
        # 读取validate_data数据
        image_code_id = attrs['image_code_id']
        text = attrs.get('text')
        # 获取连接到redis的对象
        redis_conn = get_redis_connection('verify_codes')
        # 获取redis中存储的图片验证码
        print('img_%s' % image_code_id)
        image_code_id_server = redis_conn.get('img_%s' % image_code_id)
        if image_code_id_server is None:
            raise serializers.ValidationError("无效验证码")

        # 删除redis中的图片验证码，防止暴力测试，先拿再删
        # 此逻辑不是主线逻辑，可有可无，出现异常不需要响应异常，直接忽略异常，后续逻辑继续执行
        try:
            redis_conn.delete('img_%s' % image_code_id)
        except exceptions as e:
            logger.error(e)

        # py3的redis存储的数据，读取出来的都是bytes类型
        # 需要将image_code_id_server转成str
        image_code_id_server = image_code_id_server.decode()

        # 对比text和服务器存储的图片验证码
        if text.lower() != image_code_id_server.lower():
            raise serializers.ValidationError('图片验证码输入有误')

        # 判断用户60秒内是否使用了同意手机号码获取短信
        mobile = self.context['view'].kwargs['mobile']
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            raise serializers.ValidationError('频繁发送短信验证码')

        return attrs
