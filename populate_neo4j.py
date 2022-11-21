import time
import csv
from decouple import config
from py2neo import Graph


INTERNAL_URL = config("NEO4J_URL")

# We use split to split the NEO4J_AUTH formatted as "user/password"
USERNAME, PASSWORD = config("NEO4J_CREDENTIALS").split("/")

print('Waiting for servers connections')

def populate_neo(url, username, password):
    try:
        print('Trying connection to neo')
        graph = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD), secure=False)
        transaction = graph.begin()
        print('neo connection works')
        
        
        ################### Choix des donnees NEO4J  ##################
        filename = 'data_dev.csv'

        if filename == 'data_dev.csv':
            rowNumb = " / 100"
        else:
            rowNumb = " / 17815"  

        ###############################################################

        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            
            IDPiste1 = ''
            IDPiste2 = ''
            point1 = ''
            point2 = ''
            for row in datareader:
                IDPiste1 = row[1]
                point1 = row[0]
                graph.run(f"CREATE (p:PointCycle) SET p.location = Point({{latitude: {row[4]}, longitude: {row[3]}}}),  p.Quartier = '{row[2]}',  p.IDPiste = '{row[1]}',  p.IdPoint = '{row[0]}'")

                if(IDPiste1 == IDPiste2):
                    graph.run(f"MATCH (a:PointCycle),  (b:PointCycle) WHERE a.IdPoint = '{point1}' AND b.IdPoint = '{point2}' CREATE (a)-[r:est_voisin {{longueur:{row[5]} }}]->(b) RETURN type(r), r.longueur")    
                

                print(row[0] +rowNumb)
                point2 = row[0]
                IDPiste2 = row[1]
        
        print('Neo4J Data inserted')

    except:
        print('Connection to neo failed, will retry in 5 sec')
        time.sleep(5)
        populate_neo(url=url, username=username, password=password)


populate_neo(url=INTERNAL_URL, username=USERNAME, password=PASSWORD)


