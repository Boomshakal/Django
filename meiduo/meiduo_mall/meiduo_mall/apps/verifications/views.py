import random

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from django_redis import get_redis_connection
from django.http import HttpResponse

from meiduo_mall.libs.captcha.captcha import captcha
from meiduo_mall.libs.yuntongxun.sms import CCP
from . import constants
from rest_framework.response import Response
from .serializers import ImageCodeCheckSerializer
from celery_tasks.sms.tasks import send_sms_code

# Create your views here.

import logging

# 日志记录器
logger = logging.getLogger('django')


# url('^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
class SMSCodeView(GenericAPIView):
    """发送短信验证码"""
    # 指定序列化器
    serializer_class = ImageCodeCheckSerializer

    def get(self, request, mobile):
        # 接收参数： mobile，image_code_id,text
        # 校验参数： image_code_id, text
        # 对比text和服务器存储的图片验证码内容

        # 创建序列化对象
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # 生成随机短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info(sms_code)

        # 服务器存储短信验证码
        redis_conn = get_redis_connection('verify_codes')
        """
        # redis_conn.setex('key', 'time', 'value')
        redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)

        # 存储标记，确保60s内短信验证码不重复发送
        redis_conn.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        """

        # 使用管道方法，让redis只访问一次而执行多条命令
        pl = redis_conn.pipeline()

        # redis_conn.setex('key', 'time', 'value')
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 存储标记，确保60s内短信验证码不重复发送
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)

        # 注意：：：：一定要调用execute()
        pl.execute()

        # 调用第三方接口发送短信验证码
        # CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES//60], 1)

        # 异步发送短信验证码
        # delay：一.将延时任务添加到任务队列，并触发异步任务，让worker能够观察到
        # send_sms_code.delay(mobile, sms_code)

        # 响应发送验证码结果
        return Response({'message': 'OK'})


# url(r'^image_codes/(?P<image_code_id>[\w-]+)/$', views.ImageCodeView.as_view())
class ImageCodeView(APIView):
    """图片验证码"""

    def get(self, request, image_code_id):
        """提供图形验证码"""
        # 生成图片验证码的内容和图片
        text, image = captcha.generate_captcha()
        logger.info(text)
        # 将图片验证码内容存储到redis
        """
        django-redis提供了get_redis_connection的方法，
        # 通过调用get_redis_connection方法传递redis的配置名称可获取到redis的连接对象，
        # 通过redis连接对象可以执行redis命令。
        """
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.set('img_%s' % image_code_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)

        # 将图片响应给用户
        return HttpResponse(image, content_type='image/jpg')
