# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import Trigger_status, Subsystem_view
from django.contrib.auth.decorators import login_required

from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse
import ssh_check


# Create your views here.

def index(request):
    """zabbix主页"""
    hostinfos = Trigger_status.objects.filter(applicationname='HOST')
    # subsystemnames = Trigger_status.objects.distinct('applicationname').exclude(applicationname='HOST').order_by('-triggervalue')
    subsystemnames = Subsystem_view.objects.all().order_by('-triggervalue', 'applicationname')
    # subsysteminfos = Trigger_status.objects.exclude(applicationname='HOST').order_by('-triggervalue').filter(
    # triggervalue = 1)

    # return render(request, 'zabbix/index.html', {'hostinfos': hostinfos, 'subsysteminfos': subsysteminfos,
    #                                             'subsystemnames': subsystemnames})
    return render(request, 'zabbix/index.html', {'hostinfos': hostinfos, 'subsystemnames': subsystemnames})


@login_required
@accept_websocket
def daily_check_aims(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'maintain/daily_check_aims.html')
    else:
        for message in request.websocket:
            message = message.decode('utf-8')
            if message == 'check':  # 这里根据web页面获取的值进行对应的操作
                command = 'df -h'  # 这里是要执行的命令或者脚本，我这里写死了，完全可以通过web页面获取命令，然后传到这里
                request.websocket.send(ssh_check.exec_command(command))  # 发送消息到客户端
            else:
                request.websocket.send('Access deny!'.encode('utf-8'))


@login_required
@accept_websocket
def daily_check_ib(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'maintain/daily_check_ib.html')
    else:
        for message in request.websocket:
            message = message.decode('utf-8')
            if message == 'check':  # 这里根据web页面获取的值进行对应的操作
                command = 'ls'  # 这里是要执行的命令或者脚本，我这里写死了，完全可以通过web页面获取命令，然后传到这里
                request.websocket.send(ssh_check.exec_command(command))  # 发送消息到客户端
            else:
                request.websocket.send('Access deny!'.encode('utf-8'))
