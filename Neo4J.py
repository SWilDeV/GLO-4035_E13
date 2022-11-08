#Database
from dotenv import dotenv_values
from py2neo import Graph

config = dotenv_values(".env")
INTERNAL_URL = config.get("NEO4J_URL")
USERNAME, PASSWORD = config.get("NEO4J_CREDENTIALS").split("/")

class Database:
    def __init__(self):
        # We wait for services Neo4J to start
        def validate_neo_connection(url, username, password):
            try:
                print('Trying connection to neo (App)')
                Graph(
                    url,
                    auth=(username, password),
                    secure=False
                )
                print('neo connection works')
            except:
                print('Connection to neo failed, will retry in 10 sec')
                #return(str("Oops!", sys.exc_info()[1], "occurred."))
                #time.sleep(5)
                #validate_neo_connection(url=url, username=username, password=password)
        
        #validate_neo_connection(url=INTERNAL_URL, username=USERNAME, password=PASSWORD)


    def extracted_data_Neo(self):
        GRAPH = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD))
        TRANSACTION = GRAPH.begin()
        try:
            rep=(f'{(TRANSACTION.run("MATCH p=()-[r:est_voisin]->() RETURN count(p) as total").data()[0]["total"])} segments')
            
        except:
            print("prb extracted data")
            return "prb extracted data"
        
        else:
            return rep
    
    def transformed_data_Neo(self):
        GRAPH = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD))
        TRANSACTION = GRAPH.begin()
        try:
            rep=(f'{(TRANSACTION.run("MATCH (:PointCycle)-[r:est_voisin]->(:PointCycle) return  sum(r.longueur) as total").data()[0]["total"]/1000)} KM')
            
        except:
            print("prb extracted data")
            return "prb extracted data"
        
        else:
            return rep