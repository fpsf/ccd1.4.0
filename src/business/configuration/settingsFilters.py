from PyQt5 import QtCore

from src.business.configuration.constants import camera as c


class SettingsFilters:
    def __init__(self):
        self._settings = QtCore.QSettings()
        self.setup_settings()

    def setup_settings(self):
        self._settings = QtCore.QSettings(c.FILENAME, QtCore.QSettings.IniFormat)
        self._settings.setFallbacksEnabled(False)

    def save_settings(self):
        self._settings.sync()

    def set_filters_settings(self,
                             label_filter1, wavelength_filter1, exposure_filter1, binning_filter1):

        self._settings.setValue(c.PREFIXO, label_filter1)
        self._settings.setValue(c.WAVELENGTH_FILTER1, wavelength_filter1)
        self._settings.setValue(c.EXPOSICAO, exposure_filter1)
        self._settings.setValue(c.BINNING, binning_filter1)

    def get_filters_settings(self):
        return self._settings.value(c.PREFIXO), \
               self._settings.value(c.WAVELENGTH_FILTER1), \
               self._settings.value(c.EXPOSICAO), \
               self._settings.value(c.BINNING), \


    def get_filepath(self):
        return self._settings.value(c.FILENAME)
