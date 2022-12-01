
import os
import platform
import socket
import shutil
import time



###################################################################
#   Logo                                                          #
###################################################################

logo = '''
                ______  ___      _____                    _________                    _________          
                ___   |/  /_____ ___(_)_____________      __  ____/____________ _____________  /____      
                __  /|_/ /_  __ `/_  /___  __ \  __ \     _  / __ __  ___/  __ `/_  __ \  __  /_  _ \\     
                _  /  / / / /_/ /_  / __  /_/ / /_/ /     / /_/ / _  /   / /_/ /_  / / / /_/ / /  __/     
                /_/  /_/  \__,_/ /_/  _  .___/\____/      \____/  /_/    \__,_/ /_/ /_/\__,_/  \___/      
                                      /_/                                                                 

                                                                  PROYECTO FERIA VIRTUAL MAIPO GRANDE
                                                            https://www.github.com/doqqio/maipogrande      
                                                                                          Version 2.5                      
'''


###################################################################
#   Clase Model     Contenedora  de los atributos del entorno     #
###################################################################

class Model:

    attr = {}

    def set_attr(self, **kwargs):
        self.attr.update(kwargs)

        return self.attr


    def get_attr(self) -> dict:

        return self.attr


###################################################################
#   Ruta de ejecucion                                             #
###################################################################

execution_path : str = os.getcwd()

###################################################################
#   Sistema operativo del entorno                                 #
###################################################################

platform_system = platform.system()

###################################################################
#   Ruta de proyecto                                              #
###################################################################

django_web_directory_path : str =\
    execution_path + '\\' + 'web' +'\\' + 'mysite'

django_web_mysite_directory_path : str =\
    django_web_directory_path + '\\' + 'mysite'

django_web_maipogrande_directory_path : str =\
    django_web_directory_path + '\\' + 'maipogrande'

django_web_manage_file_path : str =\
    django_web_directory_path + '\\' + 'manage.py'


###################################################################
#   Instancia de la clase Model                                   #
###################################################################

Environment = Model()

###################################################################
#   Asignacion de atributos del entorno                           #
###################################################################

Environment.set_attr(

    ###################################################################
    #   Usuario de entorno                                            #
    ###################################################################
    user = f'{socket.gethostname()}@{socket.gethostbyname(socket.gethostname())}',

    ###################################################################
    #   Sistema de ejecucion del entorno                              #
    ###################################################################
    system = {
        'os-' : platform_system
    },

    ###################################################################
    #   Rutas                                                         #
    ###################################################################
    path = {
        ###################################################################
        #   Ruta de ejecucion                                             #
        ###################################################################
        'execution' : execution_path,


        ###################################################################
        #   Ruta del proyecto de django web : web                         #
        ###################################################################

        'web' : django_web_directory_path,
        'web.mysite' : django_web_mysite_directory_path,
        'web.maipogrande' : django_web_maipogrande_directory_path,
        'web.manage' : django_web_manage_file_path,

    }


)


def print_attr():
    print(Environment.get_attr())

def print_exit():
    Environment.attr['message']['message'] = 'Conexion cerrada'

    print(f'''\n\n[ ! ]\t{Environment.attr['message']['message']}''')

def print_logo():
    print(f'''{logo}\n\n\n''')


def clear_console():
    return os.system('cls')



###################################################################
#   Instalacion de requerimientos                                 #
###################################################################

def install_requirements():
    command['clear']()
    command['print_logo']()

    requirements = [

        'djangorestframework',
        'Django',
        'Pillow',
        'xlsxwriter',
        'selenium',
        'webdriver-manager',
        'PyQt5',
        'pandas'
    ]  

    try:
        for requirement in requirements:
            return os.system(
                    f'''pip install "{requirement}" && python -m pip install --upgrade pip'''
            )

    except KeyboardInterrupt:
        print()



###################################################################
#   Django                                                        #
###################################################################

def start_django_web():
    command['clear']()
    command['print_logo']()

    try:
    
        command['makemigrations']
        command['migrate']

        return os.system(
            f'''python "{Environment.attr['path']['web.manage']}" runserver'''
        )

    except KeyboardInterrupt:
        print()


def make_migrations_django_web():
    command['clear']()
    command['print_logo']()

    try:
    
        return os.system(
            f'''python "{Environment.attr['path']['web.manage']}" makemigrations maipogrande'''
        )

    except KeyboardInterrupt:
        print()


def migrate_django_web():
    command['clear']()
    command['print_logo']()

    try:
    
        return os.system(
            f'''python "{Environment.attr['path']['web.manage']}" migrate'''
        )

    except KeyboardInterrupt:
        print()


def create_user_admin_django_web():
    command['clear']()
    command['print_logo']()

    try:
    
        return os.system(
            f'''python "{Environment.attr['path']['web.manage']}" createsuperuser'''
        )

    except KeyboardInterrupt:
        print()


def clear_project_web():
    command['clear']()
    command['print_logo']()
    
    try:
        print(f'''\n∟ [ * ]\tAnalizando ruta {Environment.attr['path']['web']}\n''')
    
        for obj in os.scandir(Environment.attr['path']['web']):
            if os.path.isdir(obj.path):
                print(f'''\t∟ [ + ]\tDirectorio encontrado {obj.path}''')
                time.sleep(0.5)
                                            
            elif os.path.isfile(obj.path):
                print(f'''\t∟ [ + ]\tArchivo encontrado {obj.path}''')
                time.sleep(0.5)
                                
                if 'db.sqlite3' == obj.name:
                    print(f'''\t\t∟ [ + ]\tArchivo {obj.name} encontrado''')

                    os.remove(f'''{Environment.attr['path']['web']}/db.sqlite3''')

                    print(
                        f'''\t\t∟ [ + ]\tArchivo {obj.name} eliminado.'''
                        f'''\n'''
                        f'''\t\t∟ [ + ]\tBase de datos {obj.name} eliminada.'''
                    )

                    time.sleep(1)

        print(f'''\n∟ [ * ]\tAnalizando ruta {Environment.attr['path']['web.maipogrande']}\n''')

        for obj in os.scandir(Environment.attr['path']['web.maipogrande']):
            if os.path.isdir(obj.path):
                print(f'''\t∟ [ + ]\tDirectorio encontrado {obj.path}''')
                time.sleep(0.5)
                                    
                if 'migrations' == obj.name:
                    print( f'''\t\t∟ [ + ]\tDirectorio encontrado {obj.name}''')

                    for _obj in os.scandir(obj.path):
                        if _obj.is_dir():
                            print(f'''\t\t\t∟ [ + ]\tDirectorio encontrado {_obj.name}''')
                        
                        elif _obj.is_file():
                            print(f'''\t\t\t∟ [ + ]\tArchivo encontrado {_obj.name}''')

                    shutil.rmtree(f'''{Environment.attr['path']['web.maipogrande']}/migrations''')

                    print(
                        f'''\t\t∟ [ + ]\tDirectorio eliminado {obj.name}'''
                        f'''\n'''
                        f'''\t\t∟ [ + ]\tDirectorio de migraciones {obj.name} eliminado.'''
                    )

                    time.sleep(0.5)
                                                
                elif '__pycache__' == obj.name:
                    print(f'''\t\t∟ [ + ]\tDirectorio encontrado {obj.name}''')

                    for _obj in os.scandir(obj.path):
                        if _obj.is_dir():
                            print(f'''\t\t\t∟ [ + ]\tDirectorio encontrado {_obj.name}''')
                        
                        elif _obj.is_file():
                            print(f'''\t\t\t∟ [ + ]\tArchivo encontrado {_obj.name}''')

                    shutil.rmtree(f'''{Environment.attr['path']['web.maipogrande']}/__pycache__''')
                    
                    print(
                        f'''\t\t∟ [ + ]\tDirectorio eliminado {obj.name}'''
                        f'''\n'''
                        f'''\t\t∟ [ + ]\tDirectorio de cache {obj.name} eliminado.'''
                    )
                    
                    time.sleep(0.5)

            elif os.path.isfile(obj.path):
                print(
                    f'''\t∟ [ + ]\tArchivo encontrado {obj.path}'''
                )

        print(f'''\n∟ [ * ]\tAnalizando ruta {Environment.attr['path']['web.mysite']}\n''')

        for obj in os.scandir(Environment.attr['path']['web.mysite']):
            if os.path.isdir(obj.path):
                print(f'''\t∟ [ + ]\tDirectorio encontrado {obj.path}''')
                time.sleep(0.5)

                if '__pycache__' == obj.name:
                    print(f'''\t\t∟ [ + ]\tDirectorio encontrado {obj.name}''')

                    for _obj in os.scandir(obj.path):
                        if _obj.is_dir():
                            print(f'''\t\t\t∟ [ + ]\tDirectorio encontrado {_obj.name}''')
                        
                        elif _obj.is_file():
                            print(f'''\t\t\t∟ [ + ]\tArchivo encontrado {_obj.name}''')

                    shutil.rmtree(f'''{Environment.attr['path']['web.mysite']}/__pycache__''')

                    print(f'''\t\t∟ [ + ]\tDirectorio eliminado {obj.name}''')

                    time.sleep(0.5)

                elif os.path.isfile(obj.path):
                    print(f'''\t∟ [ + ]\tArchivo encontrado {obj.path}''')
                    
    except KeyboardInterrupt:
        print()





def init():
    command['clear']()
    command['print_logo']()
    command['install']()

    command['clear']()
    command['print_logo']()
    command['reset-web']()

    command['clear']()
    command['print_logo']()
    command['makemigrations']()

    command['clear']()
    command['print_logo']()
    command['migrate']()
    
    command['clear']()
    command['print_logo']()
    command['create-admin']()

    command['clear']()
    command['print_logo']()
    command['start-web']()



###################################################################




command = {
    'print_logo' : print_logo,
    'print_attr' : print_attr,
    'print_exit' : print_exit,
    'clear' : clear_console,

    'start-web' : start_django_web,
    'reset-web' : clear_project_web,

    'makemigrations' : make_migrations_django_web,
    'migrate' : migrate_django_web,
    'create-admin' : create_user_admin_django_web,

    'install' : install_requirements,

    'init' : init,
}


Environment.set_attr(
    command = command
)

execution = True


def main():
    Environment.attr['command']['install']()

    Environment.attr['command']['clear']()
    Environment.attr['command']['print_logo']()

    try:
        
        while execution:

            user_input = str(input(f'''{Environment.attr['user']}\t> '''))

            for key in Environment.attr['command'].keys():

                if user_input == key:
                    Environment.attr['command'][user_input]()

            else:
                pass


    except KeyboardInterrupt:
        print_exit()


if __name__ == '__main__':
    main()
    