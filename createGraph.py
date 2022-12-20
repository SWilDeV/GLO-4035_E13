import time
from decouple import config
from py2neo import Graph
import sys


INTERNAL_URL = config("NEO4J_URL")

# We use split to split the NEO4J_AUTH formatted as "user/password"
USERNAME, PASSWORD = config("NEO4J_CREDENTIALS").split("/")

print('Waiting for servers connections')


def createProjection(url, username, password):
    try:
        graph = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD), secure=False)
        graph.run('''
            CALL gds.graph.project(
                'Graph',
                'PointCycle',
                'connecte',
                {
                    relationshipProperties: 'longueur'
                }
            )
            ''')

        print('Neo4J Graph Projection inserted')
    except:
        print('Graph Projection (createProjection)')
        time.sleep(5)
        createProjection(url=url, username=username, password=password)


createProjection(url=INTERNAL_URL, username=USERNAME, password=PASSWORD)
