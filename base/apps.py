#!/usr/bin/env python
# -- coding:utf8 --
from make_file import *


def T_create_pod(APP_NAME, NAMESPACE, REPLICAS, MEMORY, PORT, DOCKER_TAG, ZIP_URL):
    # cmd_mkdir = 'mkdir ' + APP_NAME
    # shell(cmd=cmd_mkdir)
    # 下载jar包
    # wget.download(JAR_URL,APP_NAME)
    # 生成DockerFile 并编译
    # Make_DockerFile(APP_NAME=APP_NAME,ENABLE_CHECK=ENABLE_CHECK,CHECK_URL=CHECK_URL)
    print("开始创建docker")
    Make_zip_docker(ZIP_URL=ZIP_URL, DOCKER_TAG=DOCKER_TAG)
    Make_YamlFile(APP_NAME=APP_NAME, NAMESPACE=NAMESPACE, REPLICAS=REPLICAS, MEMORY=MEMORY, PORT=PORT, IMAGE=DOCKER_TAG)
    cmd_creat_pod = 'kubectl create -f ./%s/%s' % ('k8s_file', APP_NAME + '-deploy.yaml')
    shell(cmd_creat_pod)
    return


def re_config_ng(NAMESPACE,NCONF_PATH):
    """
    生成nginx 配置文件
    :param NCONF_PATH:
    :param NAMESPACE:
    :return:
    """
    MakeNginxFile(NAMESPACE=NAMESPACE,NCONF_PATH=NCONF_PATH)
    # 重新创建主nginx的 deployment
    update_pod_cmd = "kubectl replace --force  -f  nginx-all/nginx-deployment.yaml"
    shell(update_pod_cmd)
    return


def re_zebra_ig(NAMESPACE):
    """
    动态创建 Ingrees 路由 但当前k8s 版本不支持 不执行
    :param NAMESPACE:
    :return:
    """

    MakeIgYaml(NAMESPACE=NAMESPACE)
    # verification_yaml = "kubeval nginx-all/zebra-ingress.yaml"
    # print(r_shell(verification_yaml))
    # 采用$? 验证是否应用成功 kubeval只能验证语法
    update_ingress_cmd = "kubectl replace --force  -f  nginx-all/zebra-ingress.yaml && echo $?"
    data = r_shell(update_ingress_cmd)
    print(data)
    if data[0] == 0:
        return json.dumps({'msg': '更新ingress 成功'}, ensure_ascii=False)
    else:
        return json.dumps({'msg': '更新ingress 失败'}, ensure_ascii=False)