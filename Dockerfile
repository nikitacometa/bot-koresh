FROM python:3.9

COPY . /app
WORKDIR /app

RUN apt update && \
    apt install -y tor

RUN pip3 install pipenv
RUN pipenv lock
RUN pipenv install --dev --deploy
