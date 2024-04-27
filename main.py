from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import sys
import datetime
import pickle
import os 
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import QTimer, Qt
from sface import *
import shutil



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
        #from main import Ui_MainWindow  # Import UI chính từ file main.py
        self.main_window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)
        self.main_window.showMaximized()
        self.close()

class VideoLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(VideoLabel, self).__init__(parent)

    def setPixmap(self, pixmap):
        super().setPixmap(pixmap)
        self.setScaledContents(True)

class CCTV(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("CCTV")
        MainWindow.setWindowIcon(QtGui.QIcon('icons/logo.png'))
        # Tính toán kích thước màn hình
        screen = QtWidgets.QApplication.primaryScreen().size()
        width = screen.width()
        height = screen.height()

        # Thiết lập kích thước và vị trí của cửa sổ
        MainWindow.resize(width, height)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 30, 1850, 900))
        self.widget.setObjectName("widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnBack = QtWidgets.QPushButton(self.widget)
        self.btnBack.setObjectName("btnBack")
        self.btnBack.setFixedSize(100, 25)
        self.btnBack.clicked.connect(lambda: self.back(MainWindow))
        self.btnBack.setStyleSheet("background-color: #cccccc;")
        self.verticalLayout.addWidget(self.btnBack)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtURL_1 = QtWidgets.QLabel(self.widget)
        self.txtURL_1.setObjectName("txtURL_1")
        self.horizontalLayout.addWidget(self.txtURL_1)
        self.inputURL_1 = QtWidgets.QLineEdit(self.widget)
        self.inputURL_1.setObjectName("inputURL_1")
        self.horizontalLayout.addWidget(self.inputURL_1)
        self.btnStart_1 = QtWidgets.QPushButton(self.widget)
        self.btnStart_1.setObjectName("btnStart_1")
        self.btnStart_1.clicked.connect(self.toggle_stream_1)
        self.btnStart_1.setStyleSheet("background-color: #52c9a2;")
        self.horizontalLayout.addWidget(self.btnStart_1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.scrollArea_1 = QtWidgets.QScrollArea(self.widget)
        self.scrollArea_1.setWidgetResizable(True)
        self.scrollArea_1.setObjectName("scrollArea_1")
        self.scrollAreaWidgetContents = VideoLabel()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 503, 293))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea_1.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea_1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.txtURL_2 = QtWidgets.QLabel(self.widget)
        self.txtURL_2.setObjectName("txtURL_2")
        self.horizontalLayout_2.addWidget(self.txtURL_2)
        self.inputURL_2 = QtWidgets.QLineEdit(self.widget)
        self.inputURL_2.setObjectName("inputURL_2")
        self.horizontalLayout_2.addWidget(self.inputURL_2)
        self.btnStart_2 = QtWidgets.QPushButton(self.widget)
        self.btnStart_2.setObjectName("btnStart_2")
        self.btnStart_2.clicked.connect(self.toggle_stream_2)
        self.btnStart_2.setStyleSheet("background-color: #52c9a2;")
        self.horizontalLayout_2.addWidget(self.btnStart_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.widget)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = VideoLabel()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 503, 293))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout.addWidget(self.scrollArea_2)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.txtStdID = QtWidgets.QLabel(self.widget)
        self.txtStdID.setObjectName("txtStdID")
        self.horizontalLayout_3.addWidget(self.txtStdID)
        self.inputStudentID = QtWidgets.QLineEdit(self.widget)
        self.inputStudentID.setObjectName("inputStudentID")
        self.horizontalLayout_3.addWidget(self.inputStudentID)
        self.btnSearch = QtWidgets.QPushButton(self.widget)
        self.btnSearch.setObjectName("btnSearch")
        self.btnSearch.clicked.connect(lambda: self.search(str(self.inputStudentID.text())))
        self.btnSearch.setStyleSheet("background-color: #85c9e8;")
        self.horizontalLayout_3.addWidget(self.btnSearch)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['MSSV', 'Name', 'Image', 'DateTime', 'Localtion'])
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1080, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.stream1_active = False
        self.stream2_active = False
        self.search_press = False
        self.add_data_1 = False
        self.add_data_2 = False

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CCTV"))
        self.btnBack.setText(_translate("MainWindow", "Back"))
        self.txtURL_1.setText(_translate("MainWindow", "Camera IP 1:"))
        self.btnStart_1.setText(_translate("MainWindow", "Start"))
        self.txtURL_2.setText(_translate("MainWindow", "Camera IP 2:"))
        self.btnStart_2.setText(_translate("MainWindow", "Start"))
        self.txtStdID.setText(_translate("MainWindow", "Student ID:"))
        self.btnSearch.setText(_translate("MainWindow", "Search"))

    
    # def add_data_to_table_1(self, data):
    #     row_position = self.tableWidget.rowCount()
    #     self.tableWidget.insertRow(row_position)
    #     item = QtWidgets.QTableWidgetItem('Camera 1')
    #     self.tableWidget.setItem(row_position, 4, item)
    #     for col, value in enumerate(data):
    #         item = QtWidgets.QTableWidgetItem()
    #         if col == 2:  # Image column
    #             imageLabel = self.getImageLabel(value)
    #             self.tableWidget.setCellWidget(row_position, col, imageLabel)
                
    #         else:
    #             item.setText(value)
    #             self.tableWidget.setItem(row_position, col, item)
            
            
    #     self.tableWidget.resizeRowsToContents()
    # def add_data_to_table_2(self, data):
        # row_position = self.tableWidget.rowCount()
        # self.tableWidget.insertRow(row_position)
        # item = QtWidgets.QTableWidgetItem('Camera 2')
        # self.tableWidget.setItem(row_position, 4, item)
        # for col, value in enumerate(data):
        #     item = QtWidgets.QTableWidgetItem()
        #     if col == 2:  # Image column
        #         imageLabel = self.getImageLabel(value)
        #         self.tableWidget.setCellWidget(row_position, col, imageLabel)
        #     else:
        #         item.setText(value)
        #         self.tableWidget.setItem(row_position, col, item)
                   
        # self.tableWidget.resizeRowsToContents()

    def getImageLabel(self, image):
        imageLabel = QtWidgets.QLabel()
        imageLabel.setText("")
        imageLabel.setScaledContents(True)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(bytes(image))
        imageLabel.setPixmap(pixmap)
        return imageLabel
    def add_localtion(self, data):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        for col, value in enumerate(data):
            item = QtWidgets.QTableWidgetItem()
            if col == 2:  # Image column
                imageLabel = self.getImageLabel(value)
                self.tableWidget.setCellWidget(row_position, col, imageLabel)
            else:
                item.setText(value)
                self.tableWidget.setItem(row_position, col, item)
        self.tableWidget.resizeRowsToContents()
    def add_data_to_table(self, data, camera_string):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        item = QtWidgets.QTableWidgetItem(camera_string)
        self.tableWidget.setItem(row_position, 4, item)
        for col, value in enumerate(data):
            item = QtWidgets.QTableWidgetItem()
            if col == 2:  # Image column
                imageLabel = self.getImageLabel(value)
                self.tableWidget.setCellWidget(row_position, col, imageLabel)
            else:
                item.setText(value)
                self.tableWidget.setItem(row_position, col, item)
        self.tableWidget.resizeRowsToContents()

    def toggle_stream_1(self):
        if(self.inputURL_1.text() != ''):
            if not self.stream1_active:
                url = self.inputURL_1.text()
                if type(self.inputURL_1.text()) is str and len(self.inputURL_1.text()) == 1:
                    self.cap1 = cv2.VideoCapture(int(self.inputURL_1.text()))
                else:
                    self.cap1 = cv2.VideoCapture(url)
                self.btnStart_1.setText("Stop")
                self.btnStart_1.setStyleSheet("background-color: #f36666;")
                self.stream1_active = True
                self.stream1()
            else:
                self.cap1.release()
                self.scrollAreaWidgetContents.clear()  # Clear the pixmap
                self.btnStart_1.setText("Start")
                self.btnStart_1.setStyleSheet("background-color: #52c9a2;")
                self.stream1_active = False
        else:
            QMessageBox.warning(None, "Thông báo", "Vui lòng điền IP của Camera")
    def toggle_stream_2(self):
        if(self.inputURL_2.text() != ''):
            if not self.stream2_active:
                url = self.inputURL_2.text()
                if type(self.inputURL_2.text()) is str and len(self.inputURL_2.text()) == 1:
                    self.cap2 = cv2.VideoCapture(int(self.inputURL_2.text()))
                else:
                    self.cap2 = cv2.VideoCapture(url)
                self.btnStart_2.setText("Stop")
                self.btnStart_2.setStyleSheet("background-color: #f36666;")
                self.stream2_active = True
                self.stream2()
            else:
                self.cap2.release()
                self.scrollAreaWidgetContents_2.clear()  # Clear the pixmap
                self.btnStart_2.setText("Start")
                self.btnStart_2.setStyleSheet("background-color: #52c9a2;")
                self.stream2_active = False
        else:
            QMessageBox.warning(None, "Thông báo", "Vui lòng điền IP của Camera")
    def stream1(self):
        database = r"database.db"
        conn = create_connection(database)
        directory = 'data'
        # Init models face detection & recognition
        weights = os.path.join(directory, "models", "face_detection_yunet_2022mar.onnx")
        face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))
        face_detector.setScoreThreshold(0.87)
        weights = os.path.join(directory, "models", "face_recognizer_fast.onnx")
        face_recognizer = cv2.FaceRecognizerSF_create(weights, "")
        # create a database connection
        with open('data_embeddings.pkl', 'rb') as f:
            dictionary = pickle.load(f)

        self.timer1 = QTimer()
        self.timer1.timeout.connect(lambda: self.updateFrame_1(conn, dictionary, face_detector, face_recognizer, 'Camera 1'))
        self.timer1.start(60)

    def stream2(self):
        database = r"database.db"
        conn = create_connection(database)
        directory = 'data'
        # Init models face detection & recognition
        weights = os.path.join(directory, "models", "face_detection_yunet_2022mar.onnx")
        face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))
        face_detector.setScoreThreshold(0.87)
        weights = os.path.join(directory, "models", "face_recognizer_fast.onnx")
        face_recognizer = cv2.FaceRecognizerSF_create(weights, "")
        # create a database connection
        with open('data_embeddings.pkl', 'rb') as f:
            dictionary = pickle.load(f)

        self.timer1 = QTimer()
        self.timer1.timeout.connect(lambda: self.updateFrame_2(conn, dictionary, face_detector, face_recognizer, 'Camera 2'))
        self.timer1.start(60)

    def updateFrame_1(self, conn, dictionary, face_detector, face_recognizer, camera_string):
        ret, frame = self.cap1.read()
        if ret:
            frame, name = detect_and_draw_labels(dictionary, frame, face_detector, face_recognizer)
            if name is not None:
                if self.add_data_1 == False:
                    data = select_student_by_studentID(conn, name)
                    for data in data:
                        self.add_data_to_table([data[0].__str__(), data[1].__str__(), data[4], datetime.datetime.now().__str__()], camera_string)
                        self.add_data_1 = True
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            q_img = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(q_img)
            self.scrollAreaWidgetContents.setPixmap(pixmap)
            QtWidgets.QApplication.processEvents()  # Để đảm bảo cập nhật giao diện người dùng
    
    def updateFrame_2(self, conn, dictionary, face_detector, face_recognizer, camera_string):
        ret, frame = self.cap2.read()
        if ret:
            frame, name = detect_and_draw_labels(dictionary, frame, face_detector, face_recognizer)
            if name is not None:
                if self.add_data_2 == False:
                    data = select_student_by_studentID(conn, name)
                    for data in data:
                        self.add_data_to_table([data[0].__str__(), data[1].__str__(), data[4], datetime.datetime.now().__str__()], camera_string)
                        self.add_data_2 = True
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            q_img = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(q_img)
            self.scrollAreaWidgetContents_2.setPixmap(pixmap)
            QtWidgets.QApplication.processEvents()  # Để đảm bảo cập nhật giao diện người dùng            
    
    #def stream2(self):
        # count = 0
        # database = r"database.db"
        # conn = create_connection(database)
        # directory = 'data'
        # # Init models face detection & recognition
        # weights = os.path.join(directory, "models",
        #                     "face_detection_yunet_2022mar.onnx")
        # face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))
        # face_detector.setScoreThreshold(0.87)

        # weights = os.path.join(directory, "models", "face_recognizer_fast.onnx")
        # face_recognizer = cv2.FaceRecognizerSF_create(weights, "")
        # # create a database connection
        
        # with open('data_embeddings.pkl', 'rb') as f:
        #     dictionary = pickle.load(f)
        # while self.stream2_active:
        #     ret, frame = self.cap2.read()      
        #     if ret:
        #             frame, name = detect_and_draw_labels(dictionary, frame, face_detector, face_recognizer)
                    
        #             if name is not None and count==0:
        #                 count+=1
        #                 data = select_student_by_studentID(conn, name)
        #                 for data in data:
        #                     self.add_data_to_table_2([data[0].__str__(), data[1].__str__(), data[4], datetime.datetime.now().__str__()])
                            
        #             rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #             h, w, ch = rgb_image.shape
        #             bytes_per_line = ch * w
        #             q_img = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        #             pixmap = QtGui.QPixmap.fromImage(q_img)
        #             self.scrollAreaWidgetContents_2.setPixmap(pixmap)
        #             QtWidgets.QApplication.processEvents()  # Để đảm bảo cập nhật giao diện người dùng
        #     else:
                #break
    # cctv.py
    def back(self, MainWindow):
        # Tạo một instance của giao diện
        self.another_gui_instance = Ui_MainWindow()
        self.stream1_active = False
        self.stream2_active = False
        # Hiển thị giao diện
        self.another_gui_instance.setupUi(MainWindow)

    def search(self, s):
        if s != '':
            if not self.search_press:
                for row in range(self.tableWidget.rowCount()):
                    item = self.tableWidget.item(row, 0)  # Chỉ tìm kiếm ở cột đầu tiên
                    if item:
                        text = item.text().lower()
                        if s.lower() in text:
                            self.tableWidget.setRowHidden(row, False)  # Hiển thị mục nếu chứa chuỗi tìm kiếm
                        else:
                            self.tableWidget.setRowHidden(row, True)   # Ẩn mục nếu không chứa chuỗi tìm kiếm
                self.btnSearch.setText("Reset")
                self.search_press = True
            else:
                self.showAllItems()
                self.btnSearch.setText("Search")
                self.inputStudentID.clear()
                self.search_press = False
                return
        else:
            QMessageBox.warning(None, "Thông báo", "Vui lòng điền Student ID")

            
    def showAllItems(self):
        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHidden(row, False)  # Hiển thị tất cả các hàng

class Check(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Check")
        screen = QtWidgets.QApplication.primaryScreen().size()
        width = screen.width()
        height = screen.height()
        MainWindow.resize(width, height)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(30, 10, 1820, 980))
        self.widget.setObjectName("widget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnBack = QtWidgets.QPushButton(self.widget)
        self.btnBack.setObjectName("btnBack")
        self.btnBack.clicked.connect(lambda: self.back(MainWindow))
        self.btnBack.setStyleSheet("background-color: #cccccc;")
        self.horizontalLayout.addWidget(self.btnBack)
        self.txtURL_1 = QtWidgets.QLabel(self.widget)
        self.txtURL_1.setObjectName("txtURL_1")
        self.horizontalLayout.addWidget(self.txtURL_1)
        self.url_1 = QtWidgets.QLineEdit(self.widget)
        self.url_1.setObjectName("url_1")
        self.horizontalLayout.addWidget(self.url_1)
        self.btnStart_1 = QtWidgets.QPushButton(self.widget)
        self.btnStart_1.setObjectName("btnStart_1")
        self.btnStart_1.setStyleSheet("background-color: #52c9a2;")
        self.btnStart_1.clicked.connect(self.toggle_stream_1)
        self.horizontalLayout.addWidget(self.btnStart_1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.scrollArea_1 = QtWidgets.QScrollArea(self.widget)
        self.scrollArea_1.setWidgetResizable(True)
        self.scrollArea_1.setObjectName("scrollArea_1")
        self.scrollAreaWidgetContents = VideoLabel()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 617, 593))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea_1.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea_1)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.txtURL_2 = QtWidgets.QLabel(self.widget)
        self.txtURL_2.setObjectName("txtURL_2")
        self.horizontalLayout_2.addWidget(self.txtURL_2)
        self.url_2 = QtWidgets.QLineEdit(self.widget)
        self.url_2.setObjectName("url_2")
        self.horizontalLayout_2.addWidget(self.url_2)
        self.btnStart_2 = QtWidgets.QPushButton(self.widget)
        self.btnStart_2.setObjectName("btnStart_2")
        self.btnStart_2.setStyleSheet("background-color: #52c9a2;")
        self.btnStart_2.clicked.connect(self.toggle_stream_2)
        self.horizontalLayout_2.addWidget(self.btnStart_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.widget)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = VideoLabel()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 616, 593))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.addWidget(self.scrollArea_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lbStudentID = QtWidgets.QLabel(self.widget)
        self.lbStudentID.setObjectName("lbStudentID")
        self.verticalLayout_3.addWidget(self.lbStudentID)
        self.inputStudentID = QtWidgets.QLineEdit(self.widget)
        self.inputStudentID.setObjectName("inputStudentID")
        self.verticalLayout_3.addWidget(self.inputStudentID)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.imagePath = QtWidgets.QLabel(self.widget)
        self.imagePath.setObjectName("imagePath")
        self.verticalLayout_3.addWidget(self.imagePath)
        self.imge_input = QtWidgets.QLabel(self.widget)
        self.imge_input.setFrameShape(QtWidgets.QFrame.Box)
        self.imge_input.setText("")
        self.imge_input.setObjectName("imge_input")
        self.imge_input.setFixedSize(150, 150)
        self.imge_input.setScaledContents(True)
        self.verticalLayout_3.addWidget(self.imge_input, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.btnLoadImage = QtWidgets.QPushButton(self.widget)
        self.btnLoadImage.setObjectName("btnLoadImage")
        self.btnLoadImage.clicked.connect(self.linkto)
        self.btnLoadImage.setStyleSheet("background-color: #85c9e8;")
        self.verticalLayout_3.addWidget(self.btnLoadImage, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.btnCheck = QtWidgets.QPushButton(self.widget)
        self.btnCheck.setObjectName("btnCheck")
        self.btnCheck.setStyleSheet("background-color: #52c9a2;")
        self.btnCheck.setFixedSize(100, 40)
        self.btnCheck.clicked.connect(lambda: self.recognize_image_check(self.imagePath.text(), self.inputStudentID.text()))
        self.verticalLayout_3.addWidget(self.btnCheck, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.stdInfo = QtWidgets.QLabel(self.widget)
        self.stdInfo.setObjectName("stdInfo")
        self.verticalLayout_4.addWidget(self.stdInfo)
        self.image_output = QtWidgets.QLabel(self.widget)
        self.image_output.setFrameShape(QtWidgets.QFrame.Box)
        self.image_output.setText("")
        self.image_output.setObjectName("image_output")
        self.image_output.setFixedSize(150, 150)
        self.image_output.setScaledContents(True)
        self.verticalLayout_4.addWidget(self.image_output, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.lbStudentID_2 = QtWidgets.QLabel(self.widget)
        self.lbStudentID_2.setObjectName("lbStudentID_2")
        self.verticalLayout_4.addWidget(self.lbStudentID_2)
        self.stdID = QtWidgets.QLineEdit(self.widget)
        self.stdID.setObjectName("stdID")
        self.stdID.setEnabled(False)
        self.verticalLayout_4.addWidget(self.stdID)
        self.lbStudentID_3 = QtWidgets.QLabel(self.widget)
        self.lbStudentID_3.setObjectName("lbStudentID_3")
        self.verticalLayout_4.addWidget(self.lbStudentID_3)
        self.stdName = QtWidgets.QLineEdit(self.widget)
        self.stdName.setObjectName("stdName")
        self.stdName.setEnabled(False)
        self.verticalLayout_4.addWidget(self.stdName)
        self.lbStudentID_4 = QtWidgets.QLabel(self.widget)
        self.lbStudentID_4.setObjectName("lbStudentID_4")
        self.verticalLayout_4.addWidget(self.lbStudentID_4)
        self.stdFaculty = QtWidgets.QLineEdit(self.widget)
        self.stdFaculty.setObjectName("stdFaculty")
        self.stdFaculty.setEnabled(False)
        self.verticalLayout_4.addWidget(self.stdFaculty)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1310, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.stream1_active = False
        self.stream2_active = False

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Check"))
        MainWindow.setWindowIcon(QtGui.QIcon('icons/logo.png'))
        self.btnBack.setText(_translate("MainWindow", "Back"))
        self.txtURL_1.setText(_translate("MainWindow", "URL 1:"))
        self.btnStart_1.setText(_translate("MainWindow", "Start"))
        self.txtURL_2.setText(_translate("MainWindow", "URL 2:"))
        self.btnStart_2.setText(_translate("MainWindow", "Start"))
        self.lbStudentID.setText(_translate("MainWindow", "Student ID"))
        self.label_2.setText(_translate("MainWindow", "or"))
        self.imagePath.setText(_translate("MainWindow", "Image Path"))
        self.btnLoadImage.setText(_translate("MainWindow", "Load Image"))
        self.btnCheck.setText(_translate("MainWindow", "Check"))
        self.stdInfo.setText(_translate("MainWindow", "Student Info"))
        self.lbStudentID_2.setText(_translate("MainWindow", "Student ID"))
        self.lbStudentID_3.setText(_translate("MainWindow", "Name"))
        self.lbStudentID_4.setText(_translate("MainWindow", "Faculty"))

    def recognize_image_check(self, image_url, student_ID):
        directory = 'data'
        # Init models face detection & recognition
        weights = os.path.join(directory, "models",
                            "face_detection_yunet_2022mar.onnx")
        face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))
        face_detector.setScoreThreshold(0.87)

        weights = os.path.join(directory, "models", "face_recognizer_fast.onnx")
        face_recognizer = cv2.FaceRecognizerSF_create(weights, "")
        # create a database connection
        self.inputStudentID.clear()
        self.imge_input.clear()
        self.imagePath.setText('Image Path')
        with open('data_embeddings.pkl', 'rb') as f:
            dictionary = pickle.load(f)
        if student_ID:
            database = r"database.db"
            conn = create_connection(database)
            student = select_student_by_studentID(conn, student_ID)
            
            # Kiểm tra xem có sinh viên được trả về từ truy vấn không
            if student:
                self.stdName.setText(str(student[0][1]))
                self.stdID.setText(str(student[0][0]))
                self.stdFaculty.setText(str(student[0][2]))
                # Tạo QImage từ đường dẫn ảnh
                image = QImage(str(student[0][5]))
                
                # Kiểm tra xem ảnh đã được tạo thành công không
                if not image.isNull():
                    # Chuyển đổi QImage sang QPixmap và thiết lập cho QLabel
                    pixmap = QPixmap.fromImage(image)
                    self.image_output.setPixmap(pixmap)
                else:
                    QMessageBox.warning(None, "Thông báo", "Không thể tải ảnh")
                    
            else:
                QMessageBox.warning(None, "Thông báo", "Không tìm thấy sinh viên: " + student_ID)
        elif self.imge_input.pixmap():
            result = recognize_image(image_url, dictionary, face_detector, face_recognizer)
            if result:
                database = r"database.db"
                conn = create_connection(database)
                student = select_student_by_studentID(conn, result)
                
                # Kiểm tra xem có sinh viên được trả về từ truy vấn không
                if student:
                    self.stdName.setText(str(student[0][1]))
                    self.stdID.setText(str(student[0][0]))
                    self.stdFaculty.setText(str(student[0][2]))

                    # Tạo QImage từ đường dẫn ảnh
                    image = QImage(str(student[0][5]))
                    
                    # Kiểm tra xem ảnh đã được tạo thành công không
                    if not image.isNull():
                        # Chuyển đổi QImage sang QPixmap và thiết lập cho QLabel
                        pixmap = QPixmap.fromImage(image)
                        self.image_output.setPixmap(pixmap)
                    else:
                        QMessageBox.warning(None, "Thông báo", "Không thể tải ảnh")
                else:
                    QMessageBox.warning(None, "Thông báo", "Không tìm thấy sinh viên: " + student_ID)
            else:
                QMessageBox.warning(None, "Thông báo", "Nhận diện thất bại, không tìm thấy thông tin")
        else:
            QMessageBox.warning(None, "Thông báo", "Vui lòng nhập thông tin hoặc tải lên hình ảnh")

    def linkto(self):
        link = QFileDialog.getOpenFileName(filter='*.jpg *.png')
        if self.imge_input.setPixmap(QPixmap(link[0])):
            #self.imge_input.setPixmap(QPixmap(link[0]))
            self.imagePath.setText(link[0])
        else:
            self.imagePath.setText('Image Path')
    def toggle_stream_1(self):
        if self.url_1 != '':
            if not self.stream1_active:
                url = self.url_1.text()
                self.cap1 = cv2.VideoCapture(url)
                self.btnStart_1.setText("Stop")
                self.stream1_active = True
                self.btnStart_1.setStyleSheet("background-color: #f36666;")
                self.stream1()
            else:
                self.cap1.release()
                self.scrollAreaWidgetContents.clear()  # Clear the pixmap
                self.btnStart_1.setText("Start")
                self.btnStart_1.setStyleSheet("background-color: #52c9a2;")
                self.stream1_active = False
        else:
            QMessageBox.warning(None, "Thông báo", "Vui lòng điền IP của Camera")
    def stream1(self):

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
        while self.stream1_active:
            ret, frame = self.cap1.read()      
            if ret:
                    frame = detect_and_draw_labels_target(self.stdID.text(), dictionary, frame, face_detector, face_recognizer)
                    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgb_image.shape
                    bytes_per_line = ch * w
                    q_img = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                    pixmap = QtGui.QPixmap.fromImage(q_img)
                    self.scrollAreaWidgetContents.setPixmap(pixmap)
                    QtWidgets.QApplication.processEvents()  # Để đảm bảo cập nhật giao diện người dùng
            else:
                break

    def toggle_stream_2(self):
        if self.url_2 != '':
            if not self.stream2_active:
                url = self.url_2.text()
                self.cap2 = cv2.VideoCapture(url)
                self.btnStart_2.setText("Stop")
                self.btnStart_2.setStyleSheet("background-color: #f36666;")
                self.stream2_active = True
                self.stream2()
            else:
                self.cap2.release()
                self.scrollAreaWidgetContents_2.clear()  # Clear the pixmap
                self.btnStart_2.setText("Start")
                self.btnStart_2.setStyleSheet("background-color: #52c9a2;")
                self.stream2_active = False
        else:
            QMessageBox.warning(None, "Thông báo", "Vui lòng điền IP của Camera")
    def stream2(self):
        
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
        while self.stream2_active:
            ret, frame = self.cap2.read()      
            if ret:
                    frame = detect_and_draw_labels_target(self.stdID.text(), dictionary, frame, face_detector, face_recognizer)
                    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgb_image.shape
                    bytes_per_line = ch * w
                    q_img = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                    pixmap = QtGui.QPixmap.fromImage(q_img)
                    self.scrollAreaWidgetContents_2.setPixmap(pixmap)
                    QtWidgets.QApplication.processEvents()  # Để đảm bảo cập nhật giao diện người dùng
            else:
                break

    def back(self, MainWindow):
        # Tạo một instance của giao diện
        self.another_gui_instance = Ui_MainWindow()

        # Hiển thị giao diện
        self.another_gui_instance.setupUi(MainWindow)
        self.stream1_active = False
        self.stream2_active = False
        MainWindow.showMaximized() 

class Ui_MainWindow(object):
    def __init__(self):
        self.ui = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QtGui.QIcon('icons/logo.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Set up full screen size for layout calculations
        screen = QtWidgets.QApplication.primaryScreen().size()
        width = screen.width()
        height = screen.height()

        # Calculate positions and sizes
        button_width = 300
        button_height = 300
        spacing = (width - 3 * button_width) / 4  # Calculate spacing to evenly distribute buttons

        # Tạo ba nút với hình ảnh và nhãn văn bản
        self.createButton(MainWindow, "icons/cctv.png", spacing, (height - button_height) / 2, button_width, button_height, "CCTV", "cctvButton")
        self.createButton(MainWindow, "icons/check.png", 2 * spacing + button_width, (height - button_height) / 2, button_width, button_height, "Check", "cameraButton")
        self.createButton(MainWindow, "icons/attendance.png", 3 * spacing + 2 * button_width, (height - button_height) / 2, button_width, button_height, "Attendance", "securityButton")

        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setText("Recognition System")
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setGeometry(QtCore.QRect(0, (height - button_height) / 2 - 150, width, 80))  # Adjust label size and position
        self.titleLabel.setFont(QFont("Arial", 35))


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def createButton(self, MainWindow, imagePath, x, y, width, height, labelText, objName):
        button = QtWidgets.QPushButton(self.centralwidget)
        button.setGeometry(QtCore.QRect(x, y, width, height))
        button.setObjectName(objName)
        pixmap = QtGui.QPixmap(imagePath)
        icon = QtGui.QIcon(pixmap)
        button.setIcon(icon)
        button.setIconSize(pixmap.size())
        button.setText("")

        # Tạo nhãn văn bản phía dưới nút
        label = QtWidgets.QLabel(self.centralwidget)
        label.setGeometry(QtCore.QRect(x, y + height + 10, width, 30))  # 10 là khoảng cách giữa nút và nhãn văn bản
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setText(labelText)
        label.setFont(QFont("Arial", 20))
        # Kết nối sự kiện click với xử lý
        button.clicked.connect(lambda: self.openGui(labelText, MainWindow))
        
    def openGui(self, labelText, MainWindow):

        if(labelText == 'CCTV'):
            
            ui = CCTV()
           
         
        elif(labelText == 'Check'):
            ui = Check()
        else:
            ui = Attendance()

        ui.setupUi(MainWindow)
        MainWindow.showMaximized()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Recognition System"))

class Attendance(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QtGui.QIcon('icons/logo.png'))
        MainWindow.resize(1920, 1080)
        MainWindow.setAnimated(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 1741, 951))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnBack = QtWidgets.QPushButton(self.layoutWidget)
        self.btnBack.setObjectName("btnBack")
        self.btnBack.setFixedSize(100, 30)
        self.btnBack.clicked.connect(lambda: self.back(MainWindow))
        self.btnBack.setStyleSheet("background-color: #cccccc;")
        self.btnAdd = QtWidgets.QPushButton(self.layoutWidget)
        self.btnAdd.setObjectName("btnAdd")
        self.btnAdd.setFixedSize(100, 30)
        self.btnAdd.clicked.connect(lambda: self.create_student(MainWindow))
        self.btnAdd.setStyleSheet("background-color: #85c9e8;")
        self.verticalLayout.addWidget(self.btnBack)
        self.verticalLayout.addWidget(self.btnAdd)
        self.scrollAraeWebcam = QtWidgets.QScrollArea(self.layoutWidget)
        self.scrollAraeWebcam.setWidgetResizable(True)
        self.scrollAraeWebcam.setObjectName("scrollAraeWebcam")
        self.scrollAreaWidgetContents = VideoLabel()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 863, 887))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAraeWebcam.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollAraeWebcam)
        self.btnAttendance = QtWidgets.QPushButton(self.layoutWidget)
        self.btnAttendance.setIconSize(QtCore.QSize(32, 32))
        self.btnAttendance.setObjectName("btnAttendance")
        self.btnAttendance.setFixedSize(150, 60)
        self.btnAttendance.setStyleSheet("background-color: #52c9a2;")
        self.btnAttendance.clicked.connect(self.toggle_attendance)
        self.verticalLayout.addWidget(self.btnAttendance, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.verticalLayout.addWidget(self.btnAttendance)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(100, 0, 0 ,120)
        self.studentImage = QtWidgets.QLabel(self.layoutWidget)
        self.studentImage.setMaximumSize(QtCore.QSize(400, 400))
        self.studentImage.setFrameShape(QtWidgets.QFrame.Box)
        self.studentImage.setLineWidth(2)
        self.studentImage.setText("")
        self.studentImage.setObjectName("studentImage")
        self.studentImage.setFixedSize(400, 400)
        self.studentImage.setScaledContents(True)
        self.verticalLayout_2.addWidget(self.studentImage, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setMaximumSize(QtCore.QSize(80, 40))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.studentName = QtWidgets.QLineEdit(self.layoutWidget)
        self.studentName.setObjectName("studentName")
        self.studentName.setFixedSize(300, 30)
        self.verticalLayout_2.addWidget(self.studentName, 1, QtCore.Qt.AlignHCenter)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setMaximumSize(QtCore.QSize(80, 40))
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.studentID = QtWidgets.QLineEdit(self.layoutWidget)
        self.studentID.setObjectName("studentID")
        self.studentID.setFixedSize(300, 30)
        self.verticalLayout_2.addWidget(self.studentID, 1, QtCore.Qt.AlignHCenter)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setMaximumSize(QtCore.QSize(80, 40))
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.studentFaculty = QtWidgets.QLineEdit(self.layoutWidget)
        self.studentFaculty.setObjectName("studentFaculty")
        self.studentFaculty.setFixedSize(300, 30)
        self.verticalLayout_2.addWidget(self.studentFaculty, 1, QtCore.Qt.AlignHCenter)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setMaximumSize(QtCore.QSize(80, 40))
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.timeAttendance = QtWidgets.QLineEdit(self.layoutWidget)
        self.timeAttendance.setObjectName("timeAttendance")
        self.timeAttendance.setFixedSize(300, 30)
        self.verticalLayout_2.addWidget(self.timeAttendance, 1, QtCore.Qt.AlignHCenter)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.attendace_active = False

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Attendance"))
        self.btnBack.setText(_translate("MainWindow", "Back"))
        self.btnAdd.setText(_translate("MainWindow", "Add Student"))
        self.btnAttendance.setText(_translate("MainWindow", "Start Attendance"))
        self.label.setText(_translate("MainWindow", "Name:"))
        self.label_2.setText(_translate("MainWindow", "Student ID:"))
        self.label_3.setText(_translate("MainWindow", "Faculty:"))
        self.label_4.setText(_translate("MainWindow", "Time:"))

    
    def toggle_attendance(self):
        if not self.attendace_active:
            self.cap1 = cv2.VideoCapture(0)
            self.btnAttendance.setText("Stop Attendance")
            self.attendace_active = True
            self.stream1()
        else:
            self.cap1.release()
            self.scrollAreaWidgetContents.clear()  # Clear the pixmap
            self.btnAttendance.setText("Start Attendance")
            self.attendace_active = False
    

    def stream1(self):

        database = r"database.db"
        conn = create_connection(database)
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
        while self.attendace_active:
            ret, frame = self.cap1.read()      
            if ret:
                    frame, name = detect_and_draw_labels(dictionary, frame, face_detector, face_recognizer)
                    if name is not None:
                        result = select_student_by_studentID(conn, name)
                        if result != []:
                            self.studentImage.setPixmap(QPixmap((result[0][5])))
                            self.studentName.setText(str(result[0][1]))
                            self.studentID.setText(str(result[0][0]))
                            self.studentFaculty.setText(str(result[0][2]))
                            self.timeAttendance.setText(datetime.datetime.now().__str__())
                            
                    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgb_image.shape
                    bytes_per_line = ch * w
                    q_img = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                    pixmap = QtGui.QPixmap.fromImage(q_img)
                    self.scrollAreaWidgetContents.setPixmap(pixmap)
                    QtWidgets.QApplication.processEvents()  # Để đảm bảo cập nhật giao diện người dùng
            else:
                break
    def back(self, MainWindow):
        # Tạo một instance của giao diện
        self.another_gui_instance = Ui_MainWindow()

        # Hiển thị giao diện
        self.another_gui_instance.setupUi(MainWindow)
        self.attendace_active = False
        MainWindow.showMaximized()       
    def create_student(self, MainWindow):
        # Tạo một instance của giao diện
        self.another_gui_instance = Create()

        # Hiển thị giao diện
        self.another_gui_instance.setupUi(MainWindow)
        
        # Lấy kích thước của màn hình
        screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()

        # Lấy kích thước của cửa sổ chính
        main_window_geometry = MainWindow.frameGeometry()

        # Di chuyển cửa sổ chính vào giữa màn hình
        x = (screen_geometry.width() - main_window_geometry.width()) / 2
        y = (screen_geometry.height() - main_window_geometry.height()) / 2
        MainWindow.move(x, y)
        MainWindow.show()       

class Create(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QtGui.QIcon('icons/logo.png'))
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(300, 10, 600, 750))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.back(MainWindow))
        self.pushButton.setStyleSheet("background-color: #cccccc;")
        self.verticalLayout_2.addWidget(self.pushButton, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, 20, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.widget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = VideoLabel()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 69, 69))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea.setFixedSize(380,380)
        self.verticalLayout_2.addWidget(self.scrollArea, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.btnStart = QtWidgets.QPushButton(self.widget)
        self.btnStart.setObjectName("btnStart")
        self.btnStart.setFixedSize(100, 40)
        self.btnStart.clicked.connect(self.toggle_start_webcam)
        self.btnStart.setStyleSheet("background-color: #52c9a2;")
        self.verticalLayout.addWidget(self.btnStart, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setFixedSize(600, 30)
        self.verticalLayout.addWidget(self.lineEdit)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setFixedSize(600, 30)
        self.verticalLayout.addWidget(self.lineEdit_2)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setFixedSize(600, 30)
        self.verticalLayout.addWidget(self.lineEdit_3)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_4.setFixedSize(600, 30)
        self.verticalLayout.addWidget(self.lineEdit_4)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_5.setEnabled(False)
        self.lineEdit_5.setFixedSize(600, 30)
        self.verticalLayout.addWidget(self.lineEdit_5)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.insert)
        self.pushButton_2.setStyleSheet("background-color: #85c9e8;")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.verticalLayout.setStretch(0, 3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.start_active = False

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Create Student"))
        self.pushButton.setText(_translate("MainWindow", "Back"))
        self.btnStart.setText(_translate("MainWindow", "Start"))
        self.label.setText(_translate("MainWindow", "Student ID"))
        self.label_2.setText(_translate("MainWindow", "Name"))
        self.label_3.setText(_translate("MainWindow", "Faculty"))
        self.label_4.setText(_translate("MainWindow", "Year"))
        self.label_5.setText(_translate("MainWindow", "Image Path"))
        self.pushButton_2.setText(_translate("MainWindow", "Create"))
    

    def toggle_start_webcam(self):
        if not self.start_active:
            # Bắt đầu stream video từ webcam
            self.cap1 = cv2.VideoCapture(0)
            if not self.cap1.isOpened():
                QtWidgets.QMessageBox.critical(None, "Error", "Failed to open webcam!")
                return
            # Đặt nút thành "Capture"
            self.btnStart.setText("Capture")
            # Bắt đầu stream và capture
            self.start_active = True
            self.stream1()
        elif self.btnStart.text() == "Capture":
            # Nếu đang là "Capture", thực hiện capture ảnh từ webcam
            self.capture()
            
        else:
            # Khi đang là "Stop Record", clear ScrollArea và dừng webcam
            self.cap1.release()
            self.scrollAreaWidgetContents.clear()
            self.btnStart.setText("Capture")
            self.btnStart.setStyleSheet("background-color: #f36666;")
            self.start_active = False
   
    def capture(self):
        # Kiểm tra xem thư mục images đã tồn tại chưa, nếu chưa thì tạo mới
        if not os.path.exists("images"):
            os.makedirs("images")

        # Đảm bảo rằng webcam đã được khởi tạo
        if self.cap1 is None or not self.cap1.isOpened():
            QtWidgets.QMessageBox.critical(None, "Error", "Webcam is not initialized!")
            return

        # Capture một frame từ webcam
        ret, frame = self.cap1.read()
        if ret:
            if self.lineEdit.text() and self.lineEdit_2.text():
                # Lấy MSSV từ lineEdit
                mssv = str(self.lineEdit.text())

                # Kiểm tra xem thư mục có tên là MSSV đã tồn tại trong thư mục images chưa, nếu chưa thì tạo mới
                student_folder = os.path.join("images", mssv)
                data_folder = os.path.join("data", "images")
                if not os.path.exists(student_folder):
                    os.makedirs(student_folder)

                # Lưu ảnh đã capture vào thư mục có tên là MSSV
                image_path = os.path.join(student_folder, str(self.lineEdit_2.text())+'.jpg')
                cv2.imwrite(image_path, frame)
                image_data_path = os.path.join(data_folder, str(self.lineEdit.text())+'.jpg')
                cv2.imwrite(image_data_path, frame) 
                # Resize ảnh và lưu ảnh đã resize
                resized_image = cv2.resize(frame, (70, 70))  # Resize ảnh thành kích thước 70x81
                image_path_resize = os.path.join(student_folder, str(self.lineEdit_2.text()) + '_resize.jpg')
                cv2.imwrite(image_path_resize, resized_image)

                # Hiển thị ảnh đã capture lên scrollArea
                self.load_image_to_scroll_area(image_path)
                self.lineEdit_5.setText(image_path)
                self.btnStart.setText("Start Record")
            else:
                QMessageBox.warning(None, "Thông báo", "Vui lòng điền thông tin trước!")

    def load_image_to_scroll_area(self, image_path):
        # Load ảnh từ đường dẫn và hiển thị lên scrollArea
        pixmap = QtGui.QPixmap(image_path)
        self.scrollAreaWidgetContents.setPixmap(pixmap)
        self.start_active = False

    def stream1(self):
        while self.start_active:
            ret, frame = self.cap1.read()      
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                q_img = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(q_img)
                self.scrollAreaWidgetContents.setPixmap(pixmap)
                QtWidgets.QApplication.processEvents()  # Để đảm bảo cập nhật giao diện người dùng
                # Lấy thanh cuộn ngang của QScrollArea
                horizontal_scrollbar = self.scrollArea.horizontalScrollBar()
                # Di chuyển thanh cuộn ngang vào vị trí trung tâm
                horizontal_scrollbar.setValue(horizontal_scrollbar.maximum() // 2)
            else:
                break
    def insert(self):
        # Kiểm tra xem tất cả các lineEdit có dữ liệu không
        if self.lineEdit.text() and self.lineEdit_2.text() and self.lineEdit_3.text() and self.lineEdit_4.text() and self.lineEdit_5.text():
            # Nếu tất cả các lineEdit đều có dữ liệu, tiến hành chèn vào cơ sở dữ liệu
            database = r"database.db"
            conn = create_connection(database)
            # Đường dẫn của hình ảnh bạn muốn chèn
            image_path = self.lineEdit_5.text()
            
            # Tách đường dẫn và tên tệp tin
            directory, filename = os.path.split(image_path)

            # Tạo đường dẫn mới cho tệp tin resized
            resized_filename = os.path.splitext(filename)[0] + '_resize.jpg'
            resized_image_path = os.path.join(directory, resized_filename)
            # Chuyển đổi hình ảnh thành dữ liệu blob
            image_blob = convert_image_to_blob(resized_image_path)
            image_url = self.lineEdit_5.text()
            
            # Thông tin sinh viên
            student_data = (int(self.lineEdit.text()), str(self.lineEdit_2.text()), str(str(self.lineEdit_3.text())), int(str(self.lineEdit_4.text())), image_blob, image_url)
           
            # Chèn thông tin sinh viên vào cơ sở dữ liệu
            insert_student(conn, student_data)
            # train_dir = "images/"+str(self.lineEdit.text())
            # model_save_path = "trained_model.pkl"
            # leaf_size = 30  # Optional parameter, default value is 30
            # verbose = True  # Optional parameter, default value is False
            pretrain('data')
            #pretrain_model(model_path=model_save_path, new_data_dir=train_dir, leaf_size=leaf_size, verbose=verbose)
            self.scrollAreaWidgetContents.clear()
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()
            data_folder = os.path.join("data", "images")
            shutil.rmtree(data_folder)
            os.makedirs(data_folder)
            QMessageBox.warning(None, "Thông báo", "Thêm thông tin thành công!")
        else:
            # Nếu có một hoặc nhiều lineEdit không có dữ liệu, hiển thị một thông báo cảnh báo
            QMessageBox.warning(None, "Thông báo", "Vui lòng điền đầy đủ thông tin!")


    def back(self, MainWindow):
        # Tạo một instance của giao diện
        self.another_gui_instance = Attendance()

        # Hiển thị giao diện
        self.another_gui_instance.setupUi(MainWindow)
        self.start_active = False
        MainWindow.move(0, 0)
        MainWindow.showMaximized()

def create_main_window():
    app = QtWidgets.QApplication([])
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    return app, MainWindow, ui
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    loading_screen = LoadingScreen()
    loading_screen.show()
    sys.exit(app.exec_())
