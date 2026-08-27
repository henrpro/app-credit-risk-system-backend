# Importações do projeto
from services.grupos_economicos.querys import *
from services.connections import Connections

# Importações de bibliotecas
from sqlalchemy import text
import pandas as pd


class InsumosGruposEconomicos:

    # _______________________________ Geral _______________________________

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
    def get_id_setor_by_name(cls, database: str, ds_setor: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_id_setor_by_name(database, ds_setor), cnx)
                return int(df['idSetor'].iloc[0]) if not df.empty else None
        except Exception as e:
            raise e


    @classmethod
    def get_id_grupo_by_name(cls, database: str, ds_grupo: str, exclude_id: int = None):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_id_grupo_by_name(database, ds_grupo, exclude_id), cnx)
                return int(df['idGrupo'].iloc[0]) if not df.empty else None
        except Exception as e:
            raise e

    @classmethod
    def get_emissor_by_name(cls, database: str, ds_emissor: str, exclude_id: int = None):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_id_emissor_by_name(database, ds_emissor, exclude_id), cnx)
                return int(df['idEmissor'].iloc[0]) if not df.empty else None
        except Exception as e:
            raise e

    @classmethod
    def get_max_id_grupo(cls, database: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_max_id_grupo(database), cnx)
                return int(df['max_id'].iloc[0]) if not df.empty else 0
        except Exception as e:
            raise e

    @classmethod
    def get_max_id_emissor(cls, database: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_max_id_emissor(database), cnx)
                return int(df['max_id'].iloc[0]) if not df.empty else 0
        except Exception as e:
            raise e

    # _______________________________ Cadastrar Grupo _______________________________

    @classmethod
    def get_codigo_emissor_oc3(cls, emissor: str):
        try:
            with Connections.get_cnx_select('Athena') as cnx:
                df = pd.read_sql(query_get_codigo_emissor_oc3(emissor), cnx)
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
    def execute_insert_grupo_economico(cls, database: str, id_grupo: int, ds_grupo: str):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_insert_grupo_economico(database, id_grupo, ds_grupo)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

    @classmethod
    def execute_insert_emissor(cls, database: str, id_emissor: int, cd_cnpj: str, ds_emissor: str, ic_holding: int, ic_consome_holding: int, id_holding, id_grupo: int, id_setor: int):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_insert_emissor(database, id_emissor, cd_cnpj, ds_emissor, ic_holding, ic_consome_holding, id_holding, id_grupo, id_setor)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

    @classmethod
    def execute_insert_emissor_oc3(cls, database: str, id_emissor: int, cd_oc3: str):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_insert_emissor_oc3(database, id_emissor, cd_oc3)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

    @classmethod
    def execute_insert_emissor_crims(cls, database: str, id_emissor: int, cd_crims: str):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_insert_emissor_crims(database, id_emissor, cd_crims)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

    @classmethod
    def execute_update_holding_consumo(cls, database: str, id_emissor: int, id_holding: int):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_update_holding_consumo(database, id_emissor, id_holding)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

    # _______________________________ Consultar Grupo _______________________________

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

    # _______________________________ Atualizar Grupo _______________________________

    @classmethod
    def get_ids_emissores_by_grupo(cls, database: str, id_grupo: int):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_ids_emissores_by_grupo(database, id_grupo), cnx)
                return df['idEmissor'].dropna().astype(int).tolist() if not df.empty else []
        except Exception as e:
            raise e

    @classmethod
    def execute_delete_emissor_oc3(cls, database: str, id_emissor: int):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_delete_emissor_oc3(database, id_emissor)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

    @classmethod
    def execute_delete_emissor_crims(cls, database: str, id_emissor: int):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_delete_emissor_crims(database, id_emissor)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

    @classmethod
    def execute_delete_emissor_cadastro(cls, database: str, id_emissor: int):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_delete_emissor_cadastro(database, id_emissor)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

    @classmethod
    def execute_delete_emissor_completo(cls, database: str, id_emissor: int):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_delete_emissor_oc3(database, id_emissor)))
                cnx.execute(text(query_delete_emissor_crims(database, id_emissor)))
                cnx.execute(text(query_delete_emissor_fidc(database, id_emissor)))
                cnx.execute(text(query_delete_emissor_solicitacoes_descricao(database, id_emissor)))
                cnx.execute(text(query_delete_emissor_limites_historico(database, id_emissor)))
                cnx.execute(text(query_delete_emissor_limites_vigentes(database, id_emissor)))
                cnx.execute(text(query_delete_emissor_flexibilizacao(database, id_emissor)))
                cnx.execute(text(query_delete_emissor_ratings_historico(database, id_emissor)))
                cnx.execute(text(query_delete_emissor_ratings_vigentes(database, id_emissor)))
                cnx.execute(text(query_delete_emissor_mapeamento_ativos(database, id_emissor)))
                cnx.execute(text(query_delete_emissor_controle_limites(database, id_emissor)))
                cnx.execute(text(query_update_reset_holding_dependentes(database, id_emissor)))
                cnx.execute(text(query_delete_emissor_cadastro(database, id_emissor)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

    @classmethod
    def execute_transferir_emissor_grupo(cls, database: str, id_emissor: int, id_grupo_destino: int):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_update_reset_holding_dependentes(database, id_emissor)))
                cnx.execute(text(query_transfer_emissor_grupo(database, id_emissor, id_grupo_destino)))
                cnx.execute(text(query_transfer_emissor_limites_historico(database, id_emissor, id_grupo_destino)))
                cnx.execute(text(query_transfer_emissor_limites_vigentes(database, id_emissor, id_grupo_destino)))
                cnx.execute(text(query_transfer_emissor_controle_limites(database, id_emissor, id_grupo_destino)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

    # _______________________________ Deletar Grupo _______________________________

    @classmethod
    def execute_delete_grupo_economico(cls, database: str, id_grupo: int):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_delete_grupo(database, id_grupo)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()

    @classmethod
    def deletar_grupo_completo(cls, database: str, id_grupo: int):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_delete_emissores_oc3_by_grupo(database, id_grupo)))
                cnx.execute(text(query_delete_emissores_crims_by_grupo(database, id_grupo)))
                cnx.execute(text(query_delete_emissores_fidc_by_grupo(database, id_grupo)))
                cnx.execute(text(query_delete_solicitacoes_descricao_by_grupo(database, id_grupo)))
                cnx.execute(text(query_delete_solicitacoes_resposta_by_grupo(database, id_grupo)))
                cnx.execute(text(query_delete_limites_historico_by_grupo(database, id_grupo)))
                cnx.execute(text(query_delete_limites_vigentes_by_grupo(database, id_grupo)))
                cnx.execute(text(query_delete_flexibilizacao_by_grupo(database, id_grupo)))
                cnx.execute(text(query_delete_ratings_grupo_historico(database, id_grupo)))
                cnx.execute(text(query_delete_ratings_emissor_historico_by_grupo(database, id_grupo)))
                cnx.execute(text(query_delete_ratings_grupo_vigentes(database, id_grupo)))
                cnx.execute(text(query_delete_ratings_emissor_vigentes_by_grupo(database, id_grupo)))
                cnx.execute(text(query_delete_mapeamento_ativos_by_grupo(database, id_grupo)))
                cnx.execute(text(query_delete_controle_limites_by_grupo(database, id_grupo)))
                cnx.execute(text(query_delete_solicitacoes_by_grupo(database, id_grupo)))
                cnx.execute(text(query_update_reset_holding_by_grupo(database, id_grupo)))
                cnx.execute(text(query_delete_emissores_by_grupo(database, id_grupo)))
                cnx.execute(text(query_delete_grupo(database, id_grupo)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()
