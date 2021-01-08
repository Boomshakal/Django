from rest_framework.viewsets import ModelViewSet

from user.models import User
from user.serializer import UserSerialize

class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerialize
