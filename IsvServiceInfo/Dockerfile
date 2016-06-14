FROM daocloud.io/mingchuan/isv_service_info_crawler:master-0336b00
MAINTAINER vvtan

RUN mkdir -p /usr/src/app
RUN mkdir -p /tmp/childlog
RUN mkdir -p /etc/supervisor/conf.d
WORKDIR /usr/src/app
COPY . /usr/src/app
COPY ./app.conf /etc/supervisor/conf.d/app.conf

RUN chmod 755 run.sh
RUN cd /usr/src/app/IsvServiceInfo
RUN cp /etc/localtime /etc/localtime.bak
RUN ln -svf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN easy_install supervisor


EXPOSE 6800

ENTRYPOINT  ["./run.sh"]

