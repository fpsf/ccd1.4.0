import os

import math
from datetime import datetime

import ephem
from PIL import Image
from src.business.shooters.InfosForSThread import *
from src.utils.camera import SbigDriver, Image_Path
from src.business.EphemObserverFactory import EphemObserverFactory


def str_to_raw(s):
    raw_map = {8: r'\b', 7: r'\a', 12: r'\f', 10: r'\n', 13: r'\r', 9: r'\t', 11: r'\v'}
    return r''.join(i if ord(i) > 32 else raw_map.get(ord(i), i) for i in s)


def set_headers(for_headers_dic):

    headers_camera = get_camera_settings()
    headers_project = get_project_settings()
    elevations = make_elevations_info()
    for_headers_dic['Start Time'] = Image_Path.set_path()[1]
    for_headers_dic['Binning'] = headers_camera[3]
    for_headers_dic['Set Temperature'] = headers_camera[0]
    for_headers_dic['Temperature'] = SbigDriver.get_temperature()[3]
    for_headers_dic['Imager ID'] = headers_project[2][2]
    for_headers_dic['Exposure'] = headers_camera[2]
    for_headers_dic['Filter Label'] = headers_camera[1]
    for_headers_dic['Filter Wavelength'] = get_filters_settings()[1]
    for_headers_dic['Latitude'] = headers_project[0][0]
    for_headers_dic['Longitude'] = headers_project[0][1]
    for_headers_dic['Moon Elevation'] = str(elevations[1])
    for_headers_dic['Moon Phase'] = str(elevations[0])
    for_headers_dic['Observatory'] = headers_project[2][1]
    for_headers_dic['Sun Elevation'] = str(elevations[2])

    return for_headers_dic


def make_elevations_info():
    class ObsMaker:
        def __init__(self):
            try:
                project_infos = get_project_settings()
                self.eof = EphemObserverFactory()
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

                    self.sun_elevation = "{:.2f}".format(float(math.degrees(sun_alt)))
                    self.moon_elevation = "{:.2f}".format(float(math.degrees(moon_alt)))
                    self.moon_phase = "{0:.2f}".format(frac * 100)
                except Exception as e:
                    print("ephem update -> {}".format(e))
            except Exception as e:
                print("run append_camera_settings() -> {}".format(e))
    returner = ObsMaker()
    return returner.moon_phase, returner.moon_elevation, returner.sun_elevation


def return_info_png(file_name, for_headers_dic):
    file_name = str(file_name)
    try:
        image = Image.open(file_name)
        dictionary = for_headers_dic
        for keys, values in dictionary.items():
            print(str(keys) + ": " + str(values))
        image.show
        print("\n\n")
    except Exception as e:
        print("Exception return_info_png -> {}".format(e))
