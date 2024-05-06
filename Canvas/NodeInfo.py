class NodeInfo:
    entryNode = None
    outNode = None

    def __init__(self, name, positionCanvas, positionTextCanvas, positionUtilization):
        self.name = name
        self.positionCanvas = positionCanvas
        self.positionText = positionTextCanvas
        self.positionUtilization = positionUtilization
        # self.positionsNodeEntry = []
        # self.positionsNodeExit = []

    def setEntryNode(self, entry):
        self.entryNode = entry

    def setOutNode(self, entry):
        self.outNode = entry