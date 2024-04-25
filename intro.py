from PyQt5 import QtCore, QtGui, QtWidgets

class LoadingScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Ẩn tiêu đề và khung viền cửa sổ
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Cài đặt nền trong suốt
        self.setFixedSize(800, 600)  # Kích thước cố định cho cửa sổ

        # Tạo QLabel để hiển thị GIF
        self.gif_label = QtWidgets.QLabel(self)

        # Load GIF
        movie = QtGui.QMovie("icons/facerecog.gif")
        self.gif_label.setMovie(movie)
        movie.start()

        # Tạo QTimer để chuyển đến UI chính sau khi GIF kết thúc
        self.timer = QtCore.QTimer(self)
        self.timer.singleShot(movie.frameCount() * movie.nextFrameDelay(), self.showMainUI)

        # Đặt cửa sổ vào trung tâm màn hình
        self.centerWindow()

    def centerWindow(self):
        # Lấy kích thước của màn hình
        screen_geometry = QtWidgets.QDesktopWidget().screenGeometry()
        # Lấy kích thước của cửa sổ
        window_geometry = self.frameGeometry()
        # Đặt cửa sổ vào trung tâm của màn hình
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def showMainUI(self):
        # Chờ 1 giây trước khi chuyển đến UI chính
        QtCore.QTimer.singleShot(1000, self.transitionToMainUI)

    def transitionToMainUI(self):
        from main import Ui_MainWindow  # Import UI chính từ file main.py
        self.main_window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)
        self.main_window.showMaximized()
        self.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    loading_screen = LoadingScreen()
    loading_screen.show()
    sys.exit(app.exec_())
