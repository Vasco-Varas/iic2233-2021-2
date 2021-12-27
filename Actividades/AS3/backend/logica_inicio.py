from PyQt5.QtCore import QObject, pyqtSignal

import parametros as p


class LogicaInicio(QObject):

    senal_respuesta_validacion = pyqtSignal(tuple)
    senal_abrir_juego = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def comprobar_contrasena(self, credenciales):

        test_for = credenciales[1].lower() == p.CONTRASENA.lower()
        if test_for:
            self.senal_abrir_juego.emit(credenciales[1])

        self.senal_respuesta_validacion.emit((credenciales[1], test_for))
