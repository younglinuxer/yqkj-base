#!/usr/bin/env python
# -- coding:utf8 --
import os
from shell import *
from jinja2 import Environment, FileSystemLoader
import zipfile
import wget


def Make_DockerFile(APP_NAME='test-demo', ENABLE_CHECK=False, CHECK_URL=''):
    """
    :param APP_NAME: jar包名 服务名
    :param ENABLE_CHECK: 是否在Dockerfile中开启 健康检查
    :param CHECK_URL: 健康检查的url
    :return:
    """
    dir_name = APP_NAME + '/Dockerfile'
    if ENABLE_CHECK and CHECK_URL == '':
        print("开启健康检查 需要传入CHECK_URL")
        return
    env = Environment(loader=FileSystemLoader("./"))
    template = env.get_template('./template/Dockerfile.j2')
    content = template.render(APP_NAME=APP_NAME, ENABLE_CHECK=ENABLE_CHECK, CHECK_URL=CHECK_URL)
    with open(dir_name, 'w') as fp:
        fp.write(content)


def Make_zip_docker(ZIP_URL='https://iptables.cn/file/demo-mgr.zip', DOCKER_TAG='younglinuxer/xxxx:v1'):
    """
    下载zip 镜像并编译成docker镜像 推送至远程仓库
    :param ZIP_URL: 压缩包下载地址  注意命名以zip包命名
    :param APP_NAME: app_name
    :param DOCKER_TAG: docker镜像 命名
    :return:
    """
    print("下载文件并编译")
    file_name = os.path.basename(ZIP_URL)  # 获取 zip名
    unzip_dir = os.path.splitext(file_name)[0]  # 获取zip解压后的文件名
    cmd_build_docker = 'docker build -t %s ./docker_file/%s' % (DOCKER_TAG, unzip_dir)
    cmd_push_docker = 'docker push %s' % (DOCKER_TAG)
    # 用app_name 命名 防止zip传入的命名有问题
    # wget.download(ZIP_URL, '../zip_file/%s.zip' % APP_NAME)
    # 如果原文件存在 则删除该文件 后在下载
    if os.path.exists('./zip_file/%s' % file_name): os.remove('./zip_file/%s' % file_name)
    wget.download(ZIP_URL, './zip_file/%s' % file_name)
    print('删除解压文件夹')
    # if os.path.exists('./docker_file/%s' % unzip_dir): os.remove('./docker_file/%s' % unzip_dir)
    zipF = zipfile.ZipFile('./zip_file/%s' % file_name, 'r')
    zipF.extractall('./docker_file/')
    zipF.close()
    shell(cmd_build_docker)
    shell(cmd_push_docker)
    # return


def Make_YamlFile(APP_NAME='test-demo', NAMESPACE='app', REPLICAS=1, MEMORY='1Gi', PORT='80', IMAGE='nginx'):
    """
    用于生成 k8s deployment & services yaml file
    :param APP_NAME: 应用名字
    :param NAMESPACE: 程序命名空间
    :param REPLICAS: 运行个数
    :param MEMORY: 内存限制
    :param PORT: 程序端口
    :return:
    """
    name = 'k8s_file' + '/' + APP_NAME + '-deploy.yaml'
    env = Environment(loader=FileSystemLoader("./"))
    template = env.get_template('./template/app-deploy.yaml.j2')
    content = template.render(APP_NAME=APP_NAME, NAMESPACE=NAMESPACE, REPLICAS=REPLICAS, MEMORY=MEMORY, PORT=PORT,
                              IMAGE=IMAGE)

    with open(name, 'w') as fp:
        fp.write(content)
    # return

# Make_zip_docker()
