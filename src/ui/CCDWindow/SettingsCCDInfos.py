import time

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QGridLayout, QGroupBox, QPushButton, QWidget

from src.business.consoleThreadOutput import ConsoleThreadOutput
from src.business.shooters.InfosForSThread import *
from src.business.shooters.SThread import SThread
from src.controller.camera import Camera
from src.controller.commons.Locker import Locker
from src.controller.fan import Fan
from src.ui.commons.layout import set_hbox, set_lvbox
from src.utils.Shutter_Tests import shutter_control
from src.utils.camera.SbigDriver import getlinkstatus


class SettingsCCDInfos(QWidget):
    def __init__(self, parent=None):
        super(SettingsCCDInfos, self).__init__(parent)

        # Instance attributes create_ccd_info_group
        self.p = parent
        self.info_port_ccd_l = None
        self.info_port_ccd_f = None
        self.info_camera_model_l = None
        self.info_camera_model_f = None
        self.info_pixel_array_l = None
        self.info_pixel_array_f = None

        # Instance attributes create_ccd_camera_group
        self.close_open = None
        self.temp_set_point_l = None
        self.temp_set_point_f = None
        self.temp_init_l = None
        self.temp_init_f = None
        self.time_between_photos_l = None
        self.time_between_photos_f = None
        self.one_photoButton = None
        self.tempButton = None
        self.fanButton = None

        # Instance attributes create_push_button_group
        self.saveButton = None
        self.cancelButton = None
        self.clearButton = None

        self.imager_window = parent

        self.cam = Camera()

        self.var_save_ini_camera = SettingsCamera()

        self.console = ConsoleThreadOutput()

        self.fan = Fan(self.fanButton)

        self.one_photo = SThread()

        self.lock = Locker()

        self.firmware = "????"
        self.model = "????"
        self.y_pixels = "????"
        self.x_pixels = "????"

        grid = QGridLayout()
        # Additional Parameters (Apparently Useless) 0, 1 | 1, 1 | 2, 1
        grid.addWidget(self.create_ccd_info_group())
        grid.addWidget(self.create_ccd_camera_group())
        grid.addWidget(self.create_push_button_group())
        self.setLayout(grid)
        self.w = grid.geometry().width()
        self.h = grid.geometry().height()

        self.setWindowTitle("Imager Box")
        # self.resize(500, 340)
        # self.info_cam()

    def create_ccd_info_group(self):
        group_box = QGroupBox("Info CCD")

        '''
        self.info_port_ccd_l = QtWidgets.QLabel("Camera Firmware: ", self)
        self.info_port_ccd_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.info_port_ccd_f = QtWidgets.QLabel(self.firmware)
        self.info_port_ccd_f.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        '''

        self.info_camera_model_l = QtWidgets.QLabel("Camera Model: ", self)
        self.info_camera_model_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.info_camera_model_f = QtWidgets.QLabel(self.model)
        self.info_camera_model_f.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.info_pixel_array_l = QtWidgets.QLabel("Pixel array: ", self)
        self.info_pixel_array_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.info_pixel_array_f = QtWidgets.QLabel(self.x_pixels + " X " + self.y_pixels + " Pixels")
        self.info_pixel_array_f.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        group_box.setLayout(set_lvbox(set_hbox(self.info_camera_model_l, self.info_camera_model_f),
                                      set_hbox(self.info_pixel_array_l, self.info_pixel_array_f)))
        return group_box

    def create_ccd_camera_group(self):
        group_box = QGroupBox("Settings")
        group_box.setCheckable(True)
        group_box.setChecked(False)

        self.shutter_l = QtWidgets.QLabel("Shutter:", self)
        self.shutter_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.close_open = QtWidgets.QLabel()
        self.close_open.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.temp_set_point_l = QtWidgets.QLabel("CCD Temp Set Point (°C):", self)
        self.temp_set_point_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.temp_set_point_f = QtWidgets.QLineEdit(self)
        self.temp_set_point_f.setMaximumWidth(100)
        self.temp_set_point_f.setValidator(QIntValidator(-100, 30))

        self.temp_init_l = QtWidgets.QLabel("CCD Cooling Time(s):", self)
        self.temp_init_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.temp_init_f = QtWidgets.QLineEdit(self)
        self.temp_init_f.setMaximumWidth(100)
        self.temp_init_f.setValidator(QIntValidator(0, 600))

        self.time_between_photos_l = QtWidgets.QLabel("Time Between Dark Images(s):", self)
        self.time_between_photos_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.time_between_photos_f = QtWidgets.QLineEdit(self)
        self.time_between_photos_f.setMaximumWidth(100)
        # self.time_between_photos_f.setValidator(QIntValidator(0, 600))

        self.one_photoButton = QtWidgets.QPushButton('Take Photo', self)
        self.one_photoButton.clicked.connect(self.take_one_photo)

        self.tempButton = QtWidgets.QPushButton("Set Temp", self)
        self.tempButton.clicked.connect(self.btn_temperature)

        self.fanButton = QtWidgets.QPushButton("Fan (On/Off)")
        self.fanButton.clicked.connect(self.button_fan_func)

        self.setting_values()

        group_box.setLayout(set_lvbox(set_hbox(self.shutter_l, self.close_open),
                                      set_hbox(self.temp_set_point_l, self.temp_set_point_f),
                                      set_hbox(self.temp_init_l, self.temp_init_f),
                                      set_hbox(self.time_between_photos_l, self.time_between_photos_f),
                                      set_hbox(self.one_photoButton, self.tempButton, self.fanButton, stretch2=1)))
        return group_box

    def create_push_button_group(self):
        group_box = QGroupBox("&Push Buttons")
        # group_box.setCheckable(True)
        # group_box.setChecked(True)

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.button_ok_func)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.func_cancel)

        self.clearButton = QPushButton("Clear")
        self.clearButton.clicked.connect(self.clear_all)

        group_box.setLayout(set_lvbox(set_hbox(self.saveButton, self.clearButton, self.cancelButton)))

        return group_box

    def get_values(self):
        return self.var_save_ini_camera.get_camera_settings()

    def setting_values(self):
        info = self.get_values()
        self.set_values(info[0], info[5], info[4])

    def set_values(self, temperature_camera, temp_init_f, tbf):
        self.temp_set_point_f.setText(temperature_camera)
        self.temp_init_f.setText(temp_init_f)
        self.time_between_photos_f.setText(tbf)

        srch = shutter_control(None)
        if srch[1] == 1:
            self.close_open.setText("Open")
        elif srch[1] == 2:
            self.close_open.setText("Closed")
        else:
            self.close_open.setText("????")

    def button_ok_func(self):
        try:
            self.var_save_ini_camera.set_camera_settings(self.temp_set_point_f.text(),
                                                         self.temp_init_f.text(),
                                                         self.time_between_photos_f.text())

            self.var_save_ini_camera.save_settings()
            self.console.raise_text("Camera settings successfully saved!", 1)

        except Exception as e:
            print(e)
        finally:
            self.p.close()
            self.clear_all()
            self.setting_values()
            # self.refresh_all_fields()

    def clear_all(self):
        self.temp_set_point_f.clear()
        self.temp_init_f.clear()

    def func_cancel(self):
        self.imager_window.close()

    def take_one_photo(self):
        try:
            if str(self.close_open) == "Closed":
                # self.console.raise_text("take_one_photo started: dark photo", 1)
                # time.sleep(1)
                self.cam.one_photo = True
                print("bbbbbbbbbbbbbbbbbbbbb")
                print(self.cam.one_photo)
                self.cam.start_one_photo()
                # self.one_photo.args_one_photo(self.select_filter_manual, self.select_filter_shutter)
                # self.one_photo.start()
            else:
                # self.console.raise_text("take_one_photo started: photo", 1)
                # time.sleep(1)
                self.cam.one_photo = True
                print("aaaaaaaaaaaaa")
                print(self.cam.one_photo)
                self.cam.start_one_photo()
        except Exception as e:
            self.console.raise_text("Not possible taking photo -> {}".format(e), 1)
        finally:
            self.cam.one_photo = False

    def button_fan_func(self):
        if getlinkstatus() is True:
            try:
                self.fan.set_fan()
                self.console.raise_text('State changed Fan!', 2)
            except Exception as e:
                self.console.raise_text("The camera is not connected!", 3)
                self.console.raise_text('State Fan unchanged', 3)
                self.console.raise_text("Exception -> {}".format(e))
        else:
            self.console.raise_text("The camera is not connected!", 3)
            self.console.raise_text('State Fan unchanged', 3)

    def btn_temperature(self):
        try:
            value = self.temp_set_point_f.text()
            if value is '':
                pass
            else:
                try:
                    self.cam.set_temperature(float(value))
                except TypeError:
                    self.cam.set_temperature(float(15.0))
        except Exception as e:
            print("Exception -> {}".format(e))

    def info_cam(self):
        # self.firmware,
        try:
            if self.cam.is_connected:
                self.model = self.cam.get_firmware_and_model_and_pixels()[1]
                self.x_pixels, self.y_pixels = self.cam.pass_list_str
                # self.model, self.x_pixels, self.y_pixels = self.cam.get_model_and_pixels_new()
                placeholder = None
            else:
                self.model, self.x_pixels, self.y_pixels = "????", "????", "????"

            # self.info_port_ccd_f.setText(self.firmware)
            self.info_camera_model_f.setText(self.model)
            self.info_pixel_array_f.setText(str(self.y_pixels) + " x " + str(self.x_pixels))
            placeholder = None

        except Exception as e:
            print("CCDInfos get_firmware_and_model_and_pixels -> {}".format(e))
            self.model, self.x_pixels, self.y_pixels = "????", "????", "????"
