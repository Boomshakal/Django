from django.contrib import admin
from django.urls import path

from user.views import LoginView, Register, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
