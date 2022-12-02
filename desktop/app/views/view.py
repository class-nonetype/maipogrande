
from app.views.main_window_view import (
    MainWindowView, QtCore
)
from app.views.message_view import (
    MessageView
)
from app.views.product_form import (
    PostFormView
)

from app.views.contract_form import (
    ContractFormView
)

from app.views.international_contract_form import (
    InternationalContractFormView
)

from app.views.transport_form import (
    TransportFormView
)


from app.views.login_view import (
    LoginView
)

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class View:
    
    def __init__(self, Controller):
        self.Controller = Controller

        self.LoginView = LoginView()
        self.MainWindowView = MainWindowView(self.Controller)
        self.PostFormView = PostFormView(self.Controller)
        self.TransportFormView = TransportFormView(self.Controller)
        self.ContractFormView = ContractFormView(self.Controller)
        self.InternationalContractFormView = InternationalContractFormView(self.Controller)

        self.MessageView = MessageView()
    
    def get_login_view(self):
        self.LoginView.setupUi()

        self.Controller.login_window_title()

        self.LoginView.setWindowTitle('Maipo Grande - Login')
        self.LoginView.pushButtonClose.clicked.connect(qApp.quit)
        self.LoginView.pushButtonMinimize.clicked.connect(self.LoginView.showMinimized)

        self.LoginView.lineEditUsername.setPlaceholderText('Ingresa el nombre de usuario')
        self.LoginView.lineEditUserPassword.setPlaceholderText('Ingresa la contraseña')
        self.LoginView.lineEditUserPassword.setEchoMode(QLineEdit.Password)

        self.LoginView.radioButtonRememberUser.toggled.connect(self.Controller.remember_user_session)
            
        self.LoginView.pushButtonLogin.clicked.connect(
            self.Controller.login
        )

        return self.LoginView.show()

    def get_menu_view(self):
        self.MainWindowView.setupUi()
        self.MainWindowView.setWindowTitle('Maipo Grande - Menu')
            
        # Components

        self.timer = QtCore.QTimer(self.MainWindowView)
        self.timer.timeout.connect(self.Controller.main_window_title)
        self.timer.start(1000)

        self.Controller.menu_window_restore()

            
            
        self.MainWindowView.pushButtonClose.clicked.connect(qApp.quit)
        self.MainWindowView.pushButtonMinimize.clicked.connect(self.MainWindowView.showMinimized)
        self.MainWindowView.pushButtonRestore.clicked.connect(lambda : self.Controller.menu_window_status_restore())

        self.MainWindowView.stackedWidgetModule.setCurrentWidget(self.MainWindowView.homeModule)
            
        #self.Controller.swipe_menu_panel()
        self.MainWindowView.pushButtonSwipeMenuPanel.clicked.connect(self.Controller.swipe_menu_panel)
        self.MainWindowView.pushButtonOpenWebsite.clicked.connect(self.Controller.open_web)
            
        self.MainWindowView.pushButtonHomeModule.clicked.connect(lambda : self.MainWindowView.stackedWidgetModule.setCurrentWidget(self.MainWindowView.homeModule))
        self.MainWindowView.pushButtonAnalysisModule.clicked.connect(lambda : self.MainWindowView.stackedWidgetModule.setCurrentWidget(self.MainWindowView.analysisModule))
        self.MainWindowView.pushButtonExecutionModule.clicked.connect(lambda : self.MainWindowView.stackedWidgetModule.setCurrentWidget(self.MainWindowView.executionModule))
        self.MainWindowView.pushButtonPropertiesModule.clicked.connect(lambda : self.MainWindowView.stackedWidgetModule.setCurrentWidget(self.MainWindowView.propertiesModule))
        self.MainWindowView.pushButtonLeaveSession.clicked.connect(self.Controller.logout)
            
        self.MainWindowView.pushButtonSwipePanelAnalysis.clicked.connect(self.Controller.swipe_analysis_panel)
            
            
        self.MainWindowView.lineEditSearcher.setPlaceholderText('Escribe algun dato a buscar')
        self.MainWindowView.lineEditSearcher.textChanged.connect(self.Controller.search)

        self.MainWindowView.pushButtonRequestData.clicked.connect(self.Controller.request_data)
        self.MainWindowView.pushButtonDeleteData.clicked.connect(self.Controller.delete_data)

        self.MainWindowView.pushButtonCreateProduct.clicked.connect(self.Controller.post_form_view)
        self.MainWindowView.pushButtonCreateTransport.clicked.connect(self.Controller.transport_form_view)
        self.MainWindowView.pushButtonCreateContract.clicked.connect(self.Controller.contract_form_view)
        self.MainWindowView.pushButtonCreateInternationalContract.clicked.connect(self.Controller.international_contract_form_view)


        self.MainWindowView.pushButtonExportData.clicked.connect(self.Controller.export_data)





        self.MainWindowView.lineEditExecutionPath.setEnabled(False)

        self.MainWindowView.lineEditSystem.setEnabled(False)
        self.MainWindowView.lineEditSystemVersion.setEnabled(False)
        self.MainWindowView.lineEditProcessor.setEnabled(False)
        self.MainWindowView.lineEditNode.setEnabled(False)
        self.MainWindowView.lineEditMachine.setEnabled(False)
        self.MainWindowView.lineEditArchitecture.setEnabled(False)
        self.MainWindowView.lineEditPlatform.setEnabled(False)
        self.Controller.insert_property_details()

            
        self.MainWindowView.lineEditFileSelected.setEnabled(False)
            
        #self.Controller.insert_property_details()
            
        self.Controller.insert_file_system_view()

        #self.MainWindowView.showMaximized()
        return self.MainWindowView.show()

    def get_post_form_view(self):
        self.PostFormView.setupUi()

        self.PostFormView.setWindowTitle('Maipo Grande - Formulario de subasta')
        
        self.Controller.post_form_window_title()

        self.PostFormView.pushButtonClose.clicked.connect(self.PostFormView.close)
        self.PostFormView.pushButtonMinimize.clicked.connect(self.PostFormView.showMinimized)
        self.PostFormView.pushButtonRestore.clicked.connect(lambda : self.Controller.post_form_window_status_restore())

        self.PostFormView.lineEditImageFilePath.setEnabled(False)


        self.PostFormView.pushButtonPost.clicked.connect(self.Controller.upload_post)
        self.PostFormView.pushButtonSelectImage.clicked.connect(self.Controller.select_product_image)
        
        return self.PostFormView.show()



    def get_transport_form_view(self):
        self.TransportFormView.setupUi()

        self.TransportFormView.setWindowTitle('Maipo Grande - Formulario de transporte')
        
        self.Controller.transport_form_window_title()

        self.TransportFormView.pushButtonClose.clicked.connect(self.TransportFormView.close)
        self.TransportFormView.pushButtonMinimize.clicked.connect(self.TransportFormView.showMinimized)
        self.TransportFormView.pushButtonRestore.clicked.connect(lambda : self.Controller.transport_form_window_restore())

        self.TransportFormView.lineEditImageFilePath.setEnabled(False)


        self.TransportFormView.pushButtonPost.clicked.connect(self.Controller.upload_transport)
        self.TransportFormView.pushButtonSelectImage.clicked.connect(self.Controller.select_transport_image)
        
        return self.TransportFormView.show()



    def get_contract_form_view(self):
        self.ContractFormView.setupUi()

        self.ContractFormView.setWindowTitle('Maipo Grande - Formulario de contrato')
        
        self.Controller.contract_form_window_title()

        self.ContractFormView.pushButtonClose.clicked.connect(self.ContractFormView.close)
        self.ContractFormView.pushButtonMinimize.clicked.connect(self.ContractFormView.showMinimized)
        self.ContractFormView.pushButtonRestore.clicked.connect(lambda : self.Controller.contract_form_window_restore())

        self.ContractFormView.lineEditDocumentFilePath.setEnabled(False)


        self.ContractFormView.pushButtonPost.clicked.connect(self.Controller.upload_contract)
        self.ContractFormView.pushButtonSelectImage.clicked.connect(self.Controller.select_document)
        
        return self.ContractFormView.show()


    def get_international_contract_form_view(self):
        self.InternationalContractFormView.setupUi()

        self.InternationalContractFormView.setWindowTitle('Maipo Grande - Formulario de contrato internacional')
        
        self.Controller.international_contract_form_window_title()

        self.InternationalContractFormView.pushButtonClose.clicked.connect(self.InternationalContractFormView.close)
        self.InternationalContractFormView.pushButtonMinimize.clicked.connect(self.InternationalContractFormView.showMinimized)
        self.InternationalContractFormView.pushButtonRestore.clicked.connect(lambda : self.Controller.international_contract_form_window_restore())


        self.InternationalContractFormView.pushButtonPost.clicked.connect(self.Controller.upload_international_contract)
        
        return self.InternationalContractFormView.show()



    def get_message_view(self, title: str, message : str, status : str):
        try:
        
            
            '''
            STATUS >
                        Question
                        Information
                        Warning
                        Critical
            '''
            self.MessageView.set_title(title)
            self.MessageView.set_status(status)
            self.MessageView.set_message(message)

            self.MessageView.setupUi()
            
            return self.MessageView.show()

        except Exception as exc:
            # Logger
            pass