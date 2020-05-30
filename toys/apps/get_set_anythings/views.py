import os

from django.http import FileResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from toys.settings import BASE_DIR, STATIC_URL


class Get_File_View(APIView):
    def get(self, request):
        print(request.GET.get('file_name'))

        return 'success'


class Get_Photo_View(APIView):
    def get(self, request):
        file_name = request.GET.get('file_name')
        file_path = os.path.join(BASE_DIR, STATIC_URL, file_name)
        print(file_path)
        photo = open(r'D:\文档\GitHub\Django\toys\static\photo\cat.jpg', 'rb')

        print(photo)
        response = FileResponse(photo)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="models.py"'
        return response
