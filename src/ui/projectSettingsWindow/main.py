import ctypes

from PyQt5 import QtWidgets

from src.ui.projectSettingsWindow.settingsWindow import SettingsWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        user32 = ctypes.windll.user32
        self.screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        self.init_widget()
        self.init_window_geometry()

    def init_window_geometry(self):
        self.setGeometry(self.screensize[0]/2.5, self.screensize[1]/3, 0, 0)
        self.setWindowTitle("Project Settings")

    def init_widget(self):
        a = SettingsWindow(self)
        self.setCentralWidget(a)

