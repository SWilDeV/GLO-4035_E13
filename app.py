import os
from flask import Flask
import time
import sys
from Neo4J import Database
import pymongo
from dotenv import dotenv_values
app = Flask(__name__)
app.config.from_object(__name__)

config = dotenv_values(".env")
MONGO_URL = config.get("MONGO_URL")

client = pymongo.MongoClient(MONGO_URL)
db = client["travaille_longitudinal"]
col = db["travaille_longitudinal_data"]

@app.route("/heartbeat")
def home():
    return {"Montreal":"str"}


@app.route('/extracted_data', methods=['GET'])
def extracted_data():
    try:
        db=Database()
        data = db.extracted_data_Neo()
        
    except:
        print("Oops!", sys.exc_info()[1], "occurred.")
        print("error with extracted_data")
        return "error with transformed_data "
    else:
        return {
        "nbRestaurants":col.count_documents({}),
        "nbSegments":data
        }


@app.route("/transformed_data")
def transformed_data():
    try:
        db=Database()
        data = db.transformed_data_Neo()
    except:
        print("Oops!", sys.exc_info()[1], "occurred.")
        print("error with transformed_data")
        return "error with transformed_data"
    else:
        print(col.find_one({"name":"LES ENTREPRISES ALJO"}))
        return {"restaurants":{
            "type1":"int"
        },
        "longueurCyclable":data
        }

# @app.route("/extracted_data")
# def extracted_data():
#     return {
#         "nbRestaurants":"int",
#         "nbSegments":f'{(TRANSACTION.run("MATCH p=()-[r:est_voisin]->() RETURN count(p) as total").data()[0]["total"])} segments'
#         }

# @app.route("/transformed_data")
# def transformed_data():
#     return {
#         "restaurants":{
#             "type1":"int"
#         },
#         "longueurCyclable":f'{(TRANSACTION.run("MATCH (:PointCycle)-[r:est_voisin]->(:PointCycle) return  sum(r.longueur) as total").data()[0]["total"]/1000)} KM'
#         }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)