from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class QRoundProgressBar(QWidget):
    def __init__(self, widget):
        super(QRoundProgressBar, self).__init__()

        self.mainFrame = QFrame(widget)
        self.mainFrame.setFixedSize(200, 200)
        self.mainFrame.setStyleSheet("""background-color: rgb(100, 100, 100);
        border-radius: 10px;""")
        self.mainFrame.setObjectName('frame')
        self.mainFrameGrid = QGridLayout(self.mainFrame)
        self.mainFrameGrid.setContentsMargins(0, 50, 0, 50)
        self.mainFrameGrid.setObjectName('mainFrameGrid')
        self.mainFrame.setLayout(self.mainFrameGrid)

        self.roundProgressBar = QFrame(self.mainFrame)
        self.roundProgressBar.setGeometry(QRect(5, 5, 190, 190))
        self.roundProgressBar.setStyleSheet("""border-radius: 95px;
        background-color: qconicalgradient(cx:0.5, cy:0.5, angle:-90,
        stop: 0.999 rgba(0, 255, 0, 100), stop: 1.0 rgba(0, 255, 0, 255));""")
        self.roundProgressBar.setObjectName('roundProgressBar')

        self.backFrame = QFrame(self.mainFrame)
        self.backFrame.setGeometry(QRect(20, 20, 160, 160))
        self.backFrame.setStyleSheet("""border-radius: 80px;
        background-color: rgb(100, 100, 100);""")
        self.backFrame.setObjectName('backFrame')

        self.lSent = QLabel(self.mainFrame)
        self.lSent.setAlignment(Qt.AlignCenter)
        self.lSent.setCursor(Qt.IBeamCursor)
        self.lSent.setFixedSize(120, 30)
        self.lSent.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse|Qt.TextSelectableByKeyboard)
        self.lSent.setStyleSheet(
        """
        border-radius: 15px;
        """
        )
        self.lSent.setObjectName('lSent')

        self.lReceived = QLabel(self.mainFrame)
        self.lReceived.setAlignment(Qt.AlignCenter)
        self.lReceived.setCursor(Qt.IBeamCursor)
        self.lReceived.setTextInteractionFlags(Qt.LinksAccessibleByMouse | Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        self.lReceived.setFixedSize(120, 30)
        self.lReceived.setStyleSheet(
        """
        background-color: rgb(0, 255, 0);
        border: 1px;
        border-style: solid;
        border-color: rgb(0, 255, 0);
        border-radius: 15px;
        """
        )
        self.lReceived.setObjectName('lReceived')

        self.lLoss = QLabel(self.mainFrame)
        self.lLoss.setAlignment(Qt.AlignCenter)
        self.lLoss.setCursor(Qt.IBeamCursor)
        self.lLoss.setTextInteractionFlags(Qt.LinksAccessibleByMouse | Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        self.lLoss.setFixedSize(120, 30)
        self.lLoss.setStyleSheet(
        """
        background-color: rgb(255, 0, 0);
        border: 1px;
        border-style: solid;
        border-color: rgb(255, 0, 0);
        border-radius: 15px;
        """
        )
        self.lLoss.setObjectName('lLoss')

        self.mainFrameGrid.addWidget(self.lSent, 0, 0, 1, 1)
        self.mainFrameGrid.addWidget(self.lReceived, 1, 0, 1, 1)
        self.mainFrameGrid.addWidget(self.lLoss, 2, 0, 1, 1)

    def setValue(self, sent, received, loss):
        self.lSent.setText(f"Sent: {sent}")
        self.lReceived.setText(f"Received: {received}")
        self.lLoss.setText(f"Loss: {loss}%")
        value = round(received/10, 3)

        if value == 1.0:
            stop1 = "1.0"
            stop2 = "1.0"
        else:
            value = 1.0-value
            stop1 = str(round(value-0.001, 3))
            stop2 = str(round(value, 3))

        style = """border-radius: 95px;
        background-color: qconicalgradient(cx:0.5, cy:0.5, angle:-90,
        stop: {stop1} rgba(255, 0, 0, 255), stop: {stop2} rgba(0, 255, 0, 255));"""
        style = style.replace("{stop1}", stop1).replace("{stop2}", stop2)
        self.roundProgressBar.setStyleSheet(style)

