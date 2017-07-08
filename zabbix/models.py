# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# Create your models here.
class Trigger_status(models.Model):
    rowcreatedatetime = models.DateTimeField(auto_now_add=True)
    rowoperatedatetime = models.DateTimeField(auto_now=True)
    triggerid = models.IntegerField(primary_key=True)
    triggervalue = models.IntegerField()
    triggername = models.CharField(max_length=300, null=True)
    itemid = models.IntegerField()
    applicationname = models.CharField(max_length=20)
    hostname = models.CharField(max_length=40, null=True)

    def __unicode__(self):
        return self.triggername

class Subsystem_view(models.Model):
    applicationname = models.CharField(primary_key=True,max_length=200)
    triggervalue = models.IntegerField()
    triggername = models.CharField(max_length=300,null=True)

    class Meta:
        managed = False
        db_table = "zabbix_subsystemname"
    def __unicode__(self):
        return self.applicationname