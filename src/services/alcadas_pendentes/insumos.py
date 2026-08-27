# Importações do projeto
from services.alcadas_pendentes.querys import *
from services.connections import Connections

# Importações de bibliotecas
from sqlalchemy import text
from typing import List
import pandas as pd


class InsumosAlcadasPendentes:

    # _______________________________ Geral _______________________________

    @classmethod
    def get_alcadas_pendentes(cls, database: str) -> pd.DataFrame:
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_alcadas_pendentes(database), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_solicitacao_cabecalho(cls, database: str, ids_solicitacao: List[int]) -> pd.DataFrame:
        try:
            ids_str = ", ".join(str(i) for i in ids_solicitacao)
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_solicitacao_cabecalho(database, ids_str), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_detalhes_solicitacao_descricao(cls, database: str, ids_solicitacao: List[int]) -> pd.DataFrame:
        try:
            ids_str = ", ".join(str(i) for i in ids_solicitacao)
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_detalhes_solicitacao_descricao(database, ids_str), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_limites_vigentes_grupo(cls, database: str, grupo: str) -> pd.DataFrame:
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_limites_vigentes_grupo(database, grupo), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_ratings_vigentes(cls, database: str, grupo: str) -> pd.DataFrame:
        try:
            with Connections.get_cnx_select(database) as cnx:
                df_grupo = pd.read_sql(query_get_ratings_vigentes_grupo(database, grupo), cnx)
                df_emissores = pd.read_sql(query_get_ratings_vigentes_emissores(database, grupo), cnx)
                df_consolidado = pd.concat([df_grupo, df_emissores], ignore_index=True)
                return df_consolidado
        except Exception as e:
            raise e

    # _______________________________ Execução SQL _______________________________

    @classmethod
    def execute_responder_alcada(
        cls,
        database: str,
        ids_solicitacao: List[int],
        ds_alcada: str,
        dt_resposta: str,
        cd_user_resposta: str,
        id_status: int = 2
    ):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                for id_sol in ids_solicitacao:
                    cnx.execute(text(query_insert_resposta_alcada(database, id_sol, ds_alcada, dt_resposta, cd_user_resposta)))
                    cnx.execute(text(query_update_status_solicitacao(database, id_sol, id_status)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()
