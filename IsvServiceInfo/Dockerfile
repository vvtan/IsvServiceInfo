FROM daocloud.io/vvtan/isv_service_info
MAINTAINER vvtan

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app


RUN apt-get update

RUN apt-get -y install redis-server

RUN pip install scrapy-redis

RUN cd /usr/src/app/IsvServiceInfo

RUN chmod 777 /usr/src/app/IsvServiceInfo/run.sh

EXPOSE 6800

ENTRYPOINT  ["/usr/src/app/IsvServiceInfo/run.sh"]


