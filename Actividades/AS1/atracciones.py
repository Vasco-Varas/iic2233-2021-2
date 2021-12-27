from abc import ABC, abstractmethod
import parametros as p


# Recuerda definir esta clase como abstracta!
class Atraccion(ABC):

    def __init__(self, nombre, capacidad):
        # No modificar
        self.nombre = nombre
        self.capacidad_maxima = capacidad
        self.fila = []

    def ingresar_persona(self, persona):
        # No modificar
        print(f"** {persona.nombre} ha entrado a la fila de {self.nombre}")
        self.fila.append(persona)
        persona.esperando = True

    def nueva_ronda(self):
        # No modificar
        personas_ingresadas = 0
        lista_personas = []
        while personas_ingresadas < self.capacidad_maxima and self.fila:
            lista_personas.append(self.fila.pop(0))

        self.iniciar_juego(lista_personas)

        for persona in lista_personas:
            persona.actuar()

    def iniciar_juego(self, personas):
        # No modificar
        for persona in personas:
            print(f"*** {persona.nombre} jugó esta ronda")
            persona.esperando = False
            self.efecto_atraccion(persona)
        print()

    @abstractmethod
    def efecto_atraccion(self, persona):
        # No modificar
        pass

    def __str__(self):
        return f"Atraccion {self.nombre}"


# Recuerda completar la herencia!
class AtraccionFamiliar(Atraccion):

    def __init__(self, *args, **kwargs):
        super(AtraccionFamiliar, self).__init__(*args, **kwargs)
        self.efecto_salud = p.SALUD_FAMILIA
        self.efecto_felicidad = p.FELICIDAD_FAMILIA

    def efecto_atraccion(self, persona):
        persona.felicidad += self.efecto_felicidad
        persona.salud -= self.efecto_salud


# Recuerda completar la herencia!
class AtraccionAdrenalinica(Atraccion):

    def __init__(self, nombre: str, capacidad: int, salud_necesaria: int):
        super(AtraccionAdrenalinica, self).__init__(nombre, capacidad)
        self.salud_necesaria = salud_necesaria
        self.efecto_salud = p.SALUD_ADRENALINA
        self.efecto_felicidad = p.FELICIDAD_ADRENALINA

    def efecto_atraccion(self, persona):
        if persona.salud < self.salud_necesaria:
            print(f"A {persona.nombre} lo bajaron del juego {self.nombre}")
            persona.salud += self.efecto_salud/2
            persona.felicidad -= self.efecto_felicidad/2
        else:
            persona.felicidad += self.efecto_felicidad
            persona.salud -= self.efecto_salud


# Recuerda completar la herencia!
class AtraccionAcuatica(AtraccionFamiliar):

    def __init__(self, *args, **kwargs):
        super(AtraccionAcuatica, self).__init__(*args, **kwargs)
        self.efecto_felicidad = p.FELICIDAD_ACUATICA

    def ingresar_persona(self, persona):
        if persona.tiene_pase:
            super(AtraccionAcuatica, self).ingresar_persona(persona)


# Recuerda completar la herencia!
class MontanaAcuatica(AtraccionAdrenalinica, AtraccionAcuatica):

    def __init__(self, nombre: str, capacidad: int, salud_necesaria: int, dificultad: int):
        super(MontanaAcuatica, self).__init__(nombre, capacidad, salud_necesaria)
        self.dificultad = dificultad

    def iniciar_juego(self, personas):
        for persona in personas:
            print(f"{persona.nombre} ha jugado a {self.nombre}")
            persona.esperando = False
            if persona.salud <= self.salud_necesaria*self.dificultad:
                persona.tiene_pase = False

            AtraccionAdrenalinica.efecto_atraccion(self, persona)

    def ingresar_persona(self, persona):
        AtraccionAcuatica.ingresar_persona(self, persona)
