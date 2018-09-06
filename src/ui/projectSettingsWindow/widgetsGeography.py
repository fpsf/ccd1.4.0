from PyQt5 import QtCore
from PyQt5 import QtWidgets

from src.ui.commons.layout import set_hbox, set_lvbox, add_widget_to_vbox


class WidgetsGeography(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WidgetsGeography, self).__init__(parent)

        '''grid = QGridLayout()
                        grid.addWidget(self.create_site_info_group())
                        grid.addWidget(self.create_geo_info_group())
                        grid.addWidget(self.create_sun_info_group())
                        grid.addWidget(self.create_push_button_group())
                        self.setLayout(grid)'''

        # Creating Labels
        self.lLat = QtWidgets.QLabel("Latitude (º):", self)
        self.lLat.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.lLon = QtWidgets.QLabel("Longitude (º):", self)
        self.lLon.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        '''
        self.lElev = QtWidgets.QLabel("Elevation (m):", self)
        self.lElev.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.lPres = QtWidgets.QLabel("Pressure (mb):", self)
        self.lPres.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.lTemp = QtWidgets.QLabel("Temperature (ºC):", self)
        self.lTemp.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        '''

        # Creating Input Fields
        self.eLat = QtWidgets.QLineEdit(self)
        self.eLat.setMaximumWidth(100)

        self.eLon = QtWidgets.QLineEdit(self)
        self.eLon.setMaximumWidth(100)

        '''
        self.eElev = QtWidgets.QLineEdit(self)
        self.eElev.setMaximumWidth(100)

        self.ePres = QtWidgets.QLineEdit(self)
        self.ePres.setMaximumWidth(100)

        self.eTemp = QtWidgets.QLineEdit(self)
        self.eTemp.setMaximumWidth(100)
        '''

        # self.setting_up()

    """
    set_hbox(self.lElev, self.eElev),
    set_hbox(self.lPres, self.ePres),
    set_hbox(self.lTemp, self.eTemp)
    """
    def setting_up(self):
        vbox = set_lvbox(set_hbox(self.lLat, self.eLat))
        add_widget_to_vbox(vbox, set_hbox(self.lLon, self.eLon))
        # self.setLayout(vbox)
        return vbox

    # self.eElev.text(), self.ePres.text(),
    def get_geography(self):
        return self.eLat.text(), self.eLon.text()  # self.eTemp.text()

    # elevation, pressure,
    def set_geography(self, latitude, longitude, temperature):
        self.eLat.setText(latitude)
        self.eLon.setText(longitude)
        # self.eElev.setText(elevation)
        # self.ePres.setText(pressure)
        # self.eTemp.setText(temperature)

    def clear_geography(self):
        self.eLat.clear()
        self.eLon.clear()
        # self.eElev.clear()
        # self.ePres.clear()
        # self.eTemp.clear()

    def setting_up_geo(self):
        '''group_box = QGroupBox("&Image Contrast:")
        group_box.setCheckable(True)
        group_box.setChecked(True)'''
