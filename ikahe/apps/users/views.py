from random import choice

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model, logout
from rest_framework.views import APIView

from utils.response import BaseResponse

User = get_user_model()
from django.db.models import Q
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.views.generic.base import View
from django.shortcuts import render
from itsdangerous import SignatureExpired, TimedJSONWebSignatureSerializer as Serializer
from utils.celery_tasks.tasks import send_register_active_email

from .serializer import SmSerializer, UserRegSerializer, UserDetailSerializer
from utils.yunpian import YunPian
from ikahe.settings import APIKEY, SECRET_KEY
from .models import VerifyCode


# Create your views here.

class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            print(username, password)
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmSerializer

    def generate_code(self):
        """
        生成六位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(6):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']

        # yunpian = YunPian(APIKEY)

        code = self.generate_code()

        # sms_status = yunpian.send_sms(code=code, mobile=mobile)

        # if sms_status["code"] != 0:
        #     return Response({"mobile": sms_status["msg"]}, status=status.HTTP_400_BAD_REQUEST)
        # else:
        code_record = VerifyCode(code=code, mobile=mobile)
        code_record.save()
        return Response({"mobile": mobile}, status=status.HTTP_201_CREATED)


class UserViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)

    # 用户在注册的时候是没有权限的,所以这个方法不适用
    # permissions_class = (permissions.IsAuthenticated,)
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer
        return UserDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # print(serializer)

        email = request.POST.get('email')
        username = request.POST.get('user_name')

        user = self.perform_create(serializer)

        # 加密用户的身份信息，生成激活token
        serializer_key = Serializer(SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer_key.dumps(info)  # bytes
        token = token.decode('utf8')  # 解码, str

        # 找其他人帮助我们发送邮件 celery:异步执行任务
        send_register_active_email.delay(email, username, token)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


class ActiveView(APIView):
    """用户激活"""

    def get(self, request, token):
        # 进行用户激活
        # 进行解密，获取要激活的用户信息
        resopnse = BaseResponse()
        serializer_key = Serializer(SECRET_KEY, 3600)
        try:
            info = serializer_key.loads(token)
            # 获取待激活用户的id
            user_id = info['confirm']

            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            resopnse.code = 1000
            resopnse.msg = '激活成功'

            # 跳转到登录页面
            return Response(resopnse.dict)

        except SignatureExpired as e:
            # 激活链接已过期
            resopnse.code = 1001
            resopnse.msg = '激活链接已过期'
            return Response(resopnse.dict)


class LogoutView(APIView):
    def get(self, request):
        resopnse = BaseResponse()
        logout(request)
        resopnse.code = 1000
        resopnse.msg = '注销成功'
        return Response(resopnse.dict)


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html', {})
