import time
import csv
from decouple import config
from py2neo import Graph
import geopy.distance
import sys
import string


INTERNAL_URL = config("NEO4J_URL")

# We use split to split the NEO4J_AUTH formatted as "user/password"
USERNAME, PASSWORD = config("NEO4J_CREDENTIALS").split("/")

print('Waiting for servers connections')


def populate_neo(url, username, password):
    try:
        print('Trying connection to neo')
        graph = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD), secure=False)
        print('neo connection works')

        ################### Choix des donnees NEO4J  ##################
        filename = 'data_points.csv'
        filename2 = 'data_pistes.csv'

        ###############################################################

        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile)

            for row in datareader:
                graph.run(
                    f"CREATE (p:PointCycle) SET p.x= {row[1]}, p.y={row[0]}, p.crs='wsg-84'")

        
        with open(filename2, 'r') as csvfile2:
            datareader2 = csv.reader(csvfile2)
            for row2 in datareader2:
                coords_1 = [float(row2[0][(row2[1]).find(",")+1:(row2[1]).find("]")]), float(row2[0][(row2[1]).find("[")+1:(row2[1]).find(",")]) ]
                coords_2 = [float(row2[1][(row2[1]).find(",")+1:(row2[1]).find("]")]), float(row2[1][(row2[1]).find("[")+1:(row2[1]).find(",")]) ]
                distance = float(row2[5])
                piste_id = float(row2[3])
                graph.run(f"MATCH (a:PointCycle),  (b:PointCycle) WHERE a.x ={coords_1[0]} AND a.y={coords_1[1]} AND b.x ={coords_2[0]} AND b.y={coords_2[1]}  CREATE (a)-[r:connecte]->(b) SET r.longueur={distance}, r.piste_id={piste_id}")
     
   
#MATCH (a:PointCycle),  (b:PointCycle) WHERE a.x=45.538599 AND a.y=-73.6057 AND b.x=45.547507 AND b.y=-73.602455 CREATE (a)-[r:connecte {long:1000, id:1}]->(b) return r

        print('Neo4J Multi relations inserted')
        # Ajout des intersections entre pistes cyclables
        # with open(filename2, 'r') as csvfile2:
        #     datareader2 = csv.reader(csvfile2)
        #     counter = 1
        #     for row in datareader2:
        #         graph.run(
        #             f"MATCH (a:PointCycle),  (b:PointCycle) WHERE a.IdPoint = '{row[0]}' AND b.IdPoint = '{row[3]}' CREATE (a)-[r:connexion_extremite {{longueur:{0} }}]->(b) RETURN type(r), r.longueur")
        #         print("intersection: " + str(counter))
        #         counter += 1
        print('Neo4J Data inserted')

    except:
        print('Connection to neo failed, will retry in 5 sec')
        time.sleep(5)
        populate_neo(url=url, username=username, password=password)



populate_neo(url=INTERNAL_URL, username=USERNAME, password=PASSWORD)
# populate_neoV2(url=INTERNAL_URL, username=USERNAME, password=PASSWORD)


