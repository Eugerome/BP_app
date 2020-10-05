FROM node:carbon-slim

RUN apt-get -y update \
  && apt-get install -y git

RUN npm install -g @vue/cli

WORKDIR /frontend

EXPOSE 8080