#!/usr/bin/env python
#-- coding:utf8 --
from make_file import *


def T_create_pod(APP_NAME,NAMESPACE,REPLICAS,MEMORY,PORT,DOCKER_TAG,ZIP_URL):
    # cmd_mkdir = 'mkdir ' + APP_NAME
    # shell(cmd=cmd_mkdir)
    #下载jar包
    # wget.download(JAR_URL,APP_NAME)
    # 生成DockerFile 并编译
    # Make_DockerFile(APP_NAME=APP_NAME,ENABLE_CHECK=ENABLE_CHECK,CHECK_URL=CHECK_URL)
    print("开始创建docker")
    Make_zip_docker(ZIP_URL=ZIP_URL,DOCKER_TAG=DOCKER_TAG)
    Make_YamlFile(APP_NAME=APP_NAME, NAMESPACE=NAMESPACE, REPLICAS=REPLICAS, MEMORY=MEMORY, PORT=PORT,IMAGE=DOCKER_TAG)
    cmd_creat_pod = 'kubectl create -f ./%s/%s' % ('k8s_file', APP_NAME + '-deploy.yaml')
    shell(cmd_creat_pod)
    return