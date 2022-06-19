# imports
import sys

from PyQt5.QtWidgets import QApplication

from menu_frontend import MenuFrontend
from menu_backend import MenuBackend
from error_frontend import ErrorFrontend
from game_frontend import GameFrontend
from game_backend import GameBackend
from statistics_frontend import StatisticsFrontend


def hook(type, value, traceback):
    print(type)
    print(traceback)


sys.__excepthook__ = hook

app = QApplication(sys.argv)

# Menu
menu_front = MenuFrontend()
menu_back = MenuBackend()

# Error
error_front = ErrorFrontend()

# Game

game_front = GameFrontend()
game_back = GameBackend()

# Statistics

statistics_front = StatisticsFrontend()


menu_front.sgn_start.connect(menu_back.click_start)
menu_front.sgn_ranking.connect(menu_back.click_ranking)

menu_back.sgn_open_error.connect(error_front.show_error)
menu_back.sgn_close_menu.connect(menu_front.hide)
menu_back.sgn_open_game.connect(game_back.start_game)

game_front.sgn_pause.connect(game_back.click_pause)
game_front.sgn_exit.connect(game_back.click_exit)
game_front.sgn_move.connect(game_back.move_player)
game_back.sgn_open_window.connect(game_front.show)
game_back.sgn_update_values.connect(game_front.update_values)
game_back.sgn_update_obstacles.connect(game_front.update_obstacles)
game_back.sgn_update_player.connect(game_front.update_player)
game_back.sgn_close_window.connect(game_front.hide)
game_back.sgn_open_menu.connect(menu_front.show)
game_back.sgn_show_statistics.connect(statistics_front.show_stats)

statistics_front.sgn_open_menu.connect(menu_front.show)
statistics_front.sgn_next_lvl.connect(game_back.start_game)
# Game



# Ranking

# Start

menu_front.show()
app.exec_()
