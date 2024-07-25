from PyQt5 import QtWidgets
import sys
from sface import *


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