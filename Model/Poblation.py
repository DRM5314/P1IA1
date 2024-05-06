class Poblation:
    gene = []
    name = ""
    aceptation = 0

    def __init__(self, name):
        self.name = name

    def setAceptation(self, aceptation):
        self.aceptation = aceptation

    def getAceptation(self):
        return self.aceptation

    def setGene(self,gene):
        self.gene = gene

    def addGene(self,newGene):
        self.gene.append(newGene)

    def getGene(self):
        return self.gene

