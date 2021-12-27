from atracciones import AtraccionAdrenalinica, AtraccionFamiliar
import parametros as p


# Recuerda completar la herencia!
class AtraccionTerrorifica(AtraccionAdrenalinica):

    def __init__(self, *args, **kwargs):
        super(AtraccionTerrorifica, self).__init__(*args, **kwargs)
        self.efecto_salud = p.SALUD_TERROR
        self.efecto_felicidad = p.FELICIDAD_TERROR

    def iniciar_juego(self, personas):
        for persona in personas:
            if persona.salud <= 2*self.salud_necesaria:
                print(f"{persona.nombre} necesita capacitación antes de jugar")
                persona.definir_estados()
        super(AtraccionTerrorifica, self).iniciar_juego(personas)


# Recuerda completar la herencia!
class CasaEmbrujada(AtraccionTerrorifica, AtraccionFamiliar):

    def iniciar_juego(self, personas):
        AtraccionFamiliar.iniciar_juego(self, personas)
