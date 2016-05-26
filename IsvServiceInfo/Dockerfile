FROM python:2.7.8
MAINTAINER vvtan

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app




RUN pip install -r requirements.txt &&\
    cd /usr/src/app/IsvServiceInfo && \
    chmod 777 run.sh

EXPOSE 6800

ENTRYPOINT  ["./run.sh"]

