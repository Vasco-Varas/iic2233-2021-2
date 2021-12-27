from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout,
)

import parametros as p


class VentanaInicio(QWidget):

    senal_enviar_login = pyqtSignal(tuple)

    def __init__(self, tamano_ventana):
        super().__init__()
        self.init_gui(tamano_ventana)

    def init_gui(self, tamano_ventana):
        self.setWindowIcon(QIcon(p.RUTA_ICONO))

        self.setGeometry(tamano_ventana)

        self.lbl_username = QLabel("Nombre de usuario:", self)
        self.usuario_form = QLineEdit("", self)

        self.lbl_password = QLabel("Contraseña:", self)
        self.clave_form = QLineEdit("", self)
        self.clave_form.setEchoMode(QLineEdit.Password)

        pixmap = QPixmap(p.RUTA_LOGO)
        self.lbl_logo = QLabel(self)
        self.lbl_logo.setPixmap(pixmap)
        self.lbl_logo.setMaximumSize(400, 400)

        self.ingresar_button = QPushButton("Ingresar", self)
        self.ingresar_button.clicked.connect(self.enviar_login)

        self.lyt_main = QVBoxLayout(self)
        self.lyt_main.addStretch(1)
        self.lyt_main.addWidget(self.lbl_logo)
        self.lyt_main.addStretch(1)
        self.lyt_main.addWidget(self.lbl_username)
        self.lyt_main.addWidget(self.usuario_form)

        self.lyt_main.addStretch(1)

        self.lyt_main.addWidget(self.lbl_password)
        self.lyt_main.addWidget(self.clave_form)
        self.lyt_main.addStretch(1)

        self.lyt_main.addWidget(self.ingresar_button)

        self.agregar_estilo()



    def enviar_login(self):
        self.senal_enviar_login.emit((self.ingresar_button.text(), self.clave_form.text()))

    def agregar_estilo(self):
        # Acciones y señales
        self.clave_form.returnPressed.connect(
            lambda: self.ingresar_button.click()
        )  # Permite usar "ENTER" para iniciar sesión

        # Estilo extra
        self.setStyleSheet("background-color: #fdf600")
        self.usuario_form.setStyleSheet("background-color: #000000;"
                                        "border-radius: 5px;"
                                        "color: white")
        self.clave_form.setStyleSheet("background-color: #000000;"
                                      "border-radius: 5px;"
                                      "color: white")
        self.ingresar_button.setStyleSheet(p.stylesheet_boton)

    def recibir_validacion(self, tupla_respuesta):
        if tupla_respuesta[1]:
            self.ocultar()
        else:
            self.clave_form.setText("")
            self.clave_form.setPlaceholderText("Contraseña inválida!")

    def mostrar(self):
        self.show()

    def ocultar(self):
        self.hide()
