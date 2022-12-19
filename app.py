import os
from flask import Flask, render_template, request, redirect
from flask import jsonify
import time
import sys
from Neo4J import NeoDatabase
from Mongo import MongoDatabase
# import pymongo
from dotenv import dotenv_values
import markdown
app = Flask(__name__)
app.config.from_object(__name__)


config = dotenv_values(".env")
# MONGO_URL = config.get("MONGO_URL")

content = {'ListeTypes': "---"}


@app.route("/hello", methods=("GET", "POST"))
def hello():
    if request.method == "POST":
        dbMongo = MongoDatabase()
        mongoData = dbMongo.transformed_data_Mongo()
        content['ListeTypes'] = mongoData

    return render_template('Fields.html', content=content)


@app.route("/heartbeat")
def home():
    return {"villeChoisie": "Montreal"}


@app.route('/extracted_data', methods=['GET'])
def extracted_data():

    dbNeo = NeoDatabase()
    Neodata = dbNeo.extracted_data_Neo()

    dbMongo = MongoDatabase()
    MongoData = dbMongo.extracted_data_Mongo()

    return {
        "nbRestaurants": MongoData,
        "nbSegments": Neodata
    }


@app.route("/transformed_data")
def transformed_data():

    dbNeo = NeoDatabase()
    Neodata = dbNeo.transformed_data_Neo()

    dbMongo = MongoDatabase()
    MongoData = dbMongo.transformed_data_Mongo()

    return {
        "restaurants": MongoData,
        "longueurCyclable": Neodata
    }


@app.route("/parcours")
def parcours():

    request_data = request.get_json()
    length = request_data["length"]
    type = request_data["type"]
    coordinates = request_data["startingPoint"]["coordinates"]
    if (len(type) > 1):
        type = type[0]

    dbNeo = NeoDatabase()
    ListeParcours = dbNeo.parcours_point(
        coordinates[1], coordinates[0], length, type)
    LongueurTotale = ListeParcours["totalCost"]
    data = []
    for element in ListeParcours["nodesCoord"]:
        data.append(element)

    dbMongo = MongoDatabase()
    ParcoursData = dbMongo.queryMongoDBForNeoData(data, type)

    return {
        "data": ParcoursData,
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point"
                },
                "properties": {
                    "name": "str",
                    "type": type
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "MultiLineString",
                    "coordinates": [
                        [
                            [
                                "float",
                                "float"
                            ],
                            [
                                "float",
                                "float"
                            ],
                            [
                                "float",
                                "float"
                            ]
                        ]
                    ]
                },
                "properties": {
                    "length": LongueurTotale
                }
            }
        ]

    }


@app.route("/adjacent/<idNode>")
def adjacent(idNode):

    dbNeo = NeoDatabase()
    Neodata = dbNeo.adjacent(idNode)

    return Neodata


@app.route("/path/<idNode>/<nNodes>")
def paths(idNode, nNodes):

    dbNeo = NeoDatabase()
    Neodata = dbNeo.paths(idNode, int(nNodes))

    return Neodata


@app.route("/readme")
def readme():
    readme = open("readme.md", "r")
    template = markdown.markdown(readme.read())
    return template


@app.route("/type")
def type():
    dbMongo = MongoDatabase()
    MongoData = dbMongo.extracted_type_Mongo()
    return MongoData


@app.route("/starting_point", methods=['POST'])
def starting_point():
    request_data = request.get_json()
    length = request_data["length"]
    type = request_data["type"]
    dbNeo = NeoDatabase()
    NeoData = dbNeo.getPathFromLength(length, type)
    return NeoData


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
