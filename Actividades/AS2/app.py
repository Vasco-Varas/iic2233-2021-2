from random import randint
from time import sleep
from pedido import Pedido
from shopper import Shopper
from threading import Thread


class DCComidApp(Thread):

    def __init__(self, shoppers, tiendas, pedidos):
        # NO MODIFICAR
        super().__init__()
        self.shoppers = shoppers
        self.pedidos = pedidos
        self.tiendas = tiendas

    def obtener_shopper(self):
        for shopper in self.shoppers:
            if not shopper.pedido_actual:
                return shopper
        print("Todos los shoppers están ocupados")
        # if Shopper.evento_disponible.is_set():
        #     Shopper.evento_disponible.clear()
        Shopper.evento_disponible.wait()
        Shopper.evento_disponible.clear()
        print("Se desocupó un shopper")
        return self.obtener_shopper()

    def run(self):
        while len(self.pedidos):
            pedido = self.pedidos.pop(0)
            tienda = self.tiendas[pedido[1]]

            pedido_actual = Pedido(pedido[0], pedido[1], pedido[2])

            shopper = self.obtener_shopper()
            shopper.asignar_pedido(pedido_actual)
            tienda.ingresar_pedido(pedido_actual, shopper)

            sleep(randint(1, 5))



if __name__ == '__main__':
    pass
