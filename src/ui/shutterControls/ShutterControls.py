import time

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton

from src.ui.commons.layout import set_hbox
from src.utils.Shutter_Tests import shutter_control
from src.business.consoleThreadOutput import ConsoleThreadOutput


class ShutterControls(QtWidgets.QWidget):
    def __init__(self):
        super(ShutterControls, self).__init__()

        self.console = ConsoleThreadOutput()

        self.openaction = QPushButton('Open Shutter', self)
        self.openaction.clicked.connect(self.run_true)

        self.closeaction = QPushButton('Close Shutter', self)
        self.closeaction.clicked.connect(self.run_false)

        self.setLayout(set_hbox(self.openaction, self.closeaction))

    def run_true(self):
        self.console.raise_text("Opening Shutter...", 2)
        time.sleep(1)
        if shutter_control(True) == "An Error Occured...":
            self.console.raise_text("An Error Occured...", 3)
            time.sleep(1)

    def run_false(self):
        self.console.raise_text("Closing Shutter...", 2)
        time.sleep(1)
        if shutter_control(False) == "An Error Occured...":
            self.console.raise_text("An Error Occured...", 3)
            time.sleep(1)
