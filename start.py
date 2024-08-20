from PyQt5.QtWidgets import QMainWindow
from ui_start import Ui_Start
from ui_netping import Ui_NetPing
from netping import NetPing

class Start(QMainWindow):
    def __init__(self):
        super(Start, self).__init__()
        self.ui = Ui_Start()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.runPing)

    def runPing(self):
        self.close()
        self.netPing = NetPing()
        self.ui_netping = Ui_NetPing()
        self.ui_netping.setupUi(self.netPing)
        self.netPing.show()

