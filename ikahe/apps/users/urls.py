from django.conf.urls import url

from users.views import ActiveView, LogoutView

app_name = 'apps.user'
urlpatterns = [
    url(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),  # 用户激活
    url(r'^logout/$', LogoutView.as_view(), name='logout'),  # 退出登录
]
