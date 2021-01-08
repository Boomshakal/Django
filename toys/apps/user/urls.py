from django.contrib import admin
from django.urls import path
from rest_framework import routers

from .views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, base_name='User')

urlpatterns = [

    # path('login/', LoginView.as_view(), name='login'),
    # path('register/', Register.as_view(), name='register'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('detail/', UserDetail.as_view(), name='detail'),
]
urlpatterns += router.urls
