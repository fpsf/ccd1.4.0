import os
from datetime import datetime

from PyQt5 import QtCore

from src.utils.camera import Julian_Day
from src.utils.camera import Image_Path


class Logger(QtCore.QThread):
    '''
    cria o log
    '''
    def __init__(self):
        super(Logger, self).__init__()
        self.text = None

    def set_text(self, text):
        self.text = text

    def run(self):
        try:
            tempo = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            data = tempo[0:4] + "_" + tempo[4:6] + tempo[6:8]

            data_log = datetime.utcnow().strftime('[%Y-%m-%d @ %H:%M:%S UTC]')

            from src.business.configuration.configSystem import ConfigSystem
            log_folder = ConfigSystem()

            if str(log_folder.get_log_path()) == "None":
                if log_folder():
                    name_log_folder = str(log_folder.get_log_path())
                else:
                    name_log_folder = 'Log_folder'
                    os.mkdir(name_log_folder)
            else:
                name_log_folder = str(log_folder.get_log_path())

            from src.business.configuration.configProject import ConfigProject
            ci = ConfigProject()
            name_observatory = ci.get_site_settings()[1]

            if int(tempo[9:11]) > 12:
                name_log = name_log_folder + "/" + name_observatory + "_" + data + '.txt'
                log = open(str(name_log), 'a')
                log.write(str(data_log) + " - " + str(self.text) + "\n")
                log.close()
            else:
                tempo = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
                ano = tempo[0:4]
                mes = tempo[4:6]
                dia = tempo[6:8]
                abs_julian_day = Julian_Day.jd_to_date(Julian_Day.date_to_jd(ano, mes, int(dia)) - 1)

                if (0 < abs_julian_day[2] < 10) and (0 < abs_julian_day[1] < 10):
                    name_log = name_log_folder + "/" + name_observatory + "_" + str(abs_julian_day[0]) + "_" +\
                               "0" + str(abs_julian_day[1]) + "0" + str(abs_julian_day[2]) + '.txt'
                    log = open(str(name_log), 'a')
                    log.write(str(data_log) + " - " + str(self.text) + "\n")
                    log.close()
                elif (0 < abs_julian_day[2] < 10) and (not (0 < abs_julian_day[1] < 10)):
                    name_log = name_log_folder + "/" + name_observatory + "_" + str(abs_julian_day[0]) + "_" + \
                               str(abs_julian_day[1]) + "0" + str(abs_julian_day[2]) + '.txt'
                    log = open(str(name_log), 'a')
                    log.write(str(data_log) + " - " + str(self.text) + "\n")
                    log.close()
                elif (not (0 < abs_julian_day[2] < 10)) and (0 < abs_julian_day[1] < 10):
                    name_log = name_log_folder + "/" + name_observatory + "_" + str(abs_julian_day[0]) + "_" + \
                               "0" + str(abs_julian_day[1]) + str(abs_julian_day[2]) + '.txt'
                    log = open(str(name_log), 'a')
                    log.write(str(data_log) + " - " + str(self.text) + "\n")
                    log.close()
                else:
                    # + str(abs_julian_day[1])
                    name_log = name_log_folder + "/" + name_observatory + "_" + str(abs_julian_day[0]) + "_" +\
                               str(abs_julian_day[1]) + str(abs_julian_day[2]) + '.txt'
                    log = open(str(name_log), 'a')
                    log.write(str(data_log) + " - " + str(self.text) + "\n")
                    log.close()
        except Exception as e:
            print(e)
