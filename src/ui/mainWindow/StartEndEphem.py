from PyQt5 import QtCore
from PyQt5 import QtWidgets

from src.business.schedulers.schedStartEnd import SchedStartEnd
from src.ui.commons.layout import set_hbox, set_lvbox
from src.ui.commons.widgets import get_qfont
from src.ui.mainWindow.StartEndTimeInfo import result
from src.business.consoleThreadOutput import ConsoleThreadOutput

# -*- coding: utf-8 -*-
"""
Created on Tue May  9 20:24:01 2017

@author: Cristiano
"""


class StartEndEphem(QtWidgets.QFrame):

    def __init__(self, parent=None):
        super(StartEndEphem, self).__init__(parent)

        self.start_obs_info_display = QtWidgets.QLabel(self)
        self.end_obs_info_display = QtWidgets.QLabel(self)
        self.total_obs_info_display = QtWidgets.QLabel(self)
        self.consolethreadoutput = ConsoleThreadOutput()

        self.schedstartend = SchedStartEnd(start_obs_info=self.start_obs_info_display,
                                           end_obs_info=self.end_obs_info_display,
                                           total_obs_info=self.total_obs_info_display)

        self.init_thread_start_end_obs()

        self.init_widgets()
        self.config_widgets()

        self.title = None

    def init_thread_start_end_obs(self):
        self.schedstartend.start_scheduler()

    def init_widgets(self):
        self.title = QtWidgets.QLabel("Observation Time", self)
        info_start_end = result()

        start_l = QtWidgets.QLabel("Start:", self)

        end_l = QtWidgets.QLabel("End:", self)

        time_obs_l = QtWidgets.QLabel("Total Obs. Time:", self)
        time_obs_time = str(info_start_end[2])
        time_obs_field = QtWidgets.QLabel(time_obs_time[:-3] + " Hours")
        time_obs_field.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.setLayout(set_lvbox(set_hbox(self.title),
                                 set_hbox(start_l, self.start_obs_info_display),
                                 set_hbox(end_l, self.end_obs_info_display),
                                 set_hbox(time_obs_l, self.total_obs_info_display)))

    def config_widgets(self):
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setFont(get_qfont(True))

        self.setStyleSheet("background-color: rgb(50, 50, 50); border-radius: 10px; color: white;")

'''
info_start_end = result()
start_time = str(info_start_end[0])
end_time = str(info_start_end[1])
time_obs_time = str(info_start_end[2])

log.write("Start Observation:" + start_time[:-10] + " UTC\n")
log.write("End Observation:" + end_time[:-10] + " UTC\n")
log.write("Total Observation Time:" + time_obs_time[:-10] + " Hours\n")
'''