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

from LoadingScreen import LoadingScreen
from Ui_MainWindow import Ui_MainWindow

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