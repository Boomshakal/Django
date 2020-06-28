from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

# Create your views here.

from .models import SKU
from .serializers import SKUSerializer


class SKUListView(ListAPIView):
    """
    sku商品列表数据
    """
    # 指定序列化器
    serializer_class = SKUSerializer
    # 指定排序后端
    filter_backends = (OrderingFilter,)
    # 指定排序字段：在这里不需要指定倒序，需要和模型属性同名
    ordering_fields = ('create_time', 'price', 'sales')

    def get_queryset(self):
        # 从视图的kwargs属性种读取路径参数
        category_id = self.kwargs['category_id']
        # 以category_id 对SKU进行过滤，保证查询到的sku信息都是指定的category_id所在的分类
        return SKU.objects.filter(category_id=category_id, is_launched=True)
