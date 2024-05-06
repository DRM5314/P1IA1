import random
from Canvas.NodeInfo import NodeInfo
class crossing:
    streets = []
    crossingEntry = []
    name = ""
    trafficEntry = None
    trafficOut = None

    nodeInfo = None

    def __init__(self, name):
        self.name = name

    def setNodeInfo(self, nodeInfo):
        self.nodeInfo = nodeInfo
    def setSteets(self,streets,configuration):
        if len(streets) > 0:
            self.streets = list(streets)
            self.setPercent(configuration)
            self.setOrigins()

    def setTrafficEntry(self, trafficEntry):
        self.trafficEntry = int(trafficEntry)
    def setTrafficOut(self, trafficOut):
        self.trafficOut = int(trafficOut)
    def setPercent(self,configuration):
        total = 100
        min = configuration.minimPercent
        cum = 0
        i = 0
        size = len(self.streets)
        while (i + 1) < size and size > 1 and i < 4000:
            rand = random.randint(min, total)
            if 100 - (cum + rand) >= min * (size - (i + 1)):
                self.streets[i].percent = rand
                total = total - rand
                cum += rand
                i += 1
        if len(self.streets) > 0:
            self.streets[size-1].percent = 100 - cum

    def showPercent(self):
        print("In node: "+self.name)
        count = 0
        for i in range(len(self.streets)):
            self.streets[i].showDetails()
            count += self.streets[i].percent
        print("Total "+str(count))
        print("\n")

    def setOrigins(self):
        for i in range(len(self.streets)):
            self.streets[i].setOrigin(self.name)

    def getPercentsCrossing(self):
        returns = []
        for i in range(len(self.streets)):
            returns.append(self.streets[i].percent)
        return returns

    def setPercentsCrossing(self, percents):
        for i in range(len(self.streets)):
            street = self.streets[i]
            street.percent = percents[i]

    def mixPercents(self,configuration):
        self.setPercent(configuration)
        return self.getPercents()

    def setCrossingEntry(self,crossingEntry):
        self.crossingEntry = crossingEntry

    def getPercents(self):
        listPercents = []
        for i in range(len(self.streets)):
            street = self.streets[i]
            listPercents.append(street.percent)
        return listPercents

    def viewSolution(self,percents):
        self.setPercentsCrossing(percents)
        returns = ""
        for street in self.streets:
            returns += f"For street: {street.name}, best percent is: {street.percent}\n"
        return returns

