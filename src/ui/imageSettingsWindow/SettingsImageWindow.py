from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QPushButton)

from src.business.configuration.settingsImage import SettingsImage
from src.business.consoleThreadOutput import ConsoleThreadOutput
from src.controller.camera import Camera
from src.controller.commons.Locker import Locker
from src.ui.commons.layout import set_lvbox, set_hbox
from src.utils.camera.SbigDriver import (ccdinfo)


class SettingsImageWindow(QtWidgets.QWidget):
    # Cria os campos e espaços no menu image window
    def __init__(self, parent=None):
        super(SettingsImageWindow, self).__init__(parent)

        # Instance attributes create_image_contrast_group
        self.getlevel1 = None
        self.getlevel1l = None
        self.getlevel2 = None
        self.getlevel2l = None

        # Instance attributes create_crop_group
        self.ignore_crop_l = None
        self.crop_msg = None
        self.crop_xi = None
        self.getcropxi_l = None
        self.crop_xf = None
        self.getcropxf_l = None
        self.crop_yi = None
        self.getcropyi_l = None
        self.crop_yf = None
        self.getcropyf_l = None

        # Instance attributes create_type_image_group
        self.image_png_l = None
        self.image_tif_l = None
        self.image_fit_l = None

        # Instance attributes create_push_button_group
        self.saveButton = None
        self.cancelButton = None
        self.clearButton = None

        self.image_settings = SettingsImage()

        self.camera = Camera()

        self.console = ConsoleThreadOutput()

        self.image_parent = parent

        self.lock = Locker()

        grid = QGridLayout()
        grid.addWidget(self.create_image_contrast_group())
        grid.addWidget(self.create_crop_group())
        grid.addWidget(self.create_type_image_group())
        grid.addWidget(self.create_push_button_group())
        self.setLayout(grid)

        self.setWindowTitle("Imager Box")

        self.setting_values()

    def get_image_settings(self):
        settings = SettingsImage()
        info = settings.get_image_settings()
        return info

    def get_pixels(self):
        info = self.get_info_pixels()

        return int(info[-2]), int(info[-1])

    def get_info_pixels(self):
        # Function to get the CCD Info
        # This function will return [Pixels]
        ret = None
        self.lock.set_acquire()
        try:
            ret = tuple(ccdinfo())
        except Exception as e:
            self.console.raise_text("Failed to get camera information.\n{}".format(e))
        finally:
            self.lock.set_release()

        return ret

    def create_image_contrast_group(self):
        group_box = QGroupBox("&Image Contrast:")
        group_box.setCheckable(True)
        group_box.setChecked(True)

        self.getlevel1 = QtWidgets.QLabel("Bottom Level:", self)
        self.getlevel1.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.getlevel1l = QtWidgets.QLineEdit(self)
        self.getlevel1l.setMaximumWidth(50)
        self.getlevel1l.setValidator(QIntValidator(0, 1))

        self.getlevel2 = QtWidgets.QLabel("Top Level:", self)
        self.getlevel2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.getlevel2l = QtWidgets.QLineEdit(self)
        self.getlevel2l.setMaximumWidth(50)
        self.getlevel2l.setValidator(QIntValidator(0, 1))

        group_box.setLayout(set_lvbox(set_hbox(self.getlevel1, self.getlevel1l, self.getlevel2, self.getlevel2l)))

        return group_box

    def create_crop_group(self):
        group_box = QGroupBox("&Crop")
        group_box.setCheckable(True)
        group_box.setChecked(False)

        self.ignore_crop_l = QtWidgets.QCheckBox('Ignore Crop Image', self)

        self.crop_msg = QtWidgets.QLabel("Crop Image", self)
        self.crop_xi = QtWidgets.QLabel("Width: Wi:", self)
        self.crop_xi.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.getcropxi_l = QtWidgets.QLineEdit(self)
        self.getcropxi_l.setMaximumWidth(50)
        self.getcropxi_l.setValidator(QIntValidator(0, 1000))

        self.crop_xf = QtWidgets.QLabel("Wf:", self)
        self.crop_xf.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.getcropxf_l = QtWidgets.QLineEdit(self)
        self.getcropxf_l.setMaximumWidth(50)
        self.getcropxf_l.setValidator(QIntValidator(0, 1000))

        self.crop_yi = QtWidgets.QLabel("Height: Hi:", self)
        self.crop_yi.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.getcropyi_l = QtWidgets.QLineEdit(self)
        self.getcropyi_l.setMaximumWidth(50)
        self.getcropyi_l.setValidator(QIntValidator(0, 1000))

        self.crop_yf = QtWidgets.QLabel("Hf:", self)
        self.crop_yf.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.getcropyf_l = QtWidgets.QLineEdit(self)
        self.getcropyf_l.setMaximumWidth(50)
        self.getcropyf_l.setValidator(QIntValidator(0, 1000))

        group_box.setLayout(set_lvbox(set_hbox(self.ignore_crop_l),
                                      set_hbox(self.crop_msg),
                                      set_hbox(self.crop_xi, self.getcropxi_l, self.crop_xf, self.getcropxf_l),
                                      set_hbox(self.crop_yi, self.getcropyi_l, self.crop_yf, self.getcropyf_l)))

        return group_box

    def create_type_image_group(self):
        group_box = QGroupBox("&File to save")
        group_box.setCheckable(True)
        group_box.setChecked(True)

        self.image_png_l = QtWidgets.QCheckBox('Image .png', self)
        self.image_tif_l = QtWidgets.QCheckBox('Image .tif', self)
        self.image_fit_l = QtWidgets.QCheckBox('Image .fit', self)

        group_box.setLayout(set_lvbox(set_hbox(self.image_png_l),
                                      set_hbox(self.image_tif_l),
                                      set_hbox(self.image_fit_l)))

        return group_box

    def create_push_button_group(self):
        group_box = QGroupBox()
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.button_ok_func)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.func_cancel)

        self.clearButton = QPushButton("Clear")
        self.clearButton.clicked.connect(self.clear_all)

        group_box.setLayout(set_lvbox(set_hbox(self.saveButton, self.clearButton, self.cancelButton)))

        return group_box

    def button_ok_func(self):
        try:
            y_pixels, x_pixels = self.get_pixels()
            """
            ATENCAO
            """
            # Saving the Settings
            # if int(self.getcropxi_l.text()) > int(self.getcropxf_l.text()) or \
            #    int(self.getcropyi_l.text()) > int(self.getcropyf_l.text()) or \
            #    int(self.getcropxf_l.text()) >= x_pixels or \
            #    int(self.getcropyf_l.text()) >= y_pixels:
            #
            #     self.console.raise_text("Wrong values for image crop.", 3)
            #
            # else:
            self.image_settings.set_image_settings(self.getlevel1l.text(), self.getlevel2l.text(),
                                                   self.getcropxi_l.text(), self.getcropxf_l.text(),
                                                   self.getcropyi_l.text(), self.getcropyf_l.text(),
                                                   self.ignore_crop_l.isChecked(),
                                                   self.image_png_l.isChecked(),
                                                   self.image_tif_l.isChecked(),
                                                   self.image_fit_l.isChecked())
            self.image_settings.save_settings()
            self.console.raise_text("Image settings successfully saved!", 1)

        except Exception as e:
            print("Image settings were not saved -> {}".format(e))
            self.console.raise_text("Image settings were not saved.", 3)

    def clear_all(self):
        self.getlevel1l.clear()
        self.getlevel2l.clear()
        self.getcropxi_l.clear()
        self.getcropxf_l.clear()
        self.getcropyi_l.clear()
        self.getcropyf_l.clear()

    def func_cancel(self):
        self.image_parent.close()

    def setting_values(self):
        info = self.get_image_settings()
        self.set_values(info[0], info[1], info[2], info[3], info[4],
                        info[5], info[6], info[7], info[8], info[9])

    def set_values(self, get_level1, get_level2, crop_xi, crop_xf, crop_yi, crop_yf,
                   ignore_crop, image_png, image_tif, image_fit):
        self.getlevel1l.setText(get_level1)
        self.getlevel2l.setText(get_level2)

        self.getcropxi_l.setText(crop_xi)
        self.getcropxf_l.setText(crop_xf)
        self.getcropyi_l.setText(crop_yi)
        self.getcropyf_l.setText(crop_yf)

        self.ignore_crop_l.setChecked(ignore_crop)
        self.image_png_l.setChecked(image_png)
        self.image_tif_l.setChecked(image_tif)
        self.image_fit_l.setChecked(image_fit)
