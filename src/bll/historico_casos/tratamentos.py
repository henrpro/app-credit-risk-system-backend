# Importações do projeto
from bll.historico_casos.calculadora import CalculadoraLimitesGrupo
from services.historico_casos.insumos import InsumosHistoricoCasos

# Importações de bibliotecas
from typing import Dict, Any, List
import pandas as pd


def estruturar_dados_emissores_solicitacao(df_descricao: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Estrutura os dados segregados por emissor, incluindo visões consolidadas e por mesa
    com e sem limite meta.
    """
    if df_descricao.empty:
        return []

    emissores_res = []
    emissores_unicos = df_descricao[['idEmissor', 'dsEmissor']].drop_duplicates()

    for _, emissor_row in emissores_unicos.iterrows():
        id_emissor = emissor_row['idEmissor']
        ds_emissor = emissor_row['dsEmissor']
        df_emissor = df_descricao[df_descricao['idEmissor'] == id_emissor]

        cd_rating_emissor = df_emissor['cdRatingEmissor'].dropna().iloc[0] if not df_emissor['cdRatingEmissor'].dropna().empty else None
        vl_share_divida = float(df_emissor['vlShareDividaEmissor'].dropna().iloc[0]) if not df_emissor['vlShareDividaEmissor'].dropna().empty else None

        limites_cons_sem_meta = CalculadoraLimitesGrupo.consolidar_grupo_todas_mesas(df_emissor, considerar_meta=False)
        limites_mesa_sem_meta = CalculadoraLimitesGrupo.consolidar_grupo_por_mesa(df_emissor, considerar_meta=False)
        limites_cons_com_meta = CalculadoraLimitesGrupo.consolidar_grupo_todas_mesas(df_emissor, considerar_meta=True)
        limites_mesa_com_meta = CalculadoraLimitesGrupo.consolidar_grupo_por_mesa(df_emissor, considerar_meta=True)

        emissores_res.append({
            'idEmissor': int(id_emissor),
            'dsEmissor': ds_emissor,
            'cdRating': cd_rating_emissor,
            'vlShareDivida': vl_share_divida,
            'limitesConsolidadoSemMeta': limites_cons_sem_meta,
            'limitesPorMesaSemMeta': limites_mesa_sem_meta,
            'limitesConsolidadoComMeta': limites_cons_com_meta,
            'limitesPorMesaComMeta': limites_mesa_com_meta
        })

    return emissores_res


def obter_descricao_solicitacao_historico(database: str, id_solicitacao: int) -> Dict[str, Any]:
    """
    Busca a descrição de uma solicitação finalizada individual no histórico,
    consolidando os limites do grupo com e sem meta (sem consulta a limites vigentes).
    """
    try:
        if not id_solicitacao or not str(id_solicitacao).isdigit():
            raise ValueError(f"idSolicitacao inválido: '{id_solicitacao}'")

        id_sol = int(id_solicitacao)

        # 1. Cabeçalho da solicitação individual
        df_cabecalho = InsumosHistoricoCasos.get_solicitacao_cabecalho(database, id_sol)
        if df_cabecalho.empty:
            raise ValueError(f'Nenhuma solicitação encontrada para o ID: {id_sol}')

        ds_grupo = df_cabecalho['dsGrupo'].dropna().iloc[0]
        cd_rating_grupo = df_cabecalho['cdRatingGrupo'].dropna().iloc[0] if not df_cabecalho['cdRatingGrupo'].dropna().empty else None
        vl_share_divida_grupo = float(df_cabecalho['vlShareDividaGrupo'].dropna().iloc[0]) if not df_cabecalho['vlShareDividaGrupo'].dropna().empty else None
        ds_tipo_evento = df_cabecalho['dsTipoEvento'].dropna().iloc[0] if not df_cabecalho['dsTipoEvento'].dropna().empty else ''
        cd_mesa = str(df_cabecalho['cdMesa'].dropna().iloc[0]) if not df_cabecalho['cdMesa'].dropna().empty else ''

        # 2. Linhas de limite dos emissores
        df_descricao = InsumosHistoricoCasos.get_descricao_solicitacao(database, id_sol)

        limites_grupo_cons_sem_meta = CalculadoraLimitesGrupo.consolidar_grupo_todas_mesas(df_descricao, considerar_meta=False)
        limites_grupo_mesa_sem_meta = CalculadoraLimitesGrupo.consolidar_grupo_por_mesa(df_descricao, considerar_meta=False)
        limites_grupo_cons_com_meta = CalculadoraLimitesGrupo.consolidar_grupo_todas_mesas(df_descricao, considerar_meta=True)
        limites_grupo_mesa_com_meta = CalculadoraLimitesGrupo.consolidar_grupo_por_mesa(df_descricao, considerar_meta=True)

        emissores_solicitados = estruturar_dados_emissores_solicitacao(df_descricao)

        return {
            'dsGrupo': ds_grupo,
            'cdRatingGrupo': cd_rating_grupo,
            'vlShareDividaGrupo': vl_share_divida_grupo,
            'dsTipoEvento': ds_tipo_evento,
            'cdMesa': cd_mesa,
            'idSolicitacao': id_sol,
            'limitesGrupoConsolidadoSemMeta': limites_grupo_cons_sem_meta,
            'limitesGrupoPorMesaSemMeta': limites_grupo_mesa_sem_meta,
            'limitesGrupoConsolidadoComMeta': limites_grupo_cons_com_meta,
            'limitesGrupoPorMesaComMeta': limites_grupo_mesa_com_meta,
            'emissores': emissores_solicitados
        }
    except Exception as e:
        raise e