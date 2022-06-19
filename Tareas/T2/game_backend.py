from PyQt5.QtCore import pyqtSignal, QObject, QTimer, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton
import parametros as p
from obstacles import Car, Log
from object import SpecialObject
import random


class GameBackend(QObject):
    sgn_open_window = pyqtSignal()
    sgn_close_window = pyqtSignal()
    sgn_open_menu = pyqtSignal()
    sgn_update_values = pyqtSignal(int, int, int, int, int)
    sgn_update_obstacles = pyqtSignal(list, list, list)
    sgn_update_player = pyqtSignal(int,int)
    sgn_show_statistics = pyqtSignal(int, int, int, int, int)

    def __init__(self):
        super(GameBackend, self).__init__()
        self.game_lives = p.VIDAS_INICIO
        self.game_remaining_time = p.DURACION_RONDA_INICIAL
        self.game_duration = p.DURACION_RONDA_INICIAL
        self.game_coins = 0
        self.game_lvl = 1
        self.game_score = 0

        self.hidden_speed_cars = p.VELOCIDAD_AUTOS
        self.hidden_speed_logs = p.VELOCIDAD_TRONCOS

    def re_start_game(self):
        self.game_lives = p.VIDAS_INICIO
        self.game_remaining_time = p.DURACION_RONDA_INICIAL
        self.game_duration = p.DURACION_RONDA_INICIAL
        self.game_coins = 0
        self.game_lvl = 1
        self.game_score = 0

        self.hidden_speed_cars = p.VELOCIDAD_AUTOS
        self.hidden_speed_logs = p.VELOCIDAD_TRONCOS

    def start_game(self):
        self.player_x = 380
        self.player_y = 640
        self.player_last_dir = 0
        self.lvl_score = 0

        self.cars = []
        self.logs = []
        self.special_objects = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_tick)
        self.timer.start(1000)

        self.timer_obstacle_update = QTimer()
        self.timer_obstacle_update.timeout.connect(self.obstacle_update_tick)
        self.timer_obstacle_update.start(50)  # 20 tps

        self.timer_car_spawn = QTimer()
        self.timer_car_spawn.timeout.connect(self.car_spawn)
        self.timer_car_spawn.start(p.TIEMPO_AUTOS)

        self.timer_log_spawn = QTimer()
        self.timer_log_spawn.timeout.connect(self.log_spawn)
        self.timer_log_spawn.start(p.TIEMPO_TRONCOS)

        self.timer_special_spawn = QTimer()
        self.timer_special_spawn.timeout.connect(self.special_spawn)
        self.timer_special_spawn.start(1000*p.TIEMPO_OBJETOS)

        self.send_update()

        self.sgn_update_player.emit(self.player_x, self.player_y)

        self.sgn_open_window.emit()

    def timer_tick(self):
        self.game_remaining_time -= 1
        self.send_update()

    def special_spawn(self):
        self.special_objects.append(SpecialObject(random.randint(0, 3), random.randint(0, 820), random.randint(0, 680)))

    def car_spawn(self):
        self.cars.append(Car(1, self.hidden_speed_cars, 0, 100))
        self.cars.append(Car(-1, self.hidden_speed_cars, 200, 150))
        self.cars.append(Car(-1, self.hidden_speed_cars, 400, 200))

        self.cars.append(Car(-1, self.hidden_speed_cars, 500, 300))
        self.cars.append(Car(1, self.hidden_speed_cars, 700, 350))
        self.cars.append(Car(-1, self.hidden_speed_cars, 300, 400))

    def log_spawn(self):
        self.logs.append(Log(-1, self.hidden_speed_logs, 350, 530))
        self.logs.append(Log(1, self.hidden_speed_logs, 150, 580))
        self.logs.append(Log(-1, self.hidden_speed_logs, 550, 630))

    def obstacle_update_tick(self):
        for car in self.cars.copy():
            if car.mark_removal:
                self.cars.remove(car)
            elif car.x > 861 and car.direc == 1:
                self.cars.remove(car)
            elif car.x < -100 and car.direc == -1:
                self.cars.remove(car)
            else:
                if (self.player_y) <= car.y+40-40 and (self.player_y+80) >= car.y+40 and self.player_x+80 > car.x+30 and self.player_x < car.x+70:
                    self.player_death()
            car.tick()

        player_in_water = False
        player_in_log = False
        for log in self.logs.copy():
            if log.mark_removal:
                self.logs.remove(log)
            elif log.x > 861 and log.direc == 1:
                self.logs.remove(log)
            elif log.x < -100 and log.direc == -1:
                self.logs.remove(log)
            else:
                if (self.player_y) <= log.y+40-40 and (self.player_y+80) >= log.y+20:
                    player_in_water = True
                    if self.player_x+80 > log.x+30 and self.player_x < log.x+70:
                        self.player_x += log.speed * log.direc
                        self.sgn_update_player.emit(self.player_x, self.player_y)
                        player_in_log = True
            log.tick()
        if player_in_water and not player_in_log:
            self.player_death()

        for s in self.special_objects.copy():
            if s.in_collision(self.player_x,self.player_y):
                print("Collected")
                self.special_objects.remove(s)
                if s.type == 0:  # Life
                    self.game_lives += 1
                if s.type == 1:  # Coin
                    self.game_coins += p.CANTIDAD_MONEDAS
                if s.type == 2:  # Skull
                    for log in self.logs:
                        log.speed *= 1.05
                if s.type == 3:  # Clock
                    self.game_remaining_time += 10*(self.game_remaining_time/self.game_duration)


        self.sgn_update_obstacles.emit(self.cars, self.logs, self.special_objects)

    def send_update(self):
        self.sgn_update_values.emit(self.game_lives, self.game_remaining_time,
                                    self.game_coins, self.game_lvl, self.game_score)

    def click_pause(self):
        print("Game paused")

    def click_exit(self):
        self.sgn_close_window.emit()
        self.sgn_open_menu.emit()
        self.re_start_game()

    def move_player(self, dir):
        # w,a,s,d,jump = 0,1,2,3,4
        if dir != 4:
            self.player_last_dir = dir
        if dir == 0:
            self.player_y -= p.VELOCIDAD_CAMINAR
            if len(self.logs) <= 0:
                self.player_death()
        elif dir == 1:
            self.player_x -= p.VELOCIDAD_CAMINAR
        elif dir == 2 and self.player_y < 640:
            self.player_y += p.VELOCIDAD_CAMINAR
        elif dir == 3:
            self.player_x += p.VELOCIDAD_CAMINAR
        elif dir == 4:
            if self.player_last_dir == 0:
                self.player_y -= p.PIXELES_SALTO
            elif self.player_last_dir == 1:
                self.player_x -= p.PIXELES_SALTO
            elif self.player_last_dir == 2:
                self.player_y += p.PIXELES_SALTO
            elif self.player_last_dir == 3:
                self.player_x += p.PIXELES_SALTO

        if self.player_x < 0:
            self.player_x = 0
        if self.player_x > 780:
            self.player_x = 780

        if self.player_y <= 60:
            self.player_x = 380
            self.player_y = 640
            self.player_last_dir = 0
            self.cars = []
            self.logs = []

            self.sgn_show_statistics.emit(self.game_lvl, self.game_score,
                                          self.lvl_score, self.game_lives, self.game_coins)
            self.game_lvl += 1

            self.sgn_close_window.emit()
        self.sgn_update_player.emit(self.player_x, self.player_y)

    def player_death(self):
        self.game_lives -= 1
        self.player_x = 380
        self.player_y = 640
        self.player_last_dir = 0
        self.sgn_update_player.emit(self.player_x, self.player_y)

        if self.game_lives <= 0:
            self.sgn_close_window.emit()
            self.sgn_show_statistics.emit(self.game_lvl, self.game_score,
                                          self.lvl_score, self.game_lives, self.game_coins)
