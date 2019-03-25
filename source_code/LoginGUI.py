# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoginGUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(293, 390)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/mainUpdater.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Login.setWindowIcon(icon)
        self.logo = QtWidgets.QLabel(Login)
        self.logo.setGeometry(QtCore.QRect(80, 50, 141, 121))
        self.logo.setStyleSheet("image: url(:/image/mainUpdater.png);")
        self.logo.setText("")
        self.logo.setObjectName("logo")
        self.label_username = QtWidgets.QLabel(Login)
        self.label_username.setGeometry(QtCore.QRect(40, 200, 60, 16))
        self.label_username.setObjectName("label_username")
        self.label_password = QtWidgets.QLabel(Login)
        self.label_password.setGeometry(QtCore.QRect(40, 230, 60, 16))
        self.label_password.setObjectName("label_password")
        self.edit_username = QtWidgets.QLineEdit(Login)
        self.edit_username.setGeometry(QtCore.QRect(100, 198, 151, 21))
        self.edit_username.setObjectName("edit_username")
        self.edit_password = QtWidgets.QLineEdit(Login)
        self.edit_password.setGeometry(QtCore.QRect(100, 228, 151, 21))
        self.edit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.edit_password.setObjectName("edit_password")
        self.check_remember = QtWidgets.QCheckBox(Login)
        self.check_remember.setGeometry(QtCore.QRect(40, 280, 111, 20))
        self.check_remember.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.check_remember.setChecked(True)
        self.check_remember.setObjectName("check_remember")
        self.check_auto = QtWidgets.QCheckBox(Login)
        self.check_auto.setGeometry(QtCore.QRect(180, 280, 87, 20))
        self.check_auto.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.check_auto.setChecked(True)
        self.check_auto.setObjectName("check_auto")
        self.button_login = QtWidgets.QPushButton(Login)
        self.button_login.setGeometry(QtCore.QRect(100, 320, 113, 32))
        self.button_login.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_login.setStyleSheet("QPushButton{color: rgb(255, 255, 255)}\n"
"QPushButton{background-color: rgb(48, 112, 245)}\n"
"QPushButton:pressed{color: rgb(48, 112, 245)}\n"
"QPushButton:pressed{background-color: rgb(255, 255, 255)}\n"
"QPushButton{border-radius:10px}")
        self.button_login.setObjectName("button_login")

        self.retranslateUi(Login)
        self.button_login.clicked.connect(Login.button_login_click)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Ucas Course Auto Updater"))
        self.label_username.setText(_translate("Login", "用户名："))
        self.label_password.setText(_translate("Login", "密   码："))
        self.edit_username.setPlaceholderText(_translate("Login", "邮箱"))
        self.check_remember.setText(_translate("Login", "记住账号密码"))
        self.check_auto.setText(_translate("Login", "自动登录"))
        self.button_login.setText(_translate("Login", "登录"))
        self.button_login.setShortcut(_translate("Login", "Return"))


import resource_rc
