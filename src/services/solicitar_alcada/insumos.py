# Importações do projeto
from services.solicitar_alcada.querys import *
from services.connections import Connections

# Importações de bibliotecas
from sqlalchemy import text
import pandas as pd


class InsumosSolicitarAlcada:

    # _______________________________ Geral _______________________________

    @classmethod
    def get_eventos_possiveis(cls, database: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_eventos_possiveis(database), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_ratings_distintos(cls, database: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_ratings_distintos(database), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_limites_aprovados_by_grupo(cls, database: str, grupo: str, mesa: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_limites_aprovados_by_grupo(database, grupo, mesa), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_max_id_solicitacao(cls, database: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_max_id_solicitacao(database), cnx)
                return int(df['max_id'].iloc[0]) if not df.empty else 0
        except Exception as e:
            raise e

    @classmethod
    def get_prorrogacoes_recentes(cls, database: str, grupo: str, mesa: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_prorrogacoes_recentes(database, grupo, mesa), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_disponivel_flexibilizacao(cls, database: str, grupo: str, mesa: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_disponivel_flexibilizacao(database, grupo, mesa), cnx)
                return df
        except Exception as e:
            raise e

    # _______________________________ Insert _______________________________

    @classmethod
    def execute_insert_solicitacao_alcada(cls, database: str, id_solicitacao: int, dt_solicitacao: str, cd_user: str, ds_profile: str, id_grupo: int, id_rating_grupo: int, vl_share_divida: float, id_status: int, id_tipo_evento: int):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_insert_solicitacao_alcada(database, id_solicitacao, dt_solicitacao, cd_user, ds_profile, id_grupo, id_rating_grupo, vl_share_divida, id_status, id_tipo_evento)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

    @classmethod
    def execute_insert_solicitacao_alcada_descricao(cls, database: str, id_solicitacao: int, id_emissor: int, id_rating: int, vl_prazo: float, vl_terceiros: float, vl_reserva_tecnica: float, ic_runoff: int, vl_share_divida: float):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_insert_solicitacao_alcada_descricao(database, id_solicitacao, id_emissor, id_rating, vl_prazo, vl_terceiros, vl_reserva_tecnica, ic_runoff, vl_share_divida)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

    @classmethod
    def execute_insert_solicitacao_alcada_limite_meta_descricao(cls, database: str, id_solicitacao: int, id_emissor: int, id_rating: int, vl_prazo: float, vl_terceiros: float, vl_reserva_tecnica: float, ic_runoff: int, vl_share_divida: float, dt_vencimento_limite_meta: str):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_insert_solicitacao_alcada_limite_meta_descricao(database, id_solicitacao, id_emissor, id_rating, vl_prazo, vl_terceiros, vl_reserva_tecnica, ic_runoff, vl_share_divida, dt_vencimento_limite_meta)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()
