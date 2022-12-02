



import os

for obj in os.scandir(os.getcwd()):
    
    if obj.name[-2:] == 'ui':
        file = obj.name[:-2]
        file_ui = obj.name
        file_py = file + 'py'

        os.system(
            f'python -m PyQt5.uic.pyuic -x {file_ui} -o {file_py}'
        )
        print(f'Archivo {file_py} generado.')
