#Ejercicio 2. Patrón Factoría Abstracta + Patrón Prototipo
#(Python
#Descripción
#Diseña e implementa una aplicación con la misma funcionalidad que la del ejercicio anterior,
#pero que aplique el patrón Prototipo junto con el patrón Factoría Abstracta.
#Se elegirá el lenguaje de programación Python o Ruby. Para simplificar: no es necesario
#el uso de hebras.

from abc import ABC, abstractmethod
import random
import copy
import threading
import time


#Para ejecutar python3 Ejercicio2.py

# Interfaz FactoriaCarreraYBicicleta
class FactoriaCarreraYBicicleta(ABC):
    NUM_BICICLETAS = random.randint(1, 10) * 10

    @abstractmethod
    def crearBicicleta(self):
        pass

    @abstractmethod
    def crearCarrera(self):
        pass

# Clases concretas de factorías
class FactoriaCarretera(FactoriaCarreraYBicicleta):
    def crearCarrera(self, numBicicletas):
        carrera = CarreraCarretera()
        carrera.crearCarrera(numBicicletas)
        return carrera

    def crearBicicleta(self):
        return BicicletaCarretera()
    
class FactoriaMontana(FactoriaCarreraYBicicleta):
    def crearCarrera(self, numBicicletas):
        carrera = CarreraMontana()
        carrera.crearCarrera(numBicicletas)
        return carrera

    def crearBicicleta(self):
        return BicicletaMontana()
    
# Clases prototipo
class Prototipo(ABC):
    @abstractmethod
    def clone():
        pass

class Bicicleta(Prototipo):
    idBicicleta = random.randint(1,1000)

    def clone(self):
        return copy.deepcopy(self)

class BicicletaCarretera(Bicicleta):
    def __init__(self):
        self.tipo = "Carretera"


class BicicletaMontana(Bicicleta):
    def __init__(self):
        self.tipo = "Montaña"


class Carrera():
    def __init__(self):
        self.bicicletas = []

    @abstractmethod
    def retirarBicicletas():
        pass


# Clases concretas de bicis y carreras
class CarreraCarretera(Carrera):
    def __init__(self):
        super().__init__()

    def crearCarrera(self, numBicicletas):
        bicicleta_original = BicicletaCarretera()
        for i in range(numBicicletas):
            self.bicicletas.append(bicicleta_original.clone())
        
    def retirarBicicletas(self):
        n = len(self.bicicletas) // 10
        for i in range(n):
            self.bicicletas.pop()

class CarreraMontana(Carrera):
    def __init__(self):
        super().__init__()

    def crearCarrera(self, numBicicletas):
        bicicleta_original = BicicletaMontana()
        for i in range(numBicicletas):
            self.bicicletas.append(bicicleta_original.clone())
        
    def retirarBicicletas(self):
        n = len(self.bicicletas) // 5
        for i in range(n):
            self.bicicletas.pop()


def ejercicio2():
    factoriaMontana = FactoriaMontana()
    factoriaCarretera = FactoriaCarretera()

    def hilo_montana():
        carreraMontana = factoriaMontana.crearCarrera(factoriaMontana.NUM_BICICLETAS)
        numBicicletas = len(carreraMontana.bicicletas)
        print(f"Número de bicicletas en la carrera de montaña: {numBicicletas}")
        time.sleep(2)
        carreraMontana.retirarBicicletas()
        numBicicletasRest = len(carreraMontana.bicicletas)
        print(f"Porcentaje de bicicletas retiradas en la carrera de montaña: {(numBicicletas - numBicicletasRest) / numBicicletas * 100}%")

    def hilo_carretera():
        carreraCarretera = factoriaCarretera.crearCarrera(factoriaCarretera.NUM_BICICLETAS)
        numBicicletas = len(carreraCarretera.bicicletas)
        print(f"Número de bicicletas en la carrera de carretera: {numBicicletas}")
        time.sleep(2)
        carreraCarretera.retirarBicicletas()
        numBicicletasRestantes = len(carreraCarretera.bicicletas)
        print(f"Porcentaje de bicicletas retiradas en la carrera de montaña: {(numBicicletas - numBicicletasRestantes) / numBicicletas * 100}%")

    print("-------------------")

    thread_montana = threading.Thread(target=hilo_montana)
    thread_carretera = threading.Thread(target=hilo_carretera)

    thread_montana.start()
    thread_carretera.start()

    thread_montana.join()
    thread_carretera.join()
 

ejercicio2()
