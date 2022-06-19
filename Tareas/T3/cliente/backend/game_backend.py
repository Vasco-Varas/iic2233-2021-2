from PyQt5.QtCore import pyqtSignal, QObject
from threading import Thread


class GameBackend(QObject):
    sgn_show_game = pyqtSignal(str, str, str)
    sgn_update_marbles = pyqtSignal(str, str, str)
    sgn_update_info = pyqtSignal(str, str, int)
    sgn_update_turn = pyqtSignal(bool)
    sgn_show_error = pyqtSignal(str)
    sgn_show_oponent_bet = pyqtSignal(str, str)
    sgn_delayer_start = pyqtSignal(int)
    sgn_show_win = pyqtSignal(str, str)
    sgn_hide_game = pyqtSignal()

    sgn_timers_set_val = pyqtSignal(int, int)
    sgn_timers_set_max = pyqtSignal(int, int)

    server_connection = None

    def __init__(self, *args, **kwargs):
        super(GameBackend, self).__init__(*args, **kwargs)

        self.infodelayer_locked = False
        self.infodelayer_next_info = None
        self.your_id = None
        self.keep_alive = True

    def start_game(self, player_id, player1_name, player2_name, starting_marbles):
        self.your_id = player_id
        self.update_marbles(starting_marbles, starting_marbles)
        self.update_info("Esperando a los jugadores...", "", 0)
        self.show_game(player1_name, player2_name)
        Thread(target=self.keep_listening, daemon=True).start()
        self.server_connection.send_text("GAME\nSET_READY")

    def show_game(self, p1_name, p2_name):
        self.sgn_show_game.emit(p1_name, p2_name, self.your_id)

    def update_marbles(self, p1, p2):
        self.sgn_update_marbles.emit(p1, p2, self.your_id)

    def delayer_stop(self):
        self.infodelayer_locked = False
        print("GET NEW DELAYER INPUT")
        if self.infodelayer_next_info:
            print("NEW INFO FOUND", self.infodelayer_next_info)
            self.update_info(self.infodelayer_next_info[0], self.infodelayer_next_info[1],
                             self.infodelayer_next_info[2])
        self.infodelayer_next_info = None

    def update_info(self, l1, l2, icon):
        if self.infodelayer_locked:
            print("Delayer locked")
            self.infodelayer_next_info = (l1, l2, icon)
        else:
            print("Delayer not locked")
            self.sgn_update_info.emit(l1, l2, icon)

    def update_turn(self, my_turn: bool):
        self.sgn_update_turn.emit(my_turn)

    def click_ready(self, is_even, bet_value):
        even = "TRUE" if is_even else "FALSE"
        self.server_connection.send_text(f"GAME\nSETBET\n{even}\n{bet_value}")

    def keep_listening(self):
        print("GAME STARTED LISTENING")
        while self.keep_alive:
            cmd = self.server_connection.receive().split("\n")
            print(f"GOT {cmd}")
            if len(cmd) == 5 and cmd[0] == "GAME" and cmd[1] == "SETINFO":
                self.update_info(cmd[2], cmd[3], int(cmd[4]))
            elif len(cmd) == 6 and cmd[0] == "GAME" and cmd[1] == "SETINFOPROTECT":
                self.sgn_update_info.emit(cmd[2], cmd[3], int(cmd[4]))
                self.infodelayer_locked = True
                self.sgn_delayer_start.emit(int(cmd[5]))
                self.update_info(cmd[2], cmd[3], int(cmd[4]))
            elif len(cmd) == 4 and cmd[0] == "GAME" and cmd[1] == "SETMARBLES":
                self.update_marbles(cmd[2], cmd[3])
            elif len(cmd) == 4 and cmd[0] == "GAME" and cmd[1] == "SETSELFTURN":
                my_turn = cmd[2] == "TRUE"
                self.update_turn(my_turn)
                if my_turn:
                    self.sgn_timers_set_val.emit(int(cmd[3]), 0)
                    self.sgn_timers_set_max.emit(int(cmd[3]), 100)
                else:
                    self.sgn_timers_set_val.emit(0, int(cmd[3]))
                    self.sgn_timers_set_max.emit(100, int(cmd[3]))
            elif len(cmd) == 3 and cmd[0] == "GAME" and cmd[1] == "SHOWERROR":
                self.sgn_show_error.emit(cmd[2])
            elif len(cmd) == 4 and cmd[0] == "GAME" and cmd[1] == "CHEATCODE":
                if cmd[2] == "FA":
                    self.sgn_show_error.emit(f"Tu oponente aposto {cmd[3]} canicas")
            elif len(cmd) == 4 and cmd[0] == "GAME" and cmd[1] == "OPONENTBET":
                self.sgn_show_oponent_bet.emit(cmd[2], cmd[3])
            elif len(cmd) == 4 and cmd[0] == "GAME" and cmd[1] == "END":
                self.sgn_hide_game.emit()
                self.sgn_show_win.emit(cmd[2], cmd[3])

    def cheatcode_fa(self):
        self.server_connection.send_text("GAME\nCHEATCODE\nFA")
        print("SENT! FA")

    def cheatcode_zx(self):
        self.server_connection.send_text("GAME\nCHEATCODE\nZX")
        print("SENT! XZ")
