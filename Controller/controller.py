import random
from time import sleep

from Model.Poblation import Poblation
class Controller:
    # Variables del sistema
    entryTrafic = 0
    crossing = []
    POBLATION = 100
    poblation = []
    minAceptation = 15

    # Variables de analisis
    nodesEntry = []
    nodesOut = []
    positionNodesentry = []

    nodesTwoWay = []
    dictTwoWay = dict()
    nodesAnalize = []
    streetsStep = dict()
    aceptationsStep = []

    # Variables de algoritmo
    actuallyPoblation = None
    selectFathers = []

    def __init__(self,configuration):
        self.POBLATION = configuration.poblation
        self.minAceptation = configuration.minimPercent
        self.configuration = configuration
    def analizeEntryNodes(self,nodes,streets):
        for node in nodes:
            stretsOuts = []
            for street in streets:
                if street.origin == node.name:
                    stretsOuts.append(street)
            node.setSteets(stretsOuts,self.configuration)
        self.crossing = nodes
        self.setInitalPoblation()
        self.analizeStreets()
        self.findInAndOutNodes()

    def setInitalPoblation(self):
        for i in range(self.POBLATION):
            genes = []
            for j in range(len(self.crossing)):
                crossing = self.crossing[j]
                percetnsCrossing = crossing.getPercentsCrossing()
                crossing.mixPercents(self.configuration)
                genes.append(percetnsCrossing)
            poblationAux = Poblation("Poblation: " + str(i))
            poblationAux.setGene(genes)
            self.poblation.append(poblationAux)
    def clearAnalize(self):
        self.nodesAnalize.clear()
        self.streetsStep.clear()
        self.aceptationsStep.clear()

    def analize(self,iteration,canvas):
        for i in range(len(self.poblation)):
            self.actuallyPoblation = self.poblation[i]
            aceptation = self.findAceptationPoblation(self.actuallyPoblation)
            self.actuallyPoblation.setAceptation(aceptation)
            if iteration%self.configuration.refreshCanva == 0:
                self.viewSolutionController(canvas)
            if aceptation == 1 or iteration == self.configuration.generations:
                self.viewSolutionController(canvas)
                return True
            self.clearAnalize()
        return False

    def findAceptationPoblation(self,poblationEntry):
        totalAnalize = 0
        totalAnalizeEntrys = 0
        while totalAnalize < len(self.crossing) and len(self.nodesAnalize) < len(self.crossing):
            for j in range(len(self.crossing)):
                if self.crossing[j].name not in self.nodesAnalize:
                    if totalAnalizeEntrys < len(self.nodesEntry):
                        for l in range(len(self.nodesEntry)):
                            nodeEntry = self.nodesEntry[l]
                            percents = poblationEntry.gene[self.positionNodesentry[l]]
                            if self.canBeAnalize(nodeEntry) and nodeEntry.name not in self.nodesAnalize:
                                self.analizeNode(nodeEntry, percents)
                                totalAnalize += 1
                                totalAnalizeEntrys += 1

                crossing = self.crossing[j]
                # Obtiene los porcentajes de cada calle y son seteados al modelo de cruce o nodo
                percentCrossing = poblationEntry.gene[j]
                crossing.setPercentsCrossing(percentCrossing)

                value = self.canBeAnalize(crossing)
                name = crossing.name
                if value and crossing not in self.nodesEntry and crossing.name not in self.nodesAnalize:
                    self.analizeNode(crossing, percentCrossing)
                    totalAnalize += 1
        return self.findAceptation()
    def canBeAnalize(self, node):
        out = True
        nodeName = node.name
        if len(node.crossingEntry) > 0:
            for i in range(len(node.crossingEntry)):
                crossing = node.crossingEntry[i]
                if crossing.name in self.nodesAnalize:
                    out = True
                else:
                    name = node.name + crossing.name
                    if name in self.nodesTwoWay:
                        out = True
                    else:
                        return False
        return out


    def getEntriesNode(self,crossing):
        out = 0
        nameEntry = crossing.name
        for i in range(len(self.crossing)):
            crossing1 = self.crossing[i]
            for j in range(len(crossing1.streets)):
                street = crossing1.streets[j]
                nameOutStreet = street.destination
                if nameOutStreet == crossing.name:
                    out += street.capacity
        if crossing.trafficEntry is None:
            out += crossing.trafficEntry

        return out

    def findInAndOutNodes(self):
        listReturn = []
        for i in range(len(self.crossing)):
            crossing = self.crossing[i]
            if crossing.trafficEntry is not None:
                self.nodesEntry.append(crossing)
                self.positionNodesentry.append(i)
            for j in range(len(crossing.streets)):
                street = crossing.streets[j]
                if street.destination is None:
                    self.nodesOut.append(crossing)

        return listReturn

    def findEntriesByNode(self,node):
        listRetun = []
        for i in range(len(self.crossing)):
            crossing = self.crossing[i]
            if crossing.name != node.name:
                for j in range(len(crossing.streets)):
                    street = crossing.streets[j]
                    if street.destination == node.name:
                        listRetun.append(crossing)
        node.setCrossingEntry(listRetun)
        if len(listRetun) > 0:
            self.isTwoWays(node)
        return listRetun

    def isTwoWays(self,nodeNow):
        for i in range(len(nodeNow.streets)):
            street = nodeNow.streets[i]
            for j in range(len(nodeNow.crossingEntry)):
                crossing = nodeNow.crossingEntry[j]
                if street.destination == crossing.name:
                    for k in range(len(crossing.streets)):
                        streetTwoWay = crossing.streets[k]
                        if streetTwoWay.destination == nodeNow.name:
                            self.dictTwoWay[streetTwoWay.name] = streetTwoWay.capacity
                            nodes = nodeNow.name + crossing.name
                            self.nodesTwoWay.append(nodes)

    def analizeStreets(self):
        for i in range(len(self.crossing)):
            self.findEntriesByNode(self.crossing[i])

    def analizeNode(self,node,percents):
        totalOut = 0
        totalCapacity = 0
        totalInComing = self.getIncomingTraffic(node.crossingEntry, node)
        if len(percents) == 0 and node.trafficOut is not None:
            totalInComing += node.trafficOut
            totalCapacity = totalInComing

        for i in range(len(percents)):
            percent = percents[i]/100
            streetOut = node.streets[i]
            totalOut += self.getOutgoingTraffic(streetOut,percent,totalInComing)
            totalCapacity += streetOut.capacity
        if totalInComing >= totalCapacity:
            totalInComing = totalCapacity

        result = totalOut/totalInComing
        self.aceptationsStep.append(totalOut/totalInComing)
        self.nodesAnalize.append(node.name)

    def getIncomingTraffic(self,nodesEntry, node):
        trafficResult = 0
        if node.trafficEntry is not None:
            trafficResult += node.trafficEntry

        for i in range(len(nodesEntry)):
            nodeEntry = nodesEntry[i]
            for j in range(len(nodeEntry.streets)):
                street = nodeEntry.streets[j]
                if street.destination == node.name:
                    trafficResult += self.twoWayCriterion(street)
                    continue
        return trafficResult

    def getOutgoingTraffic(self,street,percent,totalInComing):
        needsOut = totalInComing * percent
        if needsOut > street.capacity:
            needsOut = street.capacity
        if street.name not in self.streetsStep:
            self.streetsStep[street.name] = needsOut
        return needsOut


    def twoWayCriterion(self,street):
        capacity = street.capacity
        if street.name in self.dictTwoWay and street.name not in self.streetsStep:
            if street.name not in self.streetsStep:
                capacity = capacity * (self.minAceptation/100)
                self.streetsStep[street.name] = capacity
        else:
            if street.name in self.streetsStep:
                return self.streetsStep[street.name]

        return capacity

    def findAceptation(self):
        expected = len(self.crossing)
        result = 0
        for i in range(len(self.aceptationsStep)):
            result += self.aceptationsStep[i]
        return result/expected

    def findCicles(self,nodesEntry,find):
        if len(nodesEntry) > 0:
            for i in range(len(nodesEntry)):
                node = nodesEntry[i]
                if node.name == find.name:
                    return node
        else:
            return None

    def getSumAceptation(self):
        sumatory = 0
        for i in range(len(self.poblation)):
            value = self.poblation[i].getAceptation()
            sumatory += value
        return sumatory

    def selectFathersFun(self):
        numberFatherSelectd = 0
        sumatory = 0
        while numberFatherSelectd <= self.POBLATION:
            aceptationSum = self.getSumAceptation()
            numberAleatory = random.randint(0,int(aceptationSum))
            for poblation in self.poblation:
                sumatory += poblation.getAceptation()
                if sumatory >= numberAleatory:
                    self.selectFathers.append(poblation)
                    numberFatherSelectd += 1
                    sumatory = 0
                    break

    def mix(self,iteraction):
        self.selectFathers.sort(key=self.byAceptation, reverse=True)
        newGeneration = []
        i = 0
        while i < self.POBLATION:
            patern1 = self.selectFathers[i]
            patern2 = self.selectFathers[i+1]
            child1 = []
            child2 = []
            randGenPos = random.randint(0,len(self.crossing))
            # Cruce
            child1.extend(patern1.gene[:randGenPos])
            child1.extend(patern2.gene[randGenPos:])

            child2.extend(patern2.gene[:randGenPos])
            child2.extend(patern1.gene[randGenPos:])


            newChild1 = Poblation(str(iteraction))
            newChild1.setGene(child1)
            newChild2 = Poblation(str(iteraction + 1))
            newChild2.setGene(child2)

            newGeneration.append(newChild1)
            newGeneration.append(newChild2)
            i = i + 2

        if iteraction>0 and iteraction%self.configuration.mutationsXgeneratios == 0:
            count = 0
            while count < self.configuration.numberMutations:
                randMutationIndividue = random.randint(0, len(newGeneration) - 1)
                randMutationGene = random.randint(0, len(newGeneration[randMutationIndividue].gene) - 1)
                generation = newGeneration[randMutationIndividue]
                if len(generation.gene[randMutationGene]) > 1:
                    mutation = self.mutation(generation.gene[randMutationGene])
                    generation.gene[randMutationGene] = mutation
                    count += 1
        self.poblation = newGeneration

    def isTheBest(self,iteration):
        for poblation in self.poblation:
            if poblation.getAceptation() == 1:
                print(f"This is the best solution!! Aceptation:{poblation.getAceptation()}, in iteration:{iteration}")
                for i in range(len(poblation.gene)):
                    percetns = poblation.gene[i]
                    crossing = self.crossing[i]
                    print(crossing.viewSolution(percetns))
                return True
        return True

    def byAceptation(self,poblation):
        return poblation.getAceptation()

    def bestPoblation(self):
        poblationAnalize = self.poblation
        poblationAnalize.sort(key=self.byAceptation,reverse=True)
        if len(poblationAnalize) > 0:
            poblation = poblationAnalize[0]
            return f"Best solution is: {poblation.getAceptation()} "

    def mutation(self,gene):
        gene = self.randomOneGene(len(gene))
        return gene

    def randomOneGene(self,size):
        total = 100
        min = self.configuration.minimPercent
        cum = 0
        i = 0
        returns = []
        while (i + 1) < size and size > 1:
            rand = random.randint(min, total)
            if 100 - (cum + rand) >= min * (size - (i + 1)):
                returns.append(rand)
                total = total - rand
                cum += rand
                i += 1
        returns.append(100 - cum)
        return returns

    def cleanVars(self):
        self.entryTrafic = 0
        for cross in self.crossing:
            cross.streets.clear()
            cross.crossingEntry.clear()
        self.poblation.clear()
        self.nodesEntry.clear()
        self.nodesOut.clear()
        self.positionNodesentry.clear()

        self.nodesTwoWay.clear()
        self.dictTwoWay.clear()
        self.nodesAnalize.clear()
        self.streetsStep.clear()
        self.aceptationsStep.clear()

        # Variables de algoritmo
        actuallyPoblation = None
        self.selectFathers.clear()

    def viewSolutionController(self,canvas):
        percents = self.aceptationsStep
        for i in range(len(self.crossing)):
            canvas.update()
            node = self.crossing[i]
            percent = percents[i]
            nodeInfo = node.nodeInfo
            canvas.itemconfig(nodeInfo.positionUtilization,text=f"{percent*100:.1f}%")
            for streets in node.streets:
                streetInfo = streets.streetInfo
                nameStreet = streets.name
                capacity = streets.capacity
                used = self.streetsStep[nameStreet]
                if streets.destination is not None:
                    canvas.itemconfig(streetInfo.positionPercent, text=f"{streets.percent}%")
                    canvas.itemconfig(streetInfo.positionTextCapacity, text=f"{capacity} : {used}")
                else:
                    capacityOut = node.trafficOut
                    canvas.itemconfig(node.nodeInfo.outNode.text,text=f"{int(used)} : {capacityOut}")

