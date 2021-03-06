"""meiduo_mall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 富文本编辑器
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # 验证模块verifications
    url(r'^', include('verifications.urls')),
    # 判断用户是否存在
    url(r'^', include('users.urls')),
    # oauth--第三方登陆
    url(r'^oauth/', include('oauth.urls')),
    # areas行政区域
    url(r'^', include('areas.urls')),
    # 商品列表
    url(r'^', include('goods.urls')),

    url(r'docs/', include_docs_urls(title='MEIDUO API')),



]
