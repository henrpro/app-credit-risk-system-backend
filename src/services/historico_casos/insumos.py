# Importações do projeto
from services.historico_casos.querys import *
from services.connections import Connections

# Importações de bibliotecas
import pandas as pd


class InsumosHistoricoCasos:

    # _______________________________ Geral _______________________________

    @classmethod
    def get_solicitacoes_finalizadas(cls, database: str, mesa: str) -> pd.DataFrame:
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_solicitacoes_finalizadas(database, mesa), cnx)
                df = df.where(pd.notnull(df), None)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_solicitacao_cabecalho(cls, database: str, id_solicitacao: int) -> pd.DataFrame:
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_solicitacao_cabecalho(database, id_solicitacao), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_descricao_solicitacao(cls, database: str, id_solicitacao: int) -> pd.DataFrame:
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_descricao_solicitacao(database, id_solicitacao), cnx)
                return df
        except Exception as e:
            raise e
