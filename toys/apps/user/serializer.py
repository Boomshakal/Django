from rest_framework_mongoengine.serializers import DocumentSerializer

from .models import User


class UserSerialize(DocumentSerializer):
    class Meta:
        model = User
        fields = ('account', 'email', 'password')
