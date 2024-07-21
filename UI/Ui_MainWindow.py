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
