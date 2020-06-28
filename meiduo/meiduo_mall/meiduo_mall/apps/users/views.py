from django_redis import get_redis_connection
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from goods.models import SKU
from goods.serializers import SKUSerializer
from .models import User
from . import serializers, constants


# Create your views here.


class UserBrowsingHistoryView(CreateAPIView):
    """
    用户浏览历史记录
    POST /browse_histories/
    """
    # 指定序列化器
    serializer_class = serializers.AddUserBrowsingHistorySerializer
    # 指定权限：必须是登陆用户才能保存浏览记录
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        读取用户的浏览记录
        """
        user_id = request.user.id
        # 创建redis数据库链接对象
        redis_conn = get_redis_connection("history")
        # 读取出数据库的信息
        history = redis_conn.lrange("history_%s" % user_id, 0, constants.USER_BROWSING_HISTORY_COUNTS_LIMIT - 1)

        skus = []
        # 为了保持查询出的顺序与用户的浏览历史保存顺序一致
        for sku_id in history:
            sku = SKU.objects.get(id=sku_id)
            skus.append(sku)

        # 将skus列表序列化
        s = SKUSerializer(skus, many=True)
        return Response(s.data)


class AddressViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    """
    用户地址新增与修改
    """
    serializer_class = serializers.UserAddressSerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.addresses.filter(is_deleted=False)

    # GET /addresses/
    def list(self, request, *args, **kwargs):
        """
        用户地址列表数据
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        user = self.request.user
        return Response({
            'user_id': user.id,
            'default_address_id': user.default_address_id,
            'limit': constants.USER_ADDRESS_COUNTS_LIMIT,
            'addresses': serializer.data,
        })

    # POST /addresses/
    def create(self, request, *args, **kwargs):
        """
        保存用户地址数据
        """
        # 检查用户地址数据数目不能超过上限
        count = request.user.addresses.count()
        if count >= constants.USER_ADDRESS_COUNTS_LIMIT:
            return Response({'message': '保存地址数据已达到上限'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    # delete /addresses/<pk>/
    def destroy(self, request, *args, **kwargs):
        """
        处理删除
        """
        address = self.get_object()

        # 进行逻辑删除
        address.is_deleted = True
        address.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    # put /addresses/pk/status/
    @action(methods=['put'], detail=True)
    def status(self, request, pk=None):
        """
        设置默认地址
        """
        address = self.get_object()
        request.user.default_address = address
        request.user.save()
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    # put /addresses/pk/title/
    # 需要请求体参数 title
    @action(methods=['put'], detail=True)
    def title(self, request, pk=None):
        """
        修改标题
        """
        address = self.get_object()
        serializer = serializers.AddressTitleSerializer(instance=address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# url(r'^emails/verification/$', views.VerifyEmailView.as_view()),
class VerifyEmailView(APIView):
    """
    邮箱验证
    """

    def get(self, request):
        """
        # 获取token，读取出user_id，查询当前要认证的用户，将用户email_active设置为True
        :param request:
        :return:
        """
        # 获取token
        token = request.query_params.get('token')
        if not token:
            return Response({'message': '缺少token'}, status=status.HTTP_400_BAD_REQUEST)

        # 验证token
        user = User.check_verify_email_token(token)
        if user is None:
            return Response({'message': '无效token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 将用户email_active设置为True
            user.email_active = True
            user.save()
            # 响应结果
            return Response({'message': 'OK'})


# url(r'^emails/$', views.EmailView.as_view()),  # 设置邮箱
class EmailView(UpdateAPIView):
    """
    保存用户邮箱
    """
    # 指定权限
    permission_classes = [IsAuthenticated]
    # 指定序列化器
    serializer_class = serializers.EmailSerializer

    def get_object(self):
        # 响应系列化后的结果
        return self.request.user


# url(r'^users/$', views.UserDetailView.as_view()),
class UserDetailView(RetrieveAPIView):
    """
    用户基本信息详情
    用户必须登陆后才能访问此接口
    用户没有出传入主键pk，RetrieveAPIView中的get_object()方法无法获取，需要重写
    """
    # 指定序列化器
    serializer_class = serializers.UserDetailSerializer
    # 指定权限，用户必须登陆后才能访问
    permission_classes = [IsAuthenticated]

    """
    RetrieveAPIView
    得到当前登录用户user信息，
    创建序列化器对象
    进行序列化
    """

    def get_object(self):
        # 响应系列化后的结果
        return self.request.user


class UserView(CreateAPIView):
    """注册
    新增用户数据到模型类
    用户数据===》校验===》反序列化===》save()
    """
    # 指定序列化器
    serializer_class = serializers.CreateUserSerializer


# url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
class MobileCountView(APIView):
    """
    手机号数量
    """

    def get(self, request, mobile):
        """
        获取指定手机号数量
        """
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count
        }

        return Response(data)


# url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
class UsernameCountView(APIView):
    """
    用户名数量用以判断用户是否为注册用户
    """

    def get(self, request, username):
        """
        获取指定用户名数量
        """
        count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count
        }

        return Response(data)
