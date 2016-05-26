FROM daocloud.io/vvtan/isv_service_info
MAINTAINER vvtan

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

RUN pip install scrapy-redis

RUN cd /usr/src/app/IsvServiceInfo && \
        scrapy crawl isv_service_info

EXPOSE 6800


