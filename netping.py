from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QMainWindow, QLabel
from ui_netping import Ui_NetPing
import threading
import platform
import re
import os
from time import sleep
from subprocess import Popen, PIPE

class NetPing(QMainWindow):
    def __init__(self):
        super(NetPing, self).__init__()
        self.ui = Ui_NetPing()
        self.ui.setupUi(self)

        self.__os = platform.system().lower()
        self.__output = ''
        self.__i = 0
        self.__numPacks = 10

        hilo = threading.Thread(target=self.ping)
        hilo.start()
        self.progressTimer = QTimer()
        self.progressTimer.timeout.connect(self.updateBar)
        self.progressTimer.start(1000)

    def closeEvent(self, event):
        os.remove('running.lock')

    def updateBar(self):
        if self.__i < self.__numPacks:
            self.ui.progressBar.setValue((self.__i+1)*10)
            self.__i += 1
        else:
            self.progressTimer.stop()
            self.showInfo()

    def ping(self):
        if self.__os == 'windows':
            self.__output = Popen("ping -n 10 8.8.8.8", shell=PIPE, stdin=PIPE, stdout=PIPE, stderr=PIPE).stdout.read()
        if self.__os == 'linux':
            self.__output = Popen("ping -c 10 8.8.8.8", shell=PIPE, stdin=PIPE, stdout=PIPE, stderr=PIPE).stdout.read()

    def showInfo(self):
        self.ui.label.hide()
        self.ui.progressBar.hide()
        output = self.__output.decode('utf-8')

        if self.__os == 'windows':
            sent_packets = re.search(r'Sent = (\d+)', output)
            received_packets = re.search(r'Received = (\d+)', output)
            loss_percentage = re.search(r'Lost = (\d+)', output)
            sent = int(sent_packets.group(1))
            received = int(received_packets.group(1))
            loss = int(loss_percentage.group(1))

        if self.__os == 'linux':
            sent_packets = re.search(r'(\d+) packets transmitted', output)
            received_packets = re.search(r'(\d+) received', output)
            loss_percentage = re.search(r'(\d+)% packet loss', output)
            sent = int(sent_packets.group(1))
            received = int(received_packets.group(1))
            loss = int(loss_percentage.group(1))

        self.ui.sentLabel = QLabel(self.ui.centralwidget)
        self.ui.sentLabel.setText(f"Sent packets: {sent}")
        self.ui.sentLabel.setAlignment(Qt.AlignCenter)
        self.ui.sentLabel.setObjectName('sentLabel')

        self.ui.receivedLabel = QLabel(self.ui.centralwidget)
        self.ui.receivedLabel.setText(f"Received packets: {received}")
        self.ui.receivedLabel.setAlignment(Qt.AlignCenter)
        self.ui.receivedLabel.setObjectName('receivedLabel')

        self.ui.lossLabel = QLabel(self.ui.centralwidget)
        self.ui.lossLabel.setText(f"Loss percentage: {loss}%")
        self.ui.lossLabel.setAlignment(Qt.AlignCenter)
        self.ui.lossLabel.setObjectName('lossLabel')

        self.ui.gridlayout.addWidget(self.ui.sentLabel, 0, 0, 1, 1)
        self.ui.gridlayout.addWidget(self.ui.receivedLabel, 1, 0, 1, 1)
        self.ui.gridlayout.addWidget(self.ui.lossLabel, 2, 0, 1, 1)

