from PyQt5 import QtCore

from src.business.configuration.constants import camera as c


class SettingsImage:
    def __init__(self):
        self._settings = QtCore.QSettings()
        self.setup_settings()

    def setup_settings(self):
        self._settings = QtCore.QSettings(c.FILENAME, QtCore.QSettings.IniFormat)
        self._settings.setFallbacksEnabled(False)

    def save_settings(self):
        self._settings.sync()

    # image_png,
    def set_image_settings(self, get_level1, get_level2, crop_xi, crop_xf, crop_yi, crop_yf,
                           ignore_crop, image_tif, image_fit):
        """
        :param get_level1:
        :param get_level2:
        :param crop_xi:
        :param crop_xf:
        :param crop_yi:
        :param crop_yf:
        :param ignore_crop:
        :param image_png:
        :param image_tif:
        :param image_fit:
        :return:
        """
        self._settings.setValue(c.GET_LEVEL1, get_level1)
        self._settings.setValue(c.GET_LEVEL2, get_level2)
        self._settings.setValue(c.CROP_X_AXIS_XI, crop_xi)
        self._settings.setValue(c.CROP_X_AXIS_XF, crop_xf)
        self._settings.setValue(c.CROP_Y_AXIS_YI, crop_yi)
        self._settings.setValue(c.CROP_Y_AXIS_YF, crop_yf)
        self._settings.setValue(c.CHEBOX_IGNORE_CROP, ignore_crop)
        # self._settings.setValue(c.CHEBOX_IMAGE_PNG, image_png)
        self._settings.setValue(c.CHEBOX_IMAGE_TIF, image_tif)
        self._settings.setValue(c.CHEBOX_IMAGE_FIT, image_fit)

    # self._settings.value(c.CHEBOX_IMAGE_PNG, True, type=bool), \
    def get_image_settings(self):
        return self._settings.value(c.GET_LEVEL1), \
               self._settings.value(c.GET_LEVEL2), \
               self._settings.value(c.CROP_X_AXIS_XI), \
               self._settings.value(c.CROP_X_AXIS_XF), \
               self._settings.value(c.CROP_Y_AXIS_YI), \
               self._settings.value(c.CROP_Y_AXIS_YF), \
               self._settings.value(c.CHEBOX_IGNORE_CROP, True, type=bool), \
               self._settings.value(c.CHEBOX_IMAGE_TIF, True, type=bool), \
               self._settings.value(c.CHEBOX_IMAGE_FIT, True, type=bool)

    def get_filepath(self):
        return self._settings.value(c.FILENAME)
