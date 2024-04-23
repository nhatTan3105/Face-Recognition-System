import cv2
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from kdtree import predict, show_prediction_labels_on_image
import time
from sql_query import create_connection, select_all_students, select_student_by_studentID
import datetime

class VideoLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(VideoLabel, self).__init__(parent)

    def setPixmap(self, pixmap):
        super().setPixmap(pixmap)
        self.setScaledContents(True)

class CCTV(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("CCTV")

        # Tính toán kích thước màn hình
        screen = QtWidgets.QApplication.primaryScreen().size()
        width = screen.width()
        height = screen.height()

        # Thiết lập kích thước và vị trí của cửa sổ
        MainWindow.resize(width, height)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Set up QScrollArea 1
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(40, 50, width // 2, height // 2.5))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = VideoLabel()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        # Input and Start/Stop button above ScrollArea 1
        self.input_above_scrollArea1 = QtWidgets.QLineEdit(self.centralwidget)
        self.input_above_scrollArea1.setGeometry(QtCore.QRect(160, 20, 150, 25))
        self.start_button_above_scrollArea1 = QtWidgets.QPushButton(self.centralwidget)
        self.start_button_above_scrollArea1.setGeometry(QtCore.QRect(320, 20, 75, 25))
        self.start_button_above_scrollArea1.setText("Start")
        self.start_button_above_scrollArea1.clicked.connect(self.toggle_stream_1)

        # Set up QScrollArea 2
        self.scrollArea_2 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_2.setGeometry(QtCore.QRect(40, height //2,  width // 2, height // 2.5))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = VideoLabel()
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        
        # Input and Start/Stop button above ScrollArea 2
        self.input_above_scrollArea2 = QtWidgets.QLineEdit(self.centralwidget)
        self.input_above_scrollArea2.setGeometry(QtCore.QRect(160, height // 2 - 30, 150, 25))
        self.start_button_above_scrollArea2 = QtWidgets.QPushButton(self.centralwidget)
        self.start_button_above_scrollArea2.setGeometry(QtCore.QRect(320, height // 2 - 30, 75, 25))
        self.start_button_above_scrollArea2.setText("Start")
        self.start_button_above_scrollArea2.clicked.connect(self.toggle_stream_2)

        # Set up QTableWidget
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(width // 1.4, 50, width // 3.6, height // 1.15))
        self.tableWidget.setObjectName("tableWidget")

        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['MSSV', 'Name', 'Image', 'DateTime', 'Localtion'])
        

        MainWindow.setCentralWidget(self.centralwidget)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 10, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Back")
        self.pushButton.clicked.connect(lambda: self.back(MainWindow))

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, width, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Add instance variables to keep track of stream status
        self.stream1_active = False
        self.stream2_active = False
   

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

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
            url = self.input_above_scrollArea1.text()
            self.cap1 = cv2.VideoCapture(url)
            self.start_button_above_scrollArea1.setText("Stop")
            
            self.stream1_active = True
            self.stream1()
        else:
            self.cap1.release()
            self.scrollAreaWidgetContents.clear()  # Clear the pixmap
            self.start_button_above_scrollArea1.setText("Start")
            self.stream1_active = False

    def toggle_stream_2(self):
        if not self.stream2_active:
            url = self.input_above_scrollArea2.text()
            self.cap2 = cv2.VideoCapture(url)
            self.start_button_above_scrollArea2.setText("Stop")
            self.stream2_active = True
            self.stream2()
        else:
            self.cap2.release()
            self.scrollAreaWidgetContents_2.clear()  # Clear the pixmap
            self.start_button_above_scrollArea2.setText("Start")
            self.stream2_active = False

    def stream1(self):
       
        count = 29

        # create a database connection
        database = r"database.db"
        conn = create_connection(database)

        while self.stream1_active:
            ret, frame = self.cap1.read()      
            if ret:
                count+=1
                if count % 30 == 0:
                    img = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
                    predictions = predict(img, model_path="trained_model.pkl")
                    if predictions != []:
                        for name in predictions:
                            data = select_student_by_studentID(conn, name[0])
                            
                            for data in data:
                                self.add_data_to_table_1([data[0].__str__(), data[1].__str__(), data[4], datetime.datetime.now().__str__()])
                    frame = show_prediction_labels_on_image(frame, predictions)
                    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgb_image.shape
                    bytes_per_line = ch * w
                    q_img = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                    pixmap = QtGui.QPixmap.fromImage(q_img)
                    self.scrollAreaWidgetContents.setPixmap(pixmap)
                    QtWidgets.QApplication.processEvents()  # Để đảm bảo cập nhật giao diện người dùng
                   
                   
                else:
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
         # create a database connection
        database = r"database.db"
        conn = create_connection(database)
        while self.stream2_active:
            ret, frame = self.cap2.read()      
            if ret:
                count+=1
                if count % 30 == 0:
                    img = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
                    predictions = predict(img, model_path="trained_model.pkl")
                    if predictions != []:
                        for name in predictions:
                            data = select_student_by_studentID(conn, name[0])
                            
                            for data in data:
                                self.add_data_to_table_2([data[0].__str__(), data[1].__str__(), data[4], datetime.datetime.now().__str__()])
                    frame = show_prediction_labels_on_image(frame, predictions)
                    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgb_image.shape
                    bytes_per_line = ch * w
                    q_img = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                    pixmap = QtGui.QPixmap.fromImage(q_img)
                    self.scrollAreaWidgetContents_2.setPixmap(pixmap)
                    QtWidgets.QApplication.processEvents()  # Để đảm bảo cập nhật giao diện người dùng
                    
                else:
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

        # Hiển thị giao diện
        self.another_gui_instance.setupUi(MainWindow)



if __name__ == "__main__":
    
    # app = QtWidgets.QApplication([])
    # MainWindow = QtWidgets.QMainWindow()
    # ui = CCTV()
    # ui.setupUi(MainWindow)
    print('ui create')
    # MainWindow.showMaximized()  # Hiển thị cửa sổ ứng dụng với kích thước tối đa
    # sys.exit(app.exec_())

#http://nhattan:nhattan@192.168.1.8:4747/video