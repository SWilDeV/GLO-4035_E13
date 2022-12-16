import time
import csv
from decouple import config
from py2neo import Graph
import geopy.distance
import sys

INTERNAL_URL = config("NEO4J_URL")
USERNAME, PASSWORD = config("NEO4J_CREDENTIALS").split("/")
graph = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD), secure=False)

# 5 km
# point de depart: 

# test du fonctionnement de graph.ru
aa = graph.run("MATCH (p:PointCycle)<-[c:connecte {id_piste:4961}]-(p2:PointCycle) return c").data()
aa[0]

dt = 'p1'
graph.run(f"MATCH (p:PointCycle)  WHERE p.id_pointCycle = '{dt}' return p").data()
aa[0]

bb = graph.run("MATCH (p:PointCycle) return p.arrond, p.id_pointCycle LIMIT 4").data()
bb

# pour utiliser le graph dans gds
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



point_dep = 'p1'

### ce code fonctionne! mais nous devons etre capables d'introduire des parametres
graph.run('''
MATCH (source:PointCycle)
WHERE source.id_pointCycle = 'p1'
CALL gds.allShortestPaths.dijkstra.stream('Graph', {
    sourceNode: source,
    relationshipWeightProperty: 'longueur'
})
YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
RETURN
    index,
    gds.util.asNode(sourceNode).id_pointCycle AS sourceNodeId,
    gds.util.asNode(targetNode).id_pointCycle AS targetNodeId,
    totalCost,
    [nodeId IN nodeIds | gds.util.asNode(nodeId).id_pointCycle] AS nodeNames,
    costs,
    nodes(path) as path
ORDER BY index
LIMIT 5
''').to_data_frame()

## essai avec le .format

graph.run('''
MATCH (source:PointCycle)
WHERE source.id_pointCycle='{}'
CALL gds.allShortestPaths.dijkstra.stream('Graph', {
    sourceNode: source,
    relationshipWeightProperty: 'longueur'
})
YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
RETURN
    index,
    gds.util.asNode(sourceNode).id_pointCycle AS sourceNodeId,
    gds.util.asNode(targetNode).id_pointCycle AS targetNodeId,
    totalCost,
    [nodeId IN nodeIds | gds.util.asNode(nodeId).id_pointCycle] AS nodeNames,
    costs,
    nodes(path) as path
ORDER BY index
LIMIT 5
'''.format(point_dep))



graph.run('''
MATCH (start:PointCycle) 
WHERE source.id_pointCycle = 'p_1'
CALL gds.alpha.shortestPaths.stream(‘monuments’,
 {startNode:start, relationshipWeightProperty:’distance’})
YIELD nodeId, distance
WHERE gds.util.isFinite(distance) = True
RETURN gds.util.asNode(nodeId).name as monument,distance
ORDER BY distance ASC
''')



graph.run('''
MATCH (source:PointCycle {id_pointCycle: 'p1'}), (target:pointCycle {id_pointCycle: 'p97'})
CALL gds.shortestPath.dijkstra.stream('Graph', {
    sourceNode: source,
    targetNode: target,
    relationshipWeightProperty: 'longueur'
})
YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
RETURN
    index,
    gds.util.asNode(sourceNode).name AS sourceNodeName,
    gds.util.asNode(targetNode).name AS targetNodeName,
    totalCost,
    [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS nodeNames,
    costs,
    nodes(path) as path
ORDER BY index
''')


df = graph.run('''
MATCH (source:PointCycle {id_pointCycle: 'p1'}), (target:PointCycle {id_pointCycle: 'p97'})
CALL gds.shortestPath.dijkstra.stream('Graph', {
    sourceNode: source,
    targetNode: target,
    relationshipWeightProperty: 'longueur'
})
YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
RETURN
    index,
    gds.util.asNode(sourceNode).name AS sourceNodeName,
    gds.util.asNode(targetNode).name AS targetNodeName,
    totalCost,
    [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS nodeNames,
    costs,
    nodes(path) as path
ORDER BY index
''').to_data_frame()

df