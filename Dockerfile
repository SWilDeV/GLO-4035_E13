# syntax=docker/dockerfile:1

FROM python:3.10.6-slim-buster
RUN pip install --upgrade pip

WORKDIR /projet_longitudinal
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

COPY populate_neo4j.py populate_neo4j.py
COPY .env .env
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .


CMD [ "python", "app.py"]