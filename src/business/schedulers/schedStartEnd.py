from PyQt5 import QtCore

from src.business.schedulers.qthreadStartEnd import QThreadStartEnd
from src.utils.singleton import Singleton
from src.business.consoleThreadOutput import ConsoleThreadOutput
from src.business.configuration.constants import settingsUpdater as su
import datetime


class SchedStartEnd(metaclass=Singleton):
    def __init__(self, start_obs_info, end_obs_info, total_obs_info):
        self.settings_updated = 0
        self.consolethreadoutput = ConsoleThreadOutput()
        self.start_obs_info = start_obs_info
        self.end_obs_info = end_obs_info
        self.total_obs_info = total_obs_info

        self.threadStartEnd = QThreadStartEnd()

        self.threadStartEnd.values_start_end.connect(self.refresh)
        self.c = 0

    def start_scheduler(self):
        self.threadStartEnd.start()

    # Refreshing Start End Observation
    def refresh(self, value):
        the_date = datetime.datetime.utcnow()
        # self.consolethreadoutput.raise_text("F U I   C H A M A D O", 1)
        if the_date.hour == 12 and the_date.minute == 0\
                or self.c == 0 or \
                self.settings_updated != su.UPDATER:
            info_start_end = value
            start_time = str(info_start_end[0])
            start_field = start_time[:-10] + " UTC"
            end_time = str(info_start_end[1])
            end_field = end_time[:-10] + " UTC"
            # time_obs_temp = str(info_start_end[2])
            time_obs_time = str(info_start_end[2]).split(":")
            time_obs_time = [z.split(".")[0] for z in time_obs_time]
            time_obs_field = time_obs_time[0] + ":" + time_obs_time[1] + " Hours"
            try:
                self.start_obs_info.setText(start_field)
                self.end_obs_info.setText(end_field)
                self.total_obs_info.setText(time_obs_field)
            except Exception as e:
                print("refresh SchedStartEnd -> {}".format(e))
            self.c = 1
            self.settings_updated = su.UPDATER
