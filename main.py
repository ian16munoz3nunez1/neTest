import sys
import os
from PyQt5.QtWidgets import QApplication
from start import Start
from netping import NetPing

app = QApplication(sys.argv)

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

