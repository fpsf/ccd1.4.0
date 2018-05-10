import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from src.ui.CCDWindow.SettingsCCDInfos import SettingsCCDInfos


class Main(QtWidgets.QMainWindow):
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

        self.ima = SettingsCCDInfos(self)

        self.setCentralWidget(self.ima)

        self.setWindowTitle("Imager Settings")

        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        self.init_window_geometry()

    def init_window_geometry(self):
        self.setGeometry(self.screensize[0]/2.5, self.screensize[1]/2.5, 0, 0)

    def show_camera_infos(self):
        try:
            self.ima.info_cam()
        except Exception as e:
            print("show_camera_infos on menu -> {}".format(e))

