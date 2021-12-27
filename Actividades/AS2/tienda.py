from threading import Thread, Lock
from time import sleep
from random import randint


class Tienda(Thread):
    def __init__(self, nombre):
        # NO MODIFICAR
        super().__init__()
        self.nombre = nombre
        self.cola_pedidos = []
        self.abierta = True
        # COMPLETAR DESDE AQUI
        self.lock = Lock()

    def ingresar_pedido(self, pedido, shopper):
        with self.lock:
            self.cola_pedidos.append((pedido, shopper))

    def preparar_pedido(self, pedido):
        tme = randint(1, 10)
        print(f"{self.nombre}: El pedido se va a demorar {tme} segundos")
        sleep(tme)
        print(f"{self.nombre}: Pedido finalizado")

    def run(self):
        while self.abierta:
            if len(self.cola_pedidos):
                with self.lock:
                    ped = self.cola_pedidos.pop(0)[0]
                    ped.evento_pedido_listo.set()
                    if not ped.evento_llego_repartidor.is_set():
                        ped.evento_llego_repartidor.wait()
                    print(f"{self.nombre}: Llegó repartidor")
            else:
                sleep(randint(1, 5))
                print(f"{self.nombre}: No hay pedidos, la tienda se toma un descanso")
