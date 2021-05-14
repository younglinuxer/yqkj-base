FROM registry.cn-hangzhou.aliyuncs.com/glg/sky-agent:8.0.1
MAINTAINER guojing <13594163317@163.com>
#处理时区新版本是centos 模式, 老版本为ubuntu模式  https://www.hicode.club/articles/2019/05/23/1558624925684.html
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' > /etc/timezone
ADD *.jar /app/app.jar
ENV skyname="risk-biz"
ENV JAVA_OPTS=""
ENV skyip="localhost:11800"
ENV nacosAddr="cloud-nacos:8848"
ENV namespace=""
ENTRYPOINT ["sh","-c","java -javaagent:/skywalking-agent/agent/skywalking-agent.jar -Dskywalking.agent.service_name=$skyname -Dskywalking.collector.backend_service=$skyip -Dspring.cloud.nacos.discovery.server-addr=$nacosAddr -Dspring.cloud.nacos.discovery.namespace=$namespace  $JAVA_OPTS -jar /app/app.jar"]
#运行方式如下 docker run --rm  -p 8080:8080 --name dynamic -e serverAddr=localhost:8848 -e skyname=dev-dynamic-datasource-biz -e skyip=localhost11800 dev-dynamic-module-biz:latest
