from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework_jwt.settings import api_settings

from .utils import OAuthQQ
from .exceptions import QQAPIException
from .models import OAuthQQUser
from . import serializers

import logging

logger = logging.getLogger('django')


# Create your views here.


# url(r'^qq/user/$', views.QQAuthUserView.as_view()),
class QQAuthUserView(GenericAPIView):
    """ 处理oauth_callback回调页面时，获取code，access_token，openid"""

    # 指定序列化器
    serializer_class = serializers.QQAuthUserSerializer

    def get(self, request):
        """
        获取qq登录的用户数据
        """
        # 获取--code
        code = request.query_params.get('code')
        if not code:
            return Response({'message': '缺少code'}, status=status.HTTP_400_BAD_REQUEST)

        # 创建OAuthQQ对象
        oauth = OAuthQQ()
        try:
            # 使用code向qq服务器获取--access_token
            access_token = oauth.get_access_token(code)

            # 使用access_token向QQ服务器请求open_id
            open_id = oauth.get_openid(access_token)
        except QQAPIException as e:
            logger.error(e)

            return Response({'message': 'QQ服务异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 使用open_id 查询QQ用户是否在美多商城绑定过用户
        try:
            # oauth_model代表一条记录，数据是OAuthQQUser类型 的对象
            oauth_model = OAuthQQUser.objects.get(openid=open_id)
        except OAuthQQUser.DoesNotExist:
            # 如果没有绑定过，创建用户绑定到open_id

            # 生成openid签名后的结果
            token_openid = oauth.generate_save_user_token(open_id)
            # 将签名后的openid响应给用户
            return Response({'access_token': token_openid})

            # return Response({'open_id':open_id})
        else:
            # 如果 已经绑定，直接生成JWT_token,并返回
            user = oauth_model.user
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            response = Response({
                'token': token,
                'user_id': user.id,
                'username': user.username
            })
            return response

    def post(self, request):
        """openid 绑定用户的逻辑"""
        # 创建序列化器
        serializer = self.get_serializer(data=request.data)
        # 校验
        serializer.is_valid(raise_exception=True)
        # 调用create方法，实现绑定用户的保存
        user = serializer.save()

        # 生成状态保持信息
        # 生成JWT token，并响应
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return Response({
            'token': token,
            'username': user.username,
            'user_id': user.id
        })


#  url(r'^qq/authorization/$', views.QQAuthURLView.as_view()),
class QQAuthURLView(APIView):
    """
    提供获取QQ登录的url
    """

    def get(self, request):
        """
        提供用于qq登录的url
        """
        next = request.query_params.get('next')

        # 创建OAuthQQ对象
        oauth = OAuthQQ(state=next)

        # 获取qq扫码登陆页面的地址
        login_url = oauth.get_qq_login_url()

        # 响应login_url
        return Response({'login_url': login_url})
