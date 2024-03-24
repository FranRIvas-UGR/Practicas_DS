import tkinter as tk
from abc import ABC,abstractmethod
class MotorApp:
    def __init__(self, root, client, salpicadero):
        self.root = root
        self.client = client
        self.salpicadero = salpicadero
        self.root = root
        self.root.title("Salpicadero")
        
        self.label_revoluciones = tk.Label(root, text="Revoluciones: ", font=("Helvetica", 14))
        self.label_revoluciones.pack(pady=10)
        
        self.label_velocidad = tk.Label(root, text="Velocidad: ", font=("Helvetica", 14))
        self.label_velocidad.pack(pady=10)
        
        self.label_distancia = tk.Label(root, text="Distancia: ", font=("Helvetica", 14))
        self.label_distancia.pack(pady=10)
        self.root.title("Control del Motor")
        
        self.estado_motor = "APAGADO"
        self.motor_encendido = False
        
        self.label_estado = tk.Label(root, text="APAGADO", font=("Helvetica", 24))
        self.label_estado.pack(pady=20)
        
        self.boton_encender = tk.Button(root, text="Encender", command=self.toggle_motor)
        self.boton_encender.pack(side=tk.TOP, pady=5)
        
        self.boton_acelerar = tk.Button(root, text="Acelerar", command=self.acelerar, state=tk.DISABLED)
        self.boton_acelerar.pack(side=tk.TOP, padx=5)
        
        self.boton_frenar = tk.Button(root, text="Frenar", command=self.frenar, state=tk.DISABLED)
        self.boton_frenar.pack(side=tk.TOP, padx=5)
        
    def toggle_motor(self):
        if self.estado_motor == "APAGADO":
            self.estado_motor = "ENCENDIDO"
            self.motor_encendido = True
            self.label_estado.config(text="ENCENDIDO", fg="green")
            self.boton_encender.config(text="Apagar")
            self.boton_acelerar.config(state=tk.NORMAL)
            self.boton_frenar.config(state=tk.NORMAL)
            self.client.send_message(self.salpicadero.get_revoluciones(), EstadoMotor.ENCENDIDO)
            self.actualizar_datos()
        else:
            self.estado_motor = "APAGADO"
            self.motor_encendido = False
            self.label_estado.config(text="APAGADO", fg="black")
            self.boton_encender.config(text="Encender")
            self.boton_acelerar.config(state=tk.DISABLED)
            self.boton_frenar.config(state=tk.DISABLED)
            self.client.send_message(self.salpicadero.get_revoluciones(), EstadoMotor.APAGADO)
            self.actualizar_datos()
    def acelerar(self):
        if self.motor_encendido:
            if self.estado_motor == "ENCENDIDO":
                self.label_estado.config(text="ACELERANDO", fg="blue")
                self.boton_acelerar.config(text="Acelerar")
                self.boton_frenar.config(state=tk.NORMAL)
                self.client.send_message(self.salpicadero.get_revoluciones(), EstadoMotor.ACELERANDO)
                self.actualizar_datos()
                

    def frenar(self):
        if self.motor_encendido:
            if self.estado_motor == "ENCENDIDO":
                self.label_estado.config(text="FRENANDO", fg="red")
                self.boton_frenar.config(text="Frenar")
                self.boton_acelerar.config(state=tk.NORMAL)
                self.client.send_message(self.salpicadero.get_revoluciones(), EstadoMotor.FRENANDO)
                self.actualizar_datos()
    def actualizar_datos(self):
        self.label_revoluciones.config(text="Revoluciones: " + str(self.salpicadero.get_revoluciones()))
        self.label_velocidad.config(text="Velocidad: " + str(self.salpicadero.get_velocidad()) + " km/h")
        self.label_distancia.config(text="Distancia: " + str(self.salpicadero.get_distancia()) + " km")
class EstadoMotor:
    APAGADO = 0
    ENCENDIDO = 1
    ACELERANDO = 2
    FRENANDO = 3


class Filter(ABC):
    @abstractmethod
    def execute(self, revoluciones, estadoMotor):
        pass


class FiltroCalcularVelocidad(Filter):
    def __init__(self):
        self.incremento_velocidad = 0

    def execute(self, revoluciones, estadoMotor):
        if estadoMotor == EstadoMotor.APAGADO or estadoMotor == EstadoMotor.ENCENDIDO:
            self.incremento_velocidad = 0
        elif estadoMotor == EstadoMotor.FRENANDO:
            self.incremento_velocidad = -100
        elif estadoMotor == EstadoMotor.ACELERANDO:
            self.incremento_velocidad = 100
        
        
        revoluciones += self.incremento_velocidad
        if revoluciones > 5000:
            revoluciones = 5000
        
        return revoluciones


class FiltroRepercutirRozamiento(Filter):

    def execute(self, revoluciones, estadoMotor):
        if revoluciones >= 0 and estadoMotor != EstadoMotor.APAGADO:
            revoluciones -= 1
        return revoluciones


class FilterChain:
    def __init__(self):
        self.filters = []
        self.target = None

    def add_filter(self, filter):
        self.filters.append(filter)

    def set_target(self, target):
        self.target = target

    def execute(self, revoluciones, estadoMotor):
        for filter in self.filters:
            revoluciones = filter.execute(revoluciones, estadoMotor)
        if self.target is not None:
            self.target.ejecutar(revoluciones)


class Salpicadero:
    def __init__(self):
        self.velocidad = 0
        self.distancia = 0
        self.revoluciones = 0
        
    def ejecutar(self, revoluciones):
        self.revoluciones = revoluciones
        self.velocidad = 2 * 3.14 * 0.15 * revoluciones * (60 / 1000)
        
        
        if self.velocidad > 0:
            self.distancia += self.velocidad * (1 / 3600) 
        
    def get_revoluciones(self):
        return self.revoluciones
    
    def get_velocidad(self):
        return self.velocidad
    
    def get_distancia(self):
        return self.distancia




class FilterManager:
    def __init__(self, target):
        self.filter_chain = FilterChain()
        self.filter_chain.set_target(target)

    def add_filter(self, filter):
        self.filter_chain.add_filter(filter)
        
    def print_datos(self, revoluciones, estadoMotor):
        self.filter_chain.execute(revoluciones, estadoMotor)


class Client:
    def __init__(self, filter_manager, salpicadero):
        self.filter_manager = filter_manager

    def send_message(self, revoluciones, estadoMotor):
        self.filter_manager.print_datos(revoluciones, estadoMotor)


if __name__ == "__main__":
   
    salpicadero = Salpicadero()  
    
    filter_manager = FilterManager(salpicadero)
    client = Client(filter_manager, salpicadero)
    
  
    filter_manager.add_filter(FiltroCalcularVelocidad())
    filter_manager.add_filter(FiltroRepercutirRozamiento())
    root = tk.Tk()
    app = MotorApp(root,client,salpicadero)
    app.actualizar_datos()
    root.mainloop()
   
   