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

# Possibly needed for splitting the volume
#RUN pip3 install simpleitk
#RUN pip3 install numpy

# install python3
RUN apt-get update && apt-get install -y python3-pip python3-dev
RUN pip3 install setuptools pip --upgrade --force-reinstall

COPY files/interface/ /app/
COPY files/source/ /app/

RUN mkdir /app/data_share
ENV DATA_SHARE_PATH /app/data_share

CMD ["python3","-u","/app/run_container_jip.py"]