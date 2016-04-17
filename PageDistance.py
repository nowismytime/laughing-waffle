from py2neo import authenticate, Graph
from py2neo import neo4j, node, rel
from py2neo.neo4j import Index

authenticate("localhost:7474", "neo4j", "10p13dd0053")
graph = Graph()
snode = raw_input("Enter origin page")
enode = raw_input("Enter destination page")

node1 = graph.legacy.get_indexed_node("Pages" ,"name" , snode)
node2 = graph.legacy.get_indexed_node("Pages" ,"name" , enode)
print(node1)
print(node2)

query_string = "START beginning=node(%d), end=node(%d) MATCH p = shortestPath(beginning-[*..500]-end) RETURN p" % (node1._id, node2._id)
result = graph.cypher.execute(query_string)
print(result)

st1 = str(result)
count=0
for i in range(len(st1)):
    if st1[i]=='<':
        count += 1
    elif st1[i] =='>':
        count += 3
print(count)

