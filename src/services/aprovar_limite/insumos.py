# Importações do projeto
from services.aprovar_limite.querys import *
from services.connections import Connections

# Importações de bibliotecas
from sqlalchemy import text
from typing import List
import pandas as pd


class InsumosAprovarLimite:

    # _______________________________ Geral _______________________________

    @classmethod
    def get_aprovacoes_pendentes(cls, database: str) -> pd.DataFrame:
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_aprovacoes_pendentes(database), cnx)
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
    def get_ratings_distintos(cls, database: str) -> pd.DataFrame:
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_ratings_distintos(database), cnx)
                return df
        except Exception as e:
            raise e

    @classmethod
    def get_max_id_limite(cls, database: str) -> int:
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_max_id_limite(database), cnx)
                return int(df['max_id'].iloc[0]) if not df.empty and pd.notna(df['max_id'].iloc[0]) else 0
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

    @classmethod
    def get_flexibilizacao_consumo_grupo(cls, database: str, id_grupo: int) -> pd.DataFrame:
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_flexibilizacao_consumo_grupo(database, id_grupo), cnx)
                return df
        except Exception as e:
            raise e

    # _______________________________ Execução SQL _______________________________

    @classmethod
    def execute_rejeitar_solicitacoes(cls, database: str, ids_solicitacao: List[int], id_status: int = 6):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                for id_sol in ids_solicitacao:
                    cnx.execute(text(query_update_status_solicitacao(database, id_sol, id_status)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

    @classmethod
    def execute_efetivar_aprovacao_transacional(
        cls,
        database: str,
        ids_solicitacao: List[int],
        id_grupo: int,
        mesas: List[str],
        limites_historico_params: List[dict],
        limites_vigentes_params: List[dict],
        rating_grupo_params: dict,
        ratings_emissores_params: List[dict],
        flexibilizacao_params: List[dict],
        remover_flexibilizacao_anterior: bool = False
    ):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                # 1. Atualiza o status das solicitações para 4 (Aprovado)
                for id_sol in ids_solicitacao:
                    cnx.execute(text(query_update_status_solicitacao(database, id_sol, 4)))

                # 2. Inserção nas tabelas de histórico
                for item in limites_historico_params:
                    cnx.execute(text(query_insert_limite_aprovado_historico(
                        database=database,
                        id_solicitacao=item['idSolicitacao'],
                        id_limite=item['idLimite'],
                        cd_mesa=item['cdMesa'],
                        id_grupo=item['idGrupo'],
                        id_emissor=item['idEmissor'],
                        vl_prazo=item['vlPrazo'],
                        vl_terceiros=item['vlTerceiros'],
                        vl_reserva_tecnica=item['vlReservaTecnica'],
                        ic_runoff=item['icRunOff'],
                        dt_aprovacao=item['dtAprovacao'],
                        dt_vencimento=item['dtVencimento'],
                        ic_limite_meta=item['icLimiteMeta']
                    )))

                if rating_grupo_params:
                    cnx.execute(text(query_insert_rating_grupo_historico(
                        database=database,
                        id_solicitacao=rating_grupo_params['idSolicitacao'],
                        id_grupo=rating_grupo_params['idGrupo'],
                        cd_rating_grupo=rating_grupo_params['cdRatingGrupo'],
                        dt_aprovacao=rating_grupo_params['dtAprovacao'],
                        dt_vencimento=rating_grupo_params['dtVencimento']
                    )))

                for item in ratings_emissores_params:
                    cnx.execute(text(query_insert_rating_emissor_historico(
                        database=database,
                        id_solicitacao=item['idSolicitacao'],
                        id_emissor=item['idEmissor'],
                        cd_rating=item['cdRating'],
                        dt_aprovacao=item['dtAprovacao'],
                        dt_vencimento=item['dtVencimento']
                    )))

                # 3. Limpeza e inserção das tabelas vigentes
                for mesa in mesas:
                    cnx.execute(text(query_delete_limites_vigentes_by_grupo_mesa(database, id_grupo, mesa)))

                for item in limites_vigentes_params:
                    cnx.execute(text(query_insert_limite_vigente(
                        database=database,
                        id_solicitacao=item['idSolicitacao'],
                        id_limite=item['idLimite'],
                        cd_mesa=item['cdMesa'],
                        id_grupo=item['idGrupo'],
                        id_emissor=item['idEmissor'],
                        vl_prazo=item['vlPrazo'],
                        vl_terceiros=item['vlTerceiros'],
                        vl_reserva_tecnica=item['vlReservaTecnica'],
                        ic_runoff=item['icRunOff'],
                        dt_aprovacao=item['dtAprovacao'],
                        dt_vencimento=item['dtVencimento'],
                        ic_limite_meta=item['icLimiteMeta']
                    )))

                cnx.execute(text(query_delete_rating_vigente_grupo(database, id_grupo)))
                if rating_grupo_params:
                    cnx.execute(text(query_insert_rating_vigente_grupo(
                        database=database,
                        id_solicitacao=rating_grupo_params['idSolicitacao'],
                        id_grupo=rating_grupo_params['idGrupo'],
                        cd_rating_grupo=rating_grupo_params['cdRatingGrupo'],
                        dt_aprovacao=rating_grupo_params['dtAprovacao'],
                        dt_vencimento=rating_grupo_params['dtVencimento']
                    )))

                cnx.execute(text(query_delete_ratings_vigentes_emissores_grupo(database, id_grupo)))
                for item in ratings_emissores_params:
                    cnx.execute(text(query_insert_rating_vigente_emissor(
                        database=database,
                        id_solicitacao=item['idSolicitacao'],
                        id_emissor=item['idEmissor'],
                        cd_rating=item['cdRating'],
                        dt_aprovacao=item['dtAprovacao'],
                        dt_vencimento=item['dtVencimento']
                    )))

                # 4. Tratamento da flexibilização de consumo
                if remover_flexibilizacao_anterior:
                    cnx.execute(text(query_delete_flexibilizacao_consumo_grupo(database, id_grupo)))

                for item in flexibilizacao_params:
                    cnx.execute(text(query_insert_flexibilizacao_consumo(
                        database=database,
                        cd_mesa=item['cdMesa'],
                        id_emissor=item['idEmissor'],
                        vl_prazo=item['vlPrazo'],
                        vl_flexibilizado=item['vlFlexibilizado'],
                        vl_limite=item['vlLimite']
                    )))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()
