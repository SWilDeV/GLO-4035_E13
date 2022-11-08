#Database
from dotenv import dotenv_values
from py2neo import Graph

config = dotenv_values(".env")
INTERNAL_URL = config.get("NEO4J_URL")
USERNAME, PASSWORD = config.get("NEO4J_CREDENTIALS").split("/")

class Database:

    def extracted_data_Neo(self):
        GRAPH = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD))
        TRANSACTION = GRAPH.begin()
        try:
            rep=(f'{(TRANSACTION.run("MATCH p=()-[r:est_voisin]->() RETURN count(p) as total").data()[0]["total"])} segments')
            
        except:
            print("prb Neo extracted data")
            return "prb Neo extracted data"
        
        else:
            return rep
    
    def transformed_data_Neo(self):
        GRAPH = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD))
        TRANSACTION = GRAPH.begin()
        try:
            rep=(f'{(TRANSACTION.run("MATCH (:PointCycle)-[r:est_voisin]->(:PointCycle) return  sum(r.longueur) as total").data()[0]["total"]/1000)} KM')
            
        except:
            print("prb Neo transformed data")
            return "prb Neo transformed data"
        
        else:
            return rep