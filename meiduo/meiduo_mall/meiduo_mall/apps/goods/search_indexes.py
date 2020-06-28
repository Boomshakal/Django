from haystack import indexes

from .models import SKU


class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    """
    SKU索引数据模型类
    """
    # 用于接受用户输入的关键字http://api.meiduo.site:8000/skus/search/?text=wifi
    # document指明文档，描述text字段
    # use_template 在文档中使用模板语言，指明哪些字段可以传递给text字段
    # text是复合字段，可以指定多个模型类的属性被他接受1
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return SKU

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter(is_launched=True)