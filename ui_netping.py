from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Ui_NetPing(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName('MainWindow')

        MainWindow.resize(300, 200)
        MainWindow.setWindowTitle(u"Ping test")
        
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName('centralwidget')
        self.gridlayout = QGridLayout(self.centralwidget)
        self.gridlayout.setObjectName('gridlayout')
        self.centralwidget.setLayout(self.gridlayout)

        self.label = QLabel(self.centralwidget)
        self.label.setText(u"Pinging 8.8.8.8...")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName('label')

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName('progressBar')

        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridlayout.addWidget(self.progressBar, 1, 0, 1, 1)
        
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName('menubar')
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName('statusbar')

        MainWindow.setMenuBar(self.menubar)
        MainWindow.setStatusBar(self.statusbar)

