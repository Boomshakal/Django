from django.conf.urls import include, static
from django.contrib import admin
from django.urls import path, re_path

from ERP import settings
import workflow.views
import invent.urls
import basedata.urls
import selfhelp.urls
import ERP.views

urlpatterns = [
    re_path(r'^$', ERP.views.home),
    re_path(r"^admin/(?P<app>\w+)/(?P<model>\w+)/(?P<object_id>\d+)/start", workflow.views.start),
    re_path(r"^admin/(?P<app>\w+)/(?P<model>\w+)/(?P<object_id>\d+)/approve/(?P<operation>\d+)",
            workflow.views.approve),
    re_path(r"^admin/(?P<app>\w+)/(?P<model>\w+)/(?P<object_id>\d+)/restart/(?P<instance>\d+)", workflow.views.restart),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^admin/invent/', include(invent.urls)),
    re_path(r'^admin/basedata/', include(basedata.urls)),
    re_path(r'^admin/selfhelp/', include(selfhelp.urls)),
]
urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
