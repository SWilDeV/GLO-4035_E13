import os
from flask import Flask, render_template, request, redirect
from flask import jsonify
import time
import sys
from Neo4J import NeoDatabase
from Mongo import MongoDatabase
import random
import geopy.distance
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
    # -----Get info from payload----
    request_data = request.get_json()
    length = request_data["length"]
    NbreArrets = request_data["numberOfStops"]
    coordinates = request_data["startingPoint"]["coordinates"]
    try:
        typeR = request_data["type"]
    except:
        typeR = ['Restaurant']
    typeR = typeR[0]

    # ---------Get path with Neo4J------------
    dbNeo = NeoDatabase()
    ListeParcours = dbNeo.parcours_point(
        coordinates[1], coordinates[0], length, typeR)
    if ListeParcours == "empty":
        return "No path found for type " + typeR
    LongueurTotale = ListeParcours["totalCost"]
    data = []
    for element in ListeParcours["nodesCoord"]:
        data.append(element)

    # ---------Get Restaurants info from Neo4J path------------
    dbMongo = MongoDatabase()
    ParcoursData = dbMongo.queryMongoDBForNeoData(data, typeR)
    lenPD = len(ParcoursData)
    print("lenPD: " + str(lenPD))
    Paths = []
    for element in ParcoursData:
        Paths.append(element[1])

    # ---------Create response--------------
    listSplitting = getSplitting(NbreArrets, lenPD-2)

    coord1 = ParcoursData[0][1]
    start = 0
    finalResult = []
    position = 0

    print(LongueurTotale)
    if (NbreArrets > 0):
        # listSplitting.sort()
        print(listSplitting)
        print("---------------------------------------")
        for element in listSplitting:
            position = position + element
            print(position)
            print(coord1)
            point = resultPoint(
                ParcoursData[position][2], typeR, ParcoursData[position][3])

            subPaths = []
            distance = 0
            for i in range(start, position):
                subPaths.append(Paths[i])
            for el in subPaths:
                distance = distance + int(getDistance(coord1, el))
                coord1 = el
            print("distance "+str(distance))
            start = position
            print("start "+str(start))
            lines = resultMultiline(distance, subPaths)
            finalResult = finalResult + point + lines
            print("---------------------------------------")
        pointFinal = resultPoint(
            ParcoursData[lenPD-1][2], typeR, ParcoursData[lenPD-1][3])
        distance = 0
        subPaths = []
        for i in range(start, lenPD):
            subPaths.append(Paths[i])
        for el in subPaths:
            distance = distance + int(getDistance(coord1, el))
            coord1 = el
        print("distance "+str(distance))
        linesFinal = resultMultiline(distance, subPaths)
        finalResult = finalResult + pointFinal + linesFinal

    elif NbreArrets == 0:

        pointFinal = resultPoint(
            ParcoursData[lenPD-1][2], typeR, ParcoursData[lenPD-1][3])

        subPaths = []
        distance = 0
        for i in range(start, lenPD):
            subPaths.append(Paths[i])

        for el in subPaths:
            distance = distance + int(getDistance(coord1, el))
            coord1 = el
        print("distance "+str(distance))
        linesFinal = resultMultiline(distance, subPaths)
        finalResult = finalResult + pointFinal + linesFinal

    return {"type": "FeatureCollection",
            "features": finalResult}


def getDistance(coords_1, coords_2):
    coord1a = [coords_1[1], coords_1[0]]
    coord2a = [coords_2[1], coords_2[0]]
    distance = geopy.distance.geodesic(coord1a, coord2a).m
    return distance


def getSplitting(NbreArret, lenPD):
    if (NbreArret <= 0):
        return lenPD
    list = []
    while (len(list) != NbreArret):
        list = splitter(lenPD)
    return list


def splitter(lenPD, lst=[]):
    if lenPD == 0:
        return lst
    n = random.randint(1, lenPD)
    return splitter(lenPD - n, lst + [n])


def resultPoint(NomResto, typeR, coordonneeResto):
    return [{
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates":  coordonneeResto
        },
        "properties": {
            "name": NomResto,
            "Type": typeR
        }
    }]


def resultMultiline(LongueurSegment, coordonneeNodes):
    return [{
        "type": "Feature",
        "geometry": {
            "type": "MultiLineString",
            "coordinates": [coordonneeNodes]
        },
        "properties":{
            "length": LongueurSegment
        }
    }]

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


@app.route("/starting_point")
def starting_point():
    try:
        request_data = request.get_json()
    except:
        return "No payload"
    try:
        length = request_data["length"]
        type = request_data["type"]
    except:
        return "Invalid payload"
    dbNeo = NeoDatabase()
    NeoData = dbNeo.getPathFromLength(length, type)
    return NeoData


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
