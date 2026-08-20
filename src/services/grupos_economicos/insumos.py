# Importações do projeto
from src.services.grupos_economicos.querys import query_get_emissores_crims
from services.grupos_economicos.querys import *
from services.connections import Connections

# Importações de bibliotecas
import pandas as pd

class InsumosGruposEconomicos:

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
    def get_grupos_economicos_distintos(cls, database: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_grupos_economicos_distintos(database), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_codigo_emissor_oc3(cls, emissor: str):
        try:
            with Connections.get_cnx_select('Athena') as cnx:
                df = pd.read_sql(query_get_emissores_oc3(emissor), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_codigo_emissor_crims(cls, emissor: str):
        try:
            with Connections.get_cnx_select('Athena') as cnx:
                df = pd.read_sql(query_get_codigo_emissor_crims(emissor), cnx)
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

    @classmethod
    def get_emissores_oc3_by_emissor(cls, database: str, id_emissor: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_emissores_oc3(database, id_emissor), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_emissores_crims_by_emissor(cls, database: str, id_emissor: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_emissores_crims(database, id_emissor), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_ativos_consumo(cls, database: str, id_emissor: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_ativos_consumo(database, id_emissor), cnx)
                return df
        except Exception as e:
            raise e