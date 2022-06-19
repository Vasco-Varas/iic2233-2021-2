from PyQt5.QtCore import pyqtSignal, QObject
from threading import Thread


class LobbyBackend(QObject):
    sgn_show_lobby = pyqtSignal()
    sgn_update_users = pyqtSignal(dict)
    sgn_show_invitation = pyqtSignal(str, str)
    sgn_start_game = pyqtSignal(str, str, str, str)
    sgn_hide_lobby = pyqtSignal()

    server_connection = None

    users = None

    def show_lobby(self, users):
        self.users = users
        self.sgn_update_users.emit(users)
        self.sgn_show_lobby.emit()

        self.keep_alive = True

        Thread(target=self.keep_listening, daemon=True).start()

    def invite(self, uuid):
        self.server_connection.send_text(f"RETO\nINICIO\n{uuid}")

    def invitation_response(self, resp: str, uuid: str):
        print(f"The invitation by {uuid} was {resp.lower()}")

        self.server_connection.send_text(f"RETO\n{resp}\n{uuid}")

    def keep_listening(self):
        print("LOBBY STARTED LISTENING")
        while self.keep_alive:
            cmd = self.server_connection.receive().split("\n")
            print("RECIEVED", cmd)
            if len(cmd) == 5 and cmd[0] == "USER" and cmd[1] == "NEW":
                self.users[int(cmd[2])] = [cmd[3], cmd[4]]
            elif len(cmd) == 3 and cmd[0] == "CLIENTS" and cmd[1] == "DISCONNECT":
                self.users.pop(int(cmd[2]))
            elif len(cmd) == 4 and cmd[0] == "RETO" and cmd[1] == "INVITACION":
                self.sgn_show_invitation.emit(cmd[2], cmd[3])
            elif len(cmd) == 6 and cmd[0] == "GAME" and cmd[1] == "START":
                self.sgn_hide_lobby.emit()
                self.sgn_start_game.emit(cmd[2], cmd[3], cmd[4], cmd[5])
                self.keep_alive = False
            self.sgn_update_users.emit(self.users)
