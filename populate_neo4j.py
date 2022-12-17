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
        # relationsArePresent = False
        # if (DBHasData(graph) == True):
        #     relationsArePresent = True
        #     print("Neo4J already has data")

        # if (relationsArePresent != True):
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
                graph.run(
                    f"CREATE (p:PointCycle) SET p.x= {row[0]}, p.y={row[1]}, p.crs='wsg-84', p.arrond= '{row[2]}', p.id_pointCycle='{row[3]}'")
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
                try:
                    graph.run(
                        f"MATCH (a:PointCycle),  (b:PointCycle) WHERE a.x ={row2[0]} AND a.y={row2[1]} AND b.x ={row2[2]} AND b.y={row2[3]}  CREATE (a)-[r:connecte]->(b) SET r.longueur={row2[7]}, r.id_piste={row2[5]}")
                    graph.run(
                        f"MATCH (a:PointCycle),  (b:PointCycle) WHERE a.x ={row2[0]} AND a.y={row2[1]} AND b.x ={row2[2]} AND b.y={row2[3]}  CREATE (b)-[r:connecte]->(a) SET r.longueur={row2[7]}, r.id_piste={row2[5]}")
                    counter += 1
                    print(counter)

                except:
                    print("pas de relation!!!! ",
                          "[", row2[0], ",", row2[1], "],[", row2[0], ",", row2[1], "]")
                    counter += 1
                    print("Oops!", sys.exc_info()[1], "occurred.")

        print('Neo4J relations inserted')

    except:
        print("Oops!", sys.exc_info()[1], "occurred.")
        print('Relations insertion failed (insertBasicRelations)')


# populate_neo(url=INTERNAL_URL, username=USERNAME, password=PASSWORD)
