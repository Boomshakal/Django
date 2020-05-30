from django.contrib.auth import logout
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from utils.response import BaseResponse


# /user/login
class LoginView(APIView):
    def post(self, request):
        receive = request.data
        # print(receive)
        account = receive.get('account')
        password = receive.get('password')

        user = User.objects.filter(account=account, password=password)
        if user:
            return Response('Login')
        else:
            return Response('去注册')


# /user/register
class Register(APIView):
    def post(self, request):
        response = BaseResponse()
        receive = request.data
        # print(receive)

        account = receive.get('account')
        password = receive.get('password')
        email = receive.get('email')

        try:
            user = User.objects.get(account=account)
        except User.DoesNotExist:
            user = None

        if user:
            response.code = 1000
            response.msg = '用户已存在'
            # response.data = user

            return Response(response.dict)

        user = User.objects.create(account=account, password=password, email=email)

        response.code = 1000
        response.msg = '注册成功'
        response.data = str(user._id)

        return Response(response.dict)


# /user/logout
class LogoutView(APIView):
    """退出登录"""

    def get(self, request):
        response = BaseResponse()
        logout(request)

        response.code = 1000
        response.msg = '注销成功'

        return Response(response.dict)
