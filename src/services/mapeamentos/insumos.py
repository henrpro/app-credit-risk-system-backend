# Importações do projeto
from services.connections import Connections
from services.mapeamentos.querys import *

# Importações de bibliotecas
from sqlalchemy import text
import pandas as pd


class InsumosMapeamentos:

    # ________________________________ Mapeamento Managers ______________________________

    @classmethod
    def get_mapeamento_managers(cls, database: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_mapeamento_managers(database), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_managers_sem_mapeamento(cls, database: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_managers_sem_mapeamento(database), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def execute_insert_mapeamento_manager(cls, database: str, manager: str, mesa: str):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_insert_mapeamento_manager(database, manager, mesa)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

    @classmethod
    def execute_delete_mapeamento_manager(cls, database: str, manager: str):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_delete_mapeamento_manager(database, manager)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()


    # ________________________________ Mapeamento Tipo Produto ______________________________

    @classmethod
    def get_mapeamento_produtos(cls, database: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_mapeamento_produtos(database), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_produtos_sem_mapeamento(cls, database: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_produtos_sem_mapeamento(database), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def execute_insert_mapeamento_produto(cls, database: str, cd_produto_oc3: str, ic_captura: int):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_insert_mapeamento_produto(database, cd_produto_oc3, ic_captura)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

    @classmethod
    def execute_delete_mapeamento_produto(cls, database: str, cd_produto_oc3: str):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_delete_mapeamento_produto(database, cd_produto_oc3)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()


    # ________________________________ Mapeamento Ativo Consumo ______________________________

    @classmethod
    def get_mapeamento_ativos(cls, database: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_mapeamento_ativos(database), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_ativos_sem_mapeamento(cls, database: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_ativos_sem_mapeamento(database), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def execute_insert_mapeamento_ativo(cls, database: str, cd_ticker: str, id_emissor: int, id_emissor_consumo: int, vl_pc_consumo: float):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_insert_mapeamento_ativo(database, cd_ticker, id_emissor, id_emissor_consumo, vl_pc_consumo)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

    @classmethod
    def execute_delete_mapeamento_ativo(cls, database: str, cd_ticker: str):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_delete_mapeamento_ativo(database, cd_ticker)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

    @classmethod
    def get_emissores_cadastrados(cls, database: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_emissores_cadastrados(database), cnx)
                return df
        except Exception as e:
            raise e
