import sys
from PyQt5.QtWidgets import QApplication
from start import Start

app = QApplication(sys.argv)

start = Start()

start.show()

sys.exit(app.exec_())

