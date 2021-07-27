#!/usr/bin/env python
# -- coding:utf8 --
import json
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


def MakeNginxFile(NAMESPACE="young-sit", NCONF_PATH="nginx-all/nginx-all.conf"):
    """
    根据获取的services 生成nginx.conf
    :param NAMESPACE: 获取该namespace下的services
    :return:
    """
    get_all_svc = "kubectl get svc -n %s |grep '80/TCP'|awk '{print $1}'" % NAMESPACE
    SVC_LIST = r_shell(get_all_svc)[1].split()
    # SVC_LIST=('young','younglinuxer')
    print(SVC_LIST)
    env = Environment(loader=FileSystemLoader("./"))
    template = env.get_template('./template/nginxconf.j2')
    # template = env.get_template('./template/nginxconf_test.j2')
    content = template.render(SVC_LIST=SVC_LIST)
    with open(NCONF_PATH, 'w') as ng:
        ng.write(content.encode('utf-8'))
    # return


def MakeIgYaml(NAMESPACE="young-sit"):
    """
    :param NAMESPACE: g
    :return:
    """
    get_zebra_ingress = "kubectl get  ingress -n %s  zebra-ui   -o json" % NAMESPACE
    get_all_svc = "kubectl get svc -n %s |grep '80/TCP'|awk '{print $1}'" % NAMESPACE
    # 通过命令获取服务列表
    SVC_LIST = r_shell(get_all_svc)[1].split()
    zebra_ingress = json.loads(r_shell(get_zebra_ingress)[1])
    # 获取zebra-ui 下绑定的域名
    DOMAIN = zebra_ingress["spec"]["rules"][0]["host"]
    # ["spec"]["rules"][0]["host"]
    print('xxxxxxxxxxxxxxxx',DOMAIN)
    SVC_IN_LIST = []
    for i in zebra_ingress["spec"]["rules"][0]["http"]["paths"]:
        SVC_IN_LIST.append(i["backend"]["service"]["name"])
    if "found" in SVC_LIST:
        logger.info("未获取到服务列表")
        return
    else:
        logger.info("获取域名: %s 获取服务列表:%s "% (DOMAIN,SVC_LIST))
        name = 'nginx-all' + '/' + 'zebra-ingress.yaml'
        env = Environment(loader=FileSystemLoader("./"))
        template = env.get_template('./template/nginx-ingress.yaml.j2')
        content = template.render(SVC_LIST=SVC_LIST,DOMAIN=DOMAIN,NAMESPACE=NAMESPACE)
        with open(name, 'w') as ng:
            ng.write(content.encode('utf-8'))
    return 0