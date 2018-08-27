from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QPushButton

from src.ui.commons.layout import set_lvbox, set_hbox

from src.ui.CCDWindow.main import Main as CCD_menu
from src.ui.filterWindow.main import Main as filters
from src.ui.imageSettingsWindow.main import Main as imag_menu
from src.ui.projectSettingsWindow.main import MainWindow as mw
from src.ui.systemSettingsWindow.main import MainWindow as sw


class AllSettingsWindow(QtWidgets.QWidget):
    def __init__(self):
        super(AllSettingsWindow, self).__init__()
        # System
        self.a = sw(self)
        # Project
        self.b = mw(self)
        # Image
        self.imag = imag_menu(self)
        # Imager
        self.CCD_menu = CCD_menu(self)
        # Filter
        self.filters_menu = filters(self)
        self.make_buttons()
        self.init_menu()

    def make_buttons(self):
        self.swaction = QPushButton('System Settings', self)
        self.swaction.clicked.connect(self.a.show)
        # self.swaction.clicked.connect(self.open_settings_system)

        self.mwaction = QPushButton('Project Settings', self)
        self.mwaction.clicked.connect(self.b.show)
        # self.mwaction.clicked.connect(self.open_settings)

        self.imageAction = QPushButton('Image Settings', self)
        self.imageAction.clicked.connect(self.imag.show)
        # self.imageAction.clicked.connect(self.open_settings_image)

        self.imagerAction = QPushButton('Camera Settings', self)
        self.imagerAction.clicked.connect(self.CCD_menu.show)
        # self.imagerAction.clicked.connect(self.open_settings_CCD)

        self.filterAction = QPushButton('Filter Settings', self)
        self.filterAction.clicked.connect(self.filters_menu.show)
        # self.filterAction.clicked.connect(self.open_settings_filters)

    def init_menu(self):
        self.setLayout(set_lvbox(set_hbox(self.swaction),
                                 set_hbox(self.mwaction),
                                 set_hbox(self.imageAction),
                                 set_hbox(self.imagerAction),
                                 set_hbox(self.filterAction)))

    """def open_settings(self):
        settings = QtWidgets.QAction('Project Settings', self)
        settings.setShortcut("Ctrl+P")
        settings.setStatusTip("Open Settings window")

        settings.triggered.connect(self.a.show)

        return settings, "&Options"

    def open_settings_system(self):
        setS = QtWidgets.QAction('System Settings', self)
        setS.setShortcut('Ctrl+T')

        setS.triggered.connect(self.b.show)

        return setS, "&Options"

    def open_settings_camera(self):
        setC = QtWidgets.QAction('Camera Settings', self)
        setC.setShortcut("Ctrl+C")

        setC.triggered.connect(self.c.show)

        return setC, "&Options"

    def open_settings_image(self):
        setI = QtWidgets.QAction('Image Settings', self)
        setI.setShortcut("Ctrl+i")

        setI.triggered.connect(self.imag.show)

        return setI, "&Options"

    def open_settings_filters(self):
        setF = QtWidgets.QAction('Filters Settings', self)
        setF.setShortcut("Ctrl+F")

        try:
            setF.triggered.connect(self.filters_menu.show)
        except Exception as e:
            print(e)

        return setF, "&Options"

    def open_settings_CCD(self):
        setCCD = QtWidgets.QAction('Imager Settings', self)

        setCCD.triggered.connect(self.funcao_teste)

        return setCCD, "&Options"

    def funcao_teste(self):
        self.CCD_menu.show()
        self.CCD_menu.show_camera_infos()"""