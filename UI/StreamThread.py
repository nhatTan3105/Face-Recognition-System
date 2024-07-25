from PyQt5 import QtGui
import cv2
from sface import *
from PyQt5.QtCore import QThread, pyqtSignal, QTimer


class StreamThread(QThread):
    updatePixmap = pyqtSignal(QtGui.QPixmap)

    def __init__(self, url, parent=None):
        super(StreamThread, self).__init__(parent)
        self.url = url
        self.active = True
        self.cap = cv2.VideoCapture(self.url)
        self.timer = QTimer()
        self.timer.moveToThread(self.thread())  # Đảm bảo QTimer được tạo trong luồng chính
        self.timer.timeout.connect(self.read_frame)

    def run(self):
        QTimer.singleShot(0, self.start_timer)  # Khởi động QTimer trong luồng chính

    def start_timer(self):
        self.timer.start(100)  # Đọc khung hình mỗi 30 ms

    def read_frame(self):
        if self.active:
            ret, frame = self.cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                q_img = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(q_img)
                self.updatePixmap.emit(pixmap)

    def stop(self):
        self.active = False
        self.timer.stop()
        self.cap.release()
