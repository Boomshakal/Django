from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from django.contrib.auth import get_user_model
User = get_user_model()

from user.models import Address
from user.serializer import UserSerialize, AddressSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerialize


class AddressViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        """
        库存数减去购物车
        :param serializer:
        :return:
        """
        serializer['user'] = self.request.user
        serializer.save()
