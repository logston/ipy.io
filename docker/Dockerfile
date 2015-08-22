FROM ubuntu:14.04
MAINTAINER Paul Logston <code@logston.me>
LABEL Description="This image is used as a base for all ipython nb mirror containers." Version="0.1.0"

RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y python3-dev
RUN apt-get install -y g++

RUN wget --directory-prefix=/tmp/ https://bootstrap.pypa.io/get-pip.py
RUN python3 /tmp/get-pip.py
RUN pip install "ipython[notebook]"

EXPOSE 8888

