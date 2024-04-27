import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from sface import *

class VideoLabel(QLabel):
    def __init__(self, parent=None):
        super(VideoLabel, self).__init__(parent)

    def setPixmap(self, pixmap):
        super().setPixmap(pixmap)
        self.setScaledContents(True)

class WebcamApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initWebcam()

    def initUI(self):
        self.setWindowTitle('Webcam Stream with PyQt5')
        self.setGeometry(100, 100, 800, 600)
        self.label = VideoLabel(self)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def initWebcam(self):
        directory = 'data'
        # Init models face detection & recognition
        weights = os.path.join(directory, "models",
                            "face_detection_yunet_2022mar.onnx")
        face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))
        face_detector.setScoreThreshold(0.87)

        weights = os.path.join(directory, "models", "face_recognizer_fast.onnx")
        face_recognizer = cv2.FaceRecognizerSF_create(weights, "")
        # create a database connection
        
        with open('data_embeddings.pkl', 'rb') as f:
            dictionary = pickle.load(f)
        self.capture = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.updateFrame(dictionary, face_detector, face_recognizer))
        self.timer.start(150)  # cập nhật frame mỗi 20 ms

    def updateFrame(self, dictionary, face_detector, face_recognizer):
        ret, frame = self.capture.read()
        if ret:
            # Giảm kích thước khung hình đầu vào
            #frame = cv2.resize(frame, (320, 240))  # Đặt kích thước mới là 640x480

            frame, name = detect_and_draw_labels(dictionary, frame, face_detector, face_recognizer)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(1200, 800, aspectRatioMode=Qt.KeepAspectRatio)
            self.label.setPixmap(QPixmap.fromImage(p))
    def closeEvent(self, event):
        self.capture.release()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WebcamApp()
    ex.show()
    sys.exit(app.exec_())
