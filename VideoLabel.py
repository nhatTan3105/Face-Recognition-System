from PyQt5 import QtWidgets
from sface import *


class VideoLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(VideoLabel, self).__init__(parent)

    def setPixmap(self, pixmap):
        super().setPixmap(pixmap)
        self.setScaledContents(True)
