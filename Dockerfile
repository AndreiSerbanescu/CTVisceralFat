FROM ubuntu:18.04

WORKDIR /app

RUN export LD_LIBRARY_PATH=/app/:$LD_LIBRARY_PATH

RUN apt-get update
RUN apt install zlib1g