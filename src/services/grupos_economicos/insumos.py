# Importações do projeto
from services.grupos_economicos.querys import *
from services.connections import Connections

# Importações de bibliotecas
import pandas as pd

class InsumosGruposEconomicos:

    @classmethod
    def get_grupos_economicos_distintos(cls, database: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_grupos_economicos_distintos(database), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_setores_distintos(cls, database: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_setores_distintos(database), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_subsetores_distintos(cls, database: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_subsetores_distintos(database), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_grupo_economico(cls, database: str, grupo: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_grupo_economico(database, grupo), cnx)
                return df
        except Exception as e:
            raise e