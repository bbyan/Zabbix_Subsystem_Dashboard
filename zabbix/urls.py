# encoding:utf-8

"""定义zabbix的url模式"""

from django.conf.urls import url

from . import views
from django.conf.urls import include

urlpatterns = [
    # 主页
    url(r'^$', views.index, name='index'),
    url(r'^accounts/', include('registration.backends.simple.urls'),),
]
