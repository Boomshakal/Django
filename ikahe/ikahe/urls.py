"""ikahe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from ikahe.settings import MEDIA_ROOT

import xadmin
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from users.views import UserViewSet, SmsCodeViewSet, IndexView, LogoutView, ActiveView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename="users")  # 用户操作
router.register(r'code', SmsCodeViewSet, basename="code")  # Sms

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^', include(router.urls)),

    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    url(r'^api-auth/', include('rest_framework.urls')),

    # drf自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),

    # jwt的认证接口
    url(r'^login/$', obtain_jwt_token),

    # 富文本相关URL
    url(r'^ueditor/', include('DjangoUeditor.urls')),

    # url(r'^alipay/return/', AliayView.as_view(), name="alipay"),

    # index
    url(r'index/', IndexView.as_view(), name="index"),

    # 用户模块
    url(r'user/', include('users.urls', namespace='user')),

    # 第三方登录
    url('', include('social_django.urls', namespace='social')),

    # 七牛云上传测试
    # url(r'^upload/$', view=UploadImage.as_view(), name='upload'),
    # url(r'^uploadprocessor/$', view=GetImageUrl.as_view(), name='uploadprocessor'),

    url(r'docs/', include_docs_urls(title='IKAHE API')),

    path('kanban/', include('e_kanban.urls')),
]

urlpatterns += router.urls
