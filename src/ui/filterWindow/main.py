import ctypes

from PyQt5 import QtWidgets

from src.ui.filterWindow.filterWindow import FilterWindow


class Main(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        user32 = ctypes.windll.user32
        self.screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

        self.f = FilterWindow(self)
        self.setCentralWidget(self.f)

        self.setWindowTitle("Filters Settings")
        self.init_window_geometry()

    def init_window_geometry(self):
        self.setGeometry(self.screensize[0]/2.5, self.screensize[1]/2.5, 0, 0)
