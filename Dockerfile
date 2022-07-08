FROM python:3.8

COPY . /app
WORKDIR /app

RUN apt update && \
    apt install -y tor

#RUN apt-get update && \
#    apt-get install -y software-properties-common && \
#    rm -rf /var/lib/apt/lists/*
#RUN add-apt-repository ppa:micahflee/ppa
#RUN apt update
#
#RUN apt install tor

RUN pip install pipenv
RUN pipenv install --dev --deploy
