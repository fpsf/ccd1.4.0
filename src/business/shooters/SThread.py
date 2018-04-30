import time
from datetime import datetime

import ephem
import math
from PyQt5 import QtCore

from src.business.models.image import Image
from src.controller.commons.Locker import Locker
from src.utils.camera import SbigDriver
from src.business.shooters.InfosForSThread import *


class SThread(QtCore.QThread):
    """
    Threads são fluxos de programas que executam em paralelo dentro de uma aplicação, isto é,\
    uma ramificação de uma parte da aplicação que é executada de forma independente e\
    escalonada independentemente do fluxo inicial da aplicação.
    Fonte: http://imasters.com.br/artigo/20127/py/threads-em-python/?trace=1519021197&source=single
    """
    def __init__(self):
        super(SThread, self).__init__()
        self.lock = Locker()
        self.info = []
        self.img = None
        self.generic_count = 0
        self.final_image_name = None
        self.for_headers_dic = {}

    def set_config_take_image(self):
        """
        seta as configuracoes para se tirar uma foto
        """
        try:
            info_cam = get_camera_settings()
            self.for_headers_dic['Set Temperature'] = info_cam[0]
            self.for_headers_dic['????Tempo de espera'] = info_cam[1]

            info_image = get_image_settings()

            try:
                self.get_level1 = float(info_image[0])
            except Exception as e:
                # print("self.get_level1 = 0.1 -> {}".format(e))
                self.get_level1 = 0.1

            try:
                self.get_level2 = float(info_image[1])
            except Exception as e:
                # print("self.get_level2 = 0.99 -> {}".format(e))
                self.get_level2 = 0.99

            try:
                self.get_axis_xi = float(info_image[2])
            except Exception as e:
                # print("self.get_axis_xi = 0 -> {}".format(e))
                self.get_axis_xi = 0

            try:
                self.get_axis_xf = float(info_image[3])
            except Exception as e:
                # print("self.get_axis_xf = 0 -> {}".format(e))
                self.get_axis_xf = 0

            try:
                self.get_axis_yi = float(info_image[4])
            except Exception as e:
                # print("self.get_axis_yi = 0 -> {}".format(e))
                self.get_axis_yi = 0

            try:
                self.get_axis_yf = float(info_image[5])
            except Exception as e:
                # print("self.get_axis_yf = 0 -> {}".format(e))
                self.get_axis_yf = 0

            try:
                self.get_ignore_crop = info_image[6]
            except Exception as e:
                print("self.get_ignore_crop = True -> {}".format(e))
                self.get_ignore_crop = True

            try:
                self.get_image_png = info_image[7]
            except Exception as e:
                print("self.get_image_png  = True -> {}".format(e))
                self.get_image_png = True

            try:
                self.get_image_tif = info_image[8]
            except Exception as e:
                print("self.get_image_tif = True -> {}".format(e))
                self.get_image_tif = True

            try:
                self.get_image_fit = info_image[9]
            except Exception as e:
                print("self.get_image_fit = True -> {}".format(e))
                self.get_image_fit = True

            try:
                self.append_camera_settings()
            except Exception as e:
                print("self.append_camera_settings() in set_config_take_image -> {}".format(e))

        except Exception as e:
            print("Try ini definitive -> {}".format(e))

    def append_camera_settings(self):
        try:
            project_infos = get_project_settings()

            try:
                self.obs = self.eof.create_observer(longitude=project_infos[0][1],
                                                    latitude=project_infos[0][0],
                                                    elevation=project_infos[1][0])

                now_datetime = datetime.utcnow()
                self.obs.date = ephem.date(now_datetime)

                sun = ephem.Sun(self.obs)

                moon = ephem.Moon(self.obs)
                frac = moon.moon_phase

                sun_alt = ephem.degrees(sun.alt)
                moon_alt = ephem.degrees(moon.alt)

                sun_elevation = "{:.2f}".format(float(math.degrees(sun_alt)))
                moon_elevation = "{:.2f}".format(float(math.degrees(moon_alt)))
                moon_phase = "{0:.2f}".format(frac * 100)
            except Exception as e:
                print("ephem update -> {}".format(e))

            self.for_headers_dic['Latitude'] = str(project_infos[0][0])
            self.for_headers_dic['Longitude'] = str(project_infos[0][1])
            self.for_headers_dic['Elevation(m)'] = str(project_infos[0][2])
            self.for_headers_dic['Pressure(mb)'] = str(project_infos[0][3])
            self.for_headers_dic['Sun Elevation'] = str(sun_elevation)
            self.for_headers_dic['Ignore Lunar Position'] = str(project_infos[1][1])
            self.for_headers_dic['Moon Elevation'] = str(moon_elevation)
            self.for_headers_dic['Moon Phase'] = str(moon_phase)
            self.for_headers_dic['Name'] = str(project_infos[2][0])
            self.for_headers_dic['Observatory'] = str(project_infos[2][1])
            self.for_headers_dic['Imager ID'] = str(project_infos[2][2])
            self.for_headers_dic['get_level1'] = str(self.get_level1)
            self.for_headers_dic['get_level2'] = str(self.get_level2)
            self.for_headers_dic['get_axis_xi'] = str(self.get_axis_xi)
            self.for_headers_dic['get_axis_xf'] = str(self.get_axis_xf)
            self.for_headers_dic['get_axis_yi'] = str(self.get_axis_yi)
            self.for_headers_dic['get_axis_yf'] = str(self.get_axis_yf)
            self.for_headers_dic['get_ignore_crop'] = str(self.get_ignore_crop)
        except Exception as e:
            print("run append_camera_settings() -> {}".format(e))

    def take_dark(self):
        '''
        Manda instrução para o SbigDriver para tirar uma foto dark(shooter fechado)\
        com os valores na info[]
        '''
        try:
            self.set_etime_pre_binning()
            self.lock.set_acquire()
            self.info = SbigDriver.photoshoot(self.etime, self.pre, self.b, 1,
                                              self.get_axis_xi, self.get_axis_xf,
                                              self.get_axis_yi, self.get_axis_yf,
                                              self.get_ignore_crop,
                                              self.get_image_tif,
                                              self.get_image_fit)
            self.final_image_name = self.info[0] + self.info[1]
            self.init_image()
        except Exception as e:
            print(e)
        finally:
            time.sleep(1)
            self.lock.set_release()

    def set_etime_pre_binning(self):
        '''
        seta os valores para o tempo de exposição = etime, prefixo, binning, se a foto é dark ou não,\
        e valores Image contrast: bottom e top level
        '''

        try:
            info = get_camera_settings()

            self.pre = str(info[1])

            self.etime = float(info[2])
            if self.etime <= 0.12:
                self.etime = 0.12 * 100
            elif self.etime >= 3600:
                 self.etime = 3600 * 100
            else:
                self.etime = float(info[2]) * 100
            self.etime = int(self.etime)

            self.b = int(info[3])

            self.get_level1 = float(info[6])
            self.get_level2 = float(info[7])

            self.dark_photo = int(info[8])

            self.get_axis_xi = int(info[9])
            self.get_axis_xf = int(info[10])
            self.get_axis_yi = int(info[11])
            self.get_axis_yf = int(info[12])

            self.get_ignore_crop = info[13]

            self.get_image_tif = info[14]
            self.get_image_fit = info[15]


        except Exception as e:
            print(e)
            self.etime = 100
            self.b = 0
            self.dark_photo = 1
            self.get_level1 = 0.1
            self.get_level2 = 0.99

            if str(info[1]) != '':
                self.pre = str(info[1])
            else:
                self.pre = 'pre'

            self.get_axis_xi = info[9]
            self.get_axis_xf = info[10]
            self.get_axis_yi = info[11]
            self.get_axis_yf = info[12]

            self.get_ignore_crop = True

            self.get_image_tif = True
            self.get_image_fit = True

    def run(self):
        self.set_etime_pre_binning()
        self.lock.set_acquire()
        try:
            self.info = SbigDriver.photoshoot(self.etime, self.pre, self.b, self.dark_photo,
                                              self.get_axis_xi, self.get_axis_xf, self.get_axis_yi,
                                              self.get_axis_yf, self.get_ignore_crop,
                                              self.get_image_tif, self.get_image_fit)
            self.final_image_name = self.info[0] + self.info[1]
            self.init_image()
        except Exception as e:
            print(e)
        finally:
            self.lock.set_release()

    def init_image(self):
        try:
            for i in self.info:
                print(i)

            self.img = Image(self.final_image_name)
        except Exception as e:
            self.img = Image('')
        return self.img

    def get_image_info(self):
        return self.img
