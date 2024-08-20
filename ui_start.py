from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Ui_Start(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName('MainWindow')

        MainWindow.resize(300, 200)
        MainWindow.setWindowTitle(u"neTest")
        
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName('centralwidget')
        self.gridlayout = QGridLayout(self.centralwidget)
        self.gridlayout.setObjectName('gridlayout')
        self.centralwidget.setLayout(self.gridlayout)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setText(u"Start test")
        self.pushButton.setCursor(Qt.PointingHandCursor)
        self.pushButton.setStyleSheet("""QPushButton {
            min-height: 30px;
            background-color: rgb(40, 40, 40);
            border: 1px;
            border-style: solid;
            border-color: rgb(0, 160, 0);
            border-radius: 15px;
        }
        QPushButton:hover {
            background: rgb(0, 200, 0);
        }
        QPushButton:pressed {
            background: rgb(0, 180, 0);
        }""")
        self.pushButton.setObjectName('pushButton')

        self.gridlayout.addWidget(self.pushButton, 0, 0, 1, 1)
        
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName('menubar')
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName('statusbar')

        MainWindow.setMenuBar(self.menubar)
        MainWindow.setStatusBar(self.statusbar)

