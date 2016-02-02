#!/usr/bin/python


class DisjointSets:
    disjointSet = globals()

    def dsets(self):
        disjointSet = []

    def setCreate (self, element):
        hashmap={element: set(element)}
        disjointSet.extend(hashmap)

    def union (self, element1, element2):
        first_rep = self.setFind(element1)
        second_rep = self.setFind(element2)

        first_set = set()
        second_set = set()

        for index in range(len(self)):
            if first_rep in self[index]:
                first_set = self[index][first_rep]
            elif second_rep in self[index]:
                second_set = self[index][second_rep]

        if (len(first_set) != 0) & (len(second_set) != 0):
            first_set.addall(second_set)

        for index in range(len(self)):
            if first_rep in self[index]:
                self[index][first_rep] = first_set
            elif second_rep in self[index]:
                self[index].remove(second_rep)
                self.remove(self[index])

    def setFind (self, element):
        for index in range(len(self)):
            keys = self[index].keys()
            for i in range(len(keys)):
                if element in keys[i]:
                    return keys[i]

    def setSize(self):
        return len(self)


