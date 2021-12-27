from collections import deque


class NodoGrafo:
    def __init__(self, usuario):
        # No modificar
        self.usuario = usuario
        self.amistades = None

    def formar_amistad(self, nueva_amistad):
        if self.amistades and nueva_amistad not in self.amistades:
            self.amistades.append(nueva_amistad)
            nueva_amistad.formar_amistad(self)

    def eliminar_amistad(self, ex_amistad):
        if self.amistades and ex_amistad in self.amistades:
            self.amistades.remove(ex_amistad)
            ex_amistad.eliminar_amistad(self)


def recomendar_amistades(nodo_inicial, profundidad):
    """
    Recibe un NodoGrafo inicial y una profundidad de busqueda, retorna una
    lista de nodos NodoGrafo recomendados como amistad a esa profundidad.
    """
    # Debes modificarlo
    nuevas_amistades = nodo_inicial.amistades

    for i in range(profundidad):
        for node in nuevas_amistades:
            for n_node in node.amistades:
                if n_node not in nuevas_amistades:
                    nuevas_amistades.append(n_node)
    for am in nuevas_amistades.copy():
        if am in nodo_inicial.amistades:
            nuevas_amistades.remove(am)
    return nuevas_amistades


def busqueda_famosos(nodo_inicial, visitados=None, distancia_max=80):
    """
    [BONUS]
    Recibe un NodoGrafo y busca en la red social al famoso mas
    cercano, retorna la distancia y el nodo del grafo que contiene
    a el usuario famoso cercano al que se encuentra.
    """
    pass

