import tkinter as tk

from View.dragDrop import GraphApp
from View.controlView import ControlView

from Controller.controller import Controller
from Controller.Configuration import Configuration



def main():
    configuration = Configuration()

    nodes = []
    streets = []
    canvas = None
    root = tk.Tk()
    size = [root.winfo_screenwidth(),root.winfo_screenheight()]
    frameNodes = tk.Frame(root,width=size[0],height=size[1]*0.9)
    frameNodes.pack(fill=tk.X, expand=True)
    controller = Controller(configuration)
    app = GraphApp(frameNodes,canvas,nodes,streets,size,configuration)
    controlView = ControlView(root, app, size,controller,configuration)

    root.mainloop()
if __name__ == "__main__":
    main()