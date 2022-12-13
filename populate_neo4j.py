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
        print("test")
        print('neo connection works')

        # check if Neo4J volume is empty
        relationsArePresent = False
        if (DBHasData(graph) == True):
            relationsArePresent = True
            print("Neo4J already has data")

        if (relationsArePresent != True):
            insertPoints(graph, 'data_points.csv')  # Insert Points
            insertRelations(graph, 'data_pistes.csv')  # Insert Relations

    except:
        print('Connection to neo failed, will retry in 5 sec')
        time.sleep(5)
        populate_neo(url=url, username=username, password=password)


def DBHasData(graph):
    try:
        result = graph.run(
            f"RETURN exists( (:PointCycle)-[:connecte]-(:PointCycle) )").data()

        request = 'exists( (:PointCycle)-[:connecte]-(:PointCycle) )'

        return result[0][request]
    except:
        print('relationExist failed')
        print("Oops!", sys.exc_info()[1], "occurred.")


def insertPoints(graph, data):
    try:
        filename = data

        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            counter = 0

            for row in datareader:
                p_New = row[0].replace("[", "")
                p_New = p_New.replace("]", "")
                p_y, p_x = p_New.split(",")
                p = [float(p_x), float(p_y) ]
                arrond = code_arrondissement(row[1])
                graph.run(
                    f"CREATE (p:PointCycle) SET p.x= {p[0]}, p.y={p[1]}, p.crs='wsg-84', p.arrond= {arrond}, p.id_pointCycle={counter}")
                counter += 1
                print(counter)

        print('Neo4J Points inserted')

    except:
        print('Points insertion failed')
        print("Oops!", sys.exc_info()[1], "occurred.")


def insertRelations(graph, data):
    try:
        filename = data

        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            counter = 0

            for row2 in datareader:
                coord1New = row2[0].replace("[", "")
                coord1New = coord1New.replace("]", "")
                coord2New = row2[1].replace("[", "")
                coord2New = coord2New.replace("]", "")
                c11, c12 = coord1New.split(",")
                c21, c22 = coord2New.split(",")
                coords_1 = [float(c12), float(c11)]
                coords_2 = [float(c22), float(c21)]
                distance = row2[5]
                piste_id = row2[3]

                try:
                    graph.run(f"MATCH (a:PointCycle),  (b:PointCycle) WHERE a.x ={coords_1[0]} AND a.y={coords_1[1]} AND b.x ={coords_2[0]} AND b.y={coords_2[1]}  CREATE (a)-[r:connecte]->(b) SET r.longueur={distance}, r.id_piste={piste_id}")
                    counter += 1
                    print(counter)

                except:
                    print("pas de relation!!!! ", coords_1, coords_2)
                    print("Oops!", sys.exc_info()[1], "occurred.")

        print('Neo4J relations inserted')

    except:
        print("Oops!", sys.exc_info()[1], "occurred.")
        print('Relations insertion failed (insertBasicRelations)')

def code_arrondissement(text):
        if text == 'Le Plateau-Mont-Royal': return 0
        elif text == 'Mercier-Hochelaga-Maisonneuve': return 1
        elif text == 'Rosemont-La Petite-Patrie': return 2
        elif text == 'Villeray-Saint-Michel-Parc-Extension': return 3
        elif text == 'Ville-Marie': return 4
        else: raise print('arrondissement non code :', text)


populate_neo(url=INTERNAL_URL, username=USERNAME, password=PASSWORD)