from django.conf.urls import url
from . import views

urlpatterns = [
    # 获取用户登录到QQ的url
    url(r'^qq/authorization/$', views.QQAuthURLView.as_view()),
    # 处理oauth_callback回调页面时，获取code，access_token，openid
    url(r'^qq/user/$', views.QQAuthUserView.as_view()),


]
