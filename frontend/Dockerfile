FROM python:3.8-slim

RUN apt update
RUN apt upgrade -y
RUN apt-get install vim -y
RUN apt-get install git -y

# VOLUME ./BP_app

# RUN ls

# WORKDIR /BP_app

# # installing backend
# RUN ls
# RUN cd /cool/BP_app/backend && pip3 install -e ".[development]" && python3 bp_app/initialize_db.py development.ini

EXPOSE 6543