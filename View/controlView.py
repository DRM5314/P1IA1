import tkinter as tk
from tkinter import messagebox
class ControlView:
    def __init__(self, master,app,size,controller,configuration):
        self.master = master
        self.size = size
        self.app = app
        self.controller = controller
        self.frameConfiguration = tk.Frame(master=master, width=size[0],height=size[1]*20/100, bg="orange")
        self.frameConfiguration.rowconfigure(0, weight=1)
        self.frameConfiguration.columnconfigure([0, 1, 2, 3, 4, 5],  weight=1)
        self.chargeButtons()
        self.frameConfiguration.pack(fill=tk.X, expand=True)
        self.configuration = configuration

    def chargeButtons(self):
        frameConfiguration = self.frameConfiguration
        addNode = tk.Button(master=frameConfiguration, text="Nodo",width=8,height=1, command=self.abrir_ventana_datos)
        addNode.grid(row=0, column=0)
        addNode = tk.Button(master=frameConfiguration,width=8,height=1, text="Arista", command=self.optionsStreet)
        addNode.grid(row=0, column=1)
        addNode = tk.Button(master=frameConfiguration,width=8,height=1, text="Entrada/Salida", command=self.optionsE_S)
        addNode.grid(row=0, column=2)
        addNode = tk.Button(master=frameConfiguration,width=8,height=1, text="Analizar", command=self.analizeView)
        addNode.grid(row=0, column=3)
        addNode = tk.Button(master=frameConfiguration,width=8,height=1, text="configuracion", command=self.clean)
        addNode.grid(row=0, column=4)
        addNode = tk.Button(master=frameConfiguration,width=8,height=1, text="Limpar", command=self.clean)
        addNode.grid(row=0, column=5)

    def clean(self):
        self.app.nodes.clear()
        self.app.streets.clear()
        self.app.clean()
    def abrir_ventana_datos(self):
        # Función para abrir la ventana emergente y solicitar datos al usuario

        def crear():
            nombre = entry_nombre.get()
            validName = self.validNameCreate(nombre)
            # Validar que se hayan ingresado datos en ambos campos
            if not validName:
                messagebox.showerror("Error", "Por favor ingrese nombre, nombre repetido o invalido!")
                ventana_datos.lift()
                return
            ventana_datos.lift()
            self.mostrar_resultado(nombre)

        def borrar():
            name = entry_nombre.get()
            validName = (self.existsNode(name))
            if validName:
                response = messagebox.askquestion("Confirmacion","Esta seguro de borar el nodo?: "+name)
                if response == "yes":
                    self.app.deleteNode(name)
                else:
                    ventana_datos.lift()
            else:
                messagebox.showerror("Error", "Nombre no existente")
                ventana_datos.lift()


        def editar():
            name = entry_nombre.get()
            validName = self.existsNode(name)
            if validName:
                ventana_datos1 = tk.Toplevel(self.master)
                ventana_datos1.geometry("350x150")
                ventana_datos1.title("Ingresar Nuevo Nombre")

                # Agregar widgets para ingresar datos
                tk.Label(ventana_datos1, text="Nombre:").pack()
                entry_nombre1 = tk.Entry(ventana_datos1)
                entry_nombre1.pack()
                def editarNodo():
                    newNombre = entry_nombre1.get()
                    validname = (self.validNameCreate(newNombre))
                    if validname:
                        print("Editar nodo "+newNombre)
                        self.app.editNode(name,newNombre)
                        ventana_datos1.destroy()
                    else:
                        messagebox.showerror("Error", "Por favor ingrese nombre, nombre repetido o invalido!")
                        ventana_datos1.lift()

                # Botón "Aceptar" para validar y cerrar la ventana
                tk.Button(ventana_datos1, text="Editar", command=editarNodo, width=4, height=1).pack()
            else:
                messagebox.showerror("Error", "Nombre no existente")
                ventana_datos.lift()


        # Crear la ventana emergente
        ventana_datos = tk.Toplevel(self.master)
        ventana_datos.geometry("350x150")
        ventana_datos.title("Ingresar Datos Nodo")

        # Agregar widgets para ingresar datos
        tk.Label(ventana_datos, text="Nombre:").pack()
        entry_nombre = tk.Entry(ventana_datos)
        entry_nombre.pack()

        # Botón "Aceptar" para validar y cerrar la ventana
        tk.Button(ventana_datos, text="Agregar", command=crear,width=4,height=1).pack()
        tk.Button(ventana_datos, text="Editar ", command=editar, width=4,height=1).pack()
        tk.Button(ventana_datos, text="Borrar ",command=borrar , width=4,height=1).pack()

    def mostrar_resultado(self,nombre):
        # Función para mostrar los datos ingresados por el usuario
        # messagebox.showinfo("Datos Ingresados", f"Nombre: {nombre}\nEdad: {edad}")
        # self.app.add_node(745,32,nombre)
        x = self.size[0] / 4
        self.app.add_node(x,40,nombre)

    def validNameCreate(self,name):
        for node in self.app.nodes:
            if node.name == name:
                return False

        if name.strip() == "":
            return False
        return True

    def existsNode(self,name):
        for node in self.app.nodes:
            if node.name == name:
                return True
        return False

    def optionsStreet(self):
        def crear():
            fromN = entry_from.get()
            toN = entry_to.get()
            capacity = entry_capacidad.get()
            validStreet = self.validateNewStreet(fromN,toN,capacity)
            validaCapacity = self.validateNumber(capacity,"Capacidad Salida")
            # Validar que se hayan ingresado datos en ambos campos
            if not validStreet and not validaCapacity:
                ventana_datos.lift()
                return
            ventana_datos.lift()
            self.createStreet(fromN,toN,capacity)

        def borrar():
            fromN = entry_from.get()
            toN = entry_to.get()
            validStreet = self.existsStreet(fromN,toN)
            # Validar que se hayan ingresado datos en ambos campos
            if not validStreet:
                messagebox.showerror("Error ", "No existe calle")
                ventana_datos.lift()
                return
            response = messagebox.askquestion("Confirmacion", f"Esta seguro de borar el calle?: {fromN} - {toN}")
            if response == "yes":
                self.delteStreet(fromN,toN)
                ventana_datos.destroy()
            else:
                ventana_datos.lift()
        def editCapacity():
            fromN = entry_from.get()
            toN = entry_to.get()
            capacity = entry_capacidad.get()
            validStreet = self.existsStreet(fromN,toN)
            validateNumber = self.validateNumber(capacity,"Capacidad")
            # Validar que se hayan ingresado datos en ambos campos
            if validStreet:
                if validateNumber:
                    self.editStreets(fromN, toN, capacity)
                ventana_datos.lift()
                return
            else:
                messagebox.showerror("Error ", "No existe calle")
                ventana_datos.lift()

        ventana_datos = tk.Toplevel(self.master)
        ventana_datos.geometry("350x250")
        ventana_datos.title("Ingresar Datos Calle")

        # Agregar widgets para ingresar datos
        tk.Label(ventana_datos, text="Origen o (E):").pack()
        entry_from = tk.Entry(ventana_datos)
        entry_from.pack()

        tk.Label(ventana_datos, text="Destino o (S):").pack()
        entry_to = tk.Entry(ventana_datos)
        entry_to.pack()

        tk.Label(ventana_datos, text="Capacidad:").pack()
        entry_capacidad = tk.Entry(ventana_datos)
        entry_capacidad.pack()

        # Botón "Aceptar" para validar y cerrar la ventana
        tk.Button(ventana_datos, text="Agregar", command=crear, width=4, height=1).pack()
        tk.Button(ventana_datos, text="Borrar", command=borrar, width=4, height=1).pack()
        tk.Button(ventana_datos, text="Editar", command=editCapacity, width=4, height=1).pack()

    def validateNewStreet(self,fromN, toN, capacity):
        if fromN.strip() == "" or toN.strip() == "" or capacity.strip() == "":
            messagebox.showerror("Error", "Llene todos los campos")
            return False
        if fromN == toN:
            messagebox.showerror("Error", "No puede crear una arista a ella misma!")
            return False
        if self.existsStreet(fromN,toN):
            messagebox.showerror("Error", "Calle ya existe en el sistema!")
            return False
        if not self.validateNumber(capacity,"Capacidad"):
            return False

        if int(capacity) < self.configuration.minimStreetCapacity:
            messagebox.showerror("Error", "Por favor ingrese capacidad mayor a"+str(self.configuration.minimStreetCapacity))
            return False
        return True

    def existsStreet(self,fromN,toN):
        for street in self.app.streets:
            if street.origin == fromN and street.destination == toN:
                return True
        return False

    def validateNumber(self,entry,tipo):
        try:
            number = int(entry)
            if number <= 0 or number < self.configuration.minimStreetCapacity:
                messagebox.showerror("Error"," Numero tiene que ser mayor o igual "+str(self.configuration.minimStreetCapacity))
                return False
        except ValueError:
            messagebox.showerror("Error ", "Debe ser un numero entero. para: "+tipo)
            return False
        return True


    def createStreet(self, fromN, toN, capacity):
        self.app.add_Edge(fromN, toN, capacity)

    def delteStreet(self,fromN,toN):
        self.app.deleteStreets(fromN,toN)

    def editStreets(self, fromN,toN,capacity):
        self.app.editStreet(fromN,toN,capacity)

    def addEntry(self):
        self.optionsE_S(True)

    def addOut(self):
        self.optionsE_S(False)
    def optionsE_S(self):
        def crear():
            node = entry_node.get()
            capacity = entry_capacidad.get()
            isEntry = var_checkbox.get()

            validNode = self.existsNode(node)
            validCapacity = self.validateNumber(capacity,"Capacidad")
            validExistE_S = self.validEntryOut(node)

            # Validar que se hayan ingresado datos en ambos campos
            if validExistE_S:
                if validNode:
                    if validCapacity:
                        if isEntry:
                            self.app.addEntryNode(node, capacity)
                        else:
                            self.app.addOutNode(node, capacity)
                    ventana_datos.lift()
                    return
                else:
                    messagebox.showerror("Error ", "No existe nodo")
            else:
                messagebox.showerror("Error ", "Nodo ya tiene entrada o salida")
            ventana_datos.lift()

        def delete():
            node = entry_node.get()
            validNode = self.existsNode(node)
            validExistE_S = self.validEntryOut(node)

            # Validar que se hayan ingresado datos en ambos campos
            if not validExistE_S:
                if validNode:
                    self.app.delteEntryOut(node)
                    ventana_datos.lift()
                    return
                else:
                    messagebox.showerror("Error ", "Nodo no existe")
            else:
                messagebox.showerror("Error ", "Nodo no tiene entrada o salida")
            ventana_datos.lift()

        ventana_datos = tk.Toplevel(self.master)
        ventana_datos.geometry("350x250")
        ventana_datos.title("Ingresar Datos Entrada / Salida")

        # Agregar widgets para ingresar datos
        tk.Label(ventana_datos, text="Nodo").pack()
        entry_node = tk.Entry(ventana_datos)
        entry_node.pack()

        var_checkbox = tk.BooleanVar()
        checkbox = tk.Checkbutton(ventana_datos, text="Entrada:True Salida:False", variable=var_checkbox)
        checkbox.pack()

        tk.Label(ventana_datos, text="Capacidad:").pack()
        entry_capacidad = tk.Entry(ventana_datos)
        entry_capacidad.pack()

        # Botón "Aceptar" para validar y cerrar la ventana
        tk.Button(ventana_datos, text="Agregar", command=crear, width=4, height=1).pack()
        tk.Button(ventana_datos, text="Borrar",  command=delete, width=4, height=1).pack()
    def validEntryOut(self,nodeName):
        for node in self.app.nodes:
            if node.name == nodeName:
                if node.trafficEntry is not None or node.trafficOut is not None:
                    return False
        return True
    def analizeView(self):
        self.controller.analizeEntryNodes(self.app.nodes, self.app.streets)
        counter = 0
        while self.controller.isTheBest(counter):
            self.controller.selectFathersFun()
            print(f"In interaction: {counter} {self.controller.bestPoblation()}")
            self.controller.mix(counter)
            result = self.controller.analize(counter,self.app.canvas)
            if result:
                self.controller.isTheBest(counter)
                break
            counter += 1
        self.controller.cleanVars()
        return False

    def optionsConfiguration(self):
        ventana_datos = tk.Toplevel(self.master)
        ventana_datos.geometry("350x250")
        ventana_datos.title("Ingresar Datos De configuration")

        tk.Label(ventana_datos, text="Poblacion").pack()
        entry_Poblacion = tk.Entry(ventana_datos,textvariable="50")
        entry_Poblacion.pack()

        tk.Label(ventana_datos, text="Generaciones").pack()
        entry_Generaciones = tk.Entry(ventana_datos)
        entry_Generaciones.pack()

        tk.Label(ventana_datos, text="Minimo Porcentaje").pack()
        entry_Minimo_Porcentaje = tk.Entry(ventana_datos)
        entry_Minimo_Porcentaje.pack()

        tk.Label(ventana_datos, text="Minimo capacidad calle").pack()
        entry_streetMinCapacity = tk.Entry(ventana_datos)
        entry_streetMinCapacity.pack()

        tk.Label(ventana_datos, text="# mutaciones").pack()
        entry_mutations = tk.Entry(ventana_datos)
        entry_mutations.pack()

        tk.Label(ventana_datos, text="Mutations x Generations").pack()
        entrymutationsXGenerations = tk.Entry(ventana_datos)
        entrymutationsXGenerations.pack()

        tk.Label(ventana_datos, text="Refresh canva").pack()
        entry_refres_canva = tk.Entry(ventana_datos)

        # Botón "Aceptar" para validar y cerrar la ventana
        tk.Button(ventana_datos, text="Agregar", command=crear, width=4, height=1).pack()


