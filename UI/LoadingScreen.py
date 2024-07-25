from PyQt5 import QtCore, QtGui, QtWidgets
from sface import *


class LoadingScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Ẩn tiêu đề và khung viền cửa sổ
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Cài đặt nền trong suốt
        self.setFixedSize(800, 600)  # Kích thước cố định cho cửa sổ
        self.setWindowIcon(QtGui.QIcon('../icons/logo.png'))

        # Tạo QLabel để hiển thị GIF
        self.gif_label = QtWidgets.QLabel(self)

        # Load GIF
        movie = QtGui.QMovie("icons/facerecog.gif")
        self.gif_label.setMovie(movie)
        movie.start()

        self.timer = QtCore.QTimer(self)
        self.timer.singleShot(movie.frameCount() * movie.nextFrameDelay(), self.showMainUI)

        self.centerWindow()

    def centerWindow(self):
        screen_geometry = QtWidgets.QDesktopWidget().screenGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def showMainUI(self):
        QtCore.QTimer.singleShot(1000, self.transitionToMainUI)

    def transitionToMainUI(self):
        from common import Ui_MainWindow
        self.main_window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)
        self.main_window.showMaximized()
        self.close()
