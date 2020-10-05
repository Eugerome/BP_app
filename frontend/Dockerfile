FROM node:14.12.0-buster-slim

RUN apt-get -y update \
  && apt-get install -y git

RUN npm install -g @vue/cli

WORKDIR /frontend

EXPOSE 8080