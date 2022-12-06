import time
import csv
from decouple import config
from py2neo import Graph
import geopy.distance
import sys


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
        filename = 'data_short.csv'

        if filename == 'data_short.csv':
            rowNumb = " / 1000"
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
                graph.run(
                    f"CREATE (p:PointCycle) SET p.location = Point({{latitude: {row[4]}, longitude: {row[3]}}}),  p.Quartier = '{row[2]}',  p.IDPiste = '{row[1]}',  p.IdPoint = '{row[0]}'")

                if (IDPiste1 == IDPiste2):
                    graph.run(
                        f"MATCH (a:PointCycle),  (b:PointCycle) WHERE a.IdPoint = '{point1}' AND b.IdPoint = '{point2}' CREATE (a)-[r:est_voisin {{longueur:{row[5]} }}]->(b) RETURN type(r), r.longueur")

                print(row[0] + rowNumb)
                point2 = row[0]
                IDPiste2 = row[1]
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


def populate_neoV2(url, username, password):
    try:
        print('Trying connection to neo')
        graph = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD), secure=False)
        transaction = graph.begin()
        print('neo connection works')

        # insertPoints(graph,'dataV3_short.csv') #Insert Points
        # insertBasicRelations(graph, 'basicRelations_short.csv') # Insert Basic Relations
        # insertMultiRelations(graph,'multinodes_extremites_short.csv') # Insert Multi Relations

        # insertPoints(graph, 'dataV3.csv')  # Insert Points
        # # Insert Basic Relations
        # insertBasicRelations(graph, 'basicRelations.csv')
        # # Insert Multi Relations
        # insertMultiRelations(graph, 'multinodes_extremites2.csv')
    except:
        print('Connection to neo failed, will retry in 5 sec')
        time.sleep(5)
        populate_neoV2(url=url, username=username, password=password)


def insertPoints(graph, data):
    try:
        filename = data

        if filename == 'dataV3_short.csv':
            rowNumb = " / 300"
        else:
            rowNumb = " / 17815"

        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile)

            for row in datareader:
                graph.run(
                    f"CREATE (p:PointCycle) SET p.location = Point({{latitude: {row[4]}, longitude: {row[3]}}}),  p.Quartier = '{row[2]}',  p.IDPiste = '{row[1]}',  p.IdPoint = '{row[0]}'")

                print(row[0] + rowNumb)
        print('Neo4J Points inserted')
    except:
        print('Points insertion failed')


def insertBasicRelations(graph, data):
    try:
        filename = data
        rowNumb = " / 300"

        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            for row in datareader:
                coords_1 = (row[4], row[3])
                coords_2 = (row[9], row[8])
                distance = geopy.distance.geodesic(coords_1, coords_2).m
                graph.run(
                    f"MATCH (a:PointCycle),  (b:PointCycle) WHERE a.location.x ={row[3]} AND a.location.y={row[4]} AND b.location.x ={row[8]} AND b.location.y= {row[9]}  CREATE (a)-[r:est_voisin {{longueur:{distance} }}]->(b) RETURN type(r), r.longueur")

                # MATCH (a:PointCycle),  (b:PointCycle) WHERE a.location.x =-73.5456484855004 AND a.location.y=45.4714969197741 AND b.location.x =-73.5462686050043 AND b.location.y= 45.4711364611016  CREATE (a)-[r:est_voisin {longueur:5 }]->(b) RETURN type(r), r.longueur

                # MATCH (n:PointCycle)-[r:est_voisin]->() delete r

                print(row[0] + rowNumb)
        print('Neo4J relations inserted')
    except:
        print("Oops!", sys.exc_info()[1], "occurred.")
        print('Relations insertion failed (insertBasicRelations)')


def insertMultiRelations(graph, data):
    try:
        filename = data
        rowNumb = " / 50"

        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            for row in datareader:
                coords_1 = (row[1], row[2])
                coords_2 = (row[5], row[6])
                distance = geopy.distance.geodesic(coords_1, coords_2).m
                graph.run(
                    f"MATCH (a:PointCycle),  (b:PointCycle) WHERE a.location.x ={row[2]} AND a.location.y={row[1]} AND b.location.x ={row[6]} AND b.location.y= {row[5]}  CREATE (a)-[r:intersect {{longueur:{distance} }}]->(b) RETURN type(r), r.longueur")
                print(row[0] + rowNumb)
        print('Neo4J Multi relations inserted')
    except:
        print("Oops!", sys.exc_info()[1], "occurred.")
        print('Relations insertion failed (insertMultiRelations)')


populate_neo(url=INTERNAL_URL, username=USERNAME, password=PASSWORD)
# populate_neoV2(url=INTERNAL_URL, username=USERNAME, password=PASSWORD)
