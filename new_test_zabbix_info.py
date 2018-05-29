import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

# Import zabbix module
from zabbix_api import ZabbixAPI
from zabbix.models import Trigger_status

# Import configuration module
import ConfigParser
import ast


# Get the host_id of hostname
def get_host_id(host_name):
    return zapi.host.get({"filter": {"host": host_name}})[0]["hostid"]


if __name__ == '__main__':
    # Initialize external parameters
    cf = ConfigParser.ConfigParser()
    cf.read("get_zabbix_info.conf")
    hostnames = ast.literal_eval(cf.get("host", "hostnames"))
    zapi = ZabbixAPI(server=cf.get("server", "serveraddress"))
    zapi.login(cf.get("userconfig", "user"), cf.get("userconfig", "password"))

for hostname in hostnames:
    hostid = get_host_id(hostname)
    temp = zapi.trigger.get({"filter": {"hostid": get_host_id(hostname)}, "selectItems": "short"})

    trigger_list = []
    trigger_eventid = []
    for k in range(len(temp)):
        trigger_list.append(temp[k]["triggerid"])

    for k in range(len(trigger_list)):
        trigger_eventid.append(zapi.event.get(
            {"objectids": trigger_list[k], "sortorder": "DESC", "sortfield": ["clock", "eventid"], "value": "1"})[0])
    print trigger_list
    print trigger_eventid
