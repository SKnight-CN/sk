# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1122, 846)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setStyleSheet("")
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1122, 26))
        self.menubar.setObjectName("menubar")
        self.first = QtWidgets.QMenu(self.menubar)
        self.first.setObjectName("first")
        self.f1_1 = QtWidgets.QMenu(self.first)
        self.f1_1.setObjectName("f1_1")
        self.f1_2 = QtWidgets.QMenu(self.first)
        self.f1_2.setObjectName("f1_2")
        self.f1_3 = QtWidgets.QMenu(self.first)
        self.f1_3.setObjectName("f1_3")
        self.second = QtWidgets.QMenu(self.menubar)
        self.second.setObjectName("second")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.f1_1_1 = QtWidgets.QAction(MainWindow)
        self.f1_1_1.setObjectName("f1_1_1")
        self.f1_1_2 = QtWidgets.QAction(MainWindow)
        self.f1_1_2.setObjectName("f1_1_2")
        self.f1_1_3 = QtWidgets.QAction(MainWindow)
        self.f1_1_3.setObjectName("f1_1_3")
        self.f1_2_1 = QtWidgets.QAction(MainWindow)
        self.f1_2_1.setObjectName("f1_2_1")
        self.f1_2_2 = QtWidgets.QAction(MainWindow)
        self.f1_2_2.setObjectName("f1_2_2")
        self.f1_3_1 = QtWidgets.QAction(MainWindow)
        self.f1_3_1.setObjectName("f1_3_1")
        self.f1_3_2 = QtWidgets.QAction(MainWindow)
        self.f1_3_2.setObjectName("f1_3_2")
        self.f1_3_3 = QtWidgets.QAction(MainWindow)
        self.f1_3_3.setObjectName("f1_3_3")
        self.f1_3_4 = QtWidgets.QAction(MainWindow)
        self.f1_3_4.setObjectName("f1_3_4")
        self.f2_1_1 = QtWidgets.QAction(MainWindow)
        self.f2_1_1.setObjectName("f2_1_1")
        self.f2_1_2 = QtWidgets.QAction(MainWindow)
        self.f2_1_2.setObjectName("f2_1_2")
        self.f2_2_1 = QtWidgets.QAction(MainWindow)
        self.f2_2_1.setObjectName("f2_2_1")
        self.f1_1.addAction(self.f1_1_1)
        self.f1_1.addSeparator()
        self.f1_1.addAction(self.f1_1_2)
        self.f1_1.addSeparator()
        self.f1_1.addAction(self.f1_1_3)
        self.f1_2.addAction(self.f1_2_1)
        self.f1_2.addSeparator()
        self.f1_2.addAction(self.f1_2_2)
        self.f1_3.addAction(self.f1_3_1)
        self.f1_3.addSeparator()
        self.f1_3.addAction(self.f1_3_2)
        self.f1_3.addSeparator()
        self.f1_3.addAction(self.f1_3_3)
        self.f1_3.addSeparator()
        self.f1_3.addAction(self.f1_3_4)
        self.first.addAction(self.f1_1.menuAction())
        self.first.addSeparator()
        self.first.addAction(self.f1_2.menuAction())
        self.first.addSeparator()
        self.first.addAction(self.f1_3.menuAction())
        self.second.addAction(self.f2_1_1)
        self.second.addSeparator()
        self.second.addAction(self.f2_1_2)
        self.second.addSeparator()
        self.second.addAction(self.f2_2_1)
        self.menubar.addAction(self.first.menuAction())
        self.menubar.addAction(self.second.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.first.setTitle(_translate("MainWindow", "产品基本信息"))
        self.f1_1.setTitle(_translate("MainWindow", "手录产品"))
        self.f1_2.setTitle(_translate("MainWindow", "入池债"))
        self.f1_3.setTitle(_translate("MainWindow", "产品绝对收益率"))
        self.second.setTitle(_translate("MainWindow", "市场追踪"))
        self.f1_1_1.setText(_translate("MainWindow", "显示产品"))
        self.f1_1_2.setText(_translate("MainWindow", "手动录入"))
        self.f1_1_3.setText(_translate("MainWindow", "邮件抓取"))
        self.f1_2_1.setText(_translate("MainWindow", "显示入池债"))
        self.f1_2_2.setText(_translate("MainWindow", "手动录入"))
        self.f1_3_1.setText(_translate("MainWindow", "选择日期"))
        self.f1_3_2.setText(_translate("MainWindow", "产品收益率"))
        self.f1_3_3.setText(_translate("MainWindow", "单券收益率"))
        self.f1_3_4.setText(_translate("MainWindow", "退出标"))
        self.f2_1_1.setText(_translate("MainWindow", "更新近一月内发行债券"))
        self.f2_1_2.setText(_translate("MainWindow", "市场跟踪表"))
        self.f2_2_1.setText(_translate("MainWindow", "入池债跟踪"))
