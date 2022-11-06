import os
import platform



EXCEPTIONS = []

PROJECT_DIRECTORY_PATH = os.getcwd()

MYSITE_DIRECTORY_PATH = PROJECT_DIRECTORY_PATH + '/' + 'mysite'
MAIPOGRANDE_DIRECTORY_PATH = MYSITE_DIRECTORY_PATH + '/' + 'maipogrande'
MANAGE_FILE_PATH = MYSITE_DIRECTORY_PATH + '/' + 'manage.py'

PROPERTY = {
    'project' : {
        'path' : PROJECT_DIRECTORY_PATH,
        'mysite' : MYSITE_DIRECTORY_PATH,
        'maipogrande' : MAIPOGRANDE_DIRECTORY_PATH,
        'manage' : MANAGE_FILE_PATH
    }
}

LOGO = '''
========================================================================================
______  ___      _____                    _________                    _________     
___   |/  /_____ ___(_)_____________      __  ____/____________ _____________  /____ 
__  /|_/ /_  __ `/_  /___  __ \  __ \     _  / __ __  ___/  __ `/_  __ \  __  /_  _ \\
_  /  / / / /_/ /_  / __  /_/ / /_/ /     / /_/ / _  /   / /_/ /_  / / / /_/ / /  __/
/_/  /_/  \__,_/ /_/  _  .___/\____/      \____/  /_/    \__,_/ /_/ /_/\__,_/  \___/ 
                      /_/                                                            
                      
========================================================================================
'''


for value in PROPERTY.values():
    print(LOGO)
    os.system(f'''python3 "{value['manage']}" makemigrations maipogrande''')
    os.system('cls')
    
    print(LOGO)
    os.system(f'''python3 "{value['manage']}" migrate''')
    os.system('cls')

    print(LOGO)
    os.system(f'''python3 "{value['manage']}" runserver 0:8000''')
    os.system('cls')
