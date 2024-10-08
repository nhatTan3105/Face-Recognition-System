from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import os 
from PyQt5.QtWidgets import QMessageBox
from sface import *
import shutil


class Create(object):
    def setupUi(self, MainWindow):
        
        from common import VideoLabel
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QtGui.QIcon('../icons/logo.png'))
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
        from common import Database
        # Tạo một instance của giao diện
        self.another_gui_instance = Database()

        # Hiển thị giao diện
        self.another_gui_instance.setupUi(MainWindow)
        self.start_active = False
        MainWindow.move(0, 0)
        MainWindow.showMaximized()
