from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton
from PyQt5 import uic
import parametros as p


class MenuBackend(QObject):
    sgn_open_game = pyqtSignal()
    sgn_open_ranking = pyqtSignal()
    sgn_open_error = pyqtSignal(str)
    sgn_close_menu = pyqtSignal()

    def click_start(self, username):

        if len(username) < p.MIN_CARACTERES:
            self.sgn_open_error.emit(f"Username cannot have less than {p.MIN_CARACTERES} characters")
        elif len(username) > p.MAX_CARACTERES:
            self.sgn_open_error.emit(f"Username cannot have more than {p.MAX_CARACTERES} characters")
        elif not username.isalnum():
            self.sgn_open_error.emit("Username must be alphanumeric")
        else:
            self.sgn_close_menu.emit()
            self.sgn_open_game.emit()

    def click_ranking(self):
        self.sgn_open_ranking.emit()