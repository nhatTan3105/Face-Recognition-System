from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from sface import *


class Database(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Database")
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
        self.btnBack = QtWidgets.QPushButton(self.centralwidget)
        self.btnBack.setObjectName("btnBack")
        self.btnBack.setFixedSize(100, 30)
        self.btnBack.clicked.connect(lambda: self.back(MainWindow))
        self.btnBack.setStyleSheet("background-color: #cccccc;")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(100, 0, 120 ,120)
        self.studentImage = QtWidgets.QLabel(self.centralwidget)
        self.studentImage.setMaximumSize(QtCore.QSize(400, 400))
        self.studentImage.setFrameShape(QtWidgets.QFrame.Box)
        self.studentImage.setLineWidth(2)
        self.studentImage.setText("")
        self.studentImage.setObjectName("studentImage")
        self.studentImage.setFixedSize(400, 400)
        self.studentImage.setScaledContents(True)
        self.verticalLayout_2.addWidget(self.studentImage, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(80, 40))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.studentName = QtWidgets.QLineEdit(self.centralwidget)
        self.studentName.setObjectName("studentName")
        self.studentName.setFixedSize(300, 30)
        self.verticalLayout_2.addWidget(self.studentName, 1, QtCore.Qt.AlignHCenter)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setMaximumSize(QtCore.QSize(80, 40))
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.studentID = QtWidgets.QLineEdit(self.centralwidget)
        self.studentID.setObjectName("studentID")
        self.studentID.setFixedSize(300, 30)
        self.verticalLayout_2.addWidget(self.studentID, 1, QtCore.Qt.AlignHCenter)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setMaximumSize(QtCore.QSize(80, 40))
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.studentFaculty = QtWidgets.QLineEdit(self.centralwidget)
        self.studentFaculty.setObjectName("studentFaculty")
        self.studentFaculty.setFixedSize(300, 30)
        self.verticalLayout_2.addWidget(self.studentFaculty, 1, QtCore.Qt.AlignHCenter)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setMaximumSize(QtCore.QSize(80, 40))
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.studentYear = QtWidgets.QLineEdit(self.centralwidget)
        self.studentYear.setObjectName("studentYear")
        self.studentYear.setFixedSize(300, 30)
        self.verticalLayout_2.addWidget(self.studentYear, 1, QtCore.Qt.AlignHCenter)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        
        # Add new horizontal layout for Delete and Update buttons
        self.horizontalLayout_buttons = QtWidgets.QHBoxLayout()
        self.horizontalLayout_buttons.setObjectName("horizontalLayout_buttons")
        self.btnDelete = QtWidgets.QPushButton(self.widget)
        self.btnDelete.setObjectName("btnDelete")
        self.btnDelete.setStyleSheet("background-color: #ff6666;")
        self.btnDelete.setText('Delete')
        self.btnDelete.setFixedSize(100, 30)
        self.btnDelete.clicked.connect(lambda: self.handle_delete)
        self.horizontalLayout_buttons.addWidget(self.btnDelete)
        self.btnUpdate = QtWidgets.QPushButton(self.widget)
        self.btnUpdate.setObjectName("btnUpdate")
        self.btnUpdate.setStyleSheet("background-color: #85c9e8;")
        self.btnUpdate.setText('Update')
        self.btnUpdate.setFixedSize(100, 30)
        self.btnUpdate.clicked.connect(self.handle_update)
        self.horizontalLayout_buttons.addWidget(self.btnUpdate)
        self.verticalLayout_2.addLayout(self.horizontalLayout_buttons)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

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
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Student Name', 'Faculty', 'Year', 'Image', 'Image URL'])
        self.tableWidget.itemClicked.connect(self.on_item_clicked)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.btnCreateStudent = QtWidgets.QPushButton(self.widget)
        self.btnCreateStudent.setObjectName("btnCreateStudent")
        self.btnCreateStudent.setStyleSheet("background-color: #8dd9c2;")
        self.btnCreateStudent.setText('Create Student')
        self.btnCreateStudent.setFixedSize(150, 40)
        self.btnCreateStudent.clicked.connect(lambda: self.create_student(MainWindow))
        self.verticalLayout_2.addWidget(self.btnCreateStudent)
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

        self.load_data()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Database"))
        self.btnBack.setText(_translate("MainWindow", "Back"))
        self.btnSearch.setText(_translate("MainWindow", "Search"))
        self.label.setText(_translate("MainWindow", "Name:"))
        self.label_2.setText(_translate("MainWindow", "Student ID:"))
        self.label_3.setText(_translate("MainWindow", "Faculty:"))
        self.label_4.setText(_translate("MainWindow", "Year:"))

    def on_item_clicked(self, item):
        row = item.row()
        self.studentID.setText(self.tableWidget.item(row, 0).text())
        self.studentName.setText(self.tableWidget.item(row, 1).text())
        self.studentFaculty.setText(self.tableWidget.item(row, 2).text())
        self.studentYear.setText(self.tableWidget.item(row, 3).text())
        
        # Lấy URL hình ảnh từ cột 'ImageURL'
        image_url = self.tableWidget.item(row, 5).text()
        
        # Tải và hiển thị hình ảnh từ URL
        pixmap = QtGui.QPixmap(image_url)
        if not pixmap.isNull():
            self.studentImage.setPixmap(pixmap)
        else:
            self.studentImage.clear()  # Xóa hình ảnh nếu không tải được
    def handle_delete(self):
        student_id = self.studentID.text()
        if student_id:
            conn = create_connection("database.db")
            delete_student(conn, student_id)
            conn.close()
            self.load_data()  # Reload data after delete
        else:
            print("No student ID provided for deletion.")

    def handle_update(self):
        student_id = self.studentID.text()
        name = self.studentName.text()
        faculty = self.studentFaculty.text()
        year = self.studentYear.text()  
        image_url = self.tableWidget.item(self.tableWidget.currentRow(), 5).text()

        if student_id and name and faculty and image_url:
            conn = create_connection("database.db")
            try:
                update_student(conn, student_id, name, faculty, year, image_url)
                self.load_data()  # Reload data after update
                
                # Hiển thị thông báo thành công
                QMessageBox.information(self.centralwidget, "Success", "Student record updated successfully.")
            except Exception as e:
                # Hiển thị thông báo lỗi nếu có ngoại lệ
                QMessageBox.critical(self.centralwidget, "Error", f"An error occurred: {e}")
            finally:
                conn.close()
        else:
            # Hiển thị thông báo nếu có dữ liệu không đầy đủ
            QMessageBox.warning(self.centralwidget, "Incomplete Data", "Please fill all the fields.")


    def load_data(self):
        database = r"database.db"
        conn = create_connection(database)
        cursor = conn.cursor()
        cursor.execute("SELECT ID, StudentName, Faculty, Year, Image, ImageURL FROM Students")
        rows = cursor.fetchall()

        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(rows):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if column_number == 4:  # Image column
                    item = QtWidgets.QTableWidgetItem()
                    pixmap = QtGui.QPixmap()
                    pixmap.loadFromData(data)
                    item.setIcon(QtGui.QIcon(pixmap))
                    self.tableWidget.setItem(row_number, column_number, item)
                else:
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        
        conn.close()

    def create_student(self, MainWindow):
        from common import Create
        # Tạo một instance của giao diện
        self.another_gui_instance = Create()
        self.attendace_active = False
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

    def back(self, MainWindow):
        from common import Attendance
        self.another_gui_instance = Attendance()
        self.another_gui_instance.setupUi(MainWindow)