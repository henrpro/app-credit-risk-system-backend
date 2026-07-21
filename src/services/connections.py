# Importações de bibliotecas
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
import pyodbc

pyodbc.pooling = False

class Connections:

    @staticmethod
    def get_driver():
        driver_found = False
        for driver in pyodbc.drivers():
            if driver.startswith('ODBC Driver'):
                user_driver = driver
                driver_found = True
                break

        if not driver_found:
            raise Exception('Nenhum driver ODBC encontrado.')
        else:
            return user_driver
        
    @staticmethod
    def get_cnx_select(database: str) -> pyodbc.Connection:
        """
        Retorna a conexão com o banco de dados de leitura.
        """
        driver = Connections.get_driver()
        cnx = pyodbc.connect(f'DRIVER={{{driver}}};SERVER=HENRIQUE\SQLEXPRESS;DATABASE={{{database}}};Trusted_Connection=yes;')

        return cnx
    
    @staticmethod
    def get_cnx_insert(database: str) -> pyodbc.Connection:
        """
        Retorna a conexão com o banco de dados de escrita.
        """
        driver = Connections.get_driver()
        url_db = URL.create(
            drivername='mssql+pyodbc',
            query={"odbc_connect": f"DRIVER={{{driver}}};SERVER=HENRIQUE\SQLEXPRESS;DATABASE={{{database}}};Trusted_Connection=yes;"}
        )
        engine = create_engine(url_db, fast_executemany=False, echo=False)

        return engine, engine.connect()
