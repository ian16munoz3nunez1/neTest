from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView
from ui_netping import Ui_NetPing
import threading
import requests
import platform
import re
import os
from time import sleep
from subprocess import Popen, PIPE
from qroundprogressbar import QRoundProgressBar

class NetPing(QMainWindow):
    def __init__(self):
        super(NetPing, self).__init__()
        self.ui = Ui_NetPing()
        self.ui.setupUi(self)

        self.__os = platform.system().lower()
        self.__output = ''
        self.__i = 0
        self.__numPacks = 10
        self.__end = False
        self.__cancel = False

        hilo1 = threading.Thread(target=self.ping)
        hilo2 = threading.Thread(target=self.downloadDummy)
        hilo1.start()
        hilo2.start()

        self.progressTimer = QTimer()
        self.progressTimer.timeout.connect(self.updateBar)
        self.progressTimer.start(1100)

    def closeEvent(self, event):
        self.__cancel = True
        os.remove('dummy.bin')
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
            self.__output = Popen("ping -w 1000 -n 10 8.8.8.8", shell=PIPE, stdin=PIPE, stdout=PIPE, stderr=PIPE).stdout.read()
        if self.__os == 'linux':
            self.__output = Popen("ping -W 1 -c 10 8.8.8.8", shell=PIPE, stdin=PIPE, stdout=PIPE, stderr=PIPE).stdout.read()

        self.__end = True

    def downloadDummy(self):
        with requests.get("https://testfile.org/files-5GB-zip", stream=True) as req:
            req.raise_for_status()
            with open("dummy.bin", 'wb') as file:
                i = 0
                for chunk in req.iter_content(chunk_size=4096):
                    if self.__end or self.__cancel:
                        break
                    print(f"Downloading chunk number {i}")
                    file.write(chunk)
                    i += 1
            file.close()
        print("Download finished")

    def showInfo(self):
        try:
            self.ui.label.hide()
            self.ui.progressBar.hide()
            output = self.__output.decode('utf-8')

            if self.__os == 'windows':
                sent_packets = re.search(r'Sent = (\d+)', output)
                received_packets = re.search(r'Received = (\d+)', output)
                loss_percentage = re.search(r'Lost = (\d+)', output)
                min_time = re.search(r'Minimum = (\d+)ms', output)
                max_time = re.search(r'Maximum = (\d+)ms', output)
                avg_time = re.search(r'Average = (\d+)ms', output)
                sent = int(sent_packets.group(1))
                received = int(received_packets.group(1))
                loss = int(loss_percentage.group(1))
                min_latency = float(min_time.group(1))
                max_latency = float(max_time.group(1))
                avg_latency = float(avg_time.group(1))

            if self.__os == 'linux':
                sent_packets = re.search(r'(\d+) packets transmitted', output)
                received_packets = re.search(r'(\d+) received', output)
                loss_percentage = re.search(r'(\d+)% packet loss', output)
                min_time = re.search(r'rtt min/avg/max/mdev = (\d{2,3}\.\d{2,3})/\d{2,3}\.\d{2,3}/\d{2,3}\.\d{2,3}', output)
                avg_time = re.search(r'rtt min/avg/max/mdev = \d{2,3}\.\d{2,3}/(\d{2,3}\.\d{2,3})/\d{2,3}\.\d{2,3}', output)
                max_time = re.search(r'rtt min/avg/max/mdev = \d{2,3}\.\d{2,3}/\d{2,3}\.\d{2,3}/(\d{2,3}\.\d{2,3})', output)
                sent = int(sent_packets.group(1))
                received = int(received_packets.group(1))
                loss = int(loss_percentage.group(1))
                min_latency = float(min_time.group(1))
                avg_latency = float(avg_time.group(1))
                max_latency = float(avg_time.group(1))

        except Exception as e:
            QMessageBox.critical(
                self,
                "Connection error",
                "Unable to connect to internet"
            )

        self.ui.widget = QWidget(self.ui.centralwidget)
        self.ui.widget.setFixedSize(200, 200)
        self.ui.widget.setObjectName('widget')
        self.ui.widgetGrid = QGridLayout(self.ui.widget)
        self.ui.widgetGrid.setObjectName('widgetGrid')
        self.ui.widget.setLayout(self.ui.widgetGrid)

        self.ui.roundProgressBar = QRoundProgressBar(self.ui.widget)
        self.ui.roundProgressBar.setValue(sent, received, loss)
        self.ui.widgetGrid.addWidget(self.ui.roundProgressBar)

        self.ui.latencyTable = QTableWidget(self.ui.centralwidget)
        self.ui.latencyTable.setRowCount(3)
        self.ui.latencyTable.setColumnCount(2)
        self.ui.latencyTable.setHorizontalHeaderLabels(['Latencia', 'Estado'])
        self.ui.latencyTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.addLatencyResult(0, "Mínima", min_latency)
        self.addLatencyResult(1, "Máxima", max_latency)
        self.addLatencyResult(2, "Promedio", avg_latency)

        self.ui.gridlayout.addWidget(self.ui.widget, 0, 0, 1, 1)
        self.ui.gridlayout.addWidget(self.ui.latencyTable, 1, 0, 1, 1)

    def addLatencyResult(self, row, label, latency):
        """ Agrega los resultados de la latencia a la tabla """
        self.ui.latencyTable.setItem(row, 0, QTableWidgetItem(f"{label}: {latency} ms"))

        # Evaluación del estado de la latencia con colores
        if latency < 20:
            status = "Excelente"
            color = QColor(0, 255, 0)  # Verde
        elif 20 <= latency < 100:
            status = "Buena"
            color = QColor(0, 255, 0)  # Verde
        elif 100 <= latency < 200:
            status = "Regular"
            color = QColor(255, 255, 0)  # Amarillo
        else:
            status = "Mala"
            color = QColor(255, 0, 0)  # Rojo

        # Crear celda con el estado y colorearla
        item = QTableWidgetItem(status)
        item.setBackground(color)
        self.ui.latencyTable.setItem(row, 1, item)

