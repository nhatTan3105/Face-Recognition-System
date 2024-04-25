from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from sql_query import create_connection, select_student_by_studentID
import datetime
from PyQt5.QtGui import QPixmap
from sface import detect_and_draw_labels
import pickle
import os
class VideoLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(VideoLabel, self).__init__(parent)

    def setPixmap(self, pixmap):
        super().setPixmap(pixmap)
        self.setScaledContents(True)

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
        import main
        # Tạo một instance của giao diện
        self.another_gui_instance = main.Ui_MainWindow()

        # Hiển thị giao diện
        self.another_gui_instance.setupUi(MainWindow)
        self.attendace_active = False
        MainWindow.showMaximized()       
    def create_student(self, MainWindow):
        import create_student
        # Tạo một instance của giao diện
        self.another_gui_instance = create_student.Create()

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
     
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Attendance()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
