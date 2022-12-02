# Form implementation generated from reading ui file 'Menu.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtNetwork, QtWidgets, QtGui

import json


class SideGrip(QtWidgets.QWidget):

    def __init__(self, parent, edge):
        QtWidgets.QWidget.__init__(self, parent)

        #self.setStyleSheet("border : 1px solid #000000;")

        self.WidgetSideGrip = QtWidgets.QWidget(self)
        self.WidgetSideGrip.setObjectName('WidgetSideGrip')
        self.WidgetSideGrip.setStyleSheet('''
            QWidget#WidgetSideGrip {
                background: #D37242;
                border-radius: 20px;
                border: 12px solid #D37242;                   
            }
        ''')

        self.BoxLayoutSideGrip = QtWidgets.QVBoxLayout(self)
        self.BoxLayoutSideGrip.setContentsMargins(0, 0, 0, 0)
        self.BoxLayoutSideGrip.addWidget(self.WidgetSideGrip)

        if edge == QtCore.Qt.LeftEdge:
            self.setCursor(QtCore.Qt.SizeHorCursor)
            self.resizeFunction = self.resizeLeft

        elif edge == QtCore.Qt.TopEdge:
            self.setCursor(QtCore.Qt.SizeVerCursor)
            self.resizeFunction = self.resizeTop

        elif edge == QtCore.Qt.RightEdge:
            self.setCursor(QtCore.Qt.SizeHorCursor)
            self.resizeFunction = self.resizeRight

        else:
            self.setCursor(QtCore.Qt.SizeVerCursor)
            self.resizeFunction = self.resizeBottom

        self.mousePos = None



    def resizeLeft(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() - delta.x())
        geo = window.geometry()
        geo.setLeft(geo.right() - width)
        window.setGeometry(geo)

    def resizeTop(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() - delta.y())
        geo = window.geometry()
        geo.setTop(geo.bottom() - height)
        window.setGeometry(geo)

    def resizeRight(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() + delta.x())
        window.resize(width, window.height())

    def resizeBottom(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() + delta.y())
        window.resize(window.width(), height)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mousePos is not None:
            delta = event.pos() - self.mousePos
            self.resizeFunction(delta)

    def mouseReleaseEvent(self, event):
        self.mousePos = None



class PostFormView(QtWidgets.QMainWindow):
    _gripSize = 1

    def __init__(self, Controller):
        super().__init__()

        self.Controller = Controller

        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        self.sideGrips = [
            SideGrip(self, QtCore.Qt.LeftEdge), 
            SideGrip(self, QtCore.Qt.TopEdge), 
            SideGrip(self, QtCore.Qt.RightEdge), 
            SideGrip(self, QtCore.Qt.BottomEdge), 
        ]
        self.cornerGrips = [QtWidgets.QSizeGrip(self) for i in range(4)]

        self.manager = QtNetwork.QNetworkAccessManager()
        self.manager.finished.connect(self.handleResults)

    @QtCore.pyqtSlot(QtNetwork.QNetworkReply)
    def handleResults(self, reply):
        true, false, null = True, False, None

        parsed = json.loads(reply.readAll().data())
        text = json.dumps(parsed, indent=4, sort_keys=True)

        if reply.error() == QtNetwork.QNetworkReply.NoError:
            self.Controller.View.get_message_view(
                status = QMessageBox.Information,
                title = 'Operacion finalizada',
                message = f'Se ha creado la publicacion'
            )

        else:
            self.Controller.View.get_message_view(
                status = QMessageBox.Critical,
                title = 'Operacion interrumpida',
                message = f'Ha ocurrido un error inesperado:\n{reply.errorString()}'
            )
        reply.deleteLater()

    @property
    def gripSize(self):
        return self._gripSize

    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        self.setContentsMargins(*[self.gripSize] * 4)

        outRect = self.rect()
        inRect = outRect.adjusted(self.gripSize, self.gripSize,
            -self.gripSize, -self.gripSize)

        # top left
        self.cornerGrips[0].setGeometry(
            QtCore.QRect(outRect.topLeft(), inRect.topLeft()))

        # top right
        self.cornerGrips[1].setGeometry(
            QtCore.QRect(outRect.topRight(), inRect.topRight()).normalized())

        # bottom right
        self.cornerGrips[2].setGeometry(
            QtCore.QRect(inRect.bottomRight(), outRect.bottomRight()))

        # bottom left
        self.cornerGrips[3].setGeometry(
            QtCore.QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized())

        # left edge
        self.sideGrips[0].setGeometry(
            0, inRect.top(), self.gripSize, inRect.height())

        # top edge
        self.sideGrips[1].setGeometry(
            inRect.left(), 0, inRect.width(), self.gripSize)

        # right edge
        self.sideGrips[2].setGeometry(
            inRect.left() + inRect.width(), 
            inRect.top(), self.gripSize, inRect.height())

        # bottom edge
        self.sideGrips[3].setGeometry(
            self.gripSize, inRect.top() + inRect.height(), 
            inRect.width(), self.gripSize)

    def closeEvent(self, event):
        self.destroy()

    def resizeEvent(self, event):
        QtWidgets.QMainWindow.resizeEvent(self, event)
        self.updateGrips()

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

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            qApp.quit()

        else:
            super().keyPressEvent(event)

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setEnabled(True)
        self.resize(900, 619)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(900, 0))
        self.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.frameWindowPanel = QtWidgets.QFrame(self.centralWidget)
        self.frameWindowPanel.setMaximumSize(QtCore.QSize(16777215, 46))
        self.frameWindowPanel.setStyleSheet("QFrame {\n"
"    background : #000000\n"
"}")
        self.frameWindowPanel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameWindowPanel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameWindowPanel.setLineWidth(0)
        self.frameWindowPanel.setObjectName("frameWindowPanel")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frameWindowPanel)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.framePushButtonWindowPanel = QtWidgets.QFrame(self.frameWindowPanel)
        self.framePushButtonWindowPanel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.framePushButtonWindowPanel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.framePushButtonWindowPanel.setLineWidth(0)
        self.framePushButtonWindowPanel.setObjectName("framePushButtonWindowPanel")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.framePushButtonWindowPanel)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.pushButtonClose = QtWidgets.QPushButton(self.framePushButtonWindowPanel)
        self.pushButtonClose.setMinimumSize(QtCore.QSize(42, 42))
        self.pushButtonClose.setMaximumSize(QtCore.QSize(42, 42))
        self.pushButtonClose.setStyleSheet("QPushButton {\n"
"    background-color : #A93226;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"    background-color : #87281E\n"
"}")
        self.pushButtonClose.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-x.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonClose.setIcon(icon)
        self.pushButtonClose.setIconSize(QtCore.QSize(18, 18))
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.gridLayout_4.addWidget(self.pushButtonClose, 0, 2, 1, 1)
        self.pushButtonRestore = QtWidgets.QPushButton(self.framePushButtonWindowPanel)
        self.pushButtonRestore.setMinimumSize(QtCore.QSize(42, 42))
        self.pushButtonRestore.setMaximumSize(QtCore.QSize(42, 42))
        self.pushButtonRestore.setStyleSheet("QPushButton {\n"
"    background-color : #000000;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color : #555555;\n"
"}")
        self.pushButtonRestore.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-window-maximize.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonRestore.setIcon(icon1)
        self.pushButtonRestore.setIconSize(QtCore.QSize(18, 18))
        self.pushButtonRestore.setObjectName("pushButtonRestore")
        self.gridLayout_4.addWidget(self.pushButtonRestore, 0, 1, 1, 1)
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
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-window-minimize.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonMinimize.setIcon(icon2)
        self.pushButtonMinimize.setIconSize(QtCore.QSize(18, 18))
        self.pushButtonMinimize.setObjectName("pushButtonMinimize")
        self.gridLayout_4.addWidget(self.pushButtonMinimize, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.framePushButtonWindowPanel, 0, 2, 1, 1)
        self.labelWindowTitle = QtWidgets.QLabel(self.frameWindowPanel)
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
        self.gridLayout_5.addWidget(self.labelWindowTitle, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.frameWindowPanel, 0, 0, 1, 2)
        self.frameContainer = QtWidgets.QFrame(self.centralWidget)
        self.frameContainer.setStyleSheet("QFrame {\n"
"    background : #FFFFFF;\n"
"}")
        self.frameContainer.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameContainer.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameContainer.setLineWidth(0)
        self.frameContainer.setObjectName("frameContainer")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frameContainer)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.labelForm = QtWidgets.QLabel(self.frameContainer)
        self.labelForm.setMinimumSize(QtCore.QSize(0, 50))
        self.labelForm.setMaximumSize(QtCore.QSize(16777215, 50))
        self.labelForm.setStyleSheet("QLabel{\n"
"    background-color: #222222;\n"
"    font : 77 17pt \"Microsoft JhengHei UI\" bold;\n"
"    color : #FFFFFF;\n"
"    border-radius : 0px;\n"
"    text-align : left;\n"
"    padding: 10px;\n"
"}\n"
"")
        self.labelForm.setObjectName("labelForm")
        self.gridLayout_6.addWidget(self.labelForm, 0, 0, 1, 1)
        self.framePostForm = QtWidgets.QFrame(self.frameContainer)
        self.framePostForm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.framePostForm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.framePostForm.setObjectName("framePostForm")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.framePostForm)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBoxForm = QtWidgets.QGroupBox(self.framePostForm)
        self.groupBoxForm.setStyleSheet("QGroupBox {\n"
"\n"
"    font: 76 13pt \"Microsoft JhengHei UI\";\n"
"    font-weight: bold;\n"
"    color: #D37242;\n"
"}\n"
"\n"
"")
        self.groupBoxForm.setTitle("")
        self.groupBoxForm.setObjectName("groupBoxForm")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBoxForm)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButtonPost = QtWidgets.QPushButton(self.groupBoxForm)
        self.pushButtonPost.setMinimumSize(QtCore.QSize(250, 0))
        self.pushButtonPost.setStyleSheet("QPushButton{\n"
"    background-color : #D37242;\n"
"    font : 75 13pt \"Microsoft JhengHei UI\" bold;\n"
"    color : #FFFFFF;\n"
"    border-radius : 0px;\n"
"\n"
"    text-align : left;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: #BB673D;\n"
"    font : 75 13pt \"Microsoft JhengHei UI\" bold;\n"
"    color : #FFFFFF;\n"
"}\n"
"")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-paper-plane.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonPost.setIcon(icon3)
        self.pushButtonPost.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonPost.setObjectName("pushButtonPost")
        self.gridLayout_2.addWidget(self.pushButtonPost, 7, 0, 1, 2)
        self.labelPrice = QtWidgets.QLabel(self.groupBoxForm)
        self.labelPrice.setStyleSheet("QLabel {\n"
"    font: 25 11pt \"Microsoft YaHei UI Light\";\n"
"}")
        self.labelPrice.setObjectName("labelPrice")
        self.gridLayout_2.addWidget(self.labelPrice, 1, 0, 1, 1)
        self.spinBoxQuantity = QtWidgets.QSpinBox(self.groupBoxForm)
        self.spinBoxQuantity.setMinimumSize(QtCore.QSize(0, 26))
        self.spinBoxQuantity.setMaximumSize(QtCore.QSize(16777215, 26))
        self.spinBoxQuantity.setStyleSheet("QSpinBox {\n"
"    font: 25 11pt \"Microsoft YaHei UI Light\";\n"
"}")
        self.spinBoxQuantity.setMinimum(1)
        self.spinBoxQuantity.setMaximum(1000)
        self.spinBoxQuantity.setObjectName("spinBoxQuantity")
        self.gridLayout_2.addWidget(self.spinBoxQuantity, 2, 2, 1, 1)
        self.pushButtonSelectImage = QtWidgets.QPushButton(self.groupBoxForm)
        self.pushButtonSelectImage.setMinimumSize(QtCore.QSize(26, 26))
        self.pushButtonSelectImage.setMaximumSize(QtCore.QSize(16777215, 26))
        self.pushButtonSelectImage.setStyleSheet("QPushButton{\n"
"    background-color : #6B5876;\n"
"    font : 75 13pt \"Microsoft JhengHei UI\" bold;\n"
"    color : #FFFFFF;\n"
"    border-radius : 0px;\n"
"    text-align : left;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: #836C90;\n"
"    font : 75 13pt \"Microsoft JhengHei UI\" bold;\n"
"    color : #FFFFFF;\n"
"}\n"
"\n"
"")
        self.pushButtonSelectImage.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-folder-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonSelectImage.setIcon(icon4)
        self.pushButtonSelectImage.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonSelectImage.setFlat(True)
        self.pushButtonSelectImage.setObjectName("pushButtonSelectImage")
        self.gridLayout_2.addWidget(self.pushButtonSelectImage, 4, 3, 1, 1)
        self.labelDescription = QtWidgets.QLabel(self.groupBoxForm)
        self.labelDescription.setStyleSheet("QLabel {\n"
"    font: 25 11pt \"Microsoft YaHei UI Light\";\n"
"}")
        self.labelDescription.setObjectName("labelDescription")
        self.gridLayout_2.addWidget(self.labelDescription, 6, 0, 1, 1)
        self.labelTitle = QtWidgets.QLabel(self.groupBoxForm)
        self.labelTitle.setStyleSheet("QLabel {\n"
"    font: 25 11pt \"Microsoft YaHei UI Light\";\n"
"}")
        self.labelTitle.setObjectName("labelTitle")
        self.gridLayout_2.addWidget(self.labelTitle, 0, 0, 1, 1)
        self.horizontalSliderQuality = QtWidgets.QSlider(self.groupBoxForm)
        self.horizontalSliderQuality.setMinimum(1)
        self.horizontalSliderQuality.setMaximum(5)
        self.horizontalSliderQuality.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderQuality.setObjectName("horizontalSliderQuality")
        self.gridLayout_2.addWidget(self.horizontalSliderQuality, 3, 2, 1, 1)
        self.labelImage = QtWidgets.QLabel(self.groupBoxForm)
        self.labelImage.setStyleSheet("QLabel {\n"
"    font: 25 11pt \"Microsoft YaHei UI Light\";\n"
"}")
        self.labelImage.setObjectName("labelImage")
        self.gridLayout_2.addWidget(self.labelImage, 4, 0, 1, 1)
        self.labelQuality = QtWidgets.QLabel(self.groupBoxForm)
        self.labelQuality.setStyleSheet("QLabel {\n"
"    font: 25 11pt \"Microsoft YaHei UI Light\";\n"
"}")
        self.labelQuality.setObjectName("labelQuality")
        self.gridLayout_2.addWidget(self.labelQuality, 3, 0, 1, 1)
        self.lineEditTitle = QtWidgets.QLineEdit(self.groupBoxForm)
        self.lineEditTitle.setStyleSheet("QLineEdit {\n"
"    font: 25 11pt \"Microsoft YaHei UI Light\";\n"
"}")
        self.lineEditTitle.setObjectName("lineEditTitle")
        self.gridLayout_2.addWidget(self.lineEditTitle, 0, 2, 1, 1)
        self.labelQuantity = QtWidgets.QLabel(self.groupBoxForm)
        self.labelQuantity.setStyleSheet("QLabel {\n"
"    font: 25 11pt \"Microsoft YaHei UI Light\";\n"
"}")
        self.labelQuantity.setObjectName("labelQuantity")
        self.gridLayout_2.addWidget(self.labelQuantity, 2, 0, 1, 1)
        self.spinBoxPrice = QtWidgets.QSpinBox(self.groupBoxForm)
        self.spinBoxPrice.setEnabled(True)
        self.spinBoxPrice.setMinimumSize(QtCore.QSize(0, 26))
        self.spinBoxPrice.setMaximumSize(QtCore.QSize(16777215, 26))
        self.spinBoxPrice.setStyleSheet("QSpinBox {\n"
"    font: 25 11pt \"Microsoft YaHei UI Light\";\n"
"}")
        self.spinBoxPrice.setMinimum(100)
        self.spinBoxPrice.setMaximum(1000000)
        self.spinBoxPrice.setObjectName("spinBoxPrice")
        self.gridLayout_2.addWidget(self.spinBoxPrice, 1, 2, 1, 1)
        self.lineEditImageFilePath = QtWidgets.QLineEdit(self.groupBoxForm)
        self.lineEditImageFilePath.setStyleSheet("QLineEdit {\n"
"    font: 25 11pt \"Microsoft YaHei UI Light\";\n"
"}")
        self.lineEditImageFilePath.setObjectName("lineEditImageFilePath")
        self.gridLayout_2.addWidget(self.lineEditImageFilePath, 4, 2, 1, 1)
        self.plainTextEditDescription = QtWidgets.QPlainTextEdit(self.groupBoxForm)
        self.plainTextEditDescription.setStyleSheet("QPlainTextEdit {\n"
"    font: 25 11pt \"Microsoft YaHei UI Light\";\n"
"}")
        self.plainTextEditDescription.setObjectName("plainTextEditDescription")
        self.gridLayout_2.addWidget(self.plainTextEditDescription, 6, 2, 1, 2)
        self.comboBoxTypeSale = QtWidgets.QComboBox(self.groupBoxForm)
        self.comboBoxTypeSale.setStyleSheet("QComboBox {\n"
"    font: 25 11pt \"Microsoft YaHei UI Light\";\n"
"}")
        self.comboBoxTypeSale.setObjectName("comboBoxTypeSale")
        self.comboBoxTypeSale.addItem("")
        self.comboBoxTypeSale.addItem("")
        self.gridLayout_2.addWidget(self.comboBoxTypeSale, 5, 2, 1, 1)
        self.labelTypeSale = QtWidgets.QLabel(self.groupBoxForm)
        self.labelTypeSale.setStyleSheet("QLabel {\n"
"    font: 25 11pt \"Microsoft YaHei UI Light\";\n"
"}")
        self.labelTypeSale.setObjectName("labelTypeSale")
        self.gridLayout_2.addWidget(self.labelTypeSale, 5, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBoxForm, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.framePostForm, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.frameContainer, 1, 0, 1, 2)
        self.setCentralWidget(self.centralWidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelForm.setText(_translate("MainWindow", "Crear una nueva publicación"))
        self.pushButtonPost.setText(_translate("MainWindow", "Publicar"))
        self.labelPrice.setText(_translate("MainWindow", "Precio"))
        self.labelDescription.setText(_translate("MainWindow", "Descripcion"))
        self.labelTitle.setText(_translate("MainWindow", "Titulo"))
        self.labelImage.setText(_translate("MainWindow", "Imagen"))
        self.labelQuality.setText(_translate("MainWindow", "Calidad"))
        self.labelQuantity.setText(_translate("MainWindow", "Cantidad (en kg)"))
        self.comboBoxTypeSale.setItemText(0, _translate("MainWindow", "NACIONAL"))
        self.comboBoxTypeSale.setItemText(1, _translate("MainWindow", "INTERNACIONAL"))
        self.labelTypeSale.setText(_translate("MainWindow", "Tipo de venta"))
