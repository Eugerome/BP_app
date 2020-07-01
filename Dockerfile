FROM python:3.8-slim

RUN apt update
RUN apt upgrade -y
RUN apt-get install vim -y
RUN apt-get install git -y

EXPOSE 8000