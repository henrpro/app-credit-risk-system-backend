# Importações do projeto
from services.login.querys import query_get_user
from services.connections import Connections

# Importações de bibliotecas
import pandas as pd

class InsumosLogin:

    @classmethod
    def get_user(cls, database: str, username: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_user(database, username), cnx)
                return df
        except Exception as e:
            raise e