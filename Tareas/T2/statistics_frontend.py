from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton
from PyQt5 import uic


class StatisticsFrontend(QMainWindow):
    sgn_next_lvl = pyqtSignal()
    sgn_open_shop = pyqtSignal()
    sgn_open_menu = pyqtSignal()

    def __init__(self):
        super(StatisticsFrontend, self).__init__()

        uic.loadUi("resources/lvl_statistics.ui", self)

        # Widgets
        self.lbl_lvl = self.findChild(QLabel, "lbl_lvl")
        self.lbl_total_score = self.findChild(QLabel, "lbl_total_score")
        self.lbl_lvl_score = self.findChild(QLabel, "lbl_lvl_score")
        self.lbl_lives = self.findChild(QLabel, "lbl_lives")
        self.lbl_coins = self.findChild(QLabel, "lbl_coins")
        self.lbl_continue = self.findChild(QLabel, "lbl_continue")

        self.btn_shop = self.findChild(QPushButton, "btn_shop")
        self.btn_next_lvl = self.findChild(QPushButton, "btn_next_lvl")
        self.btn_exit = self.findChild(QPushButton, "btn_exit")

        self.btn_next_lvl.clicked.connect(self.click_next_lvl)

    def show_stats(self, level, total_score, lvl_score, lives, coins):
        self.lbl_lvl.setText(str(level))
        self.lbl_total_score.setText(str(total_score))
        self.lbl_lvl_score.setText(str(lvl_score))
        self.lbl_lives.setText(str(lives))
        self.lbl_coins.setText(str(coins))

        if lives <= 0:
            self.btn_shop.setEnabled(False)
            self.btn_next_lvl.setEnabled(False)
            self.lbl_continue.setText("No puedes seguir jugando :(")

        self.show()

    def click_next_lvl(self):
        self.hide()
        self.sgn_next_lvl.emit()