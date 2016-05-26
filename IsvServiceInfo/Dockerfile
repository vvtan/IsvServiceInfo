FROM daocloud.io/vvtan/isv_service_info
MAINTAINER vvtan

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app




RUN cd /usr/src/app/IsvServiceInfo

RUN chmod 777 run.sh

EXPOSE 6800

ENTRYPOINT  ["./run.sh"]

