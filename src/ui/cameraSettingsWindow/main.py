from PyQt5 import QtWidgets

from src.ui.cameraSettingsWindow.settingsWindow import SettingsWindow

import ctypes

class Main(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        user32 = ctypes.windll.user32
        self.screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        self.a = SettingsWindow(self)
        self.setGeometry(self.screensize[0]/2.5, self.screensize[1]/3, 0, 0)
        self.setCentralWidget(self.a)

        self.setWindowTitle("Camera Settings")
