import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk

from Model.crossing import crossing as Crossing
from Model.Street import Street

from Canvas.StreetInfo import StreetInfo
from Canvas.NodeInfo import NodeInfo
from Canvas.EntryOutInfo import EntryOutInfo
class GraphApp:
    def getNodes(self):
        return self.nodes

    def getStreets(self):
        return self.streets

    def __init__(self, master,canvas, nodes, streets,size,configuration):
        self.master = master
        self.canvas = canvas
        self.canvas = tk.Canvas(master=self.master,width=size[0],height=size[1]*0.9)
        self.canvas.pack(fill=tk.X, expand=True)
        self.G = nx.Graph()
        self.nodes = nodes
        self.streets = streets
        self.drag_data = None
        self.selected_node = None
        self.configuration = configuration
        # Agregar algunos nodos iniciales
        # self.add_node(100, 100,"A")
        # self.add_node(300, 200,"B")
        # self.add_node(200, 300,"C")
        # self.add_node(500, 500,"D")
        # # Arista
        # self.add_Edge("A","B",100)
        # self.add_Edge("A", "D",500)
        # self.add_Edge("A","C",100)
        # self.add_Edge("C","D",200)
        # self.add_Edge("B","D",80)
        # self.add_Edge("B","C",15)
        #
        #
        # # Entrada
        # self.addEntryNode("A",900)
        # self.addOutNode("D",700)


        self.add_node(100,200,"A")
        self.add_node(300,100,"B")
        self.add_node(300,400,"C")
        self.add_node(600,200,"D")

        self.add_Edge("A","B",100)
        self.add_Edge("A","D",500)
        self.add_Edge("A","C",100)
        self.add_Edge("B","C",15)
        self.add_Edge("B","D",80)
        self.add_Edge("C","D",200)

        self.addEntryNode("A",900)
        self.addOutNode("D",700)



        # Dibujar el grafo
        self.draw_graph()

        # Manejar eventos de arrastre
        self.canvas.bind("<ButtonPress-1>", self.on_node_press)
        self.canvas.bind("<B1-Motion>", self.on_node_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_node_release)

    def add_node(self, x, y,name):
        node = self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill="skyblue", tags="node")
        text = self.canvas.create_text(x,y,text=name,font="Arial 12 bold",fill="black")
        textUtilization = self.canvas.create_text(x,y+60,text="0%",font="Arial 10 bold",fill="black")
        nodeInfo = NodeInfo(name,node,text,textUtilization)
        crossing = Crossing(name)
        crossing.setNodeInfo(nodeInfo)
        self.nodes.append(crossing)

    def addEntryNode(self, nodeName,cantity):
        for nodeGeneral in self.nodes:
            node = nodeGeneral.nodeInfo
            if node.name == nodeName:
                nodesPosition = self.canvas.coords(node.positionCanvas)
                xNode = nodesPosition[0] + 30
                yNode = nodesPosition[1] + 30
                line = self.canvas.create_line(xNode-50, yNode, xNode - 30, yNode, fill="green", arrow=tk.LAST)
                text = self.canvas.create_text(xNode-50, yNode - 30, text=str(cantity), font="Arial 8 bold", fill="green")
                entryInfo = EntryOutInfo(text,line)
                nodeGeneral.setTrafficEntry(cantity)
                node.setEntryNode(entryInfo)
                break

    def addOutNode(self, nodeName,cantity):
        for nodeGeneral in self.nodes:
            node = nodeGeneral.nodeInfo
            if node.name == nodeName:
                nodesPosition = self.canvas.coords(node.positionCanvas)
                xNode = nodesPosition[0] + 30
                yNode = nodesPosition[1] + 30
                line = self.canvas.create_line(xNode + 30, yNode, xNode + 50, yNode, fill="orange", arrow=tk.LAST)
                text = self.canvas.create_text(xNode + 80, yNode - 10, text=cantity, font="Arial 8 bold", fill="red")
                outInfo = EntryOutInfo(text, line)
                nodeGeneral.setTrafficOut(cantity)
                node.setOutNode(outInfo)
                self.streets.append(Street(nodeName,int(cantity),nodeName,None,"."))
                break


    def add_Edge(self, fromEdge, toEdge,capacity):
        positionsFromTo = [None]*4
        nodeFrom = None
        nodeTo = None
        for nodeGeneral in self.nodes:
            node = nodeGeneral.nodeInfo
            if fromEdge == node.name:
                nodesPositionOrigin = self.canvas.coords(node.positionCanvas)
                positionsFromTo[0] = nodesPositionOrigin[0]
                positionsFromTo[1] = nodesPositionOrigin[1]
            if toEdge == node.name:
               nodesPositionDestin = self.canvas.coords(node.positionCanvas)
               positionsFromTo[2] = nodesPositionDestin[0]
               positionsFromTo[3] = nodesPositionDestin[1]

        if None is not positionsFromTo:
            xOrigin = positionsFromTo[0] + 30
            yOrigin = positionsFromTo[1] + 30
            xDestin = positionsFromTo[2] + 30
            yDestin = positionsFromTo[3] + 30
            name = ""
            orientation = ""
            xMiddle = xOrigin + xDestin
            yMiddle = yOrigin + yDestin
            direction = xDestin - xOrigin
            if direction > 0:
                line = self.canvas.create_line(xOrigin + 30, yOrigin, xDestin - 30, yDestin, fill="black", arrow=tk.LAST)
                name = fromEdge + ">" +toEdge
                orientation = ">"
            else:
                line = self.canvas.create_line(xOrigin - 30, yOrigin, xDestin + 30, yDestin, fill="black",arrow=tk.LAST)
                name = fromEdge + "<" + toEdge
                orientation = ">"
            capacity = int(capacity)
            if capacity < self.configuration.minimStreetCapacity:
                capacity = self.configuration.minimStreetCapacity
            text = self.canvas.create_text(xMiddle/2, yMiddle/2, text=name, font="Arial 8 bold", fill="black")
            capacityText = self.canvas.create_text(xMiddle / 2, (yMiddle/2)+20, text=capacity, font="Arial 10 bold", fill="black")
            percentText = self.canvas.create_text(xMiddle / 2, (yMiddle/2)+40, text="", font="Arial 8 bold", fill="black")
            streetInfo = StreetInfo(name,line,text,fromEdge,toEdge,capacityText,percentText)
            street = Street(orientation,capacity,"a","b",orientation)
            street.setStreetInfo(streetInfo)
            self.streets.append(street)


    def draw_graph(self):
        pos = nx.spring_layout(self.G)
        fig = plt.figure(figsize=(6, 4))  # Crear una figura de matplotlib
        nx.draw(self.G, pos, with_labels=True, node_size=700, node_color="skyblue")
        plt.close(fig)  # Cerrar la figura para evitar que se muestre en una ventana emergente

    def on_node_press(self, event):
        for nodeGeneral in self.nodes:
            node = nodeGeneral.nodeInfo
            nodeCanva = node.positionCanvas
            if self.canvas.coords(nodeCanva)[0] <= event.x <= self.canvas.coords(nodeCanva)[2] and \
                    self.canvas.coords(nodeCanva)[1] <= event.y <= self.canvas.coords(nodeCanva)[3]:
                self.selected_node = node
                self.drag_data = {"x": event.x, "y": event.y}

    def on_node_drag(self, event):
        if self.selected_node is not None and self.drag_data is not None:
            node = self.selected_node
            delta_x = event.x - self.drag_data["x"]
            delta_y = event.y - self.drag_data["y"]
            self.canvas.move(node.positionCanvas, delta_x, delta_y)
            self.canvas.move(node.positionText, delta_x, delta_y)
            self.canvas.move(node.positionUtilization, delta_x, delta_y)
            xLine = delta_x
            yLines = delta_y
            x = 0
            y = 0
            if node.entryNode != None:
                self.canvas.move(node.entryNode.line, delta_x, delta_y)
                self.canvas.move(node.entryNode.text, delta_x, delta_y)
            if node.outNode != None:
                self.canvas.move(node.outNode.line, delta_x, delta_y)
                self.canvas.move(node.outNode.text, delta_x, delta_y)
            for streetGeneral in self.streets:
                if streetGeneral.streetInfo is not None:
                    street = streetGeneral.streetInfo
                    line = self.canvas.coords(street.positionCanvas)
                    if street.fromN == node.name:
                        xMove = line[0] + delta_x
                        yMove = line[1] + delta_y
                        xQuiet = line[2]
                        yQuiet = line[3]
                        self.canvas.coords(street.positionCanvas, xMove, yMove, xQuiet, yQuiet)
                        self.canvas.coords(street.positionTextCanvas, ((xMove + xQuiet) / 2), ((yMove + yQuiet) / 2))
                        self.canvas.coords(street.positionTextCapacity, ((xMove + xQuiet) / 2),
                                           ((yMove + yQuiet) / 2) + 20)
                        self.canvas.coords(street.positionPercent, ((xMove + xQuiet) / 2), ((yMove + yQuiet) / 2) + 40)
                    if street.toN == node.name:
                        xQuiet = line[0]
                        yQuiet = line[1]
                        xMove = line[2] + delta_x
                        yMove = line[3] + delta_y
                        self.canvas.coords(street.positionCanvas, xQuiet, yQuiet, xMove, yMove)
                        self.canvas.coords(street.positionTextCanvas, ((xMove + xQuiet) / 2), ((yMove + yQuiet) / 2))
                        self.canvas.coords(street.positionTextCapacity, ((xMove + xQuiet) / 2),
                                           ((yMove + yQuiet) / 2) + 20)
                        self.canvas.coords(street.positionPercent, ((xMove + xQuiet) / 2), ((yMove + yQuiet) / 2) + 40)
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
    def on_node_release(self, event):
        self.drag_data = None

    def deleteNode(self,name):
        streetsDelete = []
        for streets in self.streets:
            if streets.streetInfo is not None:
                street = streets.streetInfo
                if street.toN == name or street.fromN == name or streets.name == name:
                    self.canvas.delete(street.positionCanvas)
                    self.canvas.delete(street.positionTextCanvas)
                    self.canvas.delete(street.positionUtilization)
                    self.canvas.delete(street.positionPercent)
                    streetsDelete.append(streets)
            if streets.name == name:
                streetsDelete.append(streets)

        for streets in streetsDelete:
            self.streets.remove(streets)

        for node in self.nodes:
            if node.name == name:
                nodeInfo = node.nodeInfo
                if nodeInfo.outNode is not None:
                    self.canvas.delete(nodeInfo.outNode.line)
                    self.canvas.delete(nodeInfo.outNode.text)
                if nodeInfo.entryNode is not None:
                    self.canvas.delete(nodeInfo.entryNode.line)
                    self.canvas.delete(nodeInfo.entryNode.text)
                self.canvas.delete(nodeInfo.positionCanvas)
                self.canvas.delete(nodeInfo.positionText)
                self.canvas.delete(nodeInfo.positionUtilization)
                self.nodes.remove(node)
        print("Borro "+name)

    def editNode(self,name,newName):
        for streets in self.streets:
            if streets.streetInfo is not None:
                streetInfo = streets.streetInfo
                if streetInfo.fromN == name:
                    streetInfo.fromN = newName
                    streets.origin = newName
                    self.canvas.itemconfig(streetInfo.positionTextCanvas, text=streets.getNameOrientation())
                    streetInfo.name = streets.name
                if streetInfo.toN == name:
                    streetInfo.toN = newName
                    streets.destination = newName
                    self.canvas.itemconfig(streetInfo.positionTextCanvas, text=streets.getNameOrientation())
                    streetInfo.name = streets.name
        for node in self.nodes:
            if node.name == name:
                node.name = newName
                if node.nodeInfo is not None:
                    node.nodeInfo.name = newName
                    self.canvas.itemconfig(node.nodeInfo.positionText, text=newName)
    def deleteStreets(self, fromN,toN):
        for streets in self.streets:
            if streets.origin == fromN and streets.destination == toN:
                if streets.streetInfo is not None:
                    streetInfo = streets.streetInfo
                    self.canvas.delete(streetInfo.positionCanvas)
                    self.canvas.delete(streetInfo.positionTextCanvas)
                    self.canvas.delete(streetInfo.positionTextCapacity)
                    self.canvas.delete(streetInfo.positionPercent)
                self.streets.remove(streets)

    def editStreet(self,fromN,toN,capacity):
        for streets in self.streets:
            if streets.origin == fromN and streets.destination == toN:
                streets.capacity = int(capacity)
                if streets.streetInfo is not None:
                    streetInfo = streets.streetInfo
                    self.canvas.itemconfig(streetInfo.positionTextCapacity, text=capacity)
                    return

    def delteEntryOut(self,nodeName):
        for node in self.nodes:
            if node.name == nodeName:
                positions =  None
                if node.trafficEntry is not None:
                    node.trafficEntry = None
                    positions = node.nodeInfo.entryNode
                if node.trafficOut is not None:
                    positions = node.nodeInfo.outNode
                    self.deleteStreets(nodeName,None)
                self.canvas.delete(positions.text)
                self.canvas.delete(positions.line)
                if node.trafficOut is not None:
                    node.trafficOut = None
                return
    def clean(self):
        self.canvas.delete('all')

