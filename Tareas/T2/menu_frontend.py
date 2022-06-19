from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton
from PyQt5 import uic


class MenuFrontend(QMainWindow):
    sgn_start = pyqtSignal(str)
    sgn_ranking = pyqtSignal()

    def __init__(self):
        super(MenuFrontend, self).__init__()

        uic.loadUi("resources/main_menu.ui", self)

        # Widgets
        self.tb_username = self.findChild(QLineEdit, "tb_username")

        self.btn_start = self.findChild(QPushButton, "btn_start")
        self.btn_ranking = self.findChild(QPushButton, "btn_ranking")

        self.btn_start.clicked.connect(self.click_start)
        self.btn_ranking.clicked.connect(self.sgn_ranking)

    def click_start(self):
        self.sgn_start.emit(self.tb_username.text())

    def click_ranking(self):
        self.sgn_ranking.emit()
