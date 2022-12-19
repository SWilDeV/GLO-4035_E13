# Database
from dotenv import dotenv_values
from py2neo import Graph
import sys
import random

config = dotenv_values(".env")
INTERNAL_URL = config.get("NEO4J_URL")
USERNAME, PASSWORD = config.get("NEO4J_CREDENTIALS").split("/")


class NeoDatabase:

    def extracted_data_Neo(self):
        GRAPH = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD))
        TRANSACTION = GRAPH.begin()
        try:
            rep = int(
                (f'{(TRANSACTION.run("MATCH p=()-[r:connecte]->() RETURN count(p) as total").data()[0]["total"])}'))

        except:
            print("prb Neo extracted data")
            return "prb Neo extracted data"

        else:
            return rep

    def transformed_data_Neo(self):
        GRAPH = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD))
        TRANSACTION = GRAPH.begin()
        try:
            rep = (
                f'{(TRANSACTION.run("MATCH (:PointCycle)-[r:connecte]->(:PointCycle) return  sum(r.longueur) as total").data()[0]["total"])}')

        except:
            print("prb Neo transformed data")
            return "prb Neo transformed data"

        else:
            return rep

    def parcours_point(self, point_dep, distance, type):
        graph = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD))
        try:
            if (type != ''):
                TRANSACTION = graph.begin()
                rep = ((TRANSACTION.run(
                    (f"MATCH (source:PointCycle) WHERE source.id_pointCycle = '{point_dep}' CALL gds.allShortestPaths.dijkstra.stream('Graph', {{ sourceNode: source,relationshipWeightProperty: 'longueur', nodeLabels: ['PointCycle']}}) YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path WHERE gds.util.asNode(targetNode).{type} > 1 AND totalCost > {distance*0.9} AND totalCost < {distance *1.1} AND gds.util.asNode(targetNode) <> gds.util.asNode(sourceNode)RETURN DISTINCT totalCost, gds.util.asNode(sourceNode).id_pointCycle AS sourceNodeId, gds.util.asNode(targetNode).id_pointCycle AS targetNodeId,[nodeId IN nodeIds |    [gds.util.asNode(nodeId).id_pointCycle,gds.util.asNode(nodeId).y,gds.util.asNode(nodeId).x]] AS nodesCoord SKIP 1 LIMIT 10")))).data()
            else:
                TRANSACTION = graph.begin()
                rep = ((TRANSACTION.run(
                    (f"MATCH (source:PointCycle) WHERE source.id_pointCycle = '{point_dep}' CALL gds.allShortestPaths.dijkstra.stream('Graph', {{ sourceNode: source,relationshipWeightProperty: 'longueur', nodeLabels: ['PointCycle']}}) YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path WHERE  totalCost > {distance*0.9} AND totalCost < {distance *1.1} AND gds.util.asNode(targetNode) <> gds.util.asNode(sourceNode)RETURN DISTINCT totalCost, gds.util.asNode(sourceNode).id_pointCycle AS sourceNodeId, gds.util.asNode(targetNode).id_pointCycle AS targetNodeId,[nodeId IN nodeIds |    [gds.util.asNode(nodeId).id_pointCycle,gds.util.asNode(nodeId).y,gds.util.asNode(nodeId).x]] AS nodesCoord SKIP 1 LIMIT 10")))).data()

            randomNum = random.randint(0, len((rep))-1)
            return rep[randomNum]

        except:
            print("failed request path from parcours_point")
            return "failed request path from parcours_point "

    def adjacent(self, id):
        listAdj = []
        GRAPH = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD))
        TRANSACTION = GRAPH.begin()
        try:
            request = 'MATCH (a:PointCycle {id_pointCycle:"' + id + \
                '"})-[connecte]->(b:PointCycle) RETURN b.id_pointCycle'
            rep = ((TRANSACTION.run(request).data()))
        except:
            print("failed request path from node")
            return "failed request path from node : " + request
        else:
            for x in rep:
                listAdj.append(x["b.id_pointCycle"])
            return listAdj

    def paths(self, id, nNodes):
        listPaths = [[id]]
        i = nNodes
        while i > 1:
            newListPath = []
            for path in listPaths:
                currentNode = path[len(path) - 1]
                adjNodes = self.adjacent(currentNode)
                for newNode in adjNodes:
                    newListPath = newListPath + [path + [newNode]]
            i = i - 1
            listPaths = newListPath
        return listPaths

    def getPathFromLength(self, length, types):
        GRAPH = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD))
        TRANSACTION = GRAPH.begin()
        min = length - 0.1 * length
        max = length + 0.1 * length
        try:
            if not types:
                request = 'MATCH (a:PointCycle)-[c:connecte]->(b:PointCycle) WHERE c.longueur > ' + str(
                    min) + ' AND c.longueur < ' + str(max) + ' RETURN a LIMIT 1'
                rep = TRANSACTION.run(request).data()
            else:
                for type in types:
                    request = 'MATCH (a:PointCycle)-[c:connecte]->(b:PointCycle) WHERE c.longueur > ' + str(
                        min) + ' AND c.longueur < ' + str(max) + ' AND a.' + type + ' > 0 RETURN a'
                    rep = TRANSACTION.run(request).data()
                    if len(rep) > 0:
                        break
            result = {
                "startingPoint": {
                    "type": "Point",
                    "coordinates": [
                        rep[0]["a"]["x"],
                        rep[0]["a"]["y"]
                    ]
                }
            }
        except:

            print("Oops!", sys.exc_info()[1], "occurred.")
            print("failed to request path of " + str(length) + " length")
            return "failed to request path between " + str(min) + " and " + str(max) + " length"

        return result

    def random_spawn():
        GRAPH = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD))
        TRANSACTION = GRAPH.begin()
        try:
            request = 'MATCH (a:PointCycle {id_pointCycle:"' + id + \
                '"})-[connecte]->(b:PointCycle) RETURN b.id_pointCycle'
            rep = ((TRANSACTION.run(request).data()))
        except:
            print("failed request path from node")
            return "failed request path from node : " + request
        return 0
