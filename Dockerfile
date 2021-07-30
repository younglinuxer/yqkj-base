FROM python:2.7
MAINTAINER younglinuxer younglinuxer@gamil.com

ENV APP_HOME /yqkj-base
WORKDIR $APP_HOME
# 复制项目文件
COPY base $APP_HOME/base
COPY docker_file $APP_HOME/docker_file
COPY k8s_file $APP_HOME/k8s_file
COPY nginx-all $APP_HOME/nginx-all
COPY template $APP_HOME/template
COPY zip_file $APP_HOME/zip_file
COPY tools $APP_HOME/tools
COPY requirements.txt $APP_HOME/requirements.txt
COPY run.py $APP_HOME/run.py

ADD start.sh /bin/start
RUN chmod +x /bin/start
RUN pip install -r /yqkj-base/requirements.txt

## crontab for younglinuxer
#RUN nohup python /yqkj-base/tools/update-ingress.py  > /dev/null 2>&1 &

#CMD [ "sleep", "360000000" ]
#CMD [ "python", "/yqkj-base/run.py"]
CMD ["/bin/bash","-c","start"]