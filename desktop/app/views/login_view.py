# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI - Login.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


class LoginView(QtWidgets.QMainWindow):

    def closeEvent(self, event):
        self.destroy()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos()-self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        try:
            if event.buttons() and Qt.LeftButton:
                self.move(event.globalPos()-self.m_DragPosition)
                event.accept()
        except AttributeError:
            pass

    def mouseReleaseEvent(self, event):
        self.m_drag = False

    def setupUi(self):
        if not self.objectName():
            self.setObjectName(u"MainWindow")
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.resize(920, 451)
        self.CentralWidget = QtWidgets.QWidget(self)
        self.CentralWidget.setObjectName("CentralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.CentralWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.frameContainer = QtWidgets.QFrame(self.CentralWidget)
        self.frameContainer.setStyleSheet("")
        self.frameContainer.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameContainer.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameContainer.setLineWidth(0)
        self.frameContainer.setObjectName("frameContainer")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frameContainer)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frameWindowPanel = QtWidgets.QFrame(self.frameContainer)
        self.frameWindowPanel.setMinimumSize(QtCore.QSize(0, 40))
        self.frameWindowPanel.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frameWindowPanel.setStyleSheet("QFrame {\n"
"    background-color : #000000;\n"
"}")
        self.frameWindowPanel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameWindowPanel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameWindowPanel.setLineWidth(0)
        self.frameWindowPanel.setObjectName("frameWindowPanel")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frameWindowPanel)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.framePushButtonWindowPanel = QtWidgets.QFrame(self.frameWindowPanel)
        self.framePushButtonWindowPanel.setMinimumSize(QtCore.QSize(0, 40))
        self.framePushButtonWindowPanel.setMaximumSize(QtCore.QSize(16777215, 40))
        self.framePushButtonWindowPanel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.framePushButtonWindowPanel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.framePushButtonWindowPanel.setLineWidth(0)
        self.framePushButtonWindowPanel.setObjectName("framePushButtonWindowPanel")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.framePushButtonWindowPanel)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButtonClose = QtWidgets.QPushButton(self.framePushButtonWindowPanel)
        self.pushButtonClose.setMinimumSize(QtCore.QSize(42, 42))
        self.pushButtonClose.setMaximumSize(QtCore.QSize(42, 42))
        self.pushButtonClose.setStyleSheet("QPushButton {\n"
"    background-color : #000000;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color : #A93226;\n"
"}")
        self.pushButtonClose.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-x.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonClose.setIcon(icon)
        self.pushButtonClose.setIconSize(QtCore.QSize(18, 18))
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.gridLayout_3.addWidget(self.pushButtonClose, 0, 3, 1, 1)
        self.pushButtonMinimize = QtWidgets.QPushButton(self.framePushButtonWindowPanel)
        self.pushButtonMinimize.setMinimumSize(QtCore.QSize(42, 42))
        self.pushButtonMinimize.setMaximumSize(QtCore.QSize(42, 42))
        self.pushButtonMinimize.setStyleSheet("QPushButton {\n"
"    background-color : #000000;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color : #555555;\n"
"}")
        self.pushButtonMinimize.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-window-minimize.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonMinimize.setIcon(icon1)
        self.pushButtonMinimize.setIconSize(QtCore.QSize(18, 18))
        self.pushButtonMinimize.setObjectName("pushButtonMinimize")
        self.gridLayout_3.addWidget(self.pushButtonMinimize, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 1, 1, 1)
        self.labelWindowTitle = QtWidgets.QLabel(self.framePushButtonWindowPanel)
        self.labelWindowTitle.setStyleSheet("QLabel {\n"
"    font : 77 15pt \"Microsoft JhengHei UI\";\n"
"    color : #FFFFFF;\n"
"    border-radius : 0px;\n"
"    text-align : left;\n"
"    padding-left: 5px;\n"
"}\n"
"\n"
"QLabel::hover {\n"
"    color : #4F6FA0;\n"
"}\n"
"")
        self.labelWindowTitle.setText("")
        self.labelWindowTitle.setObjectName("labelWindowTitle")
        self.gridLayout_3.addWidget(self.labelWindowTitle, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.framePushButtonWindowPanel, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frameWindowPanel, 1, 0, 1, 1)
        self.frameContent = QtWidgets.QFrame(self.frameContainer)
        self.frameContent.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameContent.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameContent.setLineWidth(0)
        self.frameContent.setObjectName("frameContent")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frameContent)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.frameLogin = QtWidgets.QFrame(self.frameContent)
        self.frameLogin.setMinimumSize(QtCore.QSize(600, 0))
        self.frameLogin.setMaximumSize(QtCore.QSize(600, 16777215))
        self.frameLogin.setStyleSheet("QFrame {\n"
"    background-color: #FFFFFF;\n"
"}")
        self.frameLogin.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameLogin.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameLogin.setLineWidth(0)
        self.frameLogin.setObjectName("frameLogin")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frameLogin)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frameLoginContent = QtWidgets.QFrame(self.frameLogin)
        self.frameLoginContent.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameLoginContent.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameLoginContent.setLineWidth(0)
        self.frameLoginContent.setObjectName("frameLoginContent")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frameLoginContent)
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout.setSpacing(9)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frameUserCredentials = QtWidgets.QFrame(self.frameLoginContent)
        self.frameUserCredentials.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameUserCredentials.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameUserCredentials.setLineWidth(0)
        self.frameUserCredentials.setObjectName("frameUserCredentials")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frameUserCredentials)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setHorizontalSpacing(0)
        self.gridLayout_5.setVerticalSpacing(5)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.labelUsername = QtWidgets.QLabel(self.frameUserCredentials)
        self.labelUsername.setStyleSheet("QLabel{\n"
"    font : 75 14pt \"Microsoft JhengHei UI\" ;\n"
"    color : #4F6FA0;\n"
"    border-radius : 0px;\n"
"    text-align : left;\n"
"    padding: 10px;\n"
"}\n"
"")
        self.labelUsername.setLineWidth(0)
        self.labelUsername.setIndent(-1)
        self.labelUsername.setObjectName("labelUsername")
        self.gridLayout_5.addWidget(self.labelUsername, 2, 0, 2, 1)
        self.lineEditUsername = QtWidgets.QLineEdit(self.frameUserCredentials)
        self.lineEditUsername.setStyleSheet("QLineEdit {\n"
"    font: 27 14pt \"Microsoft YaHei UI Light\";\n"
"}")
        self.lineEditUsername.setText("")
        self.lineEditUsername.setObjectName("lineEditUsername")
        self.gridLayout_5.addWidget(self.lineEditUsername, 3, 2, 1, 1)
        self.lineEditUserPassword = QtWidgets.QLineEdit(self.frameUserCredentials)
        self.lineEditUserPassword.setStyleSheet("QLineEdit {\n"
"    font: 27 14pt \"Microsoft YaHei UI Light\";\n"
"}")
        self.lineEditUserPassword.setText("")
        self.lineEditUserPassword.setObjectName("lineEditUserPassword")
        self.gridLayout_5.addWidget(self.lineEditUserPassword, 4, 2, 1, 1)
        self.labelUserPassword = QtWidgets.QLabel(self.frameUserCredentials)
        self.labelUserPassword.setStyleSheet("QLabel{\n"
"    font : 75 14pt \"Microsoft JhengHei UI\" ;\n"
"    color : #4F6FA0;\n"
"    border-radius : 0px;\n"
"\n"
"    text-align : left;\n"
"    padding: 10px;\n"
"}\n"
"")
        self.labelUserPassword.setLineWidth(0)
        self.labelUserPassword.setObjectName("labelUserPassword")
        self.gridLayout_5.addWidget(self.labelUserPassword, 4, 0, 1, 1)
        self.pushButtonLogin = QtWidgets.QPushButton(self.frameUserCredentials)
        self.pushButtonLogin.setMinimumSize(QtCore.QSize(280, 0))
        self.pushButtonLogin.setMaximumSize(QtCore.QSize(280, 16777215))
        self.pushButtonLogin.setStyleSheet("QPushButton{\n"
"    background-color : #D62233;\n"
"    font : 75 12pt \"Microsoft JhengHei UI\" bold;\n"
"    color : #FFFFFF;\n"
"    border-radius : 0px;\n"
"    text-align : left;\n"
"    padding : 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: #FF3346;\n"
"    font : 75 12pt \"Microsoft JhengHei UI\" bold;\n"
"    color : #FFFFFF;\n"
"}\n"
"")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-arrow-circle-right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonLogin.setIcon(icon2)
        self.pushButtonLogin.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonLogin.setFlat(True)
        self.pushButtonLogin.setObjectName("pushButtonLogin")
        self.gridLayout_5.addWidget(self.pushButtonLogin, 6, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem1, 4, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem2, 1, 0, 1, 3)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem3, 3, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem4, 7, 2, 1, 1)
        self.radioButtonRememberUser = QtWidgets.QRadioButton(self.frameUserCredentials)
        self.radioButtonRememberUser.setStyleSheet("QRadioButton {\n"
"    font : 75 11pt \"Microsoft JhengHei UI\"  bold;\n"
"    color : #000000;\n"
"    border-radius : 0px;\n"
"}\n"
"\n"
"QRadioButton:hover {\n"
"    color : #3A609B;\n"
"    border-radius : 0px;\n"
"}\n"
"\n"
"QRadioButton::checked {\n"
"    color : #3A609B;\n"
"    border-radius : 0px;\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    color : #3A609B;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked:pressed {\n"
"    color : #3A609B;\n"
"}")
        self.radioButtonRememberUser.setObjectName("radioButtonRememberUser")
        self.gridLayout_5.addWidget(self.radioButtonRememberUser, 8, 2, 1, 1)
        self.labelLoginTitle = QtWidgets.QLabel(self.frameUserCredentials)
        self.labelLoginTitle.setStyleSheet("QLabel {\n"
"    font: 25 20pt \"Microsoft YaHei UI Light\" bold ;\n"
"    color : #4F6FA0;\n"
"    padding : 10px;\n"
"}")
        self.labelLoginTitle.setObjectName("labelLoginTitle")
        self.gridLayout_5.addWidget(self.labelLoginTitle, 0, 0, 1, 3)
        spacerItem5 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_5.addItem(spacerItem5, 5, 2, 1, 1)
        self.verticalLayout.addWidget(self.frameUserCredentials)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem6)
        self.verticalLayout_2.addWidget(self.frameLoginContent)
        self.gridLayout_6.addWidget(self.frameLogin, 0, 1, 1, 1)
        self.frameInfo = QtWidgets.QFrame(self.frameContent)
        self.frameInfo.setMinimumSize(QtCore.QSize(320, 0))
        self.frameInfo.setStyleSheet("QFrame {\n"
"    /*416597*/\n"
"    background-color : #333333;\n"
"}")
        self.frameInfo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameInfo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameInfo.setObjectName("frameInfo")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.frameInfo)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.labelLogo = QtWidgets.QLabel(self.frameInfo)
        self.labelLogo.setMaximumSize(QtCore.QSize(300, 90))
        self.labelLogo.setText("")
        self.labelLogo.setPixmap(QtGui.QPixmap("app/resources/img/banners/banner-2.png"))
        self.labelLogo.setScaledContents(True)
        self.labelLogo.setWordWrap(False)
        self.labelLogo.setObjectName("labelLogo")
        self.gridLayout_7.addWidget(self.labelLogo, 0, 0, 1, 1)
        self.labelVersion = QtWidgets.QLabel(self.frameInfo)
        self.labelVersion.setStyleSheet("QLabel {\n"
"    font: 22 10pt \"Microsoft YaHei UI Light\" bold;\n"
"    color : #FFFFFF;\n"
"    padding-left : 10px;\n"
"}")
        self.labelVersion.setObjectName("labelVersion")
        self.gridLayout_7.addWidget(self.labelVersion, 1, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_7.addItem(spacerItem7, 2, 0, 1, 1)
        self.gridLayout_6.addWidget(self.frameInfo, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frameContent, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.frameContainer, 0, 0, 1, 1)
        self.setCentralWidget(self.CentralWidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelUsername.setText(_translate("MainWindow", "Nombre de usuario"))
        self.labelUserPassword.setText(_translate("MainWindow", "Contraseña"))
        self.pushButtonLogin.setText(_translate("MainWindow", "Iniciar sesion"))
        self.radioButtonRememberUser.setText(_translate("MainWindow", "Recordarme"))
        self.labelLoginTitle.setText(_translate("MainWindow", "Login"))
        self.labelVersion.setText(_translate("MainWindow", "version 1.0"))
