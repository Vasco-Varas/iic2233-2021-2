from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton
from PyQt5 import uic


class ErrorFrontend(QMainWindow):
    sgn_start = pyqtSignal(str)
    sgn_ranking = pyqtSignal()

    def __init__(self):
        super(ErrorFrontend, self).__init__()

        uic.loadUi("resources/error.ui", self)

        # Widgets
        self.lbl_error = self.findChild(QLabel, "lbl_error")
        print("SETUP")

    def show_error(self, msg):
        self.lbl_error.setText(msg)
        self.show()
