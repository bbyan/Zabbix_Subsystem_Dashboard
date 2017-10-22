# encoding:utf-8

"""定义zabbix的url模式"""

from django.conf.urls import url

from . import views
from django.conf.urls import include

urlpatterns = [
    # 主页
    url(r'^$', views.index, name='index'),
    url(r'^accounts/', include('registration.backends.simple.urls'), ),
    url(r'^daily/aims/', views.daily_check_aims, name='dailycheck_aims'),
    url(r'^daily/ib_server/', views.daily_check_ib, name='dailycheck_ib'),
]
