from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Address


class UserSerialize(DocumentSerializer):
    rep_password = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("name", "gender", "birthday", 'email',"mobile")

    def get_rep_password(self, obj):
        return obj.password[0:6]

class AddressSerializer(DocumentSerializer):
    class Meta:
        model = Address
        fields = '__all__'
