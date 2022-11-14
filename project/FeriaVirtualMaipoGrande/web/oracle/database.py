import cx_Oracle

cx_Oracle.init_oracle_client(
    lib_dir = r'/opt/oracle/instantclient_21_4'
)


class OracleDatabase:
    def __init__(self):
        self.connection = cx_Oracle.connect(
            'admin/1q2w3e4r5tt@oracle.c81tzrvyie2p.us-east-1.rds.amazonaws.com:1521/ORCL'
        )
        self.cursor = self.connection.cursor()
        self.version = cx_Oracle.version
