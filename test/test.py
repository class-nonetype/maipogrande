from ast import Str
import platform
import os
import logging
import json



# Clase de propiedades
#   Manejo de version del sistema, requerimientos, estructuracion de directorios y urls
class Properties:

    def __init__(self):

        # URLS asociadas
        self.URL = {
            'INDEX' : 'http://127.0.0.1:8000/',
            'LOGIN' : 'http://127.0.0.1:8000/login',
            'REGISTER' : 'http://127.0.0.1:8000/register',
            'FEED' : 'http://127.0.0.1:8000/feed',
            'PROFILE' : 'http://127.0.0.1:8000/profile',
            'BANK' : 'http://127.0.0.1:8000/bank'
        }

        # Version del sistema
        self.platform_system = platform.system()

        self.setup()
    
    # Metodo de construccion de entorno
    #   Retorna -> self.path : type <dict>
    #                   Diccionario encargado de contener las rutas
    def setup(self) -> dict:

        self.test_execution_path = os.getcwd() 

        # Convencion de rutas segun el sistema operativo
        if self.platform_system == 'Windows':

            chrome_driver_file_path =\
                self.test_execution_path + '\\test\\driver\\chromedriver.exe'

            pdf_output_directory_path =\
                self.test_execution_path + '\\test\\output'

            log_output_directory_path =\
                self.test_execution_path + '\\test\\log'

            self.path = {
                'DRIVER' : chrome_driver_file_path,
                'OUTPUT' : pdf_output_directory_path,
                'LOG' : log_output_directory_path
            }

        elif self.platform_system == 'Linux':
            chrome_driver_file_path =\
                self.test_execution_path + '/test/driver/chromedriver'

            pdf_output_directory_path =\
                self.test_execution_path + '/test/output'

            log_output_directory_path =\
                self.test_execution_path + '/test/output'

            self.path = {
                'DRIVER' : chrome_driver_file_path,
                'OUTPUT' : pdf_output_directory_path,
                'LOG' : log_output_directory_path
            }

        print(self.path.values())

        # Creacion de directorios LOG y OUTPUT
        if not os.path.exists(self.path['LOG']):
            os.mkdir(self.path['LOG'])

        if not os.path.exists(self.path['OUTPUT']):
            os.mkdir(self.path['OUTPUT'])
        

        # Configuracion de logger
        if self.platform_system == 'Linux':
            logging.basicConfig(
                filename = self.path['LOG'] + '/DEBUG.log',
                level = logging.DEBUG,
                format = '%(asctime)s %(message)s',
                datefmt = '%m/%d/%Y %I:%M:%S'
            )

        elif self.platform_system == 'Windows':
            logging.basicConfig(
                filename = self.path['LOG'] + '\\DEBUG.log',
                level = logging.DEBUG,
                format = '%(asctime)s %(message)s',
                datefmt = '%m/%d/%Y %I:%M:%S'
            )

        return self.path

# Importaciones
try:
    from selenium import webdriver
    from selenium.webdriver import ActionChains
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import Select

    from selenium.webdriver import ActionChains


except Exception as exc:
    # Inicializacion
    Properties().setup()

    from selenium import webdriver
    from selenium.webdriver import ActionChains
    from selenium.webdriver.common.by import By
    
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.action_chains import ActionChains

    from selenium.webdriver.support.ui import Select
    pass



# Logger
LOGGER = logging.getLogger('LOG')

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

LOGGER.addHandler(CONSOLE_HANDLER)



# Clase de prueba
#   Manejo de las pruebas automatizadas y construccion del manejo de documentos asociados a las pruebas ejecutadas
class Test:

    def __init__(self):

        # Clase de propiedades
        self.Properties = Properties()


        # El servicio asociado
        self.service = Service(self.Properties.path['DRIVER'])

        # Opciones de chrome
        self.chrome_options = webdriver.ChromeOptions()

        # Configuraciones de chrome
        self.settings = {
            "recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": "", 'default_directory': self.Properties.path['OUTPUT']}],
            "selectedDestinationId": "Save as PDF", "version": 2,
            "isLandscapeEnabled": True
            #"isCssBackgroundEnabled": True
        }

        self.prefs = {
            'printing.print_preview_sticky_settings.appState': json.dumps(self.settings),
            'savefile.default_directory': self.Properties.path['OUTPUT']
        }
        self.chrome_options.add_experimental_option('prefs', self.prefs)
        self.chrome_options.add_argument('--kiosk-printing')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--disable-software-rasterizer')

    def execute_chrome_driver(self):
        print(self.Properties.path['DRIVER'])

        # Instancia del Chrome driver

        try:
            self.chrome_driver = webdriver.Chrome(
                service = self.service,
                chrome_options = self.chrome_options
            )
        
        except Exception as exc:
            self.chrome_driver = webdriver.Chrome(
                self.Properties.path['DRIVER']
            )
            print(exc)
        self.chrome_driver.implicitly_wait(30)
        self.chrome_driver.maximize_window()


        # URL INDEX
        self.chrome_driver.get(self.Properties.URL['INDEX'])


    # Metodo de construccion de documentos PDF
    #   Retorna -> self.chrome_driver.execute_script()
    #                   Funcion encargada de ejecutar el script de generar documentos PDF
    def generate_pdf(self, module, actor, title : str):
        if len(actor) != 0:
            return self.chrome_driver.execute_script(
                f"document.title = 'FERIA VIRTUAL MAIPO GRANDE - {module} - {actor} - {title}'; window.print();"
            )

        else:
            return self.chrome_driver.execute_script(
                f"document.title = 'FERIA VIRTUAL MAIPO GRANDE - {module} - {title}'; window.print();"
            )            


    # Metodo de limpieza de consola/terminal
    def clear(self):
        print(self.label)
    
    def set_label(self, label):
        self.label = label
    
    def set_test_properties(self, *args):
        for argv in args:
            LOGGER.info(
                argv
            )
    # Metodo de inicializacion de pruebas
    def run(self):
        self.execute_chrome_driver()

        self.create_classes()

        STATUS = True

        if STATUS:
            self.set_test_properties(
                '[ * ]\t/register/\tCREACION DE CUENTA DE USUARIO'
            )
            test_register_user = self.register_user_test()

            if test_register_user:
                self.chrome_driver.refresh()
                self.set_test_properties('[ + ]\t/register/\tCREACION DE CUENTA DE USUARIO')

            self.set_test_properties('[ * ]\t/login/\tINICIO DE SESION')
            
            test_login_user = self.login_test()

            if test_login_user:
                self.chrome_driver.refresh()
                self.set_test_properties('[ + ]\t/login/\tINICIO DE SESION')

            self.set_test_properties('[ * ]\tProfile\tPERFIL DE USUARIO')
            
            test_profile_user = self.user_profile_test()
            
            if test_profile_user:
                self.chrome_driver.refresh()
                self.set_test_properties(f'[ + ][\t/profile/\tPERFIL DE USUARIO')
            
            test_post_product = self.create_product_post()

            self.set_test_properties('[ + ]\t/post/\tCREACION DE PUBLICACION DE PRODUCTO')

            if test_post_product:
                self.chrome_driver.refresh()
                self.set_test_properties('[ + ]\t/post/\tPUBLICACION CREADA')

            self.set_test_properties('[ + ]\t/bank/\tCUENTA BANCARIA DE USUARIO')
            
            test_user_bank_account = self.user_bank_test()
            
            if test_user_bank_account:
                self.chrome_driver.refresh()
                self.set_test_properties('[ + ]\t/bank/\tCUENTA BANCARIA DE USUARIO')
                self.clear()
        
        else:
            self.chrome_driver.close()
    
    def create_classes(self):

        class User:

            def __init__(self, id, username, password, email, first_name, last_name, identity_document_number):
                self.id = id
                self.username = username
                self.password = password
                self.email = email
                self.first_name = first_name
                self.last_name = last_name
                self.identity_document_number = identity_document_number

        class PostProduct:

            def __init__(self, title , price , quantity, img_file_name):

                self.title = title
                self.price = price
                self.quantity = quantity
                self.description = '''
                    Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium,
                    totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.
                    Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit,
                    sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.
                    Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit,
                    sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem
                    Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur?
                    Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur,
                    vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?
                '''

                self.img_directory_path = f'''{os.getcwd()}\\test\\img'''

                if Properties().platform_system == 'Windows':
                    self.image = str(f'''{self.img_directory_path}\\{img_file_name}''')#.encode('utf-8')


        self.ProducerUser = User(
            id = 0,
            username = 'productor',
            password = '123qwe@@@',
            email = 'go.vivanco@duocuc.cl',
            first_name = 'BRUNO ANTONIO',
            last_name = 'SANDOVAL ROJAS',
            identity_document_number = '190888000'
        )

        self.TransportistUser = User(
            id = 0,
            username = 'transportista',
            password = '123qwe@@@',
            email = 'go.vivanco@duocuc.cl',
            first_name = 'CARLOS CESAR',
            last_name = 'MEDINA SOTO',
            identity_document_number = '180999222'
        )

        self.ExternalClientUser = User(
            id = 0,
            username = 'cliente.externo',
            password = '123qwe@@@',
            email = 'go.vivanco@duocuc.cl',
            first_name = 'ANTONIO MAXIMILIANO',
            last_name = 'ROJAS CEPEDA',
            identity_document_number = '180222999'
        )

        self.InternalClientUser = User(
            id = 0,
            username = 'cliente.interno',
            password = '123qwe@@@',
            email = 'go.vivanco@duocuc.cl',
            first_name = 'ORLANDO LUCIANO',
            last_name = 'SEPULVEDA CASTRO',
            identity_document_number = '192888444'
        )


        self.Product1ProducerUser = PostProduct(
            title = 'Valle del Olimpo - Chirimoya',
            price = '5990',
            quantity = '1000',
            img_file_name = str('chirimoya.jpg')

        )

        self.Product2ProducerUser = PostProduct(
            title = 'Valle del Olimpo - Piña',
            price = '8990',
            quantity = '500',
            img_file_name = str('fruta-trucos-curiosidades_486711841_151275924_1706x960.jpg')

        )

        self.Product3ProducerUser = PostProduct(
            title = 'Valle del Olimpo - Uvas verdes',
            price = '3990',
            quantity = '1000',
            img_file_name = str('uvas.jpeg')
        )

        self.Product4ProducerUser = PostProduct(
            title = 'Valle del Olimpo - Frambuesas',
            price = '5990',
            quantity = '1000',
            img_file_name = str('03d44ae8-frambuesas-1.jpg')

        )

        self.Product5ProducerUser = PostProduct(
            title = 'Valle del Olimpo - Cerezas',
            price = '3990',
            quantity = '500',
            img_file_name = str('Cerezas-shutterstock_323577575-scaled.jpg')

        )

        self.Product6ProducerUser = PostProduct(
            title = 'Valle del Olimpo - Naranjas',
            price = '6990',
            quantity = '300',
            img_file_name = str('naranja.jfif')

        )



        return (
            self.ProducerUser,
            self.Product1ProducerUser, self.Product2ProducerUser, self.Product3ProducerUser,
            self.Product4ProducerUser, self.Product5ProducerUser, self.Product6ProducerUser
        )


    def register_user_test(self) -> bool:

        STATUS = False

        def create_producer_user() -> bool:
            STATUS_ACCOUNT = False

            BTN_REGISTER = self.chrome_driver.find_element(
                By.ID,
                'btn-register'
            )
            BTN_REGISTER.click()

            INPUT_USERNAME = self.chrome_driver.find_element(
                By.ID,
                'input-username'
            )
            INPUT_USERNAME.send_keys(
                self.ProducerUser.username
            )


            SELECT_TYPE_USER = Select(self.chrome_driver.find_element(By.ID, 'select-type-user'))
            SELECT_TYPE_USER.select_by_visible_text('PRODUCTOR')

            SELECT_COUNTRY = Select(self.chrome_driver.find_element(By.ID, 'select-country'))
            SELECT_COUNTRY.select_by_visible_text('United States')


            INPUT_EMAIL = self.chrome_driver.find_element(
                By.ID,
                'input-email'
            )
            INPUT_EMAIL.send_keys(
                self.ProducerUser.email
            )


            INPUT_IDENTITY_DOCUMENT_NUMBER = self.chrome_driver.find_element(
                By.ID,
                'input-identity-document-number'
            )
            INPUT_IDENTITY_DOCUMENT_NUMBER.send_keys(
                self.ProducerUser.identity_document_number
            )

            INPUT_PASSWORD1 = self.chrome_driver.find_element(
                By.ID,
                'input-password1'
            )
            INPUT_PASSWORD1.send_keys(
                self.ProducerUser.password
            )

            INPUT_PASSWORD2 = self.chrome_driver.find_element(
                By.ID,
                'input-password2'
            )
            INPUT_PASSWORD2.send_keys(
                self.ProducerUser.password
            )

            INPUT_FIRST_NAME = self.chrome_driver.find_element(
                By.ID,
                'input-first-name'
            )
            INPUT_FIRST_NAME.send_keys(
                self.ProducerUser.first_name
            )

            INPUT_LAST_NAME = self.chrome_driver.find_element(
                By.ID,
                'input-last-name'
            )
            INPUT_LAST_NAME.send_keys(
                self.ProducerUser.last_name
            )

            self.generate_pdf(
                'TEST 001 - /register/',
                'USUARIO PRODUCTOR',
                'CREACION DE CUENTA DE TIPO PRODUCTOR'
            )
            INPUT_LAST_NAME.submit()

            try:
                ERROR_LIST = self.chrome_driver.find_element(
                    By.CLASS_NAME,
                    'errorlist'
                )

                if ERROR_LIST:
                    
                    self.generate_pdf(
                        'TEST 001 - /register/',
                        'USUARIO PRODUCTOR',
                        'CREACION INVALIDA DE CUENTA DE TIPO PRODUCTOR'
                    )

                    while ERROR_LIST:
                        self.ProducerUser.id = self.ProducerUser.id+1
                        self.ProducerUser.username = self.ProducerUser.username + f'_{self.ProducerUser.id}'

                        INPUT_USERNAME = self.chrome_driver.find_element(
                            By.ID,
                            'input-username'
                        )
                        INPUT_USERNAME.clear()

                        INPUT_USERNAME.send_keys(self.ProducerUser.username)

                        SELECT_TYPE_USER = Select(self.chrome_driver.find_element(By.ID, 'select-type-user'))
                        SELECT_TYPE_USER.select_by_visible_text('PRODUCTOR')


                        INPUT_PASSWORD1 = self.chrome_driver.find_element(
                            By.ID,
                            'input-password1'
                        )
                        INPUT_PASSWORD1.send_keys(self.ProducerUser.password)
                    
                        INPUT_PASSWORD2 = self.chrome_driver.find_element(
                            By.ID,
                            'input-password2'
                        )
                        INPUT_PASSWORD2.send_keys(self.ProducerUser.password)

                        self.generate_pdf(
                            'TEST 001 - /register/',
                            'USUARIO PRODUCTOR',
                            'CREACION DE CUENTA DE TIPO PRODUCTOR CORREGIDA'
                        )
                        
                        INPUT_PASSWORD2.submit()

                        STATUS_ACCOUNT = True

                else:

                    STATUS_ACCOUNT = True 

            except Exception as exc:
                LOGGER.warning(exc)

                STATUS_ACCOUNT = True

                pass
            
            return STATUS_ACCOUNT



        def create_transportist_user() -> bool:
            STATUS_ACCOUNT = False

            BTN_REGISTER = self.chrome_driver.find_element(
                By.ID,
                'btn-register'
            )
            BTN_REGISTER.click()

            INPUT_USERNAME = self.chrome_driver.find_element(
                By.ID,
                'input-username'
            )
            INPUT_USERNAME.send_keys(
                self.TransportistUser.username
            )


            SELECT_TYPE_USER = Select(self.chrome_driver.find_element(By.ID, 'select-type-user'))
            SELECT_TYPE_USER.select_by_visible_text('TRANSPORTISTA')


            SELECT_COUNTRY = Select(self.chrome_driver.find_element(By.ID, 'select-country'))
            SELECT_COUNTRY.select_by_visible_text('Chile')

            INPUT_EMAIL = self.chrome_driver.find_element(
                By.ID,
                'input-email'
            )
            INPUT_EMAIL.send_keys(
                self.TransportistUser.email
            )

            INPUT_IDENTITY_DOCUMENT_NUMBER = self.chrome_driver.find_element(
                By.ID,
                'input-identity-document-number'
            )
            INPUT_IDENTITY_DOCUMENT_NUMBER.send_keys(
                self.TransportistUser.identity_document_number
            )

            INPUT_PASSWORD1 = self.chrome_driver.find_element(
                By.ID,
                'input-password1'
            )
            INPUT_PASSWORD1.send_keys(
                self.TransportistUser.password
            )

            INPUT_PASSWORD2 = self.chrome_driver.find_element(
                By.ID,
                'input-password2'
            )
            INPUT_PASSWORD2.send_keys(
                self.TransportistUser.password
            )

            INPUT_FIRST_NAME = self.chrome_driver.find_element(
                By.ID,
                'input-first-name'
            )
            INPUT_FIRST_NAME.send_keys(
                self.TransportistUser.first_name
            )

            INPUT_LAST_NAME = self.chrome_driver.find_element(
                By.ID,
                'input-last-name'
            )
            INPUT_LAST_NAME.send_keys(
                self.TransportistUser.last_name
            )

            self.generate_pdf(
                'TEST 001 - /register/',
                'USUARIO TRANSPORTISTA',
                'CREACION DE CUENTA DE TIPO TRANSPORTISTA'
            )
            INPUT_LAST_NAME.submit()

            try:
                ERROR_LIST = self.chrome_driver.find_element(
                    By.CLASS_NAME,
                    'errorlist'
                )

                if ERROR_LIST:
                    
                    self.generate_pdf(
                        'TEST 001 - /register/',
                        'USUARIO TRANSPORTISTA',
                        'CREACION INVLIDA DE CUENTA DE TIPO TRANSPORTISTA'
                    )

                    while ERROR_LIST:
                        self.TransportistUser.id = self.TransportistUser.id+1
                        self.TransportistUser.username = f'{self.TransportistUser.username} {self.TransportistUser.id}'

                        INPUT_USERNAME = self.chrome_driver.find_element(
                            By.ID,
                            'input-username'
                        )
                        INPUT_USERNAME.clear()

                        INPUT_USERNAME.send_keys(self.TransportistUser.username)

                        SELECT_TYPE_USER = Select(self.chrome_driver.find_element(By.ID, 'select-type-user'))
                        SELECT_TYPE_USER.select_by_visible_text('PRODUCTOR')



                        INPUT_PASSWORD1 = self.chrome_driver.find_element(
                            By.ID,
                            'input-password1'
                        )
                        INPUT_PASSWORD1.send_keys(self.TransportistUser.password)
                    
                        INPUT_PASSWORD2 = self.chrome_driver.find_element(
                            By.ID,
                            'input-password2'
                        )
                        INPUT_PASSWORD2.send_keys(self.TransportistUser.password)

                        self.generate_pdf(
                            'TEST 001 - /register/',
                            'USUARIO TRANSPORTISTA',
                            'CREACION DE CUENTA DE TIPO TRANSPORTISTA CORREIGDA'
                        )
                        
                        INPUT_PASSWORD2.submit()

                        STATUS_ACCOUNT = True

                else:

                    STATUS_ACCOUNT = True 

            except Exception as exc:
                LOGGER.warning(exc)

                STATUS_ACCOUNT = True

                pass
                
            return STATUS_ACCOUNT



        def create_external_client_user() -> bool:
            STATUS_ACCOUNT = False

            BTN_REGISTER = self.chrome_driver.find_element(
                By.ID,
                'btn-register'
            )
            BTN_REGISTER.click()

            INPUT_USERNAME = self.chrome_driver.find_element(
                By.ID,
                'input-username'
            )
            INPUT_USERNAME.send_keys(
                self.ExternalClientUser.username
            )


            SELECT_TYPE_USER = Select(self.chrome_driver.find_element(By.ID, 'select-type-user'))
            SELECT_TYPE_USER.select_by_visible_text('CLIENTE EXTERNO')


            SELECT_COUNTRY = Select(self.chrome_driver.find_element(By.ID, 'select-country'))
            SELECT_COUNTRY.select_by_visible_text('Ecuador')

            INPUT_IDENTITY_DOCUMENT_NUMBER = self.chrome_driver.find_element(
                By.ID,
                'input-identity-document-number'
            )
            INPUT_IDENTITY_DOCUMENT_NUMBER.send_keys(
                self.ExternalClientUser.identity_document_number
            )


            INPUT_EMAIL = self.chrome_driver.find_element(
                By.ID,
                'input-email'
            )
            INPUT_EMAIL.send_keys(
                self.ExternalClientUser.email
            )


            INPUT_PASSWORD1 = self.chrome_driver.find_element(
                By.ID,
                'input-password1'
            )
            INPUT_PASSWORD1.send_keys(
                self.ExternalClientUser.password
            )

            INPUT_PASSWORD2 = self.chrome_driver.find_element(
                By.ID,
                'input-password2'
            )
            INPUT_PASSWORD2.send_keys(
                self.ExternalClientUser.password
            )

            INPUT_FIRST_NAME = self.chrome_driver.find_element(
                By.ID,
                'input-first-name'
            )
            INPUT_FIRST_NAME.send_keys(
                self.ExternalClientUser.first_name
            )

            INPUT_LAST_NAME = self.chrome_driver.find_element(
                By.ID,
                'input-last-name'
            )
            INPUT_LAST_NAME.send_keys(
                self.ExternalClientUser.last_name
            )

            self.generate_pdf(
                'TEST 001 - /register/',
                'USUARIO CLIENTE EXTERNO',
                'CREACION DE CUENTA DE TIPO CLIENTE EXTERNO'
            )
            INPUT_LAST_NAME.submit()

            try:
                ERROR_LIST = self.chrome_driver.find_element(
                    By.CLASS_NAME,
                    'errorlist'
                )

                if ERROR_LIST:
                    
                    self.generate_pdf(
                        'TEST 001 - /register/',
                        'USUARIO CLIENTE EXTERNO',
                        'CREACION INVALIDA DE CUENTA DE TIPO CLIENTE EXTERNO'
                    )

                    while ERROR_LIST:
                        self.ExternalClientUser.id = self.ExternalClientUser.id+1
                        self.ExternalClientUser.username = f'{self.ExternalClientUser.username}{self.ExternalClientUser.id}'

                        INPUT_USERNAME = self.chrome_driver.find_element(
                            By.ID,
                            'input-username'
                        )
                        INPUT_USERNAME.clear()

                        INPUT_USERNAME.send_keys(self.ExternalClientUser.username)

                        SELECT_TYPE_USER = Select(self.chrome_driver.find_element(By.ID, 'select-type-user'))
                        SELECT_TYPE_USER.select_by_visible_text('PRODUCTOR')



                        INPUT_PASSWORD1 = self.chrome_driver.find_element(
                            By.ID,
                            'input-password1'
                        )
                        INPUT_PASSWORD1.send_keys(self.ExternalClientUser.password)
                    
                        INPUT_PASSWORD2 = self.chrome_driver.find_element(
                            By.ID,
                            'input-password2'
                        )
                        INPUT_PASSWORD2.send_keys(self.ExternalClientUser.password)

                        self.generate_pdf(
                            'TEST 001 - /register/',
                            'USUARIO CLIENTE EXTERNO',
                            'CREACION DE CUENTA DE TIPO CLIENTE EXTERNO CORREGIDA'
                        )
                        
                        INPUT_PASSWORD2.submit()

                        STATUS_ACCOUNT = True

                else:

                    STATUS_ACCOUNT = True 

            except Exception as exc:
                LOGGER.warning(exc)

                STATUS_ACCOUNT = True

                pass
                
            return STATUS_ACCOUNT



        def create_internal_client_user() -> bool:
            STATUS_ACCOUNT = False

            BTN_REGISTER = self.chrome_driver.find_element(
                By.ID,
                'btn-register'
            )
            BTN_REGISTER.click()

            INPUT_USERNAME = self.chrome_driver.find_element(
                By.ID,
                'input-username'
            )
            INPUT_USERNAME.send_keys(
                self.InternalClientUser.username
            )


            SELECT_TYPE_USER = Select(self.chrome_driver.find_element(By.ID, 'select-type-user'))
            SELECT_TYPE_USER.select_by_visible_text('CLIENTE INTERNO')


            SELECT_COUNTRY = Select(self.chrome_driver.find_element(By.ID, 'select-country'))
            SELECT_COUNTRY.select_by_visible_text('Egypt')

            INPUT_EMAIL = self.chrome_driver.find_element(
                By.ID,
                'input-email'
            )
            INPUT_EMAIL.send_keys(
                self.InternalClientUser.email
            )

            INPUT_IDENTITY_DOCUMENT_NUMBER = self.chrome_driver.find_element(
                By.ID,
                'input-identity-document-number'
            )
            INPUT_IDENTITY_DOCUMENT_NUMBER.send_keys(
                self.InternalClientUser.identity_document_number
            )

            INPUT_PASSWORD1 = self.chrome_driver.find_element(
                By.ID,
                'input-password1'
            )
            INPUT_PASSWORD1.send_keys(
                self.InternalClientUser.password
            )

            INPUT_PASSWORD2 = self.chrome_driver.find_element(
                By.ID,
                'input-password2'
            )
            INPUT_PASSWORD2.send_keys(
                self.InternalClientUser.password
            )

            INPUT_FIRST_NAME = self.chrome_driver.find_element(
                By.ID,
                'input-first-name'
            )
            INPUT_FIRST_NAME.send_keys(
                self.InternalClientUser.first_name
            )

            INPUT_LAST_NAME = self.chrome_driver.find_element(
                By.ID,
                'input-last-name'
            )
            INPUT_LAST_NAME.send_keys(
                self.InternalClientUser.last_name
            )

            self.generate_pdf(
                'TEST 001 - /register/',
                'USUARIO CLIENTE INTERNO',
                'CREACION DE CUENTA DE TIPO CLIENTE INTERNO'
            )
            INPUT_LAST_NAME.submit()

            try:
                ERROR_LIST = self.chrome_driver.find_element(
                    By.CLASS_NAME,
                    'errorlist'
                )

                if ERROR_LIST:
                    
                    self.generate_pdf(
                        'TEST 001 - /register/',
                        'USUARIO CLIENTE INTERNO',
                        'CREACION DE CUENTA DE TIPO CLIENTE INTERNO'
                    )

                    while ERROR_LIST:
                        self.InternalClientUser.id = self.InternalClientUser.id+1
                        self.InternalClientUser.username = f'{self.InternalClientUser.username}{self.InternalClientUser.id}'

                        INPUT_USERNAME = self.chrome_driver.find_element(
                            By.ID,
                            'input-username'
                        )
                        INPUT_USERNAME.clear()

                        INPUT_USERNAME.send_keys(self.InternalClientUser.username)

                        SELECT_TYPE_USER = Select(self.chrome_driver.find_element(By.ID, 'select-type-user'))
                        SELECT_TYPE_USER.select_by_visible_text('PRODUCTOR')



                        INPUT_PASSWORD1 = self.chrome_driver.find_element(
                            By.ID,
                            'input-password1'
                        )
                        INPUT_PASSWORD1.send_keys(self.InternalClientUser.password)
                    
                        INPUT_PASSWORD2 = self.chrome_driver.find_element(
                            By.ID,
                            'input-password2'
                        )
                        INPUT_PASSWORD2.send_keys(self.InternalClientUser.password)

                        self.generate_pdf(
                            'TEST 001 - /register/',
                            'USUARIO CLIENTE INTERNO',
                            'CREACION DE CUENTA DE TIPO CLIENTE INTERNO'
                        )
                        
                        INPUT_PASSWORD2.submit()

                        STATUS_ACCOUNT = True

                else:

                    STATUS_ACCOUNT = True 

            except Exception as exc:
                LOGGER.warning(exc)

                STATUS_ACCOUNT = True

                pass
                
            return STATUS_ACCOUNT




        status_producer_account = create_producer_user()

        if status_producer_account:
            status_transportist_account = create_transportist_user()

            if status_transportist_account:
                status_internal_cliente_account = create_internal_client_user()

                if status_internal_cliente_account:
                    status_external_cliente_account = create_external_client_user()

                    if status_external_cliente_account:
                        STATUS = True

                        return STATUS
        
        return STATUS


    def login_test(self) -> bool:
        STATUS = False

        def login_producer_user() -> bool:
            STATUS_LOGIN = False

            try:

                BTN_LOGIN = self.chrome_driver.find_element(
                    By.ID,
                    'btn-login'
                )
                BTN_LOGIN.click()

                INPUT_USERNAME = self.chrome_driver.find_element(
                    By.ID,
                    'username'
                )
                INPUT_USERNAME.send_keys(
                    self.ProducerUser.username
                )

                INPUT_PASSWORD = self.chrome_driver.find_element(
                    By.ID,
                    'password'
                )

                INPUT_PASSWORD.send_keys(
                    self.ProducerUser.password
                )

                BTN_LOGIN = self.chrome_driver.find_element(
                    By.ID,
                    'btn-login'
                )

                self.generate_pdf(
                    'TEST 002 - /login/',
                    'USUARIO PRODUCTOR',
                    'INICIO DE SESION CON USUARIO PRODUCTOR'
                )
                BTN_LOGIN.click()

                self.generate_pdf(
                    'TEST 003 - /feed/',
                    'USUARIO PRODUCTOR',
                    'VISTA DE PUBLICACIONES DESPUES DE INICIAR SESION'
                )

                STATUS_LOGIN = True

            except Exception as exc:
                LOGGER.warning(exc)
                pass
                
            return STATUS_LOGIN


        def login_internal_client_user() -> bool:
            STATUS_LOGIN = False

            try:

                BTN_LOGIN = self.chrome_driver.find_element(
                    By.ID,
                    'btn-login'
                )
                BTN_LOGIN.click()

                INPUT_USERNAME = self.chrome_driver.find_element(
                    By.ID,
                    'username'
                )
                INPUT_USERNAME.send_keys(
                    self.InternalClientUser.username
                )

                INPUT_PASSWORD = self.chrome_driver.find_element(
                    By.ID,
                    'password'
                )

                INPUT_PASSWORD.send_keys(
                    self.InternalClientUser.password
                )

                BTN_LOGIN = self.chrome_driver.find_element(
                    By.ID,
                    'btn-login'
                )

                self.generate_pdf(
                    'TEST 002 - /login/',
                    'USUARIO CLIENTE INTERNO',
                    'INICIO DE SESION CON USUARIO CLIENTE INTERNO '
                )
                BTN_LOGIN.click()

                self.generate_pdf(
                    'TEST 003 - /feed/',
                    'USUARIO CLIENTE INTERNO',
                    'VISTA DE PUBLICACIONES DESPUES DE INICIAR SESION'
                )

                STATUS_LOGIN = True

            except Exception as exc:
                LOGGER.warning(exc)
                pass
            
            return STATUS_LOGIN


        def login_external_client_user() -> bool:
            STATUS_LOGIN = False


            try:

                BTN_LOGIN = self.chrome_driver.find_element(
                    By.ID,
                    'btn-login'
                )
                BTN_LOGIN.click()

                INPUT_USERNAME = self.chrome_driver.find_element(
                    By.ID,
                    'username'
                )
                INPUT_USERNAME.send_keys(
                    self.ExternalClientUser.username
                )

                INPUT_PASSWORD = self.chrome_driver.find_element(
                    By.ID,
                    'password'
                )

                INPUT_PASSWORD.send_keys(
                    self.ExternalClientUser.password
                )

                BTN_LOGIN = self.chrome_driver.find_element(
                    By.ID,
                    'btn-login'
                )

                self.generate_pdf(
                    'TEST 002 - /login/',
                    'USUARIO CLIENTE EXTERNO',
                    'INICIO DE SESION CON USUARIO CLIENTE EXTERNO'
                )
                BTN_LOGIN.click()

                self.generate_pdf(
                    'TEST 003 - /feed/',
                    'USUARIO CLIENTE EXTERNO',
                    'VISTA DE PUBLICACIONES DESPUES DE INICIAR SESION'
                )

                STATUS_LOGIN = True

            except Exception as exc:
                LOGGER.warning(exc)
                pass

            return STATUS_LOGIN


        def login_transportist_user() -> bool:

            STATUS_LOGIN = False

            try:

                BTN_LOGIN = self.chrome_driver.find_element(
                    By.ID,
                    'btn-login'
                )
                BTN_LOGIN.click()

                INPUT_USERNAME = self.chrome_driver.find_element(
                    By.ID,
                    'username'
                )
                INPUT_USERNAME.send_keys(
                    self.TransportistUser.username
                )

                INPUT_PASSWORD = self.chrome_driver.find_element(
                    By.ID,
                    'password'
                )

                INPUT_PASSWORD.send_keys(
                    self.TransportistUser.password
                )

                BTN_LOGIN = self.chrome_driver.find_element(
                    By.ID,
                    'btn-login'
                )

                self.generate_pdf(
                    'TEST 002 - /login/',
                    'USUARIO TRANSPORTISTA',
                    'INICIO DE SESION CON USUARIO TRANSPORTISTA'
                )
                BTN_LOGIN.click()

                self.generate_pdf(
                    'TEST 003 - /feed/',
                    'USUARIO TRANSPORTISTA',
                    'VISTA DE PUBLICACIONES DESPUES DE INICIAR SESION'
                )

                STATUS_LOGIN = True

            except Exception as exc:
                LOGGER.warning(exc)
                pass
                
            return STATUS_LOGIN


        status_login_producer_user = login_producer_user()

        if status_login_producer_user:

            # Modificar y agregar condicionales acorde al usuario
            
            STATUS = True


        return STATUS

    def user_profile_test(self) -> bool:
        STATUS = False

        try:
            NAV_LINK_PROFILE = self.chrome_driver.find_element(
                By.ID,
                'nav-link-profile'
            )
            NAV_LINK_PROFILE.click()

            self.generate_pdf(
                'TEST 004 - /profile',
                'PERFIL DE USUARIO',
                'Mi Perfil'
            )

            STATUS = True
            

        except Exception as exc:
            LOGGER.warning(exc)
            pass
            
        return STATUS

    def user_bank_test(self) -> bool:
        STATUS = False


        def create_bank_account_producer_user() -> bool:
            STATUS_BANK_ACCOUNT = False

            try:
                NAV_LINK_BANK = self.chrome_driver.find_element(
                    By.ID,
                    'nav-link-bank'
                )
                NAV_LINK_BANK.click()

                self.generate_pdf(
                    'TEST 005 - /bank/',
                    'USUARIO PRODUCTOR',
                    'Mi banco - SIN CUENTAS DISPONIBLES'
                )

                try:
                    SELECT_BANK_NAME = Select(self.chrome_driver.find_element(By.ID, 'bank-name'))
                    SELECT_BANK_NAME.select_by_visible_text('BANCO BBVA')

                    SELECT_TYPE_BANK_ACCOUNT = Select(self.chrome_driver.find_element(By.ID, 'bank-type'))
                    SELECT_TYPE_BANK_ACCOUNT.select_by_visible_text('CUENTA AHORRO')

                    INPUT_BANK_ACCOUNT_NUMBER = self.chrome_driver.find_element(
                        By.ID,
                        'bank-account-number'
                    )
                    INPUT_BANK_ACCOUNT_NUMBER.send_keys(
                        '10123789'
                    )
                    
                    
                    BUTTON_ADD_BANK_ACCOUNT = self.chrome_driver.find_element(
                        By.ID,
                        'btn-add-bank-account'
                    )
                    try:
                        BUTTON_ADD_BANK_ACCOUNT.click()
                    
                    except:
                        BUTTON_ADD_BANK_ACCOUNT.submit()
                        INPUT_BANK_ACCOUNT_NUMBER.submit()


                
                except Exception as exc:
                    self.set_test_properties(exc)
                    pass

                try:
                    SELECT_BANK_NAME = Select(self.chrome_driver.find_element(By.ID, 'bank-name'))
                    SELECT_BANK_NAME.select_by_visible_text('BANCO SANTANDER')

                    SELECT_TYPE_BANK_ACCOUNT = Select(self.chrome_driver.find_element(By.ID, 'bank-type'))
                    SELECT_TYPE_BANK_ACCOUNT.select_by_visible_text('CUENTA VISTA')


                    INPUT_BANK_ACCOUNT_NUMBER = self.chrome_driver.find_element(
                        By.ID,
                        'bank-account-number'
                    )
                    INPUT_BANK_ACCOUNT_NUMBER.send_keys(
                        '10123789'
                    )
                    BUTTON_ADD_BANK_ACCOUNT = self.chrome_driver.find_element(
                        By.ID,
                        'btn-add-bank-account'
                    )
                    try:
                        BUTTON_ADD_BANK_ACCOUNT.click()
                    
                    except:
                        BUTTON_ADD_BANK_ACCOUNT.submit()
                        INPUT_BANK_ACCOUNT_NUMBER.submit()

                except Exception as exc:
                    self.set_test_properties(exc)
                    LOGGER.warning(exc)


                try:
                    SELECT_BANK_NAME = Select(self.chrome_driver.find_element(By.ID, 'bank-name'))
                    SELECT_BANK_NAME.select_by_visible_text('BANCO RIPLEY')

                    SELECT_TYPE_BANK_ACCOUNT = Select(self.chrome_driver.find_element(By.ID, 'bank-type'))
                    SELECT_TYPE_BANK_ACCOUNT.select_by_visible_text('CUENTA AHORRO')


                    INPUT_BANK_ACCOUNT_NUMBER = self.chrome_driver.find_element(
                        By.ID,
                        'bank-account-number'
                    )
                    INPUT_BANK_ACCOUNT_NUMBER.send_keys(
                            '10123789'
                    )
                    BUTTON_ADD_BANK_ACCOUNT = self.chrome_driver.find_element(
                        By.ID,
                            'btn-add-bank-account'
                    )

                    try:
                        BUTTON_ADD_BANK_ACCOUNT.click()
                        
                    except:
                        BUTTON_ADD_BANK_ACCOUNT.submit()
                        INPUT_BANK_ACCOUNT_NUMBER.submit()

                except Exception as exc:
                    self.set_test_properties(exc)
                    LOGGER.warning(exc)



                try:
                    SELECT_BANK_NAME = Select(self.chrome_driver.find_element(By.ID, 'bank-name'))
                    SELECT_BANK_NAME.select_by_visible_text('BANCO FALABELLA')

                    SELECT_TYPE_BANK_ACCOUNT = Select(self.chrome_driver.find_element(By.ID, 'bank-type'))
                    SELECT_TYPE_BANK_ACCOUNT.select_by_visible_text('CUENTA VISTA')


                    INPUT_BANK_ACCOUNT_NUMBER = self.chrome_driver.find_element(
                                By.ID,
                                'bank-account-number'
                    )
                    INPUT_BANK_ACCOUNT_NUMBER.send_keys(
                                '10123789'
                    )
                    BUTTON_ADD_BANK_ACCOUNT = self.chrome_driver.find_element(
                                By.ID,
                                'btn-add-bank-account'
                    )
                    try:
                        BUTTON_ADD_BANK_ACCOUNT.click()
                            
                    except:
                        BUTTON_ADD_BANK_ACCOUNT.submit()
                        INPUT_BANK_ACCOUNT_NUMBER.submit()

                except Exception as exc:
                    self.set_test_properties(exc)
                    LOGGER.warning(exc)

                try:
                    SELECT_BANK_NAME = Select(self.chrome_driver.find_element(By.ID, 'bank-name'))
                    SELECT_BANK_NAME.select_by_visible_text('BICE')

                    SELECT_TYPE_BANK_ACCOUNT = Select(self.chrome_driver.find_element(By.ID, 'bank-type'))
                    SELECT_TYPE_BANK_ACCOUNT.select_by_visible_text('CUENTA VISTA')


                    INPUT_BANK_ACCOUNT_NUMBER = self.chrome_driver.find_element(
                                    By.ID,
                                    'bank-account-number'
                    )
                    INPUT_BANK_ACCOUNT_NUMBER.send_keys(
                                    '10123789'
                    )
                    BUTTON_ADD_BANK_ACCOUNT = self.chrome_driver.find_element(
                                    By.ID,
                                    'btn-add-bank-account'
                    )
                    try:
                        BUTTON_ADD_BANK_ACCOUNT.click()
                                
                    except:
                        BUTTON_ADD_BANK_ACCOUNT.submit()
                        INPUT_BANK_ACCOUNT_NUMBER.submit()
                    

                except Exception as exc:
                    self.set_test_properties(exc)
                    pass


                self.generate_pdf(
                    'TEST 005 - /bank/',
                    'USUARIO PRODUCTOR',
                    'Mi banco - CON CUENTAS DISPONIBLES'
                )
                STATUS_BANK_ACCOUNT = True

            except Exception as exc:
                LOGGER.warning(exc)
                pass

            return STATUS_BANK_ACCOUNT
        

        status_bank_account_producer_user = create_bank_account_producer_user()

        if status_bank_account_producer_user:
            STATUS = True

            return STATUS

        return STATUS
    
    def create_product_post(self) -> bool:
        STATUS = False

        def create_post_1_producer_user() -> bool:
            STATUS_POST = False

            try:

                title = self.Product1ProducerUser.title
                price = self.Product1ProducerUser.price
                quantity = self.Product1ProducerUser.quantity
                image = self.Product1ProducerUser.image
                description = self.Product1ProducerUser.description


                self.set_test_properties(title)
                self.set_test_properties(price)
                self.set_test_properties(quantity)
                self.set_test_properties(image)



                DROPDOWN_MENU = self.chrome_driver.find_element(
                    By.XPATH,
                    "//li[@class='nav-item dropdown']"
                )
                DROPDOWN_MENU.click()


                self.set_test_properties(DROPDOWN_MENU)

                
                try:
                    DROPDOWN_ITEM_POST = self.chrome_driver.find_element(
                        By.ID,
                        'publish_product_post'
                    )
                    DROPDOWN_ITEM_POST.click()


                except Exception as exc:
                    DROPDOWN_ITEM_POST = self.chrome_driver.find_element(
                        By.XPATH,
                        "//a[@id='publish_product_post']"
                    ).click()

                    LOGGER.warning(exc)
                    pass

                self.set_test_properties(DROPDOWN_ITEM_POST)


                #   Ingreso de datos
                try:
                    INPUT_TITLE = self.chrome_driver.find_element(
                        By.ID,
                        'product-title'
                    )
                    INPUT_TITLE.send_keys(title)

                    self.set_test_properties(INPUT_TITLE)

                    INPUT_PRICE = self.chrome_driver.find_element(
                        By.ID,
                        'product-price'
                    )
                    INPUT_PRICE.send_keys(price)

                    INPUT_QUANTITY = self.chrome_driver.find_element(
                        By.ID,
                        'product-quantity'
                    )
                    INPUT_QUANTITY.send_keys(quantity)

                    INPUT_QUALITY = self.chrome_driver.find_element(
                        By.ID,
                        'product-quality'
                    )
                    INPUT_QUALITY.send_keys(5)


                    TEXTAREA_DESCRIPTION = self.chrome_driver.find_element(
                            By.ID,
                            'product-description'
                    )
                    TEXTAREA_DESCRIPTION.send_keys(description)


                    if self.Properties.platform_system == 'Windows':
                        INPUT_FILE_IMAGE = self.chrome_driver.find_element(
                            By.ID,
                            'product-img'
                        ).send_keys(
                            image
                        )

                    BTN_POST = self.chrome_driver.find_element(
                        By.ID,
                        'btn-post'
                    )

                    self.generate_pdf(
                        'TEST 006 - /post/',
                        'USUARIO PRODUCTOR',
                        'PUBLICACION 1 DE PRODUCTO'
                    )

                    try:
                        BTN_POST.click()
                        BTN_POST.submit()

                    except Exception as exc:
                        LOGGER.warning(exc)
                        self.set_test_properties(exc)
                        
                        try:
                            BTN_POST.submit()
                        
                        except Exception as exc:
                            self.set_test_properties(exc)


                            INPUT_TITLE.submit()
                            pass

                    self.generate_pdf(
                        'TEST 006 - /post/',
                        'USUARIO PRODUCTOR',
                        'PUBLICACION 1 DE PRODUCTO CREADA'
                    )
                    STATUS_POST = True

                    return STATUS_POST

                except Exception as exc:
                    LOGGER.warning(exc)
                    self.set_test_properties(exc)
                    pass

                
                    
            except Exception as exc:
                LOGGER.warning(exc)
                self.set_test_properties(exc)
                pass

            return STATUS_POST

        def create_post_2_producer_user() -> bool:
            STATUS_POST = False

            try:

                title = self.Product2ProducerUser.title
                price = self.Product2ProducerUser.price
                quantity = self.Product2ProducerUser.quantity
                image = self.Product2ProducerUser.image
                description = self.Product2ProducerUser.description


                self.set_test_properties(title)
                self.set_test_properties(price)
                self.set_test_properties(quantity)
                self.set_test_properties(image)

                DROPDOWN_MENU = self.chrome_driver.find_element(
                    By.XPATH,
                    "//li[@class='nav-item dropdown']"
                )
                DROPDOWN_MENU.click()

                
                
                try:
                    DROPDOWN_ITEM_POST = self.chrome_driver.find_element(
                        By.ID,
                        'publish_product_post'
                    )
                    DROPDOWN_ITEM_POST.click()


                except Exception as exc:
                    DROPDOWN_ITEM_POST = self.chrome_driver.find_element(
                        By.XPATH,
                        "//a[@id='publish_product_post']"
                    ).click()

                    LOGGER.warning(exc)
                    pass
                self.set_test_properties(DROPDOWN_ITEM_POST)

                #   Ingreso de datos
                try:
                    INPUT_TITLE = self.chrome_driver.find_element(
                        By.ID,
                        'product-title'
                    )
                    INPUT_TITLE.send_keys(title)

                    INPUT_PRICE = self.chrome_driver.find_element(
                        By.ID,
                        'product-price'
                    )
                    INPUT_PRICE.send_keys(price)

                    INPUT_QUANTITY = self.chrome_driver.find_element(
                        By.ID,
                        'product-quantity'
                    )
                    INPUT_QUANTITY.send_keys(quantity)
                    INPUT_QUALITY = self.chrome_driver.find_element(
                        By.ID,
                        'product-quality'
                    )
                    INPUT_QUALITY.send_keys(3)
                    TEXTAREA_DESCRIPTION = self.chrome_driver.find_element(
                            By.ID,
                            'product-description'
                    )
                    TEXTAREA_DESCRIPTION.send_keys(description)


                    if self.Properties.platform_system == 'Windows':
                        INPUT_FILE_IMAGE = self.chrome_driver.find_element(
                            By.ID,
                            'product-img'
                        ).send_keys(
                            image
                        )

                    BTN_POST = self.chrome_driver.find_element(
                        By.ID,
                        'btn-post'
                    )

                    try:
                        BTN_POST.click()
                        BTN_POST.submit()

                    except Exception as exc:
                        LOGGER.warning(exc)
                        self.set_test_properties(exc)
                        
                        try:
                            BTN_POST.submit()
                        
                        except Exception as exc:
                            self.set_test_properties(exc)


                            INPUT_TITLE.submit()
                            pass

                    self.generate_pdf(
                        'TEST 006 - /post/',
                        'USUARIO PRODUCTOR',
                        'PUBLICACION 2 DE PRODUCTO CREADA'
                    )

                    STATUS_POST = True
                    return STATUS_POST
                    
                except Exception as exc:
                    LOGGER.warning(exc)
                    pass   
            except Exception as exc:
                LOGGER.warning(exc)
                pass

            
            return STATUS_POST

        def create_post_3_producer_user() -> bool:
            STATUS_POST = False

            try:

                title = self.Product3ProducerUser.title
                price = self.Product3ProducerUser.price
                quantity = self.Product3ProducerUser.quantity
                image = self.Product3ProducerUser.image
                description = self.Product3ProducerUser.description



                self.set_test_properties(title)
                self.set_test_properties(price)
                self.set_test_properties(quantity)
                self.set_test_properties(image)

                DROPDOWN_MENU = self.chrome_driver.find_element(
                    By.XPATH,
                    "//li[@class='nav-item dropdown']"
                )
                DROPDOWN_MENU.click()

                
                
                try:
                    DROPDOWN_ITEM_POST = self.chrome_driver.find_element(
                        By.ID,
                        'publish_product_post'
                    )
                    DROPDOWN_ITEM_POST.click()


                except Exception as exc:
                    DROPDOWN_ITEM_POST = self.chrome_driver.find_element(
                        By.XPATH,
                        "//a[@id='publish_product_post']"
                    ).click()

                    LOGGER.warning(exc)
                    pass
                self.set_test_properties(DROPDOWN_ITEM_POST)


                #   Ingreso de datos
                try:
                    INPUT_TITLE = self.chrome_driver.find_element(
                        By.ID,
                        'product-title'
                    )
                    INPUT_TITLE.send_keys(title)

                    INPUT_PRICE = self.chrome_driver.find_element(
                        By.ID,
                        'product-price'
                    )
                    INPUT_PRICE.send_keys(price)

                    INPUT_QUANTITY = self.chrome_driver.find_element(
                        By.ID,
                        'product-quantity'
                    )
                    INPUT_QUANTITY.send_keys(quantity)
                    INPUT_QUALITY = self.chrome_driver.find_element(
                        By.ID,
                        'product-quality'
                    )
                    INPUT_QUALITY.send_keys(2)
                    TEXTAREA_DESCRIPTION = self.chrome_driver.find_element(
                            By.ID,
                            'product-description'
                    )
                    TEXTAREA_DESCRIPTION.send_keys(description)


                    if self.Properties.platform_system == 'Windows':
                        INPUT_FILE_IMAGE = self.chrome_driver.find_element(
                            By.ID,
                            'product-img'
                        ).send_keys(
                            image
                        )

                    BTN_POST = self.chrome_driver.find_element(
                        By.ID,
                        'btn-post'
                    )

                    self.generate_pdf(
                        'TEST 006 - /post/',
                        'USUARIO PRODUCTOR',
                        'PUBLICACION 3 DE PRODUCTO'
                    )

                    try:
                        BTN_POST.click()
                        BTN_POST.submit()

                    except Exception as exc:
                        LOGGER.warning(exc)
                        self.set_test_properties(exc)
                        
                        try:
                            BTN_POST.submit()
                        
                        except Exception as exc:
                            self.set_test_properties(exc)


                            INPUT_TITLE.submit()
                            pass

                    self.generate_pdf(
                        'TEST 006 - /post/',
                        'USUARIO PRODUCTOR',
                        'PUBLICACION 3 DE PRODUCTO CREADA'
                    )

                    STATUS_POST = True

                    return STATUS_POST
                    

                except Exception as exc:
                    LOGGER.warning(exc)
                    self.set_test_properties(exc)


                

            except Exception as exc:
                LOGGER.warning(exc)

                self.set_test_properties(exc)
                pass
            
            
            return STATUS_POST
            
        def create_post_4_producer_user() -> bool:
            STATUS_POST = False

            try:

                title = self.Product4ProducerUser.title
                price = self.Product4ProducerUser.price
                quantity = self.Product4ProducerUser.quantity
                image = self.Product4ProducerUser.image
                description = self.Product4ProducerUser.description



                self.set_test_properties(title)
                self.set_test_properties(price)
                self.set_test_properties(quantity)
                self.set_test_properties(image)

                DROPDOWN_MENU = self.chrome_driver.find_element(
                    By.XPATH,
                    "//li[@class='nav-item dropdown']"
                )
                DROPDOWN_MENU.click()

                
                
                try:
                    DROPDOWN_ITEM_POST = self.chrome_driver.find_element(
                        By.ID,
                        'publish_product_post'
                    )
                    DROPDOWN_ITEM_POST.click()


                except Exception as exc:
                    DROPDOWN_ITEM_POST = self.chrome_driver.find_element(
                        By.XPATH,
                        "//a[@id='publish_product_post']"
                    ).click()

                    LOGGER.warning(exc)
                    pass
                self.set_test_properties(DROPDOWN_ITEM_POST)


                #   Ingreso de datos
                try:
                    INPUT_TITLE = self.chrome_driver.find_element(
                        By.ID,
                        'product-title'
                    )
                    INPUT_TITLE.send_keys(title)

                    INPUT_PRICE = self.chrome_driver.find_element(
                        By.ID,
                        'product-price'
                    )
                    INPUT_PRICE.send_keys(price)

                    INPUT_QUANTITY = self.chrome_driver.find_element(
                        By.ID,
                        'product-quantity'
                    )
                    INPUT_QUANTITY.send_keys(quantity)
                    INPUT_QUALITY = self.chrome_driver.find_element(
                        By.ID,
                        'product-quality'
                    )
                    INPUT_QUALITY.send_keys(5)
                    TEXTAREA_DESCRIPTION = self.chrome_driver.find_element(
                            By.ID,
                            'product-description'
                    )
                    TEXTAREA_DESCRIPTION.send_keys(description)


                    if self.Properties.platform_system == 'Windows':
                        INPUT_FILE_IMAGE = self.chrome_driver.find_element(
                            By.ID,
                            'product-img'
                        ).send_keys(
                            image
                        )

                    BTN_POST = self.chrome_driver.find_element(
                        By.ID,
                        'btn-post'
                    )

                    self.generate_pdf(
                        'TEST 006 - /post/',
                        'USUARIO PRODUCTOR',
                        'PUBLICACION 4 DE PRODUCTO'
                    )

                    try:
                        BTN_POST.click()
                        BTN_POST.submit()

                    except Exception as exc:
                        LOGGER.warning(exc)
                        self.set_test_properties(exc)
                        
                        try:
                            BTN_POST.submit()
                        
                        except Exception as exc:
                            self.set_test_properties(exc)


                            INPUT_TITLE.submit()
                            pass

                    self.generate_pdf(
                        'TEST 006 - /post/',
                        'USUARIO PRODUCTOR',
                        'PUBLICACION 4 DE PRODUCTO CREADA'
                    )

                    STATUS_POST = True

                    return STATUS_POST
                    

                except Exception as exc:
                    LOGGER.warning(exc)
                    self.set_test_properties(exc)


                

            except Exception as exc:
                LOGGER.warning(exc)

                self.set_test_properties(exc)
                pass
            
            
            return STATUS_POST

        def create_post_5_producer_user() -> bool:
            STATUS_POST = False

            try:

                title = self.Product5ProducerUser.title
                price = self.Product5ProducerUser.price
                quantity = self.Product5ProducerUser.quantity
                image = self.Product5ProducerUser.image
                description = self.Product5ProducerUser.description



                self.set_test_properties(title)
                self.set_test_properties(price)
                self.set_test_properties(quantity)
                self.set_test_properties(image)

                DROPDOWN_MENU = self.chrome_driver.find_element(
                    By.XPATH,
                    "//li[@class='nav-item dropdown']"
                )
                DROPDOWN_MENU.click()

                
                
                try:
                    DROPDOWN_ITEM_POST = self.chrome_driver.find_element(
                        By.ID,
                        'publish_product_post'
                    )
                    DROPDOWN_ITEM_POST.click()


                except Exception as exc:
                    DROPDOWN_ITEM_POST = self.chrome_driver.find_element(
                        By.XPATH,
                        "//a[@id='publish_product_post']"
                    ).click()

                    LOGGER.warning(exc)
                    pass
                self.set_test_properties(DROPDOWN_ITEM_POST)


                #   Ingreso de datos
                try:
                    INPUT_TITLE = self.chrome_driver.find_element(
                        By.ID,
                        'product-title'
                    )
                    INPUT_TITLE.send_keys(title)

                    INPUT_PRICE = self.chrome_driver.find_element(
                        By.ID,
                        'product-price'
                    )
                    INPUT_PRICE.send_keys(price)

                    INPUT_QUANTITY = self.chrome_driver.find_element(
                        By.ID,
                        'product-quantity'
                    )
                    INPUT_QUANTITY.send_keys(quantity)
                    INPUT_QUALITY = self.chrome_driver.find_element(
                        By.ID,
                        'product-quality'
                    )
                    INPUT_QUALITY.send_keys(4)
                    TEXTAREA_DESCRIPTION = self.chrome_driver.find_element(
                            By.ID,
                            'product-description'
                    )
                    TEXTAREA_DESCRIPTION.send_keys(description)


                    if self.Properties.platform_system == 'Windows':
                        INPUT_FILE_IMAGE = self.chrome_driver.find_element(
                            By.ID,
                            'product-img'
                        ).send_keys(
                            image
                        )

                    BTN_POST = self.chrome_driver.find_element(
                        By.ID,
                        'btn-post'
                    )

                    self.generate_pdf(
                        'TEST 006 - /post/',
                        'USUARIO PRODUCTOR',
                        'PUBLICACION 5 DE PRODUCTO'
                    )

                    try:
                        BTN_POST.click()
                        BTN_POST.submit()

                    except Exception as exc:
                        LOGGER.warning(exc)
                        self.set_test_properties(exc)
                        
                        try:
                            BTN_POST.submit()
                        
                        except Exception as exc:
                            self.set_test_properties(exc)


                            INPUT_TITLE.submit()
                            pass

                    self.generate_pdf(
                        'TEST 006 - /post/',
                        'USUARIO PRODUCTOR',
                        'PUBLICACION 5 DE PRODUCTO CREADA'
                    )

                    STATUS_POST = True

                    return STATUS_POST
                    

                except Exception as exc:
                    LOGGER.warning(exc)
                    self.set_test_properties(exc)


                

            except Exception as exc:
                LOGGER.warning(exc)

                self.set_test_properties(exc)
                pass
            
            
            return STATUS_POST
   

        def create_post_6_producer_user() -> bool:
            STATUS_POST = False

            try:

                title = self.Product6ProducerUser.title
                price = self.Product6ProducerUser.price
                quantity = self.Product6ProducerUser.quantity
                image = self.Product6ProducerUser.image
                description = self.Product6ProducerUser.description



                self.set_test_properties(title)
                self.set_test_properties(price)
                self.set_test_properties(quantity)
                self.set_test_properties(image)

                DROPDOWN_MENU = self.chrome_driver.find_element(
                    By.XPATH,
                    "//li[@class='nav-item dropdown']"
                )
                DROPDOWN_MENU.click()

                
                
                try:
                    DROPDOWN_ITEM_POST = self.chrome_driver.find_element(
                        By.ID,
                        'publish_product_post'
                    )
                    DROPDOWN_ITEM_POST.click()


                except Exception as exc:
                    DROPDOWN_ITEM_POST = self.chrome_driver.find_element(
                        By.XPATH,
                        "//a[@id='publish_product_post']"
                    ).click()

                    LOGGER.warning(exc)
                    pass
                self.set_test_properties(DROPDOWN_ITEM_POST)


                #   Ingreso de datos
                try:
                    INPUT_TITLE = self.chrome_driver.find_element(
                        By.ID,
                        'product-title'
                    )
                    INPUT_TITLE.send_keys(title)

                    INPUT_PRICE = self.chrome_driver.find_element(
                        By.ID,
                        'product-price'
                    )
                    INPUT_PRICE.send_keys(price)

                    INPUT_QUANTITY = self.chrome_driver.find_element(
                        By.ID,
                        'product-quantity'
                    )
                    INPUT_QUANTITY.send_keys(quantity)

                    INPUT_QUALITY = self.chrome_driver.find_element(
                        By.ID,
                        'product-quality'
                    )
                    INPUT_QUALITY.send_keys(1)

                    TEXTAREA_DESCRIPTION = self.chrome_driver.find_element(
                            By.ID,
                            'product-description'
                    )
                    TEXTAREA_DESCRIPTION.send_keys(description)


                    if self.Properties.platform_system == 'Windows':
                        INPUT_FILE_IMAGE = self.chrome_driver.find_element(
                            By.ID,
                            'product-img'
                        ).send_keys(
                            image
                        )

                    BTN_POST = self.chrome_driver.find_element(
                        By.ID,
                        'btn-post'
                    )

                    self.generate_pdf(
                        'TEST 006 - /post/',
                        'USUARIO PRODUCTOR',
                        'PUBLICACION 6 DE PRODUCTO'
                    )

                    try:
                        BTN_POST.click()
                        BTN_POST.submit()

                    except Exception as exc:
                        LOGGER.warning(exc)
                        self.set_test_properties(exc)
                        
                        try:
                            BTN_POST.submit()
                        
                        except Exception as exc:
                            self.set_test_properties(exc)


                            INPUT_TITLE.submit()
                            pass

                    self.generate_pdf(
                        'TEST 006 - /post/',
                        'USUARIO PRODUCTOR',
                        'PUBLICACION 6 DE PRODUCTO CREADA'
                    )

                    STATUS_POST = True

                    return STATUS_POST
                    

                except Exception as exc:
                    LOGGER.warning(exc)
                    self.set_test_properties(exc)


                

            except Exception as exc:
                LOGGER.warning(exc)

                self.set_test_properties(exc)
                pass
            
            
            return STATUS_POST
   


        status_post_1_producer_user = create_post_1_producer_user()

        if status_post_1_producer_user:
            status_post_2_producer_user = create_post_2_producer_user()

            if status_post_2_producer_user:
                status_post_3_producer_user = create_post_3_producer_user()

                if status_post_3_producer_user:
                    status_post_4_producer_user = create_post_4_producer_user()

                    if status_post_4_producer_user:
                        status_post_5_producer_user = create_post_5_producer_user()

                        if status_post_5_producer_user:
                            status_post_6_producer_user = create_post_6_producer_user()

                            if status_post_6_producer_user:
                                STATUS = True

                                return STATUS

        return STATUS


test = Test()
test.set_label('')

test.run()
