# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogGUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 120)
        self.label_message = QtWidgets.QLabel(Dialog)
        self.label_message.setGeometry(QtCore.QRect(20, 20, 360, 60))
        self.label_message.setLineWidth(1)
        self.label_message.setTextFormat(QtCore.Qt.AutoText)
        self.label_message.setAlignment(QtCore.Qt.AlignCenter)
        self.label_message.setObjectName("label_message")
        self.button_ok = QtWidgets.QPushButton(Dialog)
        self.button_ok.setGeometry(QtCore.QRect(330, 90, 50, 20))
        self.button_ok.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_ok.setStyleSheet("QPushButton{color: rgb(255, 255, 255)}\n"
"QPushButton{background-color: rgb(48, 112, 245)}\n"
"QPushButton:pressed{color: rgb(48, 112, 245)}\n"
"QPushButton:pressed{background-color: rgb(255, 255, 255)}\n"
"QPushButton{border-radius:10px}")
        self.button_ok.setObjectName("button_ok")

        self.retranslateUi(Dialog)
        self.button_ok.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Title"))
        self.label_message.setText(_translate("Dialog", "message"))
        self.button_ok.setText(_translate("Dialog", "OK"))
        self.button_ok.setShortcut(_translate("Dialog", "Return"))


