from database import OracleDatabase

import os


ORACLE_DATABASE = OracleDatabase()



SCRIPTS_DIRECTORY = os.getcwd() + '/scripts'

if not os.path.exists(SCRIPTS_DIRECTORY):
    os.mkdir(SCRIPTS_DIRECTORY)

print(ORACLE_DATABASE.connection)
print(ORACLE_DATABASE.cursor)
print(ORACLE_DATABASE.version)



SELECT_ALL_TABLES = '''

SELECT table_name, column_name
FROM cols
WHERE table_name LIKE 'MAIPOGRANDE%'

'''







for file in os.scandir(SCRIPTS_DIRECTORY):

    with open(f'{file.path}', 'r') as script:
        ORACLE_DATABASE.cursor.execute(script.read())
        ROWS = ORACLE_DATABASE.cursor.fetchall()
        for row in ROWS:
            print(row)
    script.close()