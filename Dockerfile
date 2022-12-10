# syntax=docker/dockerfile:1

FROM python:3.10.6-slim-buster

WORKDIR /app


COPY populate_neo4j.py populate_neo4j.py
COPY populate_mongo.py populate_mongo.py
COPY source/data_full.csv data_full.csv
COPY source/data_short.csv data_short.csv
COPY source/dataV3_short.csv dataV3_short.csv
COPY source/dataV3.csv dataV3.csv
COPY source/data_dev.csv data_dev.csv
COPY source/intersection_extremites_short.csv intersection_extremites_short.csv
COPY source/multinodes_extremites_short.csv multinodes_extremites_short.csv
COPY source/multinodes_extremites2.csv multinodes_extremites2.csv
COPY source/basicRelations_short.csv basicRelations_short.csv
COPY source/basicRelations.csv basicRelations.csv
COPY source/intersection_short.csv intersection_short.csv
COPY source/intersection.csv intersection.csv
COPY source/data_points.csv data_points.csv
COPY source/data_pistes.csv data_pistes.csv
COPY businesses.geojson businesses.geojson
COPY app.py app.py
COPY Mongo.py Mongo.py
COPY Neo4J.py Neo4J.py
COPY .env .env
COPY requirements.txt requirements.txt
RUN pip install -Ur requirements.txt
