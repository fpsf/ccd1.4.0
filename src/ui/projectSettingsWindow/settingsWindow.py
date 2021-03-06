import time

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGridLayout, QGroupBox

from src.business.configuration.configProject import ConfigProject
from src.business.consoleThreadOutput import ConsoleThreadOutput
from src.ui.commons.layout import set_hbox
from src.ui.projectSettingsWindow.widgetsGeography import WidgetsGeography
from src.ui.projectSettingsWindow.widgetsSite import WidgetsSite
from src.ui.projectSettingsWindow.widgetsSun import WidgetsSun
from src.business.configuration.constants import settingsUpdater as su


class SettingsWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.p = parent
        self.console = ConsoleThreadOutput()

        self.site = WidgetsSite(self)
        self.geo = WidgetsGeography(self)
        self.sun = WidgetsSun(self)
        self.button_clear = QtWidgets.QPushButton('Clear', self)
        self.button_ok = QtWidgets.QPushButton('Save', self)
        self.button_cancel = QtWidgets.QPushButton('Cancel', self)
        self.button_settings()

        # Init Interface
        # self.setting_up()
        self.grid = self.setting_up()
        self.w = self.grid.geometry().width()
        self.h = self.grid.geometry().height()
        self.refresh_all_fields()

    def button_settings(self):
        self.button_clear.clicked.connect(self.clear_all)
        self.button_cancel.clicked.connect(self.func_cancel)
        self.button_ok.clicked.connect(self.func_ok)

    def func_cancel(self):
        self.p.close()
        #self.clear_all()

    def func_ok(self):
        try:
            self.save_settings()
            su.UPDATER += 1
            self.console.raise_text("Project settings successfully saved!", 1)
        except:
            self.console.raise_text("Unable to save the project settings.", 3)
        finally:
            self.p.close()
            self.clear_all()
            self.refresh_all_fields()

    def clear_all(self):
        self.site.clear_site()
        self.geo.clear_geography()
        self.sun.clear_sun()

    def refresh_all_fields(self):
        try:
            st = ConfigProject()
            infoSite = st.get_site_settings()
            self.site.set_site_info(infoSite[0], infoSite[1], infoSite[2])
            infoGeo = st.get_geographic_settings()
            # infoGeo[3], infoGeo[4]
            self.geo.set_geography(infoGeo[0], infoGeo[1], infoGeo[4])
            infoSun = st.get_moonsun_settings()
            self.sun.set_sun(str(infoSun[0]), infoSun[1], str(infoSun[2]), str(infoSun[3]))
        except Exception as e:
            print(e)

    def save_settings(self):
        try:
            st = ConfigProject()
            self.save_site(st)
            self.save_geo(st)
            self.save_sun(st)
            st.save_settings()
        except Exception as e:
            print(e)

    def save_site(self, set):
        info1 = self.site.get_site_info()
        set.set_site_settings(info1[0], info1[1], info1[2])

    def save_geo(self, set):
        info2 = self.geo.get_geography()
        # info2[2], info2[3], info2[4]
        set.set_geographic_settings(info2[0], info2[1], '0', '0', '0')

    def save_sun(self, set):
        info3 = self.sun.get_sun()
        set.set_moonsun_settings(info3[0], info3[1], info3[2], info3[3])

    def setting_up(self):
        '''self.setLayout(set_lvbox(set_hbox(self.site),
                                 set_hbox(self.geo),
                                 set_hbox(self.sun),
                                 set_hbox(self.button_ok, self.button_clear, self.button_cancel, stretch2=1)))'''
        grid = QGridLayout()
        grid.addWidget(self.setting_up_site())
        grid.addWidget(self.setting_up_geo())
        grid.addWidget(self.setting_up_sun())
        grid.addWidget(self.setting_up_buttons())
        self.setLayout(grid)
        return grid

    def setting_up_site(self):
        group_box = QGroupBox("&Site Settings:")
        group_box.setCheckable(True)
        group_box.setChecked(False)
        group_box.setLayout(self.site.setting_up())
        return group_box

    def setting_up_geo(self):
        group_box = QGroupBox("&Geographic Settings:")
        group_box.setCheckable(True)
        group_box.setChecked(False)
        group_box.setLayout(self.geo.setting_up())
        return group_box

    def setting_up_sun(self):
        group_box = QGroupBox("&Sun and Moon Options:")
        group_box.setCheckable(True)
        group_box.setChecked(False)
        group_box.setLayout(self.sun.setting_up())
        return group_box

    def setting_up_buttons(self):
        group_box = QGroupBox()
        group_box.setLayout(set_hbox(self.button_ok, self.button_clear, self.button_cancel))
        return group_box