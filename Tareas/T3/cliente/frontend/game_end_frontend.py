from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
from PyQt5 import uic


class GameEndFrontend(QMainWindow):
    sgn_play_again = pyqtSignal()
    sgn_reconnect = pyqtSignal()

    server_connection = None

    def __init__(self, resources):
        super(GameEndFrontend, self).__init__()

        uic.loadUi(f"{resources}/game_end.ui", self)

        # Widgets
        self.lbl_winner = self.findChild(QLabel, "lbl_winner")
        self.lbl_loser = self.findChild(QLabel, "lbl_loser")

        self.btn_play_again = self.findChild(QPushButton, "btn_play_again")
        self.btn_play_again.clicked.connect(self.click_play_again)

    def show_game_end(self, winner, loser):
        self.lbl_winner.setText(winner)
        self.lbl_loser.setText(loser)
        self.show()

    def click_play_again(self):
        self.server_connection.send_text("DISCONNECTION")
        self.server_connection.close()
        self.sgn_reconnect.emit()
        self.hide()
        self.sgn_play_again.emit()
