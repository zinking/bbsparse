FROM ubuntu:latest

MAINTAINER zinking3@gmail.com


RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python python-pip
RUN apt-get install -y git
RUN apt-get install -y python-mysqldb python-setuptools python-urllib3
RUN apt-get install -y cron

RUN mkdir /bbsparse
RUN git clone https://github.com/zinking/bbsparse.git /bbsparse

RUN ln -sfn /data/bbsparse/volume/pageharvest/secrets.py /bbsparse/pageharvest/secrets.py
RUN ln -sfn /data/bbsparse/volume/pageharvest/settings.py /bbsparse/pageharvest/settings.py
RUN ln -sfn /data/bbsparse/volume/settings.py /bbsparse/settings.py

RUN cp /bbsparse/bbsparse-cron /etc/cron.d/
RUN chmod 0644 /etc/cron.d/bbsparse-cron
RUN cron


RUN pip install -r /bbsparse/requirements.txt

EXPOSE 8001

RUN chmod 0744 /bbsparse/docker/entry_point.sh

ENTRYPOINT ["/bbsparse/docker/entry_point.sh"]
