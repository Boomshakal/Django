from django.contrib import admin
from django.urls import path

from get_set_anythings.views import Get_File_View, Get_Photo_View, Get_Music_View

urlpatterns = [
    path('get_file/', Get_File_View.as_view(), name='file'),
    path('get_photo/', Get_Photo_View.as_view(), name='file'),
    path('get_music/', Get_Music_View.as_view(), name='file'),
]
