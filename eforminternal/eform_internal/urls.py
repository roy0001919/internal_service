from django.contrib import admin
from django.urls import path, include
from django.views import static ##新增
from django.conf import settings ##新增
from django.conf.urls import url ##新增


urlpatterns = [
    path('eform/admin/', admin.site.urls),
    path('eform/', include('eform.urls', namespace='eform')),
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
    # url(r'^', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]