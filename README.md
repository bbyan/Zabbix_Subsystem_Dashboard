## 基于Django、bootstrap和zabbix的监控展示页面
- get_zabbix_info.py用于获取'zbbix'监控平台的相关`item`，`trigger`，`trigger_name`，`trigger_status`,`application`的数据，并通过`Django`的ORM，向`mysql`中写数据。
- Django以子系统为单位，显示网页内容。
