from django.conf.urls import url
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [

    # 判断用户是否存在
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
    # 判断手机号是否已注册
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    # 注册
    url(r'^users/$', views.UserView.as_view()),
    # JWT 登陆
    url(r'^authorizations/$', obtain_jwt_token),
    # 用户基本信息
    url(r'^user/$', views.UserDetailView.as_view()),
    # 添加邮箱
    url(r'^email/$', views.EmailView.as_view()),
    # 邮箱验证
    url(r'^emails/verification/$', views.VerifyEmailView.as_view()),
    # 用户浏览记录
    url(r'^browse_histories/$', views.UserBrowsingHistoryView.as_view()),

]

router = routers.DefaultRouter()
router.register(r'addresses', views.AddressViewSet, basename='addresses')

urlpatterns += router.urls
# POST /addresses/ 新建  -> create
# PUT /addresses/<pk>/ 修改  -> update
# GET /addresses/  查询  -> list
# DELETE /addresses/<pk>/  删除 -> destroy
# PUT /addresses/<pk>/status/ 设置默认 -> status
# PUT /addresses/<pk>/title/  设置标题 -> title