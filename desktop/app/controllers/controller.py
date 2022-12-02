




from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtNetwork

from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

from app.models.model import Model
from app.views.view import View

import time
import requests
import platform
import os
import pandas as pd
import socket


class Controller:
    
    
    def __init__(self):
        
        self.Model = Model()
        self.set_environment_model_attr()

        self.View = View(self)
    
    def set_environment_model_attr(self):

        self.Model.EnvironmentModel.set_attr(
            session = str(socket.gethostname() + '@' + socket.gethostbyname(socket.gethostname())),

            system = {
                'os' : platform.system(),
                'system' : platform.system(),
                'version' : platform.version(),
                'processor' : platform.processor(),
                'node' : platform.node(),
                'machine' : platform.machine(),
                'architecture' : platform.architecture(),
                'platform' : platform.platform()
            }
        )

        if self.Model.EnvironmentModel.attr['system']['os'] == 'Windows':
            self.Model.EnvironmentModel.set_attr(
                path = {
                    'execution' : os.getcwd(),
                    'controllers' : str(os.getcwd() + '\\app\\controllers'),
                    'models' : str(os.getcwd() + '\\app\\models'),
                    'views' : str(os.getcwd() + '\\app\\views'),
                    'resources' : str(os.getcwd() + '\\app\\resources')
                }
            )
        
        elif self.Model.EnvironmentModel.attr['system']['os'] == 'Linux':
            self.Model.EnvironmentModel.set_attr(
                path = {
                    'execution' : os.getcwd(),
                    'controllers' : str(os.getcwd() + '/app/controllers'),
                    'models' : str(os.getcwd() + '/app/models'),
                    'views' : str(os.getcwd() + '/app/views'),
                    'resources' : str(os.getcwd() + '/app/resources')
                }
            )

        dns_EC2 = '54-242-75-104'
        url_EC2 = f'http://ec2-{dns_EC2}.compute-1.amazonaws.com'
        url_web_EC2 = f'{url_EC2}:8000'

        url_web_local_host = 'http://127.0.0.1:8000'
        

        # Cambiar en caso de ocupar AWS
        url_API = f'{url_web_local_host}/api'


        self.Model.EnvironmentModel.set_attr(
            url = {
                'EC2' : url_web_EC2,
                'localhost' : url_web_local_host,
                'API' : url_API

            }
        )




        return self.Model.EnvironmentModel.attr
    
    def main_window_view(self):
        return self.View.get_menu_view()
    
    def login_window_view(self):
        return self.View.get_login_view()
    
    def post_form_view(self):
        return self.View.get_post_form_view()
    
    def transport_form_view(self):
        return self.View.get_transport_form_view()
    
    def contract_form_view(self):
        return self.View.get_contract_form_view()
    
    def international_contract_form_view(self):
        return self.View.get_international_contract_form_view()
    


    def logout(self):
        if self.Model.EnvironmentModel.attr['system']['os'] == 'Windows':
            session_model_python_file_path = self.Model.EnvironmentModel.attr['path']['models'] + '\\session_model.py'

        elif self.Model.EnvironmentModel.attr['system']['os'] == 'Linux':
            session_model_python_file_path = self.Model.EnvironmentModel.attr['path']['models'] + '/session_model.py'

        os.remove(session_model_python_file_path)

        return self.View.MainWindowView.destroy(), self.login_window_view()

        
        

    def set_user_session(self, username, password):
        # Variables para hacer valido el formato JSON
        true, false, null = True, False, None

        try:

            username, password = username, password


            data = requests.get(
                self.Model.EnvironmentModel.attr['url']['API'] + '/custom-user/'
            )
            
            data = eval(data.text)

            __credential = []

            for value in data:
                value = dict(value)

                __username = value['username']
                __password = value['password']
                __credential.append((__username, __password))


                if username == __username:
                    if password == __password:
                        return self.main_window_view()

            return self.login_window_view()

            
        except Exception as exc:
            return self.View.get_message_view(
                status = QMessageBox.Warning,
                title = 'Operacion interrumpida',
                message = f'Esta columna no dispone de datos disponibles\nException : {exc}'
            )


    def login(self):
        true, false, null = True, False, None

        username, password = self.View.LoginView.lineEditUsername.text(), self.View.LoginView.lineEditUserPassword.text()

        try:
            data = requests.get(
                self.Model.EnvironmentModel.attr['url']['API'] + '/custom-user/'
            )
            
            data = eval(data.text)

            for value in data:
                value = dict(value)

                if username == value['username']:

                    print(True)

                    if password == value['password']:
                        print(True)
                        
                        return self.View.LoginView.destroy(), self.main_window_view()

                    else:
                        return self.View.get_message_view(
                            status = QMessageBox.Critical,
                            title = 'Operacion invalida',
                            message = f'La contraseña es incorrecta'   
                        )
        except Exception as exc:
            return self.View.get_message_view(
                status = QMessageBox.Warning,
                title = 'Operacion interrumpida',
                message = f'Exception : {exc}'
            )
        
    def remember_user_session(self):
        
        if self.Model.EnvironmentModel.attr['system']['os'] == 'Windows':
            session_model_python_file_path = self.Model.EnvironmentModel.attr['path']['models'] + '\\session_model.py'
            with open(session_model_python_file_path, '+w') as session_model_file:
                session_model_file.write(
                    '# -*- coding: utf-8 -*-\nclass SessionModel:\n\tdef __init__(self):\n\t\tself.username = "{}"\n\t\tself.password = "{}"'.format(
                        self.View.LoginView.lineEditUsername.text(),
                        self.View.LoginView.lineEditUserPassword.text()
                    )
                )
            session_model_file.close()


        elif self.Model.EnvironmentModel.attr['system']['os'] == 'Linux':
            session_model_python_file_path = self.Model.EnvironmentModel.attr['path']['models'] + '/session_model.py'

            with open(session_model_python_file_path, '+w') as session_model_file:
                session_model_file.write(
                    '# -*- coding: utf-8 -*-\nclass SessionModel:\n\tdef __init__(self):\n\t\tself.username = "{}"\n\t\tself.password = "{}"'.format(
                        self.View.LoginView.lineEditUsername.text(),
                        self.View.LoginView.lineEditUserPassword.text()
                    )
                )
            session_model_file.close()
        



        
        #return self.main_window_view()
    
    def main_window_title(self):
        self.View.MainWindowView.labelWindowTitle.setText(
            f'''{time.asctime()} - {self.Model.EnvironmentModel.attr['session']}'''
        )

    def login_window_title(self):
        self.View.LoginView.labelWindowTitle.setText(
            f'''Login - {self.Model.EnvironmentModel.attr['session']}'''
        )
    
    def post_form_window_title(self):
        self.View.PostFormView.labelWindowTitle.setText(
            'Formulario - Creación de publicación de subasta'
        )

    def transport_form_window_title(self):
        self.View.TransportFormView.labelWindowTitle.setText(
            'Formulario - Creación de publicación de transporte'
        )

    def contract_form_window_title(self):
        self.View.ContractFormView.labelWindowTitle.setText(
            'Formulario - Creación de publicación de contrato'
        )

    def international_contract_form_window_title(self):
        self.View.InternationalContractFormView.labelWindowTitle.setText(
            'Formulario - Creación de publicación de contrato internacional'
        )

    
    def swipe_menu_panel(self):
        if True:
            width = self.View.MainWindowView.frameMenuPanel.width()
            normal = 46

            if width == 46:
                extend = 250
            else:
                extend = normal

            self.animation_menu_panel = QtCore.QPropertyAnimation(self.View.MainWindowView.frameMenuPanel, b'minimumWidth')
            self.animation_menu_panel.setDuration(350)
            self.animation_menu_panel.setStartValue(width)
            self.animation_menu_panel.setEndValue(extend)
            self.animation_menu_panel.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation_menu_panel.start()

    def swipe_analysis_panel(self):
        if True:
            width = self.View.MainWindowView.frameAnalysisPanel.width()
            normal = 46

            if width == 46:
                extend = 300
            else:
                extend = normal

            self.animation_analysis_panel = QtCore.QPropertyAnimation(self.View.MainWindowView.frameAnalysisPanel, b'minimumWidth')
            self.animation_analysis_panel.setDuration(350)
            self.animation_analysis_panel.setStartValue(width)
            self.animation_analysis_panel.setEndValue(extend)
            self.animation_analysis_panel.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation_analysis_panel.start()
    
    def menu_window_restore(self):
        def dobleClickMaximizeRestore(event):
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(8, lambda: self.menu_window_status_restore())
                
        self.View.MainWindowView.frameWindowPanel.mouseDoubleClickEvent = dobleClickMaximizeRestore

    def post_form_window_restore(self):
        def dobleClickMaximizeRestore(event):
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(8, lambda: self.post_form_window_status_restore())
                
        self.View.PostFormView.frameWindowPanel.mouseDoubleClickEvent = dobleClickMaximizeRestore

    def transport_form_window_restore(self):
        def dobleClickMaximizeRestore(event):
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(8, lambda: self.transport_form_window_status_restore())
                
        self.View.TransportFormView.frameWindowPanel.mouseDoubleClickEvent = dobleClickMaximizeRestore

    def contract_form_window_restore(self):
        def dobleClickMaximizeRestore(event):
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(8, lambda: self.contract_form_window_status_restore())
                
        self.View.ContractFormView.frameWindowPanel.mouseDoubleClickEvent = dobleClickMaximizeRestore

    def international_contract_form_window_restore(self):
        def dobleClickMaximizeRestore(event):
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(8, lambda: self.international_contract_form_window_status_restore())
                
        self.View.InternationalContractFormView.frameWindowPanel.mouseDoubleClickEvent = dobleClickMaximizeRestore


    def insert_property_details(self):

        self.View.MainWindowView.lineEditExecutionPath.setText(
            self.Model.EnvironmentModel.attr['path']['execution']
        )

        self.View.MainWindowView.lineEditSystem.setText(
            self.Model.EnvironmentModel.attr['system']['system']
        )

        self.View.MainWindowView.lineEditSystemVersion.setText(
            self.Model.EnvironmentModel.attr['system']['version']
        )

        self.View.MainWindowView.lineEditProcessor.setText(
            self.Model.EnvironmentModel.attr['system']['processor']
        )

        self.View.MainWindowView.lineEditNode.setText(
            self.Model.EnvironmentModel.attr['system']['node']
        )

        self.View.MainWindowView.lineEditMachine.setText(
            self.Model.EnvironmentModel.attr['system']['machine']
        )

        self.View.MainWindowView.lineEditArchitecture.setText(
            str(self.Model.EnvironmentModel.attr['system']['architecture'][0])
        )

        self.View.MainWindowView.lineEditPlatform.setText(
            self.Model.EnvironmentModel.attr['system']['platform']
        )




    def menu_window_status_restore(self):
        def menu_window_maximize():
            return self.View.MainWindowView.showMaximized()

        def menu_window_minimize():
            return self.View.MainWindowView.showNormal()
        
        if self.View.MainWindowView.windowState() == QtCore.Qt.WindowState.WindowNoState:
            
            menu_window_maximize()
            
            self.View.MainWindowView.pushButtonRestore.setToolTip('Restore')
            
            _icon = QtGui.QIcon()
            _icon.addPixmap(
                QtGui.QPixmap('app/resources/img/icons/24x24/cil-window-restore.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            
            self.View.MainWindowView.pushButtonRestore.setIcon(_icon)
            self.View.MainWindowView.pushButtonRestore.setIconSize(QtCore.QSize(20, 20))
        
        else:
            
            menu_window_minimize()
            
            self.View.MainWindowView.pushButtonRestore.setToolTip('Maximize')
            
            _icon = QtGui.QIcon()
            _icon.addPixmap(
                QtGui.QPixmap(u'app/resources/img/icons/24x24/cil-window-maximize.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            
            self.View.MainWindowView.pushButtonRestore.setIcon(_icon)
            self.View.MainWindowView.pushButtonRestore.setIconSize(QtCore.QSize(20, 20))

    def post_form_window_status_restore(self):
        def post_form_window_maximize():
            return self.View.PostFormView.showMaximized()

        def post_form_window_minimize():
            return self.View.PostFormView.showNormal()
        
        if self.View.PostFormView.windowState() == QtCore.Qt.WindowState.WindowNoState:
            
            post_form_window_maximize()
            
            self.View.PostFormView.pushButtonRestore.setToolTip('Restore')
            
            _icon = QtGui.QIcon()
            _icon.addPixmap(
                QtGui.QPixmap('app/resources/img/icons/24x24/cil-window-restore.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            
            self.View.PostFormView.pushButtonRestore.setIcon(_icon)
            self.View.PostFormView.pushButtonRestore.setIconSize(QtCore.QSize(20, 20))
        
        else:
            
            post_form_window_minimize()
            
            self.View.PostFormView.pushButtonRestore.setToolTip('Maximize')
            
            _icon = QtGui.QIcon()
            _icon.addPixmap(
                QtGui.QPixmap(u'app/resources/img/icons/24x24/cil-window-maximize.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            
            self.View.PostFormView.pushButtonRestore.setIcon(_icon)
            self.View.PostFormView.pushButtonRestore.setIconSize(QtCore.QSize(20, 20))

    def transport_form_window_status_restore(self):
        def transport_form_window_maximize():
            return self.View.TransportFormView.showMaximized()

        def transport_form_window_minimize():
            return self.View.TransportFormView.showNormal()
        
        if self.View.TransportFormView.windowState() == QtCore.Qt.WindowState.WindowNoState:
            
            transport_form_window_maximize()
            
            self.View.TransportFormView.pushButtonRestore.setToolTip('Restore')
            
            _icon = QtGui.QIcon()
            _icon.addPixmap(
                QtGui.QPixmap('app/resources/img/icons/24x24/cil-window-restore.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            
            self.View.TransportFormView.pushButtonRestore.setIcon(_icon)
            self.View.TransportFormView.pushButtonRestore.setIconSize(QtCore.QSize(20, 20))
        
        else:
            
            transport_form_window_minimize()
            
            self.View.TransportFormView.pushButtonRestore.setToolTip('Maximize')
            
            _icon = QtGui.QIcon()
            _icon.addPixmap(
                QtGui.QPixmap(u'app/resources/img/icons/24x24/cil-window-maximize.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            
            self.View.TransportFormView.pushButtonRestore.setIcon(_icon)
            self.View.TransportFormView.pushButtonRestore.setIconSize(QtCore.QSize(20, 20))

    def contract_form_window_status_restore(self):
        def contract_form_window_maximize():
            return self.View.ContractFormView.showMaximized()

        def contract_form_window_minimize():
            return self.View.ContractFormView.showNormal()
        
        if self.View.ContractFormView.windowState() == QtCore.Qt.WindowState.WindowNoState:
            
            contract_form_window_maximize()
            
            self.View.ContractFormView.pushButtonRestore.setToolTip('Restore')
            
            _icon = QtGui.QIcon()
            _icon.addPixmap(
                QtGui.QPixmap('app/resources/img/icons/24x24/cil-window-restore.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            
            self.View.ContractFormView.pushButtonRestore.setIcon(_icon)
            self.View.ContractFormView.pushButtonRestore.setIconSize(QtCore.QSize(20, 20))
        
        else:
            
            contract_form_window_minimize()
            
            self.View.ContractFormView.pushButtonRestore.setToolTip('Maximize')
            
            _icon = QtGui.QIcon()
            _icon.addPixmap(
                QtGui.QPixmap(u'app/resources/img/icons/24x24/cil-window-maximize.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            
            self.View.ContractFormView.pushButtonRestore.setIcon(_icon)
            self.View.ContractFormView.pushButtonRestore.setIconSize(QtCore.QSize(20, 20))

    def international_contract_form_window_status_restore(self):
        def international_contract_form_window_maximize():
            return self.View.InternationalContractFormView.showMaximized()

        def international_contract_form_window_minimize():
            return self.View.InternationalContractFormView.showNormal()
        
        if self.View.InternationalContractFormView.windowState() == QtCore.Qt.WindowState.WindowNoState:
            
            international_contract_form_window_maximize()
            
            self.View.InternationalContractFormView.pushButtonRestore.setToolTip('Restore')
            
            _icon = QtGui.QIcon()
            _icon.addPixmap(
                QtGui.QPixmap('app/resources/img/icons/24x24/cil-window-restore.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            
            self.View.InternationalContractFormView.pushButtonRestore.setIcon(_icon)
            self.View.InternationalContractFormView.pushButtonRestore.setIconSize(QtCore.QSize(20, 20))
        
        else:
            
            international_contract_form_window_minimize()
            
            self.View.InternationalContractFormView.pushButtonRestore.setToolTip('Maximize')
            
            _icon = QtGui.QIcon()
            _icon.addPixmap(
                QtGui.QPixmap(u'app/resources/img/icons/24x24/cil-window-maximize.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            
            self.View.InternationalContractFormView.pushButtonRestore.setIcon(_icon)
            self.View.InternationalContractFormView.pushButtonRestore.setIconSize(QtCore.QSize(20, 20))



















































    def open_web(self):

        try:
            os.system(f'''start {self.Model.EnvironmentModel.attr['url']['localhost']}''')
        
        except Exception as exc:
            return self.View.get_message_view(
                status = QMessageBox.Warning,
                title = 'Operacion interrumpida',
                message = f'Esta columna no dispone de datos disponibles\nException : {exc}'
            )

    def insert_system_file_path(self, index):
        path = self.View.MainWindowView.treeViewFileSystem.model().filePath(index)
        self.View.MainWindowView.lineEditFileSelected.setText(path)


    def insert_file_system_view(self):

        FileSystemModel = QtWidgets.QFileSystemModel()
        FileSystemModel.setRootPath('')
        
        self.View.MainWindowView.treeViewFileSystem.setModel(FileSystemModel)
        self.View.MainWindowView.treeViewFileSystem.setAnimated(False)
        self.View.MainWindowView.treeViewFileSystem.setIndentation(20)
        self.View.MainWindowView.treeViewFileSystem.setSortingEnabled(True)

        header = self.View.MainWindowView.treeViewFileSystem.header()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
 
    def search(self, s):
        self.View.MainWindowView.tableWidgetAnalysis.setCurrentItem(None)
        if not s:
            return

        matching_items = self.View.MainWindowView.tableWidgetAnalysis.findItems(self.View.MainWindowView.lineEditSearcher.text(), QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive)

        if matching_items:
            for item in matching_items:
                self.View.MainWindowView.tableWidgetAnalysis.selectRow(item.row())
    
    def select_product_image(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.View.PostFormView, 
            "Open Image", 
            QtCore.QDir.currentPath(), 
            "Archivos de imagen (*.png *.jpg *.bmp)"
        )
        if filename:
            self.View.PostFormView.lineEditImageFilePath.setText(filename)

    def select_transport_image(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.View.PostFormView, 
            "Open Image", 
            QtCore.QDir.currentPath(), 
            "Archivos de imagen (*.png *.jpg *.bmp)"
        )
        if filename:
            self.View.TransportFormView.lineEditImageFilePath.setText(filename)



    def select_document(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.View.PostFormView, 
            "Open Image", 
            QtCore.QDir.currentPath(), 
            "Archivos de documentos (*.pdf)"
        )
        if filename:
            self.View.ContractFormView.lineEditDocumentFilePath.setText(filename)










    def upload_post(self):

        from time import strftime


        # '2022-11-01T04:17:56.138853-03:00'

        __id = 0
        __id+=1

        data = {
            "id" : __id,
            "timestamp" : strftime("%Y-%m-%d %H:%M:%S"),
            "title": self.View.PostFormView.lineEditTitle.text(),
            "description": self.View.PostFormView.plainTextEditDescription.toPlainText(),
            "price": self.View.PostFormView.spinBoxPrice.value(),
            "quantity": self.View.PostFormView.spinBoxQuantity.value(),
            "quality" : self.View.PostFormView.horizontalSliderQuality.value(),
            "type_sale" : self.View.PostFormView.comboBoxTypeSale.currentText(),
            "user" : 1
        }

        files = {"image": self.View.PostFormView.lineEditImageFilePath.text()}
        multi_part = self.construct_multipart(data, files)
        if multi_part:
            url = QtCore.QUrl(self.Model.EnvironmentModel.attr['url']['API'] + '/post/')
            request = QtNetwork.QNetworkRequest(url)
            print(request)
            reply = self.View.PostFormView.manager.post(request, multi_part)
            multi_part.setParent(reply)


    def upload_transport(self):

        from time import strftime


        # '2022-11-01T04:17:56.138853-03:00'

        __id = 0
        __id+=1

        data = {
            "id" : __id,
            "timestamp" : strftime("%Y-%m-%d %H:%M:%S"),
            "type": self.View.TransportFormView.comboBoxType.currentText(),
            "patent": self.View.TransportFormView.lineEditPatent.text(),
            "size": self.View.TransportFormView.lineEditSize.text(),
            "capacity": self.View.TransportFormView.spinBoxCapacity.value(),
            "refrigeration" : self.View.TransportFormView.comboBoxRefrigeration.currentText(),
            "user" : 1
        }

        files = {"image": self.View.TransportFormView.lineEditImageFilePath.text()}
        multi_part = self.construct_multipart(data, files)
        if multi_part:
            url = QtCore.QUrl(self.Model.EnvironmentModel.attr['url']['API'] + '/transport/')
            request = QtNetwork.QNetworkRequest(url)
            print(request)
            reply = self.View.TransportFormView.manager.post(request, multi_part)
            multi_part.setParent(reply)

    def upload_contract(self):


        __id = 0
        __id+=1

        data = {
            "id" : __id
        }

        files = {"document": self.View.ContractFormView.lineEditDocumentFilePath.text()}
        multi_part = self.construct_multipart(data, files)
        if multi_part:
            url = QtCore.QUrl(self.Model.EnvironmentModel.attr['url']['API'] + '/contract/')
            request = QtNetwork.QNetworkRequest(url)
            print(request)
            reply = self.View.ContractFormView.manager.post(request, multi_part)
            multi_part.setParent(reply)


    def upload_international_contract(self):

        from time import strftime


        # '2022-11-01T04:17:56.138853-03:00'

        __id = 0
        __id+=1

        data = {
            "id" : __id,
            "contract_term" : strftime("%Y-%m-%dT%H:%M:%S-03:00"),
            "contract_closing_date" : self.View.InternationalContractFormView.dateEdit.text() + 'T00:00:00-03:00',
            "contract_validity" : self.View.InternationalContractFormView.comboBoxValidity.currentText()
        }

        multi_part = self.construct_multipart_without_file(data)
        if multi_part:
            url = QtCore.QUrl(self.Model.EnvironmentModel.attr['url']['API'] + '/international-contract/')
            request = QtNetwork.QNetworkRequest(url)
            print(request)
            reply = self.View.InternationalContractFormView.manager.post(request, multi_part)
            multi_part.setParent(reply)







    def construct_multipart_without_file(self, data):
        multi_part = QtNetwork.QHttpMultiPart(QtNetwork.QHttpMultiPart.FormDataType)
        for key, value in data.items():
            post_part = QtNetwork.QHttpPart()
            post_part.setHeader(QtNetwork.QNetworkRequest.ContentDispositionHeader, 
                "form-data; name=\"{}\"".format(key))
            post_part.setBody(str(value).encode())
            multi_part.append(post_part)
        return multi_part


    def construct_multipart(self, data, files):
        multi_part = QtNetwork.QHttpMultiPart(QtNetwork.QHttpMultiPart.FormDataType)
        for key, value in data.items():
            post_part = QtNetwork.QHttpPart()
            post_part.setHeader(QtNetwork.QNetworkRequest.ContentDispositionHeader, 
                "form-data; name=\"{}\"".format(key))
            post_part.setBody(str(value).encode())
            multi_part.append(post_part)
        for field, filepath in  files.items():
            file = QtCore.QFile(filepath)
            if not file.open(QtCore.QIODevice.ReadOnly):
                break
            post_part = QtNetwork.QHttpPart()
            post_part.setHeader(QtNetwork.QNetworkRequest.ContentDispositionHeader,
                "form-data; name=\"{}\"; filename=\"{}\"".format(field, file.fileName()))
            post_part.setBodyDevice(file)
            file.setParent(multi_part)
            multi_part.append(post_part)
        return multi_part




    def delete_data(self):
        try:
            rows = {index.row() for index in self.View.MainWindowView.tableWidgetAnalysis.selectionModel().selectedIndexes()}
            output = []
            for row in rows:
                row_data = []
                for column in range(self.View.MainWindowView.tableWidgetAnalysis.model().columnCount()):
                    index = self.View.MainWindowView.tableWidgetAnalysis.model().index(row, column)
                    row_data.append(index.data())
                output.append(row_data)

            if len(output) >= 2:
                for id in output:
                    url = f'{selected_item}{id[0]}'
                    requests.delete(
                        url
                    )
            else:
                for id in output:
                    url = f'{selected_item}{id[0]}'
                    
                    requests.delete(
                        url
                    )


            return self.View.get_message_view(
                status = QMessageBox.Information,
                title = 'Operacion finalizada',
                message = f'Se ha eliminado la fila con los datos, vuelva a solicitar para ver los cambios realizados:\n{output[0]}\n{output[1]}\n{output[2]}\n{output[3]}\n. . . '
            )



        
        except Exception as exc:
            return self.View.get_message_view(
                status = QMessageBox.Warning,
                title = 'Operacion interrumpida',
                message = f'Exception : {exc}'
            )


    def request_data(self):
        try:
            true, false, null = True, False, None

            data = requests.get(
                self.Model.EnvironmentModel.attr['url']['API']
            )
            __data = eval(data.text)

            ModelItemListViewFileHistory = QtGui.QStandardItemModel()

            self.View.MainWindowView.listViewTables.setModel(ModelItemListViewFileHistory)
            self.View.MainWindowView.listViewTables.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

            for data in list(__data.values()):
                item = QtGui.QStandardItem(data)

                ModelItemListViewFileHistory.appendRow(item)

            def select(index):
                true, false, null = True, False, None

                global selected_item
                selected_item = index.data()

                try:
                    data_request = requests.get(selected_item)
                    data = eval(data_request.text)

                    row_count = len(data)

                    for value in data:
                        value = dict(value)
                        column_count = len(value.keys())

                    data_table(
                        row_count,
                        column_count,
                        data
                    )

                except Exception as exc:
                    return self.View.get_message_view(
                        status = QMessageBox.Warning,
                        title = 'Operacion interrumpida',
                        message = f'Esta columna no dispone de datos disponibles\nException : {exc}'
                    )

            def data_table(row_count : int, column_count : int, data : list):

                row_count = (row_count)
                column_count = (column_count)
                self.View.MainWindowView.tableWidgetAnalysis.setColumnCount(column_count)
                self.View.MainWindowView.tableWidgetAnalysis.setRowCount(row_count)
                self.View.MainWindowView.tableWidgetAnalysis.setHorizontalHeaderLabels((list(data[0].keys())))

                __header = self.View.MainWindowView.tableWidgetAnalysis.horizontalHeader()

                global _header
                _header = list(data[0].keys())

                try:

                    for row in range(row_count):
                        #item = (str(list_value[i]))
                        for column in range(column_count):
                            item = (list(data[row].values())[column])
                            __header.setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
                            set_item(row, column, item)

                except Exception as exc:
                    print(exc)
                    return self.View.get_message_view(
                        status = QMessageBox.Warning,
                        title = 'Operacion interrumpida',
                        message = f'Exception : {exc}'
                    )
                
            def set_item(row, column, item):
                self.View.MainWindowView.tableWidgetAnalysis.setItem(row, column, QTableWidgetItem(str(item)))
                return self.View.get_message_view(
                    status = QMessageBox.Information,
                    title = 'Operacion finalizada',
                    message = f'La solicitud ha sido cargada correctamente'
                )

            self.View.MainWindowView.listViewTables.doubleClicked.connect(select)

        
        except Exception as exc:
            return self.View.get_message_view(
                status = QMessageBox.Warning,
                title = 'Operacion interrumpida',
                message = f'Exception : {exc}'
            )


    def export_data(self):

        try:
            file_name = QtWidgets.QFileDialog.getSaveFileName(self.View.MainWindowView, 'Guardar el archivo', './', 'Libro de Excel (*.xlsx)')[0]

            exported_data = []
            processed_data = []
            counted_data = 0


            for number_rows in range(self.View.MainWindowView.tableWidgetAnalysis.model().rowCount()):
                
                cells = [

                    self.View.MainWindowView.tableWidgetAnalysis.model().data(
                        self.View.MainWindowView.tableWidgetAnalysis.model().index(number_rows, number_column), QtCore.Qt.DisplayRole)
                    for number_column in range(self.View.MainWindowView.tableWidgetAnalysis.model().columnCount())
                ]
                
                exported_data.append(cells)

            for data in exported_data:

                data = tuple(data)
                counted_data+=1
                processed_data.append(data)

                df = pd.DataFrame(processed_data)
                df.columns = _header


            excel_writer = pd.ExcelWriter(
                f'{file_name}',
                engine = 'xlsxwriter',
                engine_kwargs = {'options': {'strings_to_urls': False}}
            )
            df.to_excel(excel_writer)

            excel_writer_book = excel_writer.book
            excel_writer_sheets = excel_writer.sheets
            excel_writer_sheets = excel_writer_sheets['Sheet1']



            id_format = excel_writer_book.add_format(
                {
                    'bg_color': '#6178B2',
                    'font_color' : '#FFFFFF',
                    'font_size' : '12',
                    'font' : 'Microsoft JhengHei UI',
                    'bold':  True,
                    'align': 'left',
                    'border': 1,
                    'align': 'left',
                    'valign': 'vleft',
                    'text_wrap': True
                }
            )

            header_format = excel_writer_book.add_format(
                {
                    'bg_color': '#D37242',
                    'font_color' : '#FFFFFF',
                    'font_size' : '12',
                    'font' : 'Microsoft JhengHei UI',
                    'bold':  True,
                    'align': 'left',
                    'border': 1,
                    'align': 'left',
                    'valign': 'vleft',
                    'text_wrap': True
                }
            )

            format = excel_writer_book.add_format(
                {
                    'bg_color': '#FFFFFF',
                    'font_color' : '#6178B2',
                    'font_size' : '10',
                    'font' : 'Microsoft JhengHei UI',
                    'align': 'left',
                    'border': 1,
                    'align': 'left',
                    'valign': 'vleft',
                    'text_wrap': True
                }
            )

            excel_writer_sheets.set_column("B:B", 16, cell_format = format)
            excel_writer_sheets.set_column("C:D", 30, cell_format = format)
            excel_writer_sheets.set_column("E:F", 28, cell_format = format)
            excel_writer_sheets.set_column("G:I", 35, cell_format = format)
            excel_writer_sheets.set_column("J:K", 24, cell_format = format)
            excel_writer_sheets.set_column("L:L", 45, cell_format = format)

            for column_number, value in enumerate(df.columns.values):
                excel_writer_sheets.write(0, column_number + 1, value, header_format)

            excel_writer_sheets.conditional_format(
                f'A1:A{df.shape[0]+1}', {
                    'type': 'no_blanks','format': id_format
                }
            )
            excel_writer.save()


            return self.View.get_message_view(
                status = QMessageBox.Information,
                title = 'Operation finalizada',
                message = f'El DataFrame ha sido exportaddo en:\n{file_name}'
            )


        except Exception as exc:
            return self.View.get_message_view(
                status = QMessageBox.Warning,
                title = 'Operacion interrumpida',
                message = f'Exception : {exc}'
            )