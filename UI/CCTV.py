from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import sys
import datetime
import pickle
import os 
import pandas as pd
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QFont
from sface import *
import shutil
from PyQt5.QtCore import QThread, pyqtSignal, QTimer



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
        self.btnExport = QtWidgets.QPushButton(self.widget)
        self.btnExport.setObjectName("btnExport")
        self.btnExport.setStyleSheet("background-color: #85c9e8;")
        self.btnExport.setText('Export Data')
        self.btnExport.setFixedSize(100, 30)
        self.btnExport.clicked.connect(self.export_to_excel)
        self.verticalLayout_2.addWidget(self.btnExport)
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
        self.called_add_data_to_table_1 = False
        self.called_add_data_to_table_2 = False

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

    def export_to_excel(self):
        # Number of rows and columns in the table
        row_count = self.tableWidget.rowCount()
        column_count = self.tableWidget.columnCount()

        # Create a list to hold data
        data = []

        # Iterate over rows and columns to extract data
        for row in range(row_count):
            row_data = []
            for column in range(column_count):
                item = self.tableWidget.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    # Handle the case where the cell might be empty or have a widget like an image
                    cell_widget = self.tableWidget.cellWidget(row, column)
                    if isinstance(cell_widget, QtWidgets.QLabel) and cell_widget.pixmap():
                        row_data.append('Image')
                    else:
                        row_data.append('')
            data.append(row_data)

        # Create a DataFrame
        df = pd.DataFrame(data, columns=[self.tableWidget.horizontalHeaderItem(i).text() for i in range(column_count)])

        # Specify the path and name of the Excel file
        file_path = QFileDialog.getSaveFileName(None, "Save File", "", "Excel files (*.xlsx)")[0]
        if file_path:
            # Write the DataFrame to an Excel file
            df.to_excel(file_path, index=False)
            QMessageBox.information(None, "Export Successful", "Data has been exported successfully to " + file_path)

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
        if self.inputURL_1.text() != '':
            if not self.stream1_active:
                url = self.inputURL_1.text()
                if type(self.inputURL_1.text()) is str and len(self.inputURL_1.text()) == 1:
                    self.stream1_thread = StreamThread(int(self.inputURL_1.text()))
                else:
                    self.stream1_thread = StreamThread(url)
                self.stream1_thread.updatePixmap.connect(lambda pixmap: self.update_stream_1(pixmap, dictionary, face_detector, face_recognizer, conn))
                self.stream1_thread.start()
                self.btnStart_1.setText("Stop")
                self.btnStart_1.setStyleSheet("background-color: #f36666;")
                self.stream1_active = True
            else:
                self.stream1_thread.stop()
                self.stream1_thread.quit()
                self.stream1_thread.wait()
                self.scrollAreaWidgetContents.clear()
                self.btnStart_1.setText("Start")
                self.btnStart_1.setStyleSheet("background-color: #52c9a2;")
                self.stream1_active = False
        else:
            QMessageBox.warning(None, "Thông báo", "Vui lòng điền IP của Camera")

    def toggle_stream_2(self):
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
        if self.inputURL_2.text() != '':
            if not self.stream2_active:
                url = self.inputURL_2.text()
                if type(self.inputURL_2.text()) is str and len(self.inputURL_2.text()) == 1:
                    self.stream2_thread = StreamThread(int(self.inputURL_2.text()))
                else:
                    self.stream2_thread = StreamThread(url)
                self.stream2_thread.updatePixmap.connect(lambda pixmap: self.update_stream_2(pixmap, dictionary, face_detector, face_recognizer, conn))
                self.stream2_thread.start()
                self.btnStart_2.setText("Stop")
                self.btnStart_2.setStyleSheet("background-color: #f36666;")
                self.stream2_active = True
            else:
                self.stream2_thread.stop()
                self.stream2_thread.quit()
                self.stream2_thread.wait()
                self.scrollAreaWidgetContents_2.clear()
                self.btnStart_2.setText("Start")
                self.btnStart_2.setStyleSheet("background-color: #52c9a2;")
                self.stream2_active = False
        else:
            QMessageBox.warning(None, "Thông báo", "Vui lòng điền IP của Camera")
   
    global processed_names_camera_1
    processed_names_camera_1 = set()
    
    def update_stream_1(self, pixmap, dictionary, face_detector, face_recognizer, conn,):
        if self.stream1_active:
            rgb_image = pixmap.toImage()
            width, height = rgb_image.width(), rgb_image.height()
            ptr = rgb_image.constBits()
            ptr.setsize(rgb_image.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # RGBA format

            frame = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

            frame, name = detect_and_draw_labels(dictionary, frame, face_detector, face_recognizer)
            if name is not None and not self.called_add_data_to_table_1:
                for n in name:
                    if n not in processed_names_camera_1:
                        data = select_student_by_studentID(conn, n)
                        for d in data:
                            self.add_data_to_table_1([d[0].__str__(), d[1].__str__(), d[4], datetime.datetime.now().__str__()])
                            processed_names_camera_1.add(n)  # Thêm giá trị đã được xử lý vào tập hợp
                
            q_img = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(q_img)
            self.scrollAreaWidgetContents.setPixmap(pixmap)
       
    global processed_names_camera_2
    processed_names_camera_2 = set()
    
    def update_stream_2(self, pixmap, dictionary, face_detector, face_recognizer, conn,):
        if self.stream2_active:
            rgb_image = pixmap.toImage()
            width, height = rgb_image.width(), rgb_image.height()
            ptr = rgb_image.constBits()
            ptr.setsize(rgb_image.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # RGBA format

            frame = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)

            frame, name = detect_and_draw_labels(dictionary, frame, face_detector, face_recognizer)
            if name is not None and not self.called_add_data_to_table_2:
                for n in name:
                    if n not in processed_names_camera_2:
                        data = select_student_by_studentID(conn, n)
                        for d in data:
                            self.add_data_to_table_2([d[0].__str__(), d[1].__str__(), d[4], datetime.datetime.now().__str__()])
                            processed_names_camera_2.add(n)  # Thêm giá trị đã được xử lý vào tập hợp
                #self.called_add_data_to_table_1 = True
            q_img = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(q_img)
            self.scrollAreaWidgetContents_2.setPixmap(pixmap)

    def back(self, MainWindow):
        self.another_gui_instance = Ui_MainWindow()
        self.stream1_active = False
        self.stream2_active = False
        self.another_gui_instance.setupUi(MainWindow)

    def search(self, s):
        if s != '':
            if not self.search_press:
                for row in range(self.tableWidget.rowCount()):
                    item = self.tableWidget.item(row, 0)  
                    if item:
                        text = item.text().lower()
                        if s.lower() in text:
                            self.tableWidget.setRowHidden(row, False) 
                        else:
                            self.tableWidget.setRowHidden(row, True)  
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
            self.tableWidget.setRowHidden(row, False) 
