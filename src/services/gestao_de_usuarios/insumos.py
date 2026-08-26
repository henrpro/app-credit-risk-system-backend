# Importações do projeto
from services.gestao_de_usuarios.querys import *
from services.connections import Connections

# Importações de bibliotecas
from sqlalchemy import text
import pandas as pd


class InsumosGestaoUsuarios:

    # _______________________________ Geral _______________________________

    @classmethod
    def get_usuarios_cadastrados(cls, database: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_usuarios_cadastrados(database), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_usuario(cls, database: str, user: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_usuario(database, user), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_id_profile(cls, database: str, profile: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_id_profile(database, profile), cnx)
                return int(df['idProfile'].iloc[0]) if not df.empty else None
        except Exception as e:
            raise e

    # _______________________________ Execução SQL _______________________________

    @classmethod
    def execute_insert_usuario(cls, database: str, user: str, nome: str, password: str, idprofile: int, aprovador: str = None, peso: float = None):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_insert_usuario(database, user, nome, password, idprofile, aprovador, peso)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

    @classmethod
    def execute_delete_usuario(cls, database: str, user: str):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_delete_usuario(database, user)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()
