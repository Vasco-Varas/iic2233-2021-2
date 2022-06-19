from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton
from PyQt5 import uic


class GameFrontend(QMainWindow):
    sgn_pause = pyqtSignal()
    sgn_exit = pyqtSignal()
    sgn_move = pyqtSignal(int)

    def __init__(self):
        super(GameFrontend, self).__init__()

        uic.loadUi("resources/game.ui", self)

        # Widgets
        self.lbl_lives = self.findChild(QLabel, "lbl_lives")
        self.lbl_time = self.findChild(QLabel, "lbl_time")
        self.lbl_coins = self.findChild(QLabel, "lbl_coins")
        self.lbl_lvl = self.findChild(QLabel, "lbl_lvl")
        self.lbl_score = self.findChild(QLabel, "lbl_score")

        self.obj_froggy = self.findChild(QLabel, "obj_froggy")

        self.btn_pause = self.findChild(QPushButton, "btn_pause")
        self.btn_exit = self.findChild(QPushButton, "btn_exit")

        self.btn_pause.clicked.connect(self.click_pause)
        self.btn_exit.clicked.connect(self.click_exit)

        self.lbl_cars = []
        self.lbl_logs = []
        self.lbl_cars_empty = []
        self.lbl_logs_empty = []

        self.lbl_objects = []
        self.lbl_objects_empty = []

    def click_pause(self):
        self.sgn_pause.emit()

    def click_exit(self):
        self.sgn_exit.emit()

    def update_values(self, game_lives, game_remaining_time, game_coins, game_lvl, game_score):
        self.lbl_lives.setText(f"VIDAS: {game_lives}")
        self.lbl_time.setText(f"TIEMPO: {game_remaining_time} sgds.")
        self.lbl_coins.setText(f"MONEDAS: {game_coins}")
        self.lbl_lvl.setText(f"NIVEL: {game_lvl}")
        self.lbl_score.setText(f"PUNTAJE: {game_score}")

    def update_obstacles(self, cars, logs, objects):
        lbl_car_alive = False
        for lbl_car in self.lbl_cars.copy():
            for car in cars:
                if lbl_car == car.designated_label:
                    lbl_car_alive = True
                    break
            if not lbl_car_alive:
                lbl_car.hide()
                self.lbl_cars_empty.append(lbl_car)
                self.lbl_cars.remove(lbl_car)
        for car in cars:
            if car.designated_label in self.lbl_cars:
                car.designated_label.move(car.x, car.y)
                car.designated_label.show()
            elif car.designated_label == None:
                if len(self.lbl_cars_empty) > 0:
                    car.designated_label = self.lbl_cars_empty.pop()
                    self.lbl_cars.append(car.designated_label)
                    car.designated_label.setPixmap(QPixmap(car.sprite))
                    car.designated_label.move(car.x, car.y)
                    break
                car.designated_label = QLabel(self)
                car.designated_label.setGeometry(car.x, car.y, 100, 80)
                car.designated_label.setPixmap(QPixmap(car.sprite))
                car.designated_label.setScaledContents(True)
                self.lbl_cars.append(car.designated_label)
            else:
                # Should never be reached... Still, just to be safe...
                print("There was an error somewhere")
                car.mark_removal = True

        lbl_log_alive = False
        for lbl_log in self.lbl_logs.copy():
            for log in logs:
                if lbl_log == log.designated_label:
                    lbl_log_alive = True
                    break
            if not lbl_log_alive:
                lbl_log.hide()
                self.lbl_logs_empty.append(lbl_log)
                self.lbl_logs.remove(lbl_log)
        for log in logs:
            if log.designated_label in self.lbl_logs:
                log.designated_label.move(log.x, log.y)
                log.designated_label.show()
            elif log.designated_label == None:
                if len(self.lbl_logs_empty) > 0:
                    log.designated_label = self.lbl_logs_empty.pop()
                    self.lbl_logs.append(log.designated_label)
                    log.designated_label.move(log.x, log.y)
                    break
                log.designated_label = QLabel(self)
                log.designated_label.setGeometry(log.x, log.y, 100, 40)
                log.designated_label.setPixmap(QPixmap("sprites/Mapa/elementos/tronco.png"))
                log.designated_label.setScaledContents(True)
                self.lbl_logs.append(log.designated_label)
            else:
                # Should never be reached... Still, just to be safe...
                print("There was an error somewhere")
                car.mark_removal = True

        lbl_obj_alive = False
        for lbl_obj in self.lbl_objects.copy():
            for obj in objects:
                if lbl_obj == obj.designated_label:
                    lbl_obj_alive = True
                    break
            if not lbl_obj_alive:
                lbl_obj.hide()
                self.lbl_objects_empty.append(lbl_obj)
                self.lbl_objects.remove(lbl_obj)
        for obj in objects:
            if obj.designated_label in self.lbl_objects:
                obj.designated_label.move(obj.x, obj.y)
                obj.designated_label.show()
            elif obj.designated_label == None:
                if len(self.lbl_objects_empty) > 0:
                    obj.designated_label = self.lbl_objects_empty.pop()
                    self.lbl_logs.append(obj.designated_label)
                    obj.designated_label.move(obj.x, obj.y)
                    obj.designated_label.setPixmap(QPixmap("sprites/Mapa/Objetos/" + ["Corazon.png", "Moneda.png",
                                                                                      "Calavera.png",
                                                                                      "Relog.png"][obj.type]))
                    break
                obj.designated_label = QLabel(self)
                obj.designated_label.setGeometry(obj.x, obj.y, 100, 40)
                obj.designated_label.setPixmap(QPixmap("sprites/Mapa/Objetos/" + ["Corazon.png", "Moneda.png",
                                                                                  "Calavera.png",
                                                                                  "Relog.png"][obj.type]))
                obj.designated_label.setScaledContents(True)
                self.lbl_objects.append(obj.designated_label)
            else:
                # Should never be reached... Still, just to be safe...
                print("There was an error somewhere")
                car.mark_removal = True

    def keyPressEvent(self, event):
        if event.text() == 'w':
            self.sgn_move.emit(0)
        elif event.text() == 'a':
            self.sgn_move.emit(1)
        elif event.text() == 's':
            self.sgn_move.emit(2)
        elif event.text() == 'd':
            self.sgn_move.emit(3)
        elif event.text() == 'v':
            self.sgn_move.emit(4)

    def update_player(self, x, y):
        self.obj_froggy.move(x, y)