from py2neo import authenticate, Graph, neo4j

authenticate("localhost:7474", "neo4j", "10p13dd0053")
graph_db = Graph()
snode = raw_input("Enter origin page")
enode = raw_input("Enter destination page")
"""
node1 = graph_db.legacy.get_indexed_node("Pages" ,"name" , snode.lower())
node2 = graph_db.legacy.get_indexed_node("Pages" ,"name" , enode.lower())
print(node1)
print(node2)

query_string = "START beginning=node(%d), end=node(%d) MATCH p = allShortestPaths((beginning)-[*..500]-(end)) RETURN p" % (node1._id, node2._id)
result = graph_db.cypher.execute(query_string)

st1 = str(result[0].p)
print(st1)
count=0
for i in range(len(st1)):
    if st1[i]=='<':
        count += 1
    elif st1[i] =='>':
        count += 3
print(count)

# meta path
metapath =""
i=0
while i<len(st1) and st1[i]!='<':
    i+=1
relations =[]

prev = '<'
prev_i = i
i+=2
while i<len(st1):
    if st1[i] == '<' or st1[i] == '>':
        if (st1[i] == '<' and prev == '>') or (st1[i] == '>' and prev == '<'):
            for j in range(prev_i,i):
                k1 = j+4
                temp11 = st1[j:k1]
                if temp11 == "name":
                    t5 = j+6
                    while t5<i and st1[t5]!= '"':
                        t5 += 1
                    t1 = st1[j+6:t5].lower()
                    if len(relations)>0 and relations[len(relations)-1]!=t1:
                        relations.append(st1[j+6:t5].lower())
                    elif len(relations)==0:
                        relations.append(st1[j+6:t5].lower())
        prev = st1[i]
        prev_i = i
    i +=1

for i in range(len(relations)):
    metapath += relations[i]
    metapath += "-"
metapath = metapath[:-1]
print(metapath)
"""
q1 = "MATCH (n) WHERE n.name = 'petyr baelish' RETURN n"
n1 = graph_db.cypher.execute(q1)
print n1

q2 = "MATCH (n) WHERE n.name = 'robert baratheon' RETURN n"
n2 = graph_db.cypher.execute(q2)
print n2

q3 = "MATCH (a),(b) WHERE a.name = 'petyr baelish' AND b.name = 'robert baratheon' CREATE (a)-[r:RELTYPE{ name : a.name + '<->' + b.name }]->(b) RETURN r"
n3 = graph_db.cypher.execute(q3)
print n3