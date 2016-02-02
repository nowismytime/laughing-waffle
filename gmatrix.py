#!/usr/bin/python
import nltk
from clusterize import AgCluster
from dsets import DisjointSets
# floyd warshall algorithm
def flwa(gmatrix):
    N = len(gmatrix[0])
    dmatrix = []
    for a in range(N):
        temp = []
        for b in range(N):
            temp.extend([0])
        dmatrix.append(temp)

    for a in range(N):
        for b in range(N):
            if (a!=b) & (gmatrix[a][b]==0):
                dmatrix[a][b]=9999
            else:
                dmatrix[a][b]=gmatrix[a][b]

    for k in range(N):
        for i in range(N):
            for j in range(N):
                if dmatrix[i][k]+dmatrix[k][j] < dmatrix[i][j]:
                    dmatrix[i][j] = dmatrix[i][k]+dmatrix[k][j]

    return dmatrix

hm1 = {}
hm2 = {}
finalwords = []
finalwords1 = []

# getting stopwords
with open("D:\\User Libraries\\Documents\\NLP\\stopwords.txt") as f:
    stopwords = [line.rstrip('\n') for line in open("D:\\User Libraries\\Documents\\NLP\\stopwords.txt")]
# print(stopwords)

# getting input file
with open("D:\\User Libraries\\Documents\\NLP\\ii.txt") as f:
    for line in f:
        words = nltk.word_tokenize(line)
        finalwords.extend(nltk.pos_tag(words))
# print(finalwords)
# print (len(finalwords))

# removing stopwords
for index in range(len(finalwords)):
    words = finalwords[index]
    temp = words[0].lower()
    if temp not in stopwords:
        if (temp != ".") & (temp != ",") & (temp != "–") & (temp != ":"):
            finalwords1.append(words)
# print (finalwords1)
# print (len(finalwords1))

# getting hashmaps
i = 0
for index in range(len(finalwords1)):
    words = finalwords1[index]
    temp = words[0].lower()
    if temp not in hm1.keys():
        hm1[temp] = i
        hm2[i] = temp
        i += 1

# generating adjacency matrix
gmatrix = []
for a in range(len(hm1)):
    temp = []
    for b in range(len(hm1)):
        temp.extend([0])
    gmatrix.append(temp)
for a in range(len(finalwords1)):
    for b in range(a-5,a+5):
        if(b >= 0) & (b < len(finalwords1)) & (b != a):
            a1 = finalwords1[a][1]
            a2 = finalwords1[b][1]
            if a1 == a2:
                row = hm1[finalwords1[a][0].lower()]
                col = hm1[finalwords1[b][0].lower()]
                gmatrix[row][col]=1
#print(gmatrix)

# getting geodesic matrix
dmatrix = flwa(gmatrix)
#print(dmatrix)

dset = AgCluster.agcluster(AgCluster.mro(),dmatrix,hm2)
print(dset)



