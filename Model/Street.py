from Canvas.StreetInfo import StreetInfo
class Street:
    name = ""
    capacity = 0
    usedCapacity = 0
    percent = 0
    destination = ""
    origin = ""
    streetInfo = None
    orientation = ""

    def __init__(self, name, capacity, origin, destination,orientation):
        self.name = name
        self.capacity = int(capacity)
        self.destination = destination
        self.origin = origin
        self.orientation = orientation

    def setStreetInfo(self, streetInfo):
        self.streetInfo = streetInfo
        self.name = streetInfo.name
        self.origin = streetInfo.fromN
        self.destination = streetInfo.toN
    def showDetails(self):
        print(f' {self.name} , {self.direction} , {self.capatity} , {self.percent} ')

    def setOrigin(self,origin):
        self.origin = origin

    def getNameOrientation(self):
        newName = self.origin + self.orientation + self.destination
        self.name = newName
        return newName