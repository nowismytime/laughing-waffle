from py2neo import authenticate, Graph, neo4j


authenticate("localhost:7474", "neo4j", "10p13dd0053")
graph_db = Graph()
snode = raw_input("Enter origin page")
enode = raw_input("Enter destination page")

node1 = graph_db.legacy.get_indexed_node("Pages" ,"name" , snode.lower())
node2 = graph_db.legacy.get_indexed_node("Pages" ,"name" , enode.lower())
print(node1)
print(node2)

query_string = "START beginning=node(%d), end=node(%d) MATCH p = shortestPath((beginning)-[*..500]-(end)) RETURN p" % (node1._id, node2._id)
result = graph_db.cypher.execute(query_string)
print(result)

st1 = str(result)
count=0
for i in range(len(st1)):
    if st1[i]=='<':
        count += 1
    elif st1[i] =='>':
        count += 3
print(count)

