from dsets import DisjointSets

# testing push operation
class AgCluster :
    def agcluster (self, geomatrix, words):
        disjointSet = DisjointSets.disjointSet
        for i in range(len(words)):
            DisjointSets.setCreate(DisjointSets.mro(), words[i])
        while len(disjointSet)>20:
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
            first = words[imin]
            second = words[jmin]
            print(imin, jmin)
            geomatrix[imin][jmin] = 9999

            if not DisjointSets.setFind(DisjointSets.mro(),first) != DisjointSets.setFind(DisjointSets.mro(), second):
                DisjointSets.union(DisjointSets.mro(), first, second)

            for i in range(len(disjointSet)):
                keys = disjointSet[i].keys()
                for j in range(keys):
                    temp = disjointSet[i][keys[j]]
                    for k in range(len(temp)):
                        print (temp[k])
                        print (" ")
                    print ("\n")

        return disjointSet


