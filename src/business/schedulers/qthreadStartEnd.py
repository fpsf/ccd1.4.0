import time

from PyQt5 import QtCore

from src.ui.mainWindow.StartEndTimeInfo import result


class QThreadStartEnd(QtCore.QThread):
    values_start_end = QtCore.pyqtSignal(tuple)

    def __init__(self):
        super(QThreadStartEnd, self).__init__()

    def run(self):
        while True:
            time.sleep(1)
            info_start_end = result()

            self.values_start_end.emit(info_start_end)
