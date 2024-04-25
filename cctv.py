import cv2
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from sql_query import create_connection, select_student_by_studentID
import datetime
from sface import detect_and_draw_labels
import pickle
import os 

class VideoLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(VideoLabel, self).__init__(parent)

    def setPixmap(self, pixmap):
        super().setPixmap(pixmap)
        self.setScaledContents(True)

class CCTV(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        
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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnBack.setText(_translate("MainWindow", "Back"))
        self.txtURL_1.setText(_translate("MainWindow", "Camera IP 1:"))
        self.btnStart_1.setText(_translate("MainWindow", "Start"))
        self.txtURL_2.setText(_translate("MainWindow", "Camera IP 2:"))
        self.btnStart_2.setText(_translate("MainWindow", "Start"))
        self.txtStdID.setText(_translate("MainWindow", "Student ID:"))
        self.btnSearch.setText(_translate("MainWindow", "Search"))

    
    def add_data_to_table_1(self, data):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        item = QtWidgets.QTableWidgetItem('Camera 1')
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
    def add_data_to_table_2(self, data):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        item = QtWidgets.QTableWidgetItem('Camera 2')
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


    def toggle_stream_1(self):
        if not self.stream1_active:
            url = self.inputURL_1.text()
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

    def toggle_stream_2(self):
        if not self.stream2_active:
            url = self.inputURL_2.text()
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

    def stream1(self):
        count = 29
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
        while self.stream1_active:
            ret, frame = self.cap1.read()      
            if ret:
                    frame, name = detect_and_draw_labels(dictionary, frame, face_detector, face_recognizer)
                    count+=1
                    if name is not None and count%30==0:
                        data = select_student_by_studentID(conn, name)
                        for data in data:
                            self.add_data_to_table_1([data[0].__str__(), data[1].__str__(), data[4], datetime.datetime.now().__str__()])
                            
                    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgb_image.shape
                    bytes_per_line = ch * w
                    q_img = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                    pixmap = QtGui.QPixmap.fromImage(q_img)
                    self.scrollAreaWidgetContents.setPixmap(pixmap)
                    QtWidgets.QApplication.processEvents()  # Để đảm bảo cập nhật giao diện người dùng
            else:
                break

    def stream2(self):
        count = 29
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
        while self.stream2_active:
            ret, frame = self.cap2.read()      
            if ret:
                    frame, name = detect_and_draw_labels(dictionary, frame, face_detector, face_recognizer)
                    count+=1
                    if name is not None and count%30==0:
                        data = select_student_by_studentID(conn, name)
                        for data in data:
                            self.add_data_to_table_2([data[0].__str__(), data[1].__str__(), data[4], datetime.datetime.now().__str__()])
                            
                    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgb_image.shape
                    bytes_per_line = ch * w
                    q_img = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                    pixmap = QtGui.QPixmap.fromImage(q_img)
                    self.scrollAreaWidgetContents_2.setPixmap(pixmap)
                    QtWidgets.QApplication.processEvents()  # Để đảm bảo cập nhật giao diện người dùng
            else:
                break
    # cctv.py
    def back(self, MainWindow):
        import main
        # Tạo một instance của giao diện
        self.another_gui_instance = main.Ui_MainWindow()
        self.stream1_active = False
        self.stream2_active = False
        # Hiển thị giao diện
        self.another_gui_instance.setupUi(MainWindow)

    def search(self, s):
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

            
    def showAllItems(self):
        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHidden(row, False)  # Hiển thị tất cả các hàng




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = CCTV()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
