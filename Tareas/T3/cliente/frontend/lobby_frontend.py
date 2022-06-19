from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
from PyQt5 import uic


class LobbyFrontend(QMainWindow):
    sgn_invite = pyqtSignal(str)

    def __init__(self, resources):
        super(LobbyFrontend, self).__init__()

        uic.loadUi(f"{resources}/lobby.ui", self)

        # Widgets
        self.lbls = []
        self.lbls.append(self.findChild(QLabel, "lbl_p1"))
        self.lbls.append(self.findChild(QLabel, "lbl_p2"))
        self.lbls.append(self.findChild(QLabel, "lbl_p3"))

        self.btns = []
        self.btns.append(self.findChild(QPushButton, "btn_p1"))
        self.btns.append(self.findChild(QPushButton, "btn_p2"))
        self.btns.append(self.findChild(QPushButton, "btn_p3"))

        for btn in self.btns:
            btn.clicked.connect(self.click_user)

        self.lbl_status = self.findChild(QLabel, "lbl_status")

    def click_user(self):
        print(f"1. {self.lbls[0].text()}")
        if self.sender().objectName() == "btn_p1":
            usr = list(filter(lambda x: f"1. {x[1]}" == self.lbls[0].text(), self.user_list))[0][0]
        if self.sender().objectName() == "btn_p2":
            usr = list(filter(lambda x: f"2. {x[1]}" == self.lbls[1].text(), self.user_list))[0][0]
        if self.sender().objectName() == "btn_p3":
            usr = list(filter(lambda x: f"3. {x[1]}" == self.lbls[2].text(), self.user_list))[0][0]
        print(usr)
        self.sgn_invite.emit(str(usr))

    def update_users(self, users: dict):
        self.user_list = sorted(
            [[user_id, user[0], user[1] == "TRUE"] for user_id, user in users.items()],
            key=lambda x: x[0])

        for x in range(3):
            print(x)
            self.lbls[x].hide()
            self.btns[x].hide()

        for last_element, user in enumerate(self.user_list):
            print(f"{last_element} user {user[1]}: {user[2]}")
            self.lbls[last_element].setText(f"{last_element + 1}. {user[1]}")
            self.lbls[last_element].show()
            if user[2]:
                self.btns[last_element].show()
