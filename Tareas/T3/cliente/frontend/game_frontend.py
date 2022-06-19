from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QSpinBox, \
    QRadioButton, QProgressBar
from PyQt5 import uic


class GameFrontend(QMainWindow):

    sgn_ready = pyqtSignal(bool, int)
    sgn_delayer_tick = pyqtSignal()

    sgn_cheatcode_fa = pyqtSignal()
    sgn_cheatcode_zx = pyqtSignal()

    def __init__(self, resources):
        super(GameFrontend, self).__init__()

        uic.loadUi(f"{resources}/game.ui", self)

        # Widgets
        self.lbl_your_name = self.findChild(QLabel, "lbl_your_name")
        self.lbl_oponent_name = self.findChild(QLabel, "lbl_oponent_name")
        self.lbl_your_marbles = self.findChild(QLabel, "lbl_your_marbles")
        self.lbl_oponent_marbles = self.findChild(QLabel, "lbl_oponent_marbles")
        self.lbl_oponent_bet = self.findChild(QLabel, "lbl_oponent_bet")
        self.lbl_oponent_bet_value = self.findChild(QLabel, "lbl_oponent_bet_value")
        self.lbl_info_l1 = self.findChild(QLabel, "lbl_info_l1")
        self.lbl_info_l2 = self.findChild(QLabel, "lbl_info_l2")
        self.lbl_info_image = self.findChild(QLabel, "lbl_info_image")
        self.lbl_your_icon = self.findChild(QLabel, "lbl_your_icon")
        self.lbl_oponent_icon = self.findChild(QLabel, "lbl_oponent_icon")

        self.pb_your_timer = self.findChild(QProgressBar, "pb_your_timer")
        self.pb_oponent_timer = self.findChild(QProgressBar, "pb_oponent_timer")

        self.sb_bet = self.findChild(QSpinBox, "sb_bet")
        self.rb_even = self.findChild(QRadioButton, "rb_even")
        self.rb_odd = self.findChild(QRadioButton, "rb_odd")

        self.rb_even.toggled.connect(self.set_bet)
        self.rb_odd.toggled.connect(self.set_bet)

        self.btn_ready = self.findChild(QPushButton, "btn_ready")
        self.btn_ready.clicked.connect(self.click_ready)

        self.icon_skull = QPixmap("Sprites\\Decoraciones\\calavera_blanca.png")
        self.icon_clock = QPixmap("Sprites\\Decoraciones\\reloj.png")

        self.second_counter = QTimer()
        self.second_counter.timeout.connect(self.update_timers)
        self.second_counter.start(1000)

        self.key_down_f = False
        self.key_down_z = False

    def update_timers(self):
        your_time_max = self.pb_your_timer.maximum()
        oponent_time_max = self.pb_oponent_timer.maximum()
        your_time_val = self.pb_your_timer.value()
        oponent_time_val = self.pb_oponent_timer.value()

        if your_time_max > 0 and your_time_val > 0:
            self.pb_your_timer.setValue(your_time_val - 1)
        elif oponent_time_max > 0 and oponent_time_val > 0:
            self.pb_oponent_timer.setValue(oponent_time_val - 1)

    def show_game(self, p1_name, p2_name, your_id):
        if your_id == "1":
            self.lbl_your_name.setText(f"Jugador 1: {p1_name}")
            self.lbl_your_icon.setPixmap(QPixmap('Sprites\\Avatares\\Avatar-1.png'))
            self.lbl_oponent_name.setText(f"Jugador 2: {p2_name}")
            self.lbl_oponent_icon.setPixmap(QPixmap('Sprites\\Avatares\\Avatar-2.png'))
        else:
            self.lbl_your_name.setText(f"Jugador 2: {p2_name}")
            self.lbl_your_icon.setPixmap(QPixmap('Sprites\\Avatares\\Avatar-2.png'))
            self.lbl_oponent_name.setText(f"Jugador 1: {p1_name}")
            self.lbl_oponent_icon.setPixmap(QPixmap('Sprites\\Avatares\\Avatar-1.png'))
        self.show()

    def update_marbles(self, p1, p2, your_id):
        print("MARBLES:", p1, p2, your_id)
        if your_id == "1":
            self.lbl_your_marbles.setText(f"Canicas restantes: {p1}")
            self.lbl_oponent_marbles.setText(f"Canicas restantes: {p2}")
        else:
            self.lbl_your_marbles.setText(f"Canicas restantes: {p2}")
            self.lbl_oponent_marbles.setText(f"Canicas restantes: {p1}")

    def set_bet(self):
        if self.sender() == self.rb_even:
            self.rb_odd.setChecked(not self.rb_even.isChecked())

        if self.sender() == self.rb_odd:
            self.rb_even.setChecked(not self.rb_odd.isChecked())

    def click_ready(self):
        if self.rb_even.isChecked() != self.rb_odd.isChecked():
            self.sgn_ready.emit(self.rb_even.isChecked(), self.sb_bet.value())

    def start_delayer(self, ms):
        QTimer.singleShot(ms, self.delayer_tick)

    def delayer_tick(self):
        self.sgn_delayer_tick.emit()

    def update_info(self, l1, l2, icon):
        self.lbl_info_l1.setText(l1)
        self.lbl_info_l2.setText(l2)
        if icon == 0:
            self.lbl_info_image.setPixmap(self.icon_clock)
        if icon == 1:
            self.lbl_info_image.setPixmap(self.icon_skull)

    def update_turn(self, my_turn):
        self.btn_ready.setEnabled(my_turn)
        self.sb_bet.setEnabled(my_turn)
        self.rb_even.setEnabled(my_turn)
        self.rb_odd.setEnabled(my_turn)

    def update_oponent_bet(self, bet_amount, bet_even):
        self.lbl_oponent_bet.setText(bet_amount)
        self.lbl_oponent_bet_value.setText("Par" if bet_even else "Impar")

    def sgn_timers_set_max(self, your_timer, oponent_timer):
        self.pb_your_timer.setMaximum(your_timer)
        self.pb_oponent_timer.setMaximum(oponent_timer)

    def sgn_timers_set_val(self, your_timer, oponent_timer):
        self.pb_your_timer.setValue(your_timer)
        self.pb_oponent_timer.setValue(oponent_timer)

    def keyPressEvent(self, event):
        print("PRESSED", event.key, self.key_down_f, self.key_down_z)
        if event.key() == Qt.Key_F:
            self.key_down_f = True
        elif event.key() == Qt.Key_Z:
            self.key_down_z = True
        elif event.key() == Qt.Key_A and self.key_down_f:
            self.sgn_cheatcode_fa.emit()
        elif event.key() == Qt.Key_X and self.key_down_z:
            self.sgn_cheatcode_zx.emit()
        super(GameFrontend, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_F:
            self.key_down_f = False
        elif event.key() == Qt.Key_Z:
            self.key_down_z = False
        super(GameFrontend, self).keyReleaseEvent(event)

