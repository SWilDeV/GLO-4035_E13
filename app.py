import os
from flask import Flask
import time
import sys
from Neo4J import Database

app = Flask(__name__)
app.config.from_object(__name__)


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
        return "error with transformed_data"
    else:
        return {
        "nbRestaurants":"int",
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
    app.run(host='0.0.0.0', port=8080, debug=True)