import random
import threading
import time


class Caballo(threading.Thread):
    "Representa un caballo."

    def __init__(self, numero: int, distancia_meta: float):
        self.fuerza = random.gauss(15, 2)
        self.resitencia = random.gauss(10, 2)
        self.suerte = abs(random.gauss(2, 0.5))
        self.numero = numero
        self.distancia = 0
        self.distancia_meta = distancia_meta
        super().__init__()

    def mover(self):
        "Hace que el caballo se mueva."
        x = random.gauss(self.fuerza, self.suerte)
        t = abs(random.gauss(1/self.resitencia, self.suerte))
        time.sleep(t)
        self.distancia += x
        print(f'Caballo #{self.numero}, está en {self.distancia:.2f}')
    
    def __repr__(self) -> str:
        return f'> Caballo #{self.numero}, Fuerza: {self.fuerza}, Resistencia: {self.resitencia}'

    def run(self):
        "Representa la carrera del caballo."
        while self.distancia < self.distancia_meta:
            self.mover()
        print(f'El caballo #{self.numero} ha llegado a la meta.')


caballos = [Caballo(i, 1000) for i in range(11)]

for caballo in caballos:
    print(caballo)

input('Pulsa enter para empezar la carrera')


for caballo in caballos:
    caballo.start()

for caballo in caballos:
    caballo.join()
