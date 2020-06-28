from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'areas', views.AreasViewSet, basename='areas')

urlpatterns = []

urlpatterns += router.urls
