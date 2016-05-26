FROM python:2.7.11
MAINTAINER vvtan

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

RUN chmod 777 run.sh
RUN pip install -r requirements.txt
RUN cd /usr/src/app/IsvServiceInfo


EXPOSE 6800

ENTRYPOINT  ["scrapy"]
CMD ["crawl", "isv_service_info","-s REDIS_URL=$REDIS_URL"]

