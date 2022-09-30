import os
import platform

SYSTEM = platform.system()

REQUIREMENTS = [
    'Django',
    'Pillow',
    'djangorestframework'
]

EXCEPTIONS = [

]

index = 0
import_status = False

for r in REQUIREMENTS:
    index +=1

    if SYSTEM == 'Windows':
        os.system('cls')

    elif SYSTEM == 'Linux':
        os.system('clear')

    print(f'\n[ {index} / {len(REQUIREMENTS)} ]\tInstalling {r}...\n')

    try:
        os.system(f'pip install {r}')
        import_status = True
    
    except Exception as exc:
        EXCEPTIONS.append(exc)


    if index == len(REQUIREMENTS):
        print(f'\n[ {import_status} ]\tRequirements\n')



PROJECT_DIRECTORY_PATH = os.getcwd()

if SYSTEM == 'Windows':
    MYSITE_DIRECTORY_PATH = PROJECT_DIRECTORY_PATH + '\\' + 'mysite'
    MAIPOGRANDE_DIRECTORY_PATH = MYSITE_DIRECTORY_PATH + '\\' + 'maipogrande'
    MANAGE_FILE_PATH = MYSITE_DIRECTORY_PATH + '\\' + 'manage.py'

elif SYSTEM == 'Linux':
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

for value in PROPERTY.values():

    if SYSTEM == 'Windows':
        os.system(f'''python {value['manage']} runserver''')
    
    elif SYSTEM == 'Linux':
        os.system(f'''python3 "{value['manage']}" runserver''')
