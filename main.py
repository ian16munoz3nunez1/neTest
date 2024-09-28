import sys
import os
from PyQt5.QtWidgets import QApplication
from start import Start
from netping import NetPing

app = QApplication(sys.argv)
app.setStyleSheet(
"""
QWidget {
    background-color: rgb(100, 100, 100);
}
QLabel {
    font: 12pt 'monospace';
    color: white;
}
QPushButton {
    font: 12pt 'monospace';
    color: white;
    background-color: rgb(40, 40, 40);
    max-height: 30px;
    border: 1px;
    border-style: solid;
    border-color: rgb(0, 100, 0);
    border-radius: 15px;
}

QPushButton:hover {
    background-color: rgb(0, 200, 0);
}

QPushButton:pressed {
    background-color: rgb(0, 180, 0);
}
"""
)

running = 'running.lock'
if os.path.isfile(running):
    with open(running, 'r') as file:
        content = file.read()
    file.close()

    if content == 'netping':
        netPing = NetPing()
        netPing.show()

else:
    with open(running, 'w') as file:
        file.write("running")
    file.close()

    start = Start()

    start.show()

sys.exit(app.exec_())

