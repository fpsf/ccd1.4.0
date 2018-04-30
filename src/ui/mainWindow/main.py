from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QAction

from src.business.configuration.configSystem import ConfigSystem
from src.controller.camera import Camera
from src.ui.filterWindow.main import Main as filters
from src.ui.imageSettingsWindow.main import Main as imag_menu
from src.ui.CCDWindow.main import Main as CCD_menu
from src.ui.ephemerisShooterWindow.main import Main as eph
from src.ui.mainWindow.mainWindow import MainWindow
from src.ui.mainWindow.status import Status
from src.ui.projectSettingsWindow.main import MainWindow as sw
from src.ui.systemSettingsWindow.main import MainWindow as mw
from src.ui.testWindow.MainWindow2 import MainWindow2 as conts

import ctypes

class Main(QtWidgets.QMainWindow):
    """
    classe de criacao da interface
    """
    def __init__(self):
        super(Main, self).__init__()
        Status(self)
        # Init Layouts
        user32 = ctypes.windll.user32
        self.screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        self.init_widgets()
        self.init_user_interface()
        self.createActions()

        self.createToolBars()

    def init_user_interface(self):
        self.cont = conts(self)
        self.ephem = eph(self)
        self.a = sw(self)
        self.b = mw(self)
        self.imag = imag_menu(self)
        self.CCD_menu = CCD_menu(self)
        self.cam = Camera()
        self.filters_menu = filters(self)
        self.init_menu()
        self.init_window_geometry()

        self.cs = ConfigSystem()

        info = self.cs.get_site_settings()

        # Connect Camera
        if info[0] == True:
            self.cam.connect()
            self.cam.start_ephemeris_shooter()

    def init_widgets(self):
        a = MainWindow(self)
        self.setCentralWidget(a)

    def init_window_geometry(self):
        # 300, 100, 800, 700
        self.setGeometry(self.screensize[0]/4, self.screensize[1]/4 - self.screensize[1]/6, 0, 0)
        '''qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())'''
        self.setWindowTitle("CCD Controller 1.0.0")
        self.show()
        # self.showMaximized()
    # Creating menubar

    def init_menu(self):
        """
        Creating the Menu Bar
        """
        menubar = self.menuBar()

        a3 = self.action_connect_disconnect()
        self.add_to_menu(menubar, a3[0], a3[1], a3[2])
        a4 = self.action_continuous_shooter()
        a5 = self.action_ephemeris_shooter()
        m = self.add_to_menu(menubar, 'Operation Mode')
        self.add_to_menu(m, 'Manual', a4[0], a4[1])
        self.add_to_menu(m, 'Automatic', a5[0], a5[1])
        a2 = self.open_settings()
        self.add_to_menu(menubar, "System Settings", self.open_settings_system()[0])
        self.add_to_menu(menubar, "Project Settings", a2[0])
        self.add_to_menu(menubar, "Image Settings", self.open_settings_image()[0])
        self.add_to_menu(menubar, "Filters Settings", self.open_settings_filters()[0])
        self.add_to_menu(menubar, "Imager Settings", self.open_settings_CCD()[0])
        # self.add_to_menu(menubar, a2[1], self.open_settings_system()[0], a2[0], self.open_settings_camera()[0])

        # add_to_menu(menubar, open_settings_system(self))

    # All actions needs return a QAction and a menuType, line '&File'
    def action_close(self):
        """
        Creating the button to close the application
        """
        aexit = QtWidgets.QAction(QIcon('\icons\exit.png'), "&Exit", self)
        aexit.setShortcut("Ctrl+Q")
        aexit.setStatusTip("Exit Application")

        # noinspection PyUnresolvedReferences
        aexit.triggered.connect(QtWidgets.qApp.exit)

        return aexit, "&File"

    def action_continuous_shooter(self):
        """
        Inicia e para o modo manual
        """
        actionStart = QtWidgets.QAction('&Start', self)
        actionStop = QtWidgets.QAction('&Stop', self)

        actionStart.triggered.connect(self.cam.start_taking_photo)
        actionStop.triggered.connect(self.cam.stop_taking_photo)

        return actionStart, actionStop

    def action_ephemeris_shooter(self):
        """
        Inicia e para o modo automatico
        """
        actionStart = QtWidgets.QAction('&Start', self)
        actionStop = QtWidgets.QAction('&Stop', self)

        actionStart.triggered.connect(self.cam.start_ephemeris_shooter)
        actionStop.triggered.connect(self.cam.stop_ephemeris_shooter)

        return actionStart, actionStop

    def open_settings(self):
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
        self.CCD_menu.show_camera_infos()

    def action_connect_disconnect(self):
        setAC = QtWidgets.QAction('Connect', self)
        setAD = QtWidgets.QAction('Disconnect', self)

        setAC.triggered.connect(self.cam.connect)

        setAD.triggered.connect(self.cam.disconnect)

        return 'Connection', setAC, setAD

    def add_to_menu(self, menubar, menu, *args):
        m = menubar.addMenu(menu)
        for w in args:
            m.addAction(w)

        return m

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                         "Are you sure to quit?", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def createActions(self):
        self.connectAction = QAction(QIcon('icons/Connect.png'), 'Connect', self)
        self.connectAction.triggered.connect(self.cam.connect)
        '''
        self.connectAction.setCheckable(True)
        self.connectAction.setChecked(True)
        self.setDisabled(True)
        '''

        self.disconnectAction = QAction(QIcon('icons/Disconnect.png'), 'Disconnect', self)
        self.disconnectAction.triggered.connect(self.cam.disconnect)

        self.automaticAction = QAction(QIcon('icons/Run_Automatic.png'), 'Run Automatic', self)
        self.automaticAction.triggered.connect(self.cam.start_ephemeris_shooter)
        '''
        self.automaticAction.setCheckable(True)
        self.automaticAction.setChecked(True)
        '''
        self.manualAction = QAction(QIcon('icons/Run_Manual.png'), 'Run Manual', self)
        self.manualAction.triggered.connect(self.cam.start_taking_photo)
        '''
        self.manualAction.setCheckable(True)
        self.manualAction.setChecked(False)
        '''

        self.stopAction = QAction(QIcon('icons/Stop.png'), 'Stop', self)
        try:
            if self.cam.start_taking_photo:
                self.stopAction.triggered.connect(self.cam.stop_taking_photo)
            elif self.cam.start_ephemeris_shooter:
                self.stopAction.triggered.connect(self.cam.stop_ephemeris_shooter)
            else:
                print("Nothing to stop")
        except Exception as e:
            print(e)

    def createToolBars(self):
        self.toolbar = self.addToolBar('Close Toolbar')
        self.toolbar.setIconSize(QtCore.QSize(70, 70))
        self.toolbar.addAction(self.connectAction)
        self.toolbar.addAction(self.disconnectAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.automaticAction)
        self.toolbar.addAction(self.manualAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.stopAction)
        self.toolbar.addSeparator()
