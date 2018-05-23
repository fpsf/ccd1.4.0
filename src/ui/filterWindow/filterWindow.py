from PyQt5 import QtWidgets
from PyQt5.QtGui import QIntValidator

from src.business.consoleThreadOutput import ConsoleThreadOutput
from src.business.configuration.settingsFilters import SettingsFilters
from src.ui.commons.layout import set_lvbox, set_hbox


class FilterWindow(QtWidgets.QWidget):
    # Cria os campos e espaços no menu filter window

    def __init__(self, parent=None):
        super(FilterWindow, self).__init__(parent)

        self.setField_label_label = None
        self.setField_wavelength_label = None
        self.setField_exposure_label = None
        self.setField_binning_label = None

        self.setField_1 = None

        self.setField_label_filter1 = None
        self.setField_wavelength_filter1 = None
        self.setField_exposure_filter1 = None
        self.setField_binning_filter1 = None

        self.button_ok = None
        self.button_clear = None
        self.button_cancel = None

        self.create_filters_widgets()
        self.var_save_ini_filters = SettingsFilters()
        self.f = parent

        self.console = ConsoleThreadOutput()

        self.setting_values()
        self.setLayout(set_lvbox(set_hbox(self.setField_label_label,
                                          self.setField_wavelength_label,
                                          self.setField_exposure_label,
                                          self.setField_binning_label),
                                 set_hbox(self.setField_1, self.setField_label_filter1,
                                          self.setField_wavelength_filter1,
                                          self.setField_exposure_filter1,
                                          self.setField_binning_filter1),
                                 set_hbox(self.button_ok, self.button_clear, self.button_cancel, stretch2=1)))

    def get_values(self):
        return self.var_save_ini_filters.get_filters_settings()

    def setting_values(self):
        info = self.get_values()
        self.set_values(info[0], info[1], info[2], info[3])

    def set_values(self,
                   label_filter1, wavelength_filter1, exposure_filter1, binning_filter1):

        binning_var1 = self.error_binning(binning_filter1)

        self.setField_label_filter1.setText(label_filter1)
        self.setField_wavelength_filter1.setText(wavelength_filter1)
        self.setField_exposure_filter1.setText(exposure_filter1)
        self.setField_exposure_filter1.setValidator(QIntValidator(0, 360))
        self.setField_binning_filter1.setCurrentIndex(binning_var1)

    def create_filters_widgets(self):
        self.setField_label_label = QtWidgets.QLabel("    Filter Label", self)
        self.setField_wavelength_label = QtWidgets.QLabel("          Wavelength (nm)", self)
        self.setField_exposure_label = QtWidgets.QLabel("                 Exposure (s)", self)
        self.setField_binning_label = QtWidgets.QLabel("                        Binning", self)

        self.setField_1 = QtWidgets.QLabel("1", self)

        self.setField_label_filter1 = QtWidgets.QLineEdit(self)
        self.setField_wavelength_filter1 = QtWidgets.QLineEdit(self)
        self.setField_exposure_filter1 = QtWidgets.QLineEdit(self)
        self.setField_binning_filter1 = QtWidgets.QComboBox(self)
        self.setField_binning_filter1.addItem("1x1", 0)
        self.setField_binning_filter1.addItem("2x2", 1)
        self.setField_binning_filter1.addItem("3x3", 2)
        # self.setField_binning_filter1.addItem("4x4", 3)
        # self.setField_binning_filter1.addItem("5x5", 4)
        # self.setField_binning_filter1.addItem("6x6", 5)

        self.button_ok = QtWidgets.QPushButton("Save", self)
        self.button_ok.clicked.connect(self.button_ok_func)

        self.button_clear = QtWidgets.QPushButton('Clear', self)
        self.button_clear.clicked.connect(self.clear_all)

        self.button_cancel = QtWidgets.QPushButton("Cancel", self)
        self.button_cancel.clicked.connect(self.func_cancel)

    def error_binning(self, binning_var):
        try:
            binning_filter = int(binning_var)
        except TypeError:
            binning_filter = 0
        return binning_filter

    def button_ok_func(self):
        try:
            self.var_save_ini_filters.set_filters_settings(self.setField_label_filter1.text(),
                                                           self.setField_wavelength_filter1.text(),
                                                           self.setField_exposure_filter1.text(),
                                                           self.setField_binning_filter1.currentIndex())
            self.var_save_ini_filters.save_settings()
            self.console.raise_text("Filter settings successfully saved!", 1)

        except Exception as e:
            self.console.raise_text("Filter settings NOT saved!", 2)
            print("Filter settings save ERROR -> {}".format(e))

    def clear_all(self):
        self.setField_label_filter1.clear()

        self.setField_wavelength_filter1.clear()

        self.setField_exposure_filter1.clear()

    def func_cancel(self):
        self.f.close()
