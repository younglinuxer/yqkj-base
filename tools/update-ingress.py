#!/usr/bin/env python
# -- coding:utf8 --
import commands
import requests
import uuid,datetime,logging
from apscheduler.schedulers.blocking import BlockingScheduler
logging.basicConfig(filename='./update-ingress.log', level=logging.INFO)

def re_ingress():
    get_namespace = "kubectl get namespaces |grep -v  -E 'kube|nginx|default|NAME|zebra'|awk '{print $1}'"
    for namespace in commands.getstatusoutput(get_namespace)[1].split():
        print(namespace)
        url = "http://127.0.0.1:8081/re_ingress"
        payload = '{"namespace":"%s"}' % namespace
        headers = {'content-type': "application/json"}
        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text)



def exec_apscheduler():
    """Exec
    date: 特定的时间点触发
    interval: 固定时间间隔触发
    cron: 在特定时间周期性地触发
    day_of_week 0-6 or mon,tue,wed,thu,fri,sat,sun)  注意时间从0开始计算 hour 0-23 minutes 0-59
    """
    # today = datetime.datetime.today().strftime('%Y%m%d')
    scheduler = BlockingScheduler()
    """更新所有namespace下的ingress"""
    scheduler.add_job(re_ingress,trigger='interval',minutes=1)
    scheduler.start()

exec_apscheduler()

# re_ingress()
