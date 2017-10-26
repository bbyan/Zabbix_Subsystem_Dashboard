#coding:utf-8
import paramiko
from django.shortcuts import render
from django.http import HttpResponse


def exec_command(comn):
    hostname = '10.211.55.111'
    username = 'zabbix'
    password = '57336969'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(comn)
    result = stdout.read()
    ssh.close()
    return result

