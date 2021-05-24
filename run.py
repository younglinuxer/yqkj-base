#!/usr/bin/env python
# -- coding:utf8 --

from flask import Flask, request
import json
from base.apps import *
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

executor = ThreadPoolExecutor(3)


@app.route('/create_pod', methods=["POST"])
def create_pod():
    # data = request.form
    data = request.json
    APP_NAME, NAMESPACE, REPLICAS, MEMORY, PORT, DOCKER_TAG,ZIP_URL = \
        data['app_name'], data['namespace'], data['replica'], data['memory'], \
        data['port'], data['docker_tag'],data['zip_url']
    # if ENABLE_CHECK != 'True': ENABLE_CHECK = False
    #不占用当前线程 编译时间太长
    executor.submit(T_create_pod, APP_NAME=APP_NAME,NAMESPACE=NAMESPACE, REPLICAS=REPLICAS, MEMORY=MEMORY, PORT=PORT,
                    ZIP_URL=ZIP_URL,DOCKER_TAG=DOCKER_TAG)
    return json.dumps({'msg': '创建中 /get_pod_status 查看创建状态'}, ensure_ascii=False)


@app.route('/get_pod_status', methods=["GET"])
def get_pod_status():
    content = request.json
    print(content)
    if not content['app_name'] or not content['namespace']: return json.dumps({'msg': '请传入正常参数'}, ensure_ascii=False)
    APP_NAME, NAMESPACE = content['app_name'], content['namespace']
    print(APP_NAME, NAMESPACE)
    cmd_get_pod_status = "kubectl get pod  -n %s |grep %s|awk '{print $3}'" % (NAMESPACE, APP_NAME)
    print(cmd_get_pod_status)
    data = commands.getstatusoutput(cmd_get_pod_status)[1].split()
    print(data)
    if not data:return json.dumps({'msg': '未查询到该pod'}, ensure_ascii=False)
    if 'Running' in data:
        return json.dumps({'msg': 'pod is running'}, ensure_ascii=False)
    elif 'No' and 'namespace.' in data:
        return json.dumps({'msg':'未查询到namespace '},ensure_ascii=False)
    else:
        return json.dumps({'msg': 'pod is not running'}, ensure_ascii=False)


@app.route('/re_create_ng', methods=["POST"])
def re_create_ng():
    # data = request.form
    data = request.json
    NAMESPACE,NCONF_PATH = data['namespace'],data['nconf_path']
    re_config_ng(NAMESPACE=NAMESPACE,NCONF_PATH=NCONF_PATH)
    return json.dumps({'msg': '创建中 /get_pod_status 查看创建状态'}, ensure_ascii=False)


@app.route('/re_ingress', methods=["POST"])
def re_ingress():
    # data = request.form
    data = request.json
    NAMESPACE = data['namespace']
    re_zebra_ig(NAMESPACE=NAMESPACE)
    return json.dumps({'msg': '创建中 /get_pod_status 查看创建状态'}, ensure_ascii=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True, threaded=True)
