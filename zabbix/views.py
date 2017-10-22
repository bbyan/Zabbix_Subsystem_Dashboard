# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import Trigger_status, Subsystem_view
from django.contrib.auth.decorators import login_required

# for auth
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse


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
def daily_check_aims(request):
    return render(request, 'maintain/daily_check_aims.html')


@login_required
def daily_check_ib(request):
    return render(request, 'maintain/daily_check_ib.html')
