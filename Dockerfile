FROM python:2.7
MAINTAINER younglinuxer younglinuxer@gamil.com



ENV APP_HOME /yqkj-base
WORKDIR $APP_HOME

COPY base $APP_HOME/base
COPY docker_file $APP_HOME/docker_file
COPY k8s_file $APP_HOME/k8s_file
COPY nginx-all $APP_HOME/nginx-all
COPY template $APP_HOME/template
COPY zip_file $APP_HOME/zip_file
COPY requirements.txt $APP_HOME/requirements.txt
COPY run.py $APP_HOME/run.py
RUN pip install -r /yqkj-base/requirements.txt

#CMD [ "sleep", "360000000" ]
CMD [ "python", "/yqkj-base/run.py"]