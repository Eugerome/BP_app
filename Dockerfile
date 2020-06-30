FROM ubuntu:18.04

RUN apt update
RUN apt upgrade -y
RUN apt-get install python3.8 -y
RUN apt-get install python3-pip -y
RUN apt-get install python3-venv -y
RUN apt-get install git -y

EXPOSE 8000