#!/usr/bin/env python
import nltk
import math
import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy import linalg, mat, dot;

def svd(gmatrix):

    U, s, V = linalg.svd(gmatrix)
    #print(s)
    energy=0
    for index in range(len(s)):
        energy += s[index]*s[index]
    energy *= 0.8
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


# floyd warshall algorithm
def flwa(gmatrix):
    N = len(gmatrix[0])
    dmatrix1 = []
    for a in range(N):
        temp = []
        for b in range(N):
            temp.extend([0])
        dmatrix1.append(temp)

    for a in range(N):
        for b in range(N):
            if (a!=b) & (gmatrix[a][b]==0):
                dmatrix1[a][b]=9999
            else:
                dmatrix1[a][b]=gmatrix[a][b]

    for k in range(N):
        for i in range(N):
            for j in range(N):
                if dmatrix1[i][k]+dmatrix1[k][j] < dmatrix1[i][j]:
                    dmatrix1[i][j] = dmatrix1[i][k]+dmatrix1[k][j]
    max1 =0

    for c in range(N):
        for d in range(N):
            if (dmatrix1[c][d]>max1) & (dmatrix1[c][d]<9999):
                max1 = dmatrix1[c][d];
    max1 *= 2
    for a in range(N):
        for b in range(N):
            if (a!=b) & (dmatrix1[a][b]==9999):
                dmatrix1[a][b]=max1

    return dmatrix1

# disjoint sets functions

# create sets for each element
def setCreate (disets, element):
    nset = set()
    nset.add(element)
    hashmap={element: nset}
    disets.append(hashmap)

# union two sets containing elements 1 and 2
def union (disets, element1, element2):
    first_rep = setFind(disets, element1)
    second_rep = setFind(disets, element2)

    first_set = set()
    second_set = set()

    for index in range(len(disets)):
        if first_rep in disets[index]:
            first_set = disets[index][first_rep]
        elif second_rep in disets[index]:
            second_set = disets[index][second_rep]

    if (len(first_set) != 0) & (len(second_set) != 0):
        first_set=first_set.union(second_set)

    for index in range(len(disets)):
        if first_rep in disets[index]:
            disets[index][first_rep] = first_set

    for index in range(len(disets)):
        if second_rep in disets[index]:
            del disets[index][second_rep]
            disets.remove(disets[index])
            break

# find the representative for the set containing the element
def setFind (disets, element):
    for index in range(len(disets)):
        keys = disets[index].keys()
        for key in keys:
            if element in disets[index][key]:
                return key

# clustering function
def agcluster (disets, geomatrix, words):
    for i in range(len(words)):
        setCreate(disets, words[i])
    while len(disets)>10:
        N = len(geomatrix[0])
        imin = -1
        jmin = -1
        min = 9999
        for i in range(N):
            for j in range(N):
                if (geomatrix[i][j] != 0) & (geomatrix[i][j]<min):
                    imin = i
                    jmin = j
                    min = geomatrix[i][j]
        if (imin==-1):
            break
        first = words[imin]
        second = words[jmin]
        geomatrix[imin][jmin] = 9999

        if setFind(disets, first) != setFind(disets, second):
            union(disets, first, second)

        #for i in range(len(disets)):
         #   keys = disets[i].keys()
          #  for key in keys:
           #     temp = disets[i][key]
            #    for t1 in temp:
             #       print (t1)
              #      print (" ")
               # print ("\n")

    return disets

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
with open("text8.txt") as f:
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

print ("Words removed and no. of 1s in their row")
rmatrix = svd(gmatrix)
count1=0
for i1 in range(len(rmatrix)):
    f1 = 0
    for j in range(len(rmatrix)):
        if (rmatrix[i1][j]!=0):
            f1=1
            break
    if (f1==0):
        sum11=0
    else:
        sum11=0
        for j in range(len(gmatrix)):
            sum11 += gmatrix[i1][j]
        print (hm2[i1])
        print(sum11)
        count1 += 1

disets = []
print(count1)
#dlist = agcluster(disets,dmatrix,hm2)
#
# fileWrite(disets,hm1,gmatrix,hm2)

#for index in range(len(dlist)):
  #  print(dlist[index])
   # print("\n")



