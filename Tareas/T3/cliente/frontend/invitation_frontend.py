from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
from PyQt5 import uic


class InvitationFrontend(QMainWindow):
    sgn_answer = pyqtSignal(str, str)

    def __init__(self, resources):
        super(InvitationFrontend, self).__init__()

        uic.loadUi(f"{resources}/invitation.ui", self)

        # Widgets
        self.lbl_invitation = self.findChild(QLabel, "lbl_invitation")

        self.btn_accept = self.findChild(QPushButton, "btn_accept")
        self.btn_refuse = self.findChild(QPushButton, "btn_refuse")

        self.btn_accept.clicked.connect(self.click_accept)
        self.btn_refuse.clicked.connect(self.click_refuse)

    def click_accept(self):
        self.hide()
        self.sgn_answer.emit("ACCEPTED", self.uuid)

    def click_refuse(self):
        self.hide()
        self.sgn_answer.emit("REFUSED", self.uuid)

    def show_invitation(self, username, uuid):
        self.lbl_invitation.setText(f"{username} te ha invitado a jugar")
        self.uuid = uuid
        self.show()
