import os
from flask import Flask
from dotenv import dotenv_values
from py2neo import Graph, Node, Relationship

app = Flask(__name__)

config = dotenv_values(".env")
INTERNAL_URL = config.get("NEO4J_INTERNAL_URL")
USERNAME, PASSWORD = config.get("NEO4J_CREDENTIALS").split("/")
GRAPH = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD))
TRANSACTION = GRAPH.begin()

@app.route("/extracted_data")
def extracted_data():
    return {
        "nbRestaurants":"int",
        "nbSegments":f'{(TRANSACTION.run("MATCH p=()-[r:est_voisin]->() RETURN count(p) as total").data()[0]["total"])} segments'
        }

@app.route("/transformed_data")
def transformed_data():
    return {
        "restaurants":{
            "type1":"int"
        },
        "longueurCyclable":f'{(TRANSACTION.run("MATCH (:PointCycle)-[r:est_voisin]->(:PointCycle) return  sum(r.longueur) as total").data()[0]["total"]/1000)} KM'
        }
    

@app.route("/heartbeat")
def home():
    return {"Montreal":"str"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)