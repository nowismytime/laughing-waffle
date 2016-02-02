class Disjoint:

    def __init__(self):
        self.sets = []

    def createSet(self, repr):
        self.sets.append([repr])

    def mergeSets(self, repr1, repr2):
        set1 = self.findSet(repr1)
        set2 = self.findSet(repr2)
        if set1 != set2:
            set1.extend(set2);
            self.sets.remove(set2)

    def findSet(self, repr1):
        for oneSet in self.sets:
            if repr1 in oneSet:
                return oneSet


    def getSets(self):
        return self.sets