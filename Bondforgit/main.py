import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import mainwindow
import untitled
from WindPy import w

if __name__ == '__main__':
    w.start()
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    #ui = untitled.Ui_MainWindow()
    ui = mainwindow.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
