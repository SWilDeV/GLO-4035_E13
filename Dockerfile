# syntax=docker/dockerfile:1

FROM python:3.10.6-slim-buster

WORKDIR /app


COPY populate_neo4j.py populate_neo4j.py
COPY populate_mongo.py populate_mongo.py
COPY data_full.csv data_full.csv
COPY data_short.csv data_short.csv
COPY businesses.geojson businesses.geojson
COPY app.py app.py
COPY Neo4J.py Neo4J.py
COPY .env .env
COPY requirements.txt requirements.txt
RUN pip install -Ur requirements.txt
