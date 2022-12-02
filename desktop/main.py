


import sys
import os



from PyQt5.QtWidgets import QApplication
from app.controllers.controller import Controller


qApp = QApplication(sys.argv)


environment = {
    'controller' : Controller(),
    'model' : Controller().Model,
    'view' : Controller().View
}




def check_session_model_file():



    if environment['model'].EnvironmentModel.attr['system']['os'] == 'Windows':
        session_model_python_file_path = environment['model'].EnvironmentModel.attr['path']['models'] + '\\session_model.py'

    elif environment['model'].EnvironmentModel.system == 'Linux':
        session_model_python_file_path = environment['model'].EnvironmentModel.attr['path']['models'] + '/session_model.py'

    
    if os.path.exists(session_model_python_file_path):
        try:
            from app.models.session_model import SessionModel

            session_model = SessionModel()

            return environment['controller'].set_user_session(
                    session_model.username,
                    session_model.password
            )
            
        except Exception as exc:

            os.remove(f'''{session_model_python_file_path}''')

            return environment['controller'].login_window_view()

                

    else:
        return environment['controller'].login_window_view()



check_session_model_file()
sys.exit(qApp.exec_())