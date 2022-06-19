from PyQt5.QtCore import pyqtSignal, QObject


class InvitationBackend(QObject):
    sgn_show_lobby = pyqtSignal()
    sgn_update_users = pyqtSignal(dict)
    server_connection = None

    users = None

    def show_lobby(self, users):
        self.users = users
        self.sgn_update_users.emit(users)
        self.sgn_show_lobby.emit()

