# syntax=docker/dockerfile:1

FROM python:3.10.6-slim-buster

WORKDIR /app


COPY populate_neo4j.py populate_neo4j.py
COPY populate_mongo.py populate_mongo.py
COPY source/data_pistes.csv data_pistes.csv
COPY source/data_point_with_mongo.csv data_point_with_mongo.csv
COPY source/MongoData.geojson MongoData.geojson
COPY createGraph.py createGraph.py
COPY app.py app.py
COPY Mongo.py Mongo.py
COPY Neo4J.py Neo4J.py
COPY .env .env
COPY requirements.txt requirements.txt
COPY Fields.html templates/Fields.html
COPY readme.md readme.md
RUN pip install -Ur requirements.txt
