from PyQt5 import QtWidgets, QtCore

from src.business.schedulers.SchedTemperature import SchedTemperature
from src.ui.commons.layout import set_hbox, set_lvbox
from src.ui.commons.widgets import get_qfont


class TempMonitor(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(TempMonitor, self).__init__(parent)
        self.tempMonitor = QtWidgets.QLabel(self)
        self.Sched = SchedTemperature(self.tempMonitor)
        """
        self.title = QtWidgets.QLabel("CCD Information", self)
        set_hbox(self.title),
        """
        self.title = QtWidgets.QLabel("CCD Information", self)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setFont(get_qfont(True))
        self.label = QtWidgets.QLabel("Temperature:                        ", self)
        # , stretch=1
        self.setLayout(set_lvbox(set_hbox(self.title), set_hbox(self.label, self.tempMonitor)))

    def stop_monitor(self):
        self.Sched.stop_job()

    def start_monitor(self):
        self.Sched.start_job()
