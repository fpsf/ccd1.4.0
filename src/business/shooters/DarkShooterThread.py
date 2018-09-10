import time

from PyQt5 import QtCore

from src.business.consoleThreadOutput import ConsoleThreadOutput
from src.business.shooters.SThread import SThread
from src.business.configuration.settingsCamera import SettingsCamera


class DarkShooterThread(QtCore.QThread):

    def __init__(self, timeSleep):
        self.continuous = None
        super(DarkShooterThread, self).__init__()
        self.console = ConsoleThreadOutput()
        self.s = timeSleep
        self.ss = SThread()
        self.settings = SettingsCamera()

    def run(self):
        self.s = int(self.settings.get_camera_settings()[4])
        while self.continuous:
            time.sleep(self.s)
            if self.continuous:
                self.console.raise_text("Taking dark photo", 1)
                self.ss.take_dark()
