from PyQt5.QtCore import pyqtSignal, QObject


class MainMenuBackend(QObject):
    sgn_login_response = pyqtSignal()
    sgn_error = pyqtSignal(str)

    sgn_hide_mainmenu = pyqtSignal()
    sgn_show_lobby = pyqtSignal(dict)

    sgn_reconnect = pyqtSignal()

    sgn_hide_all = pyqtSignal()

    server_connection = None

    def check_server_status(self, check_state):
        if check_state == 0:  # Every 2 seconds
            self.server_connection.send_text("PING")
        if not self.server_connection.alive:
            if self.server_connection.death_type == 0:
                self.sgn_error.emit("This should not have happened... Local host error")
            elif self.server_connection.death_type == 1:
                self.sgn_error.emit(
                    "Error al conectarse al servidor... \nIntentalo de nuevo más tarde")
            self.sgn_hide_all.emit()

    def click_login(self, username: str, birthday: str):
        username = username.replace('\n', '')
        birthday = birthday.replace('\n', '')
        self.server_connection.send_text(f"LOGIN\n{username}\n{birthday}")
        print("SENT USERNAME QUESTION", self.server_connection.alive)
        response = self.server_connection.receive()
        print("GOT RESPONSE", self.server_connection.alive)
        print("RESPONSE", response)
        if response:
            response = response.split("\n")
        else:
            return
        print("r:", self.server_connection.alive, response)
        if len(response) == 3 and response[0] == "CLIENT":
            if response[1] == "USERNAME":
                if response[2] == "ACCEPTED":
                    users = self.server_connection.receive().split("\n")
                    users_dict = {}
                    if len(users) >= 2:
                        i = 2
                        while i < len(users):
                            users_dict[int(users[i])] = [users[i + 1], users[i + 2]]
                            i += 3
                    self.sgn_hide_mainmenu.emit()
                    self.sgn_show_lobby.emit(users_dict)
                elif response[2] == "INUSE":
                    print("Username in use")
                    self.sgn_error.emit("Username already in use!")
                elif response[2] == "NOTVALID":
                    self.sgn_error.emit("Username is not valid!")
            elif response[1] == "BIRTHDAYERROR":
                self.sgn_error.emit(response[2])
            elif response[1] == "LOBBYFULL":
                print("The lobby is full!")
                self.sgn_error.emit(response[2])
                # self.server_connection.close()
                # self.sgn_reconnect.emit()
                print("SHOWED MESSAGE")
        else:
            self.sgn_error.emit("Unexpected error when logging in... Try again later!")
