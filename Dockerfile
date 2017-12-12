FROM python:2.7

# ENV
ARG PROJ_FOLDER_NAME=ymt-merch-manage
ARG PROJ_NAME=ymt-merch-manage
ENV SERVER_ID container
ENV SERVICE_ID $PROJ_NAME

# set timezone
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install python requirements.txt
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# install software
RUN pip install uwsgi

# copy project files
COPY . /src

# create logs dir
RUN mkdir -p /var/log/axinfu/ymt-merch-appserver/

WORKDIR /src

EXPOSE 80
CMD uwsgi --processes=1 -M --gevent=100 --http-socket :80 -w devel:app

