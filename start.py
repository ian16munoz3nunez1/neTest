from PyQt5.QtWidgets import QMainWindow
from ui_start import Ui_Start
import os
import platform

class Start(QMainWindow):
    def __init__(self):
        super(Start, self).__init__()
        self.ui = Ui_Start()
        self.ui.setupUi(self)

        self.__os = platform.system().lower()

        self.ui.pushButton.clicked.connect(self.runPing)

    def closeEvent(self, event):
        with open('running.lock', 'r') as file:
            content = file.read()
        file.close()
        if content == 'running':
            os.remove('running.lock')

    def runPing(self):
        with open('running.lock', 'w') as file:
            file.write("netping")
        file.close()
        self.close()

        if self.__os == 'windows':
            os.system('main.exe')
        if self.__os == 'linux':
            os.system('./main')

