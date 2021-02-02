from django.contrib import admin
from django.urls import path
from user.views import one_to_one

urlpatterns = [
    path('one_to_one/', one_to_one),
]