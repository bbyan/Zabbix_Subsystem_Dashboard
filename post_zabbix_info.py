#!/usr/bin/python
# coding:utf-8

import os
import django
from django.db import connection
import json
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()


def execute_query(sql):
    cursor = connection.cursor()  # 获得一个游标(cursor)对象
    cursor.execute(sql)
    rawData = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    result = []
    for row in rawData:
        objDict = {}
        # 把每一行的数据遍历出来放到Dict中
        for index, value in enumerate(row):
            objDict[col_names[index]] = value
        result.append(objDict)
        # return json.dumps(result,sort_keys=True)
    return result


def generate_json(query_result):
    data_dict = {'ProvinceID': '1010', '_DATA_': query_result}
    return data_dict


if __name__ == '__main__':
    trigger_status_sql = "select triggerlastchange occurTime,applicationname belongModule," \
                         "triggerid alertID, triggercomment alertDescr,triggerpriority level,triggervalue status " \
                         "from zabbix_trigger_status where applicationname <> 'host'"
    trigger_status = json.dumps(generate_json(execute_query(trigger_status_sql)), sort_keys=True)
    print trigger_status

    # host_status_sql = "select date_format(cast(rowoperatedatetime as char),'%Y-%m-%d %H:%m:%s') RowOperateDatetime," \
    #                   "triggername TriggerName,triggervalue TriggerValue" \
    #                   " from zabbix_trigger_status where applicationname = 'host'"
    # host_status = json.dumps(generate_json(execute_query(host_status_sql)), sort_keys=True)


    # todo:添加post函数
