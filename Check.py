from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import pickle
import os 
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from sface import *



class Check(object):

    def setupUi(self, MainWindow):
        from VideoLabel import VideoLabel
        MainWindow.setObjectName("Check")
        MainWindow.setWindowIcon(QtGui.QIcon('icons/logo.png'))
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
        from StreamThread import StreamThread
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
        if self.url_1.text() != '':
            if not self.stream1_active:
                url = self.url_1.text()
                if type(self.url_1.text()) is str and len(self.url_1.text()) == 1:
                    self.stream1_thread = StreamThread(int(self.url_1.text()))
                else:
                    self.stream1_thread = StreamThread(url)
                self.stream1_thread.updatePixmap.connect(lambda pixmap: self.update_stream_1(pixmap, dictionary, face_detector, face_recognizer))
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

    # def load_model(directory):
        
    def toggle_stream_2(self):
        from StreamThread import StreamThread
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
        if self.url_2.text() != '':
            if not self.stream2_active:
                url = self.url_2.text()
                if type(self.url_2.text()) is str and len(self.url_2.text()) == 1:
                    self.stream2_thread = StreamThread(int(self.url_2.text()))
                else:
                    self.stream2_thread = StreamThread(url)
                self.stream2_thread.updatePixmap.connect(lambda pixmap: self.update_stream_2(pixmap, dictionary, face_detector, face_recognizer))
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
   
    
    def update_stream_1(self, pixmap, dictionary, face_detector, face_recognizer):
        if self.stream1_active:
            rgb_image = pixmap.toImage()
            width, height = rgb_image.width(), rgb_image.height()
            ptr = rgb_image.constBits()
            ptr.setsize(rgb_image.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # RGBA format
            frame = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
            if self.stdID.text():
                frame = detect_and_draw_labels_target(self.stdID.text(), dictionary, frame, face_detector, face_recognizer)
            q_img = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(q_img)
            self.scrollAreaWidgetContents.setPixmap(pixmap)
    
    def update_stream_2(self, pixmap, dictionary, face_detector, face_recognizer):
        if self.stream2_active:
            rgb_image = pixmap.toImage()
            width, height = rgb_image.width(), rgb_image.height()
            ptr = rgb_image.constBits()
            ptr.setsize(rgb_image.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # RGBA format
            frame = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
            if self.stdID.text():
                frame = detect_and_draw_labels_target(self.stdID.text(), dictionary, frame, face_detector, face_recognizer)
            q_img = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(q_img)
            self.scrollAreaWidgetContents_2.setPixmap(pixmap)

    def back(self, MainWindow):
        from common import Ui_MainWindow
        # Tạo một instance của giao diện
        self.another_gui_instance = Ui_MainWindow()

        # Hiển thị giao diện
        self.another_gui_instance.setupUi(MainWindow)
        self.stream1_active = False
        self.stream2_active = False
        MainWindow.showMaximized() 
