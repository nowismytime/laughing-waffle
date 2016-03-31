#!/usr/bin/env python
import nltk
import math
import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy import linalg, mat, dot;
import os

def kmeans(data, k):

    centroids = []

    centroids = randomize_centroids(data, centroids, k)

    old_centroids = [[] for i in range(k)]

    iterations = 0
    while not (has_converged(centroids, old_centroids, iterations)):
        iterations += 1

        clusters = [[] for i in range(k)]

        # assign data points to clusters
        clusters = euclidean_dist(data, centroids, clusters)

        # recalculate centroids
        index = 0
        for cluster in clusters:
            old_centroids[index] = centroids[index]
            centroids[index] = np.mean(cluster, axis=0, dtype= 'float').tolist()
            index += 1


    print("The total number of data instances is: " + str(len(data)))
    print("The total number of iterations necessary is: " + str(iterations))
    print("The means of each cluster are: " + str(centroids))
    print("The clusters are as follows:")
    for cluster in clusters:
        print("Cluster with a size of " + str(len(cluster)) + " starts here:")
        print(np.array(cluster).tolist())
        print("Cluster ends here.")

    return centroids, clusters

# Calculates euclidean distance between
# a data point and all the available cluster
# centroids.
def euclidean_dist(data, centroids, clusters):
    for instance in data:
        # Find which centroid is the closest
        # to the given data point.

       # minima = 999999
        #iminima=-1
        #for index, center in enumerate(centroids):
         #   tdis =0
          #  for k1 in range(len(center)):
           #     tdis1 = float(instance[k1])-float(center[k1])
            #    tdis += tdis1*tdis1
            #tmin = math.sqrt(tdis)
            #if (tmin<minima):
             #   minima = tmin
              #  iminima = index
        #mu_index = iminima
        mu_index = min([(i[0], np.linalg.norm(instance-np.asarray(centroids[i[0]]))) \
                          for i in enumerate(centroids)], key=lambda t:t[1])[0]
        try:
            clusters[mu_index].append(instance)
        except KeyError:
            clusters[mu_index] = [instance]

    # If any cluster is empty then assign one point
    # from data set randomly so as to not have empty
    # clusters and 0 means.
    for cluster in clusters:
        if not cluster:
            cluster.append(data[np.random.randint(0, len(data), size=1)].flatten().tolist())

    return clusters


# randomize initial centroids
def randomize_centroids(data, centroids, k):
    for cluster in range(0, k):
        centroids.append(data[np.random.randint(0, len(data), size=1)].flatten().tolist())
    return centroids


# check if clusters have converged
def has_converged(centroids, old_centroids, iterations):
    MAX_ITERATIONS = 1000
    if iterations > MAX_ITERATIONS:
        return True
    return old_centroids == centroids

def svd(gmatrix):

    U, s, V = linalg.svd(gmatrix)
    #print(s)
    energy=0
    for index in range(len(s)):
        energy += s[index]*s[index]
    energy *= 0.5
    #print (energy)
    sum=0
    index = len(s)-1
    while sum<energy:
        sum += s[index]*s[index]
        #print (sum)
        index -= 1
    index += 1
    #print(index)
    for i in range(index,len(s)):
        s[i]=0
    #print(s)
    s11 = np.dot(U, np.dot(np.diag(s), V))
    #print(s11)
    for i in range (len(s11)):
        for j in range(len(s11)):
            s11[i][j]= '%.2f' % s11[i][j]
    #for i in range (len(s11)):
     #   print (s11[i])
    #print(len(s11))
    #plt.plot(s11)
    #plt.show()
    return s11


# main function
hm1 = {}
hm2 = {}
finalwords = []
finalwords1 = []

# getting stopwords
with open("stopwords.txt") as f:
    stopwords = [line.rstrip('\n') for line in open("stopwords.txt")]
# print(stopwords)

# getting input file
with open("ii.txt") as f:
    for line in f:
        words = nltk.word_tokenize(line)
        finalwords.extend(nltk.pos_tag(words))
# print(finalwords)
# print (len(finalwords))

# removing stopwords
for index in range(len(finalwords)):
    words = finalwords[index]
    temp = words[0].lower()
    if temp not in stopwords and (temp != ".") & (temp != ",") & (temp != "–") & (temp != ":") & (temp != "(") & (
        temp != ")"):
        finalwords1.append(words)
#print (finalwords1)
#print (len(finalwords1))

# getting hashmaps
i = 0
for index in range(len(finalwords1)):
    words = finalwords1[index]
    temp = words[0].lower()
    if temp not in hm1.keys():
        hm1[temp] = i
        hm2[i] = temp
        i += 1
#print(hm2[0])
print ("total words before reduction")
print(len(hm1))

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
            if a1.lower() == a2.lower():
                row = hm1[finalwords1[a][0].lower()]
                col = hm1[finalwords1[b][0].lower()]
                gmatrix[row][col] += 1
#print(gmatrix)


# getting geodesic matrix
#dmatrix = flwa(gmatrix)
#print(dmatrix)
rmatrix2 = []
rmatrix1 =[]
rmatrix = svd(gmatrix)
#print (rmatrix)
cols =[]

for i1 in range(len(rmatrix)):
    f1 = 0
    for j in range(len(rmatrix)):
        if (rmatrix[i1][j]!=0):
            f1=1
            break
    if (f1==1):
        rmatrix1.append(rmatrix[i1])
        cols.append(i1)

for i1 in range(len(rmatrix1)):
    temp=[]
    for j in range(len(rmatrix)):
        if (j in cols):
            temp.append(rmatrix1[i1][j])
    rmatrix2.append(temp)

#print(len(rmatrix2[0]))
rhm1={}
rhm2={}
ind1 = 0
for index in range(len(hm1)):
    if (index not in cols):
        rhm2[ind1] = hm2[index]
        rhm1[hm2[index]]=ind1
        ind1 +=1

distmat = []
for i in range(len(rmatrix2)):
    temp1 = []
    for j in range(len(rmatrix2)):
        temp1.insert(0,0)
    distmat.append(temp1)

for i in range(len(rmatrix2)):
    for j in range(i+1,len(rmatrix2)):
        dist = 0
        for k in range(len(rmatrix2)):
            psum = rmatrix2[i][k]-rmatrix2[j][k]
            dist += psum*psum
        distmat[i][j]=np.linalg.norm(np.asarray(rmatrix2[i])-np.asarray(rmatrix2[j]))

for i in range(len(rmatrix2)):
    for j in range(i):
        distmat[j][i]= '%.2f' % distmat[j][i]
        distmat[i][j] = distmat[j][i]

centroids=[]
clusters=[]
centroids, clusters = kmeans(np.asarray(distmat,float),5)
#print(distmat)


#dlist = agcluster(disets,dmatrix,hm2)
#
# fileWrite(disets,hm1,gmatrix,hm2)

#for index in range(len(dlist)):
  #  print(dlist[index])
   # print("\n")



