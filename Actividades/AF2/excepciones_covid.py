class RiesgoCovid(Exception):

    def __init__(self, sintoma, nombre_invitade):
        self.sintoma = sintoma
        self.nombre_invitade = nombre_invitade

    def alerta_de_covid(self):
        if self.sintoma == "fiebre":
            print("El invitado tiene fiebre... No puede entrar")
        elif self.sintoma == "dolor_cabeza":
            print("El invitado tiene dolor de cabeza... No puede entrar")
        elif self.sintoma == "tos":
            print("El invitado tiene toz... No puede entrar")

