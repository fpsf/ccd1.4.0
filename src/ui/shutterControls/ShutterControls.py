import time

import serial
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton

from src.ui.commons.layout import set_hbox
from src.utils.Leitura_portas import serial_ports


class ShutterControls(QtWidgets.QWidget):
    def __init__(self):
        super(ShutterControls, self).__init__()

        self.openaction = QPushButton('Open Shutter', self)
        self.openaction.clicked.connect(self.run_true)

        self.closeaction = QPushButton('Close Shutter', self)
        self.closeaction.clicked.connect(self.run_false)

        self.setLayout(set_hbox(self.openaction, self.closeaction))

    def run_true(self):
        self.shutter_control(True)

    def run_false(self):
        self.shutter_control(False)

    def shutter_control(self, cont):
        if len(serial_ports()) < 1:
            self.console.raise_text("No Serial Equipment!", 3)
            time.sleep(1)
        else:
            ser = serial.Serial(serial_ports()[len(serial_ports()) - 1], 9600,
                                bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE)
            if cont is True:
                self.console.raise_text("Opening Shutter", 1)
                time.sleep(1)
                send = bytes([235, 144, 86, 1, 46])
                ser.write(send)
                # time.sleep(15)
            else:
                self.console.raise_text("Closing Shutter", 1)
                time.sleep(1)
                send = bytes([235, 144, 214, 1, 174])
                ser.write(send)
                # time.sleep(15)
            '''
            except Exception:
                self.console.raise_text("No Serial Equipment!", 3)
            '''
