# Importações do projeto
from services.consultar_solicitacao.querys import *
from services.connections import Connections

# Importações de bibliotecas
from sqlalchemy import text
import pandas as pd


class InsumosConsultarSolicitacao:

    # _______________________________ Geral _______________________________

    @classmethod
    def get_solicitacoes_pendentes(cls, database: str, mesa: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_solicitacoes_pendentes(database, mesa), cnx)
                df = df.where(pd.notnull(df), None)
                return df
        except Exception as e:
            raise e

    # _______________________________ Update _______________________________

    @classmethod
    def execute_update_status_aprovacao_pendente(cls, database: str, id_solicitacao: int):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(update_status_aprovacao_pendente(database, id_solicitacao)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()
