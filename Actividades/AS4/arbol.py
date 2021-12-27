class NodoFama:

    def __init__(self, usuario, padre=None):
        # No modificar
        self.usuario = usuario
        self.padre = padre
        self.hijo_izquierdo = None
        self.hijo_derecho = None


class ArbolBinario:

    def __init__(self):
        # No modificar
        self.raiz = None

    def crear_arbol(self, nodos_fama):
        # No modificar
        for nodo in nodos_fama:
            self.insertar_nodo(nodo, self.raiz)

    def insertar_nodo(self, nuevo_nodo, padre=None):
        if self.raiz and not padre:
            self.insertar_nodo(nuevo_nodo, self.raiz)
        if not self.raiz:
            self.raiz = nuevo_nodo
            return
        if nuevo_nodo.usuario.fama > padre.usuario.fama:
            if padre.hijo_derecho:
                self.insertar_nodo(nuevo_nodo, padre.hijo_derecho)
            else:
                padre.hijo_derecho = nuevo_nodo

        elif nuevo_nodo.usuario.fama <= padre.usuario.fama:
            if padre.hijo_izquierdo:
                self.insertar_nodo(nuevo_nodo, padre.hijo_izquierdo)
            else:
                padre.hijo_izquierdo = nuevo_nodo


    def buscar_nodo(self, fama, padre=None):
        if self.raiz and not padre:
            return self.buscar_nodo(fama, self.raiz)

        if fama > padre.usuario.fama:
            if padre.hijo_derecho:
                return self.buscar_nodo(fama, padre.hijo_derecho)
            return None
        elif fama < padre.usuario.fama:
            if padre.hijo_izquierdo:
                return self.buscar_nodo(fama, padre.hijo_izquierdo)
            return None
        else:
            return padre


    def print_arbol(self, nodo=None, nivel_indentacion=0):
        # No modificar
        indentacion = "|   " * nivel_indentacion
        if nodo is None:
            print("** DCCelebrity Arbol Binario**")
            self.print_arbol(self.raiz)
        else:
            print(f"{indentacion}{nodo.usuario.nombre}: "
                  f"{nodo.usuario.correo}")
            if nodo.hijo_izquierdo:
                self.print_arbol(nodo.hijo_izquierdo,
                                 nivel_indentacion + 1)
            if nodo.hijo_derecho:
                self.print_arbol(nodo.hijo_derecho,
                                 nivel_indentacion + 1)
