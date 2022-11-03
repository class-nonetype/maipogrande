import os
import platform

SYSTEM = platform.system()

REQUIREMENTS = [
    'Django',
    'Pillow',
    'djangorestframework',
    'numpy'
]

EXCEPTIONS = []

PROJECT_DIRECTORY_PATH = os.getcwd()

index = 0

for requirement in REQUIREMENTS:
    index +=1

    print(f'\n[ {index} | {len(REQUIREMENTS)} ]\tInstalling {requirement}...\n')

    try:
        if SYSTEM == 'Windows':

            MYSITE_DIRECTORY_PATH = PROJECT_DIRECTORY_PATH + '\\' + 'mysite'
            MAIPOGRANDE_DIRECTORY_PATH = MYSITE_DIRECTORY_PATH + '\\' + 'maipogrande'
            MANAGE_FILE_PATH = MYSITE_DIRECTORY_PATH + '\\' + 'manage.py'

            os.system(f'pip install {requirement} && cls')
        
        elif SYSTEM == 'Linux':

            MYSITE_DIRECTORY_PATH = PROJECT_DIRECTORY_PATH + '/' + 'mysite'
            MAIPOGRANDE_DIRECTORY_PATH = MYSITE_DIRECTORY_PATH + '/' + 'maipogrande'
            MANAGE_FILE_PATH = MYSITE_DIRECTORY_PATH + '/' + 'manage.py'

            os.system(f'pip3 install {requirement} && clear')
            
    except Exception as exc:
        EXCEPTIONS.append(exc)
        pass

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

print(LOGO)

for value in PROPERTY.values():

    if SYSTEM == 'Windows':
        os.system(f'''python "{value['manage']}" runserver''')
    
    elif SYSTEM == 'Linux':
        os.system(f'''python3 "{value['manage']}" runserver''')
