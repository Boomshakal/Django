import os

from django.http import FileResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from toys.settings import BASE_DIR


class Get_File_View(APIView):
    def get(self, request):
        print(request.GET.get('file_name'))

        return 'success'


class Get_Photo_View(APIView):
    def get(self, request):
        file_name = request.GET.get('file_name')

        file_path = BASE_DIR + '\static\photo\\' + file_name
        photo = open(file_path, 'rb')
        response = FileResponse(photo)
        return response


class Get_Music_View(APIView):
    def get(self, request):
        file_name = request.GET.get('file_name')

        file_path = BASE_DIR + '\static\music\\' + file_name
        photo = open(file_path, 'rb')
        response = FileResponse(photo)
        return response
