# Importações do projeto
from services.solicitar_alcada.querys import *
from services.connections import Connections

# Importações de bibliotecas
from sqlalchemy import text
import pandas as pd


class InsumosSolicitarAlcada:

    # _______________________________ Geral _______________________________

    @classmethod
    def get_id_grupo_by_name(cls, database: str, grupo: str) -> int:
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_id_grupo_by_name(database, grupo), cnx)
                return int(df['idGrupo'].iloc[0]) if not df.empty else None
        except Exception as e:
            raise e

    @classmethod
    def get_emissor_by_name(cls, database: str, emissor: str) -> int:
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_emissor_by_name(database, emissor), cnx)
                return int(df['idEmissor'].iloc[0]) if not df.empty else None
        except Exception as e:
            raise e

    @classmethod
    def get_eventos_possiveis(cls, database: str) -> pd.DataFrame:
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_eventos_possiveis(database), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_ratings_distintos(cls, database: str) -> pd.DataFrame:
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_ratings_distintos(database), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_limites_aprovados_by_grupo(cls, database: str, grupo: str, mesa: str) -> pd.DataFrame:
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_limites_aprovados_by_grupo(database, grupo, mesa), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_max_id_solicitacao(cls, database: str) -> int:
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_max_id_solicitacao(database), cnx)
                return int(df['max_id'].iloc[0]) if not df.empty else 0
        except Exception as e:
            raise e

    @classmethod
    def get_prorrogacoes_recentes(cls, database: str, grupo: str, mesa: str) -> pd.DataFrame:
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_prorrogacoes_recentes(database, grupo, mesa), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_disponivel_flexibilizacao(cls, database: str, grupo: str, mesa: str) -> pd.DataFrame:
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_disponivel_flexibilizacao(database, grupo, mesa), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_solicitacao_cabecalho_by_id(cls, database: str, id_solicitacao: int) -> pd.DataFrame:
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_solicitacao_cabecalho_by_id(database, id_solicitacao), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_solicitacao_descricao_by_id(cls, database: str, id_solicitacao: int) -> pd.DataFrame:
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_solicitacao_descricao_by_id(database, id_solicitacao), cnx)
                return df
        except Exception as e:
            raise e

    # _______________________________ Execução SQL _______________________________

    @classmethod
    def execute_insert_solicitacao_completa(
        cls,
        database: str,
        solicitacao_params: dict,
        linhas_descricao_params: list
    ):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_insert_solicitacao_alcada(
                    database=database,
                    id_solicitacao=solicitacao_params['idSolicitacao'],
                    dt_solicitacao=solicitacao_params['dtSolicitacao'],
                    cd_user=solicitacao_params['cdUser'],
                    cd_mesa=solicitacao_params['cdMesa'],
                    id_grupo=solicitacao_params['idGrupo'],
                    cd_rating_grupo=solicitacao_params['cdRatingGrupo'],
                    vl_share_divida=solicitacao_params['vlShareDivida'],
                    id_status=solicitacao_params['idStatus'],
                    ds_tipo_evento=solicitacao_params['dsTipoEvento']
                )))

                for item in linhas_descricao_params:
                    cnx.execute(text(query_insert_solicitacao_alcada_descricao(
                        database=database,
                        id_solicitacao=item['idSolicitacao'],
                        id_emissor=item['idEmissor'],
                        cd_rating=item['cdRating'],
                        vl_prazo=item['vlPrazo'],
                        vl_terceiros=item['vlTerceiros'],
                        vl_reserva_tecnica=item['vlReservaTecnica'],
                        ic_runoff=item['icRunOff'],
                        vl_share_divida=item['vlShareDivida'],
                        ic_limite_meta=item['icLimiteMeta'],
                        dt_vencimento_limite_meta=item['dtVencimentoLimiteMeta']
                    )))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

    @classmethod
    def execute_update_solicitacao_completa(
        cls,
        database: str,
        id_solicitacao: int,
        solicitacao_params: dict,
        linhas_descricao_params: list
    ):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                # 1. Deleta respostas anteriores se houverem
                cnx.execute(text(query_delete_solicitacao_alcada_resposta(
                    database=database,
                    id_solicitacao=id_solicitacao
                )))

                # 2. Deleta linhas de descrição antigas
                cnx.execute(text(query_delete_solicitacao_alcada_descricao(
                    database=database,
                    id_solicitacao=id_solicitacao
                )))

                # 3. Deleta cabeçalho antigo
                cnx.execute(text(query_delete_solicitacao_alcada_cabecalho(
                    database=database,
                    id_solicitacao=id_solicitacao
                )))

                # 4. Reinserção do cabeçalho com o mesmo idSolicitacao e idStatus = 1
                cnx.execute(text(query_insert_solicitacao_alcada(
                    database=database,
                    id_solicitacao=id_solicitacao,
                    dt_solicitacao=solicitacao_params['dtSolicitacao'],
                    cd_user=solicitacao_params['cdUser'],
                    cd_mesa=solicitacao_params['cdMesa'],
                    id_grupo=solicitacao_params['idGrupo'],
                    cd_rating_grupo=solicitacao_params['cdRatingGrupo'],
                    vl_share_divida=solicitacao_params['vlShareDivida'],
                    id_status=1,
                    ds_tipo_evento=solicitacao_params['dsTipoEvento']
                )))

                # 5. Reinserção das linhas com o mesmo idSolicitacao
                for item in linhas_descricao_params:
                    cnx.execute(text(query_insert_solicitacao_alcada_descricao(
                        database=database,
                        id_solicitacao=id_solicitacao,
                        id_emissor=item['idEmissor'],
                        cd_rating=item['cdRating'],
                        vl_prazo=item['vlPrazo'],
                        vl_terceiros=item['vlTerceiros'],
                        vl_reserva_tecnica=item['vlReservaTecnica'],
                        ic_runoff=item['icRunOff'],
                        vl_share_divida=item['vlShareDivida'],
                        ic_limite_meta=item['icLimiteMeta'],
                        dt_vencimento_limite_meta=item['dtVencimentoLimiteMeta']
                    )))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

