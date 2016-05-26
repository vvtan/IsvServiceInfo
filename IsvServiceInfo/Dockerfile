FROM daocloud.io/vvtan/isv_service_info
MAINTAINER vvtan

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

RUN echo /usr/bin/redis-server >> /etc/rc.local


RUN apt-get update

RUN apt-get -y install redis-server

RUN cd /usr/src/app/IsvServiceInfo

EXPOSE 6800

ENTRYPOINT  ["scrapy crawl isv_service_info"]


