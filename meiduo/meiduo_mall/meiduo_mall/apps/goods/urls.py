from django.conf.urls import url
from rest_framework import routers
from . import views

# 生成一个注册器实列对象
router = routers.DefaultRouter()

urlpatterns = [

    # 商品列表
    url(r'^categories/(?P<category_id>\d+)/skus/', views.SKUListView.as_view()),

]

router.register(r'goods', views.GoodsViewSet, base_name='good')
urlpatterns += router.urls
