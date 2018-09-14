import os
import time

import skimage.io
from PIL.ImageQt import ImageQt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from astropy.io.fits import getdata
from scipy.misc import toimage

from src.business.consoleThreadOutput import ConsoleThreadOutput
from src.business.shooters.InfosForSThread import get_camera_settings
from src.controller.camera import Camera
from src.ui.commons.layout import set_hbox, set_lvbox
from src.utils.Shutter_Tests import shutter_control
from src.utils.camera import Image_Processing, SbigDriver
from src.business.configuration.settingsCamera import SettingsCamera


# Aux Functions
from src.utils.camera.Image_Headers import make_elevations_info


def set_width(*s):
    for o in s:
        o.setMaximumWidth(25)
        o.setMaxLength(2)


class Shooter(QtWidgets.QWidget):
    """
    Class for Taking photo Widget
    """

    def __init__(self, parent=None):
        super(Shooter, self).__init__(parent)
        self.console = ConsoleThreadOutput()
        self.cam = Camera()
        self.cond = 0
        self.sref_calc = SettingsCamera()

        # Label for Image
        self.img = QtWidgets.QLabel(self)
        self.config_img_label()

        # Creating a Pallete
        self.pa = QtGui.QPalette()

        self.set_layout()
        self.link_signals()

    def log_ephem_infos(self):
        elevations = make_elevations_info()
        headers_camera = get_camera_settings()
        temp = SbigDriver.get_temperature()[3]
        set_temp = headers_camera[0]
        temp_filtro = shutter_control(None)[0]
        ephem_infos_1 = "Sun Elevation: " + str(elevations[2]) + "; Moon Elevation: " + str(elevations[1]) +\
                        "; Moon Phase: " + str(elevations[0])
        self.console.save_log(ephem_infos_1)
        time.sleep(2)
        ephem_infos_2 = "Camera Temperature: " + "{0:.2f}".format(temp) + "; Set Temperature: " +\
                        set_temp + "; Status Temp. Filtro: " + "{0:.2f}".format(temp_filtro) + "ºC"
        self.console.save_log(ephem_infos_2)

    def link_signals(self):
        self.cam.ephemerisShooterThread.continuousShooterThread.ss.finished.connect(self.get_image_automatic)
        self.cam.continuousShooterThread.ss.finished.connect(self.get_image_manual)

    def get_image_automatic(self):
        img = self.cam.ephemerisShooterThread.continuousShooterThread.ss.get_image_info()
        self.set_image(img)

    def get_image_manual(self):
        img = self.cam.continuousShooterThread.ss.get_image_info()
        self.set_image(img)

    def set_layout(self):
        hb2 = set_hbox(self.prefix, self.date, self.hour)

        self.setLayout(set_lvbox(set_hbox(self.img), hb2))
        self.config_pallete()

    def config_img_label(self):
        self.img.setPixmap(QtGui.QPixmap("noimage.png"))
        self.img.setMaximumSize(425, 425)
        self.prefix = QtWidgets.QLabel(self)
        self.date = QtWidgets.QLabel(self)
        self.hour = QtWidgets.QLabel(self)

    def config_pallete(self):
        self.pa.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)  # Setting the style
        self.prefix.setPalette(self.pa)
        self.date.setPalette(self.pa)
        self.hour.setPalette(self.pa)

    def shoot_function(self):
        self.cam.shoot(int(self.tb.text()), self.pre.text(), int(self.combo.currentIndex()))
        self.set_image()

    def auto_shoot(self):
        try:
            self.cam.autoshoot(int(self.htext.text()), int(self.mtext.text()), int(self.tb.text()), self.pre.text(), int(self.combo.currentIndex()))
        except Exception as e:
            print(e)

    def set_image(self, img):
        print("Setting Pixmap")
        print("CCCCCCCCCCCCCCCCCCCCCCCCCCC")
        try:
            path = img.final_image_name

            # image = Image.open(path)]

            try:
                if os.path.splitext(path)[1] == '.fit':
                    print("1111111111111111111")
                    img = getdata(path)
                else:
                    print("222222222222222222222")
                    # img = skimage.io.imread('/home/cristiano')
                    img = skimage.io.imread(path)

                print("\n\n>>>>>>>>>>>>>>>>>>>>>>")
                print(img)

            except Exception as e:
                print("Exception os.path.splitext -> {}".format(e))
            image = img  #im

            sref_min = float(self.sref_calc.get_camera_settings()[6])
            sref_max = float(self.sref_calc.get_camera_settings()[7])

            img_hist_equal = Image_Processing.img_hist_equal(image, sref_min, sref_max)
            im3 = toimage(img_hist_equal)
            im4 = im3.resize((int(425), int(425)))
            im5 = Image_Processing.draw_image(im4, path)

            try:
                qim = ImageQt(im5)
                self.img.setPixmap(QtGui.QPixmap.fromImage(qim))
            except Exception as e:
                print("Exception setPixmap(QtGui.QPixmap(image_to_show)) -> {}".format(e))

            print(path)
            self.log_ephem_infos()
        except Exception as e:
            print("Exception Setting Pixmap -> {}".format(e))

    def fill_combo(self):
        self.combo.addItem("1x1", 0)
        self.combo.addItem("2x2", 1)
        self.combo.addItem("3x3", 2)

    def clear_image_info(self):
        self.prefix.clear()
