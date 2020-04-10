FROM ubuntu:18.04

WORKDIR /app

RUN apt-get update
RUN apt-get install wget -y
# installing libpng
RUN wget http://mirrors.kernel.org/ubuntu/pool/main/libp/libpng/libpng12-0_1.2.54-1ubuntu1_amd64.deb -P /tmp
RUN dpkg -i /tmp/libpng12-0_1.2.54-1ubuntu1_amd64.deb

RUN apt-get install vim -y # debugging

# path to libqt-mt.so.3
ENV LD_LIBRARY_PATH=/app

# Installing dependencies
RUN apt-get install libglu1-mesa -y
RUN apt-get install libfontconfig -y
RUN apt-get install libaudio2 -y
RUN apt-get install libjpeg-turbo8 -y
RUN apt-get install libxi6 -y
RUN apt-get install libxrender1 -y
RUN apt-get install libxrandr2 -y
RUN apt-get install libxcursor1 -y
RUN apt-get install libxinerama1 -y
RUN apt-get install libxft2 -y

# install python3
RUN apt-get update && apt-get install -y python3-pip python3-dev
RUN pip3 install setuptools pip --upgrade --force-reinstall
COPY ./src/ /app/src
COPY listen.py /app/listen.py
RUN mkdir /app/common
COPY common/listener_server.py /app/common/listener_server.py
COPY common/utils.py /app/common/utils.py
RUN mv /app/src/* /app/ && rm -rf /app/src