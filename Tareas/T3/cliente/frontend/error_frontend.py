from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5 import uic


class ErrorFrontend(QMainWindow):
    def __init__(self, resources):
        super(ErrorFrontend, self).__init__()

        uic.loadUi(f"{resources}/errordialog.ui", self)

        # Widgets
        self.lbl_error = self.findChild(QLabel, "lbl_error")

    def show_error(self, msg):
        self.lbl_error.setText(msg)
        self.show()
