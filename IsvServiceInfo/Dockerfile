FROM daocloud.io/mingchuan/isv_service_info_crawler:master-0336b00
MAINTAINER vvtan

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

RUN chmod 755 run.sh
RUN cd /usr/src/app/IsvServiceInfo


EXPOSE 6800

ENTRYPOINT  ["/run.sh"]

