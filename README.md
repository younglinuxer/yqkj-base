### 部署
```
基于python2.7 
pip install -r requirements.txt
python run.py
```

### 目录说明
```
docker_file: zip包下载后解压的目录 包含Dockerfile 和jar包
zip_file: zip_file 下载临时存储的位置 
k8s_file: 生成的k8s部署文件
```

### 调用
```
#创建编译镜像并创建pod
http://192.168.44.130:8081/create_pod

curl --location --request POST 'http://192.168.44.130:8081/create_pod' \
--header 'Content-Type: application/json' \
--data-raw '{
    "app_name":"yqkj-app",
    "namespace":"default",
    "replica":"2",
    "memory":"500Mi",
    "port":"80",
    "docker_tag":"registry.cn-hangzhou.aliyuncs.com/jck/young-demo:v1",
    "zip_url":"https://iptables.cn/file/demo-mgr.zip"
}'



参数说明:
app_name:服务名 pod service 都是这个名字
zip_url: jar包和Dockerfile 压缩包的下载地址
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