from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QPushButton
from PyQt5 import uic


class MainMenuFrontend(QMainWindow):
    sgn_login = pyqtSignal(str, str)
    sgn_check_server_status = pyqtSignal(int)

    def __init__(self, resources):
        super(MainMenuFrontend, self).__init__()

        uic.loadUi(f"{resources}/mainmenu.ui", self)

        # Widgets
        self.tb_username = self.findChild(QLineEdit, "tb_username")
        self.tb_date_of_birth = self.findChild(QLineEdit, "tb_date_of_birth")

        self.btn_login = self.findChild(QPushButton, "btn_login")

        self.btn_login.clicked.connect(self.click_login)

        self.server_tester = QTimer()
        self.server_tester.timeout.connect(self.check_server)
        self.server_tester.start(500)
        self.server_tester_state = 0

        self.key_down_f = False
        self.key_down_z = False

    def check_server(self):
        self.server_tester_state = (self.server_tester_state + 1) % 4
        self.sgn_check_server_status.emit(self.server_tester_state)

    def click_login(self):
        self.sgn_login.emit(self.tb_username.text(), self.tb_date_of_birth.text())
