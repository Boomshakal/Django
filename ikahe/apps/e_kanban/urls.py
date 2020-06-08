from django.conf.urls import url

from e_kanban.views import JihuaView, ProdectView, LineInfoView

app_name = 'apps.kanban'
urlpatterns = [
    url(r'^jihua/$', JihuaView.as_view(), name='jihua'),  # 计划看板
    url(r'^shengchan/', ProdectView.as_view(), name='shengchan'),  # 生产看板
    url(r'^lineinfo/', LineInfoView.as_view(), name='lineinfo'),  # 生产看板
]
