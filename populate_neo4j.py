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
        print('neo connection works')

        filename = 'data_points.csv'
        filename2 = 'data_pistes.csv'

        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile)

            for row in datareader:
                graph.run(
                    f"CREATE (p:PointCycle) SET p.x= {row[1]}, p.y={row[0]}, p.crs='wsg-84'")

        with open(filename2, 'r') as csvfile2:
            datareader2 = csv.reader(csvfile2)
            for row2 in datareader2:
                coord1New = row2[0].replace("[", "")
                coord1New = coord1New.replace("]", "")
                coord2New = row2[1].replace("[", "")
                coord2New = coord2New.replace("]", "")
                c11, c12 = coord1New.split(",")
                c21, c22 = coord2New.split(",")
                coords_1 = [float(c12), float(c11) ]
                coords_2 = [float(c22), float(c21) ]
                distance = row2[5]
                piste_id = row2[3]
                try: graph.run(f"MATCH (a:PointCycle),  (b:PointCycle) WHERE a.x ={coords_1[0]} AND a.y={coords_1[1]} AND b.x ={coords_2[0]} AND b.y={coords_2[1]}  CREATE (a)-[r:connecte]->(b) SET r.longueur={distance}, r.piste_id={piste_id}")
                except: print("pas de relation!!!! ",coords_1,coords_2)

        print('Neo4J Data inserted')

    except:
        print('Connection to neo failed, will retry in 5 sec')
        time.sleep(5)
        populate_neo(url=url, username=username, password=password)

populate_neo(url=INTERNAL_URL, username=USERNAME, password=PASSWORD)
# populate_neoV2(url=INTERNAL_URL, username=USERNAME, password=PASSWORD)


