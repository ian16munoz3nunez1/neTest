from PyQt5.QtWidgets import QMainWindow
from ui_netping import Ui_NetPing

class NetPing(QMainWindow):
    def __init__(self):
        super(NetPing, self).__init__()
        self.ui = Ui_NetPing()
        self.ui.setupUi(self)

