from PyQt5 import QtWidgets

from src.ui.systemSettingsWindow.systemSettingsWindow import SystemSettingsWindow

import ctypes


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        user32 = ctypes.windll.user32
        self.screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        self.init_widget()
        self.init_window_geometry()


    def init_window_geometry(self):
        self.setGeometry(self.screensize[0]/2.5, self.screensize[1]/2.5, 0, 0)
        self.setWindowTitle("System Settings")

    def init_widget(self):
        a = SystemSettingsWindow(self)
        self.setCentralWidget(a)