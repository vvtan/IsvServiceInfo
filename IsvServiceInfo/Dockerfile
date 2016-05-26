FROM daocloud.io/mingchuan/isv_service_info_crawler:master-1b70a38
MAINTAINER vvtan

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

RUN chmod 777 run.sh

RUN cd /usr/src/app/IsvServiceInfo


EXPOSE 6800

ENTRYPOINT  ["scrapy", "crawl", "isv_service_info"]
CMD ["-s REDIS_URL=$REDIS_URL"]

