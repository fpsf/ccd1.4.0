import sys
from PyQt5.QtWidgets import QMainWindow
# from PyQt5 import QtWidgets

from src.ui.allSettingsWindow.AllSettingsWindow import AllSettingsWindow


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        if sys.platform.startswith("win"):
            import ctypes
            user32 = ctypes.windll.user32
            self.screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        else:
            import subprocess
            output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
            self.screensize = output.split()[0].split(b'x')
            self.screensize[0] = str(self.screensize[0], "utf-8")
            self.screensize[1] = str(self.screensize[1], "utf-8")
            self.screensize[0] = int(self.screensize[0])
            self.screensize[1] = int(self.screensize[1])

        self.all = AllSettingsWindow()
        self.setCentralWidget(self.all)
        self.setWindowTitle("Settings")
        self.init_window_geometry()

    def init_window_geometry(self):
        self.setGeometry(self.screensize[0] / 2.5, self.screensize[1] / 2.5, 0, 0)