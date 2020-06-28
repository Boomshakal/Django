# 主页静态化处理

from collections import OrderedDict
from django.conf import settings
from django.template import loader
import os
import time

from goods.models import GoodsChannel
from .models import ContentCategory


def generate_static_index_html():
    """
    生成静态的主页html文件
    """
    print('%s: generate_static_index_html' % time.ctime())
    # 商品频道及分类菜单
    # 使用有序字典保存类别的顺序
    # categories = {
    #     1: { # 组1
    #         'channels': [{'id':, 'name':, 'url':},{}, {}...],
    #         'sub_cats': [{'id':, 'name':, 'sub_cats':[{},{}]}, {}, {}, ..]
    #     },
    #     2: { # 组2
    #
    #     }
    # }
    categories = OrderedDict()
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    for channel in channels:
        group_id = channel.group_id  # 当前组

        if group_id not in categories:
            categories[group_id] = {'channels': [], 'sub_cats': []}

        cat1 = channel.category  # 当前频道的类别

        # 追加当前频道
        categories[group_id]['channels'].append({
            'id': cat1.id,
            'name': cat1.name,
            'url': channel.url
        })
        # 构建当前类别的子类别
        for cat2 in cat1.goodscategory_set.all():
            cat2.sub_cats = []
            for cat3 in cat2.goodscategory_set.all():
                cat2.sub_cats.append(cat3)
            categories[group_id]['sub_cats'].append(cat2)

    # 广告内容
    contents = {}
    content_categories = ContentCategory.objects.all()
    for cat in content_categories:
        contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

    # 渲染模板
    context = {
        'categories': categories,
        'contents': contents
    }
    # 获取要渲染的模板文件
    # loader.get_template('index.html')会去到项目的templates文件夹中寻找指定的要渲染的模板文件
    template = loader.get_template('index.html')

    # 拿着查询并购造出来的context上下文，去渲染上一部加载出来的模板文件
    # html_text渲染之后的结果，是一个html文本字符串
    html_text = template.render(context)

    # 指定静态文件存储的路径settings.GENERATED_STATIC_HTML_FILES_DIR  指向front_end_pc + 'index.html'
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'index.html')

    # 开始写入到'index.html'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_text)
