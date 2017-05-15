# -*- coding: utf-8 -*-
#导入django的运行环境，并进行初始化
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
import django
django.setup()

#导入zabbix模块
from zabbix_api import ZabbixAPI
from zabbix.models import Trigger_status

#导入参数模块
import ConfigParser
import ast
cf = ConfigParser.ConfigParser()
cf.read("zabbix.conf")
#初始化各参数
hostnames = ast.literal_eval(cf.get("host","hostnames"))
zapi = ZabbixAPI(server=cf.get("server","serveraddress"))
zapi.login(cf.get("userconfig","user"), cf.get("userconfig","password"))


# 获取hostname的hostid
def get_hostid(host_name):
    return zapi.host.get({"filter": {"host": host_name}})[0]["hostid"]


# 根据hostid,获取trigger的id,状态和解释和取得item的application值
def get_triggerListInfo(hostId):
    trigger_list = []
    trigger_value = []
    trigger_description = []
    trigger_itemid_row = []
    trigger_itemid_list = []
    trigger_itemid = []
    application_row = []
    application_name = []
    # 处理trigger的信息
    temp = zapi.trigger.get({"filter": {"hostid": hostId}, "selectItems": "short"})
    for k in xrange(len(temp)):
        trigger_list.append(temp[k]["triggerid"])
        trigger_value.append(temp[k]["value"])
        trigger_description.append(temp[k]["description"])
        trigger_itemid_row.append(temp[k]["items"])
    for k in xrange(len(trigger_itemid_row)):
        trigger_itemid_list.append([tempid['itemid'] for tempid in trigger_itemid_row[k]])
    for k in xrange(len(trigger_itemid_list)):
        trigger_itemid.append(trigger_itemid_list[k][0])
    # 获得application的信息
    for k in xrange(len(trigger_itemid)):
        application_row.append(zapi.application.get({"itemids": trigger_itemid[k]}))
        application_name.append([tempname['name'] for tempname in application_row[k]])

    triggerListInfo = zip(trigger_list, trigger_value, trigger_description, trigger_itemid, application_name)
    return triggerListInfo


def update_mysql(triggerid, triggervalue, triggername, triggerapplicationname, triggeritemid, host_name):
    Trigger_status.objects.update_or_create(triggerid=triggerid,
                                            defaults={"triggervalue": triggervalue, "triggername": triggername,
                                                      "applicationname": triggerapplicationname, "hostname": host_name,
                                                      "itemid": triggeritemid},
                                            )


for hostname in hostnames:
    hostid = get_hostid(hostname)
    triggerinfos = get_triggerListInfo(hostid)

    for triggerinfo in triggerinfos:
        info_triggerid = triggerinfo[0]
        info_triggervalue = triggerinfo[1]
        info_triggername = triggerinfo[2]
        info_triggeritemid = triggerinfo[3]
        info_triggerapplicationname = triggerinfo[4]
        update_mysql(info_triggerid, info_triggervalue, info_triggername, info_triggerapplicationname[0],
                     info_triggeritemid, hostname)
