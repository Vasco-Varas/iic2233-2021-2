import random
import parametros as p

class Mascota:
    def __init__(self, nombre, raza, dueno,
                 saciedad, entretencion):
        self.nombre = nombre
        self.raza = raza
        self.dueno = dueno
        
        # Los siguientes valores están en %.
        self._saciedad = saciedad
        self._entretencion = entretencion

    # COMPLETAR
    @property
    def saciedad(self):
        return self._saciedad

    @saciedad.setter
    def saciedad(self, value):
        if value > 100:
            self._saciedad = 100
        elif value < 0:
            self._saciedad = 0
        else:
            self._saciedad = value

    @property
    def entretencion(self):
        return self._entretencion

    @entretencion.setter
    def entretencion(self, value):
        if value > 100:
            self._entretencion = 100
        elif value < 0:
            self._entretencion = 0
        else:
            self._entretencion = value

    @property
    def satisfaccion(self):
        return (self.saciedad//2 + self.entretencion//2)
    
    def comer(self, comida):
        if random.random() < comida.probabilidad_vencer:
            self.saciedad -= comida.calorias
            print(f"La comida estaba vencida! A {self.nombre} le duele la pancita :(")
        else:
            self.saciedad += comida.calorias
            print(f"{self.nombre} está comiendo {comida.nombre}, que rico!")

    def pasear(self):
        self.entretencion += p.ENTRETENCION_PASEAR
        self.saciedad += p.SACIEDAD_PASEAR
    
    def __str__(self):
        return f'''Nombre: {self.nombre}
2 Saciedad: {self.saciedad}
3 Entretención: {self.entretencion}
4 Satisfacción: {self.satisfaccion}'''
        pass


class Perro(Mascota):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.especie = "PERRO"

    def saludar(self):
        print("guau guau")
        

class Gato(Mascota):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.especie = "GATO"

    def saludar(self):
        print("miau miau")

class Conejo(Mascota):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.especie = "CONEJO"

    def saludar(self):
        print("chillidos")
