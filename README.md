### 部署
```
基于python2.7 
pip install -r requirements.txt
python run.py
```

### 调用
```
#创建编译镜像并创建pod
http://192.168.44.130:8081/create_pod

curl --location --request POST 'http://192.168.44.130:8081/create_pod' \
--header 'Content-Type: application/json' \
--data-raw '{
    "app_name":"yqkj-demo2",
    "enable_check":"True",
    "check_url":"http://localhost",
    "namespace":"default",
    "replica":"1",
    "memory":"500Mi",
    "port":"80",
    "jar_url":"https://iptables.cn/file/demo.jar",
    "docker_tag":"younglinuxer/yqkj-demo2:latest"
}'

参数说明:
app_name:服务名 pod service 都是这个名字
enable_check: 编译Dockerfile 的时候是否开启健康检查  需要 True
check_url: 如果开启健康检查 需要配置健康检查的地址 
namespace: k8s对应的namespace
replica: k8s对应需要生成的多少个pod
memory:pod内存限制 500m的写法500Mi  2g的写法 2Gi
port: 应用的端口 和创建service 的对应端口
jar_url: 程序jar包对应的下载地址
docker_tag:docker编译镜像的tag 及k8s下载镜像的地址



# 查看pod 状态 post
http://192.168.44.130:8081/get_pod_status


curl --location --request GET 'http://192.168.44.130:8081/get_pod_status' \
--header 'Content-Type: application/json' \
--data-raw '{"app_name":"yqxkj-demo","namespace":"app"}'

参数说明： {"app_name":"yqkj-demo","namespace":"app"}
app_name: 服务名 
namespace: k8s namespace  

{"msg": "未查询到该pod"}
{"msg": "pod is not running"}
{"msg": "pod is running"}
```