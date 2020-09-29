FROM python:3.8-slim

RUN apt update
RUN apt upgrade -y
RUN apt-get install vim -y
RUN apt-get install git -y

# COPY . /BP_app

# WORKDIR /BP_app

# RUN pip3 install -e ".[development]"
# RUN python3 bp_app/initialize_db.py development.ini

# CMD [ "pserve", "development.ini" ]

EXPOSE 6543