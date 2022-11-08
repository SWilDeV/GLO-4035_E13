import time

from decouple import config
from py2neo import Graph, Node, Relationship


INTERNAL_URL = config("NEO4J_URL")

# We use split to split the NEO4J_AUTH formatted as "user/password"
USERNAME, PASSWORD = config("NEO4J_CREDENTIALS").split("/")

print('Waiting for servers connections')


# We wait for services Neo4J to start
def validate_neo_connection(url, username, password):
    try:
        print('Trying connection to neo')
        Graph(
            url,
            auth=(username, password),
            secure=False
        )
        
    except:
        print('Connection to neo failed, will retry in 10 sec')
        time.sleep(10)
        validate_neo_connection(url=url, username=username, password=password)


validate_neo_connection(url=INTERNAL_URL, username=USERNAME, password=PASSWORD)

graph = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD), secure=False)
transaction = graph.begin()
graph.delete_all()
graph.commit(transaction)
print('data deleted')

