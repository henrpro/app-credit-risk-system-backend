# Importações do projeto
from services.alcadas_pendentes.insumos import InsumosAlcadasPendentes
from bll.alcadas_pendentes.calculadora import CalculadoraLimitesGrupo

# Importações de bibliotecas
from typing import Dict, Any, List
from datetime import datetime
import pandas as pd


def extrair_lista_ids_solicitacao(ids_solicitacao: Any) -> List[int]:
    """
    Função auxiliar linear para converter diferentes formatos de entrada de idSolicitacao
    em uma lista de inteiros.
    """
    if isinstance(ids_solicitacao, list):
        return [int(i) for i in ids_solicitacao if str(i).isdigit()]

    if isinstance(ids_solicitacao, (int, float)):
        return [int(ids_solicitacao)]

    if isinstance(ids_solicitacao, str):
        itens = ids_solicitacao.replace('[', '').replace(']', '').split(',')
        return [int(i.strip()) for i in itens if i.strip().isdigit()]

    return []


def obter_alcadas_pendentes_consolidadas(database: str) -> pd.DataFrame:
    """
    Busca as solicitações com status 'Alçada Pendente' e consolida por Grupo e Tipo de Evento.
    Se houverem duas solicitações para o mesmo grupo e evento vindas de mesas distintas, junta ambas.
    """
    try:
        df = InsumosAlcadasPendentes.get_alcadas_pendentes(database)

        if df.empty:
            return pd.DataFrame(columns=['dsGrupo', 'dsTipoEvento', 'dsNome', 'cdMesa', 'idSolicitacao', 'dtSolicitacao'])

        registros_consolidados = []
        grupos_agrupados = df.groupby(['dsGrupo', 'dsTipoEvento'])

        for (ds_grupo, ds_tipo_evento), grupo_df in grupos_agrupados:
            mesas = ', '.join(sorted(set(str(m) for m in grupo_df['cdMesa'].dropna() if str(m).strip())))
            solicitantes = ', '.join(sorted(set(str(n) for n in grupo_df['dsNome'].dropna() if str(n).strip())))
            ids_sol = sorted(list(set(int(i) for i in grupo_df['idSolicitacao'].dropna())))
            data_solicitacao = str(grupo_df['dtSolicitacao'].dropna().iloc[0]) if not grupo_df['dtSolicitacao'].dropna().empty else None

            registros_consolidados.append({
                'dsGrupo': ds_grupo,
                'dsTipoEvento': ds_tipo_evento,
                'dsNome': solicitantes,
                'cdMesa': mesas,
                'idSolicitacao': ids_sol if len(ids_sol) > 1 else ids_sol[0],
                'dtSolicitacao': data_solicitacao
            })

        return pd.DataFrame(registros_consolidados)
    except Exception as e:
        raise e


def estruturar_dados_emissores_solicitacao(df_descricao: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Monta a lista de dados e limites por emissor para a solicitação (consolidado e por mesa).
    Soma o share da dívida entre as diferentes mesas e verifica convergência/divergência de ratings.
    """
    if df_descricao.empty:
        return []

    emissores_lista = []
    emissores_unicos = sorted(df_descricao['dsEmissor'].dropna().unique())

    for emissor in emissores_unicos:
        df_emissor = df_descricao[df_descricao['dsEmissor'] == emissor]
        
        # Share da dívida somado entre as mesas distintas
        share_por_mesa = df_emissor.groupby('cdMesa')['vlShareDividaEmissor'].first().dropna()
        vl_share = float(share_por_mesa.sum()) if not share_por_mesa.empty else None

        # Ratings preenchidos por cada mesa
        ratings_mesa_list = []
        ratings_preenchidos_set = set()

        for mesa, sub_df in df_emissor.groupby('cdMesa'):
            mesa_str = str(mesa).strip()
            r_series = sub_df['cdRatingEmissor'].dropna()
            r_val = str(r_series.iloc[0]).strip() if not r_series.empty and str(r_series.iloc[0]).strip() and str(r_series.iloc[0]).strip().lower() != 'none' else None
            if r_val:
                ratings_preenchidos_set.add(r_val)
            ratings_mesa_list.append({
                'cdMesa': mesa_str,
                'cdRating': r_val
            })

        # Divergência se mais de um rating distinto foi preenchido
        ic_divergencia_rating = len(ratings_preenchidos_set) > 1
        cd_rating = ', '.join(sorted(ratings_preenchidos_set)) if ratings_preenchidos_set else None

        limites_cons_sem_meta = CalculadoraLimitesGrupo.consolidar_emissor_todas_mesas(df_emissor, considerar_meta=False)
        limites_mesa_sem_meta = CalculadoraLimitesGrupo.consolidar_emissor_por_mesa(df_emissor, considerar_meta=False)
        limites_cons_com_meta = CalculadoraLimitesGrupo.consolidar_emissor_todas_mesas(df_emissor, considerar_meta=True)
        limites_mesa_com_meta = CalculadoraLimitesGrupo.consolidar_emissor_por_mesa(df_emissor, considerar_meta=True)

        emissores_lista.append({
            'dsEmissor': emissor,
            'cdRatingEmissor': cd_rating,
            'icDivergenciaRating': ic_divergencia_rating,
            'ratingsPorMesa': ratings_mesa_list,
            'vlShareDividaEmissor': vl_share,
            'limitesConsolidadoSemMeta': limites_cons_sem_meta,
            'limitesPorMesaSemMeta': limites_mesa_sem_meta,
            'limitesConsolidadoComMeta': limites_cons_com_meta,
            'limitesPorMesaComMeta': limites_mesa_com_meta
        })

    return emissores_lista


def estruturar_dados_emissores_vigentes(df_vigentes: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Monta a lista de limites vigentes por emissor (consolidado e por mesa).
    """
    if df_vigentes.empty:
        return []

    emissores_lista = []
    emissores_unicos = sorted(df_vigentes['dsEmissor'].dropna().unique())

    for emissor in emissores_unicos:
        df_emissor = df_vigentes[df_vigentes['dsEmissor'] == emissor]

        limites_cons_sem_meta = CalculadoraLimitesGrupo.consolidar_emissor_todas_mesas(df_emissor, considerar_meta=False)
        limites_mesa_sem_meta = CalculadoraLimitesGrupo.consolidar_emissor_por_mesa(df_emissor, considerar_meta=False)
        limites_cons_com_meta = CalculadoraLimitesGrupo.consolidar_emissor_todas_mesas(df_emissor, considerar_meta=True)
        limites_mesa_com_meta = CalculadoraLimitesGrupo.consolidar_emissor_por_mesa(df_emissor, considerar_meta=True)

        emissores_lista.append({
            'dsEmissor': emissor,
            'limitesConsolidadoSemMeta': limites_cons_sem_meta,
            'limitesPorMesaSemMeta': limites_mesa_sem_meta,
            'limitesConsolidadoComMeta': limites_cons_com_meta,
            'limitesPorMesaComMeta': limites_mesa_com_meta
        })

    return emissores_lista


def obter_detalhes_alcada(database: str, ids_solicitacao_raw: Any) -> Dict[str, Any]:
    """
    Busca os detalhes completos da solicitação de alçada:
    - Dados do grupo (nome, rating por mesa com detecção de divergência, share da dívida somado, tipo de evento, mesas)
    - Limites consolidados do grupo (todas as mesas e por mesa, com e sem limite meta)
    - Limites dos emissores (consolidado e por mesa, com e sem limite meta, share somado e ratings por mesa)
    - Limites e ratings vigentes correspondentes.
    """
    try:
        ids_solicitacao = extrair_lista_ids_solicitacao(ids_solicitacao_raw)

        if not ids_solicitacao:
            raise ValueError('Nenhum identificador de solicitação (idSolicitacao) válido foi fornecido.')

        # 1. Cabeçalho da solicitação
        df_cabecalho = InsumosAlcadasPendentes.get_solicitacao_cabecalho(database, ids_solicitacao)
        if df_cabecalho.empty:
            raise ValueError(f'Nenhuma solicitação encontrada para o(s) ID(s): {ids_solicitacao}')

        ds_grupo = df_cabecalho['dsGrupo'].dropna().iloc[0]
        ds_tipo_evento = df_cabecalho['dsTipoEvento'].dropna().iloc[0] if not df_cabecalho['dsTipoEvento'].dropna().empty else ''
        cd_mesa = ', '.join(sorted(set(str(m) for m in df_cabecalho['cdMesa'].dropna() if str(m).strip())))

        # Share da dívida do grupo somado entre as mesas/solicitações
        shares_grupo = df_cabecalho['vlShareDividaGrupo'].dropna()
        vl_share_divida_grupo = float(shares_grupo.sum()) if not shares_grupo.empty else None

        # Ratings do grupo por mesa e detecção de divergência
        ratings_grupo_mesa_list = []
        ratings_grupo_set = set()

        for mesa, sub_df in df_cabecalho.groupby('cdMesa'):
            mesa_str = str(mesa).strip()
            r_series = sub_df['cdRatingGrupo'].dropna()
            rg = str(r_series.iloc[0]).strip() if not r_series.empty and str(r_series.iloc[0]).strip() and str(r_series.iloc[0]).strip().lower() != 'none' else None
            if rg:
                ratings_grupo_set.add(rg)
            ratings_grupo_mesa_list.append({
                'cdMesa': mesa_str,
                'cdRating': rg
            })

        ic_divergencia_rating_grupo = len(ratings_grupo_set) > 1
        cd_rating_grupo = ', '.join(sorted(ratings_grupo_set)) if ratings_grupo_set else None

        # 2. Limites solicitados (Grupo e Emissores)
        df_descricao = InsumosAlcadasPendentes.get_detalhes_solicitacao_descricao(database, ids_solicitacao)

        limites_grupo_cons_sem_meta = CalculadoraLimitesGrupo.consolidar_grupo_todas_mesas(df_descricao, considerar_meta=False)
        limites_grupo_mesa_sem_meta = CalculadoraLimitesGrupo.consolidar_grupo_por_mesa(df_descricao, considerar_meta=False)
        limites_grupo_cons_com_meta = CalculadoraLimitesGrupo.consolidar_grupo_todas_mesas(df_descricao, considerar_meta=True)
        limites_grupo_mesa_com_meta = CalculadoraLimitesGrupo.consolidar_grupo_por_mesa(df_descricao, considerar_meta=True)

        emissores_solicitados = estruturar_dados_emissores_solicitacao(df_descricao)

        # 3. Limites Vigentes (Grupo e Emissores)
        df_vigentes = InsumosAlcadasPendentes.get_limites_vigentes_grupo(database, ds_grupo)

        limites_vig_grupo_cons_sem_meta = CalculadoraLimitesGrupo.consolidar_grupo_todas_mesas(df_vigentes, considerar_meta=False)
        limites_vig_grupo_mesa_sem_meta = CalculadoraLimitesGrupo.consolidar_grupo_por_mesa(df_vigentes, considerar_meta=False)
        limites_vig_grupo_cons_com_meta = CalculadoraLimitesGrupo.consolidar_grupo_todas_mesas(df_vigentes, considerar_meta=True)
        limites_vig_grupo_mesa_com_meta = CalculadoraLimitesGrupo.consolidar_grupo_por_mesa(df_vigentes, considerar_meta=True)

        emissores_vigentes = estruturar_dados_emissores_vigentes(df_vigentes)

        # 4. Ratings Vigentes
        df_ratings = InsumosAlcadasPendentes.get_ratings_vigentes(database, ds_grupo)
        rating_grupo_vigente = None
        ratings_emissores_vigentes = []

        if not df_ratings.empty:
            df_rg = df_ratings[df_ratings['tipoEntidade'] == 'Grupo']
            if not df_rg.empty:
                rating_grupo_vigente = {
                    'dsGrupo': df_rg['dsEntidade'].iloc[0],
                    'cdRating': df_rg['cdRating'].iloc[0],
                    'dtVencimento': str(df_rg['dtVencimento'].iloc[0]) if pd.notna(df_rg['dtVencimento'].iloc[0]) else None
                }

            df_re = df_ratings[df_ratings['tipoEntidade'] == 'Emissor']
            for _, row in df_re.iterrows():
                ratings_emissores_vigentes.append({
                    'dsEmissor': row['dsEntidade'],
                    'cdRating': row['cdRating'],
                    'dtVencimento': str(row['dtVencimento']) if pd.notna(row['dtVencimento']) else None
                })

        return {
            'dsGrupo': ds_grupo,
            'cdRatingGrupo': cd_rating_grupo,
            'icDivergenciaRatingGrupo': ic_divergencia_rating_grupo,
            'ratingsGrupoPorMesa': ratings_grupo_mesa_list,
            'vlShareDividaGrupo': vl_share_divida_grupo,
            'dsTipoEvento': ds_tipo_evento,
            'cdMesa': cd_mesa,
            'idsSolicitacao': ids_solicitacao,
            'limitesGrupoConsolidadoSemMeta': limites_grupo_cons_sem_meta,
            'limitesGrupoPorMesaSemMeta': limites_grupo_mesa_sem_meta,
            'limitesGrupoConsolidadoComMeta': limites_grupo_cons_com_meta,
            'limitesGrupoPorMesaComMeta': limites_grupo_mesa_com_meta,
            'emissores': emissores_solicitados,
            'limitesVigentes': {
                'limitesGrupoConsolidadoSemMeta': limites_vig_grupo_cons_sem_meta,
                'limitesGrupoPorMesaSemMeta': limites_vig_grupo_mesa_sem_meta,
                'limitesGrupoConsolidadoComMeta': limites_vig_grupo_cons_com_meta,
                'limitesGrupoPorMesaComMeta': limites_vig_grupo_mesa_com_meta,
                'emissores': emissores_vigentes
            },
            'ratingsVigentes': {
                'ratingGrupo': rating_grupo_vigente,
                'ratingsEmissores': ratings_emissores_vigentes
            }
        }
    except Exception as e:
        raise e


def realizar_resposta_alcada(database: str, payload: dict):
    """
    Processa a deliberação da alçada, inserindo a resposta e atualizando o status de todas
    as solicitações consolidadas para o status definido (default 2 = Aprovado).
    """
    try:
        ids_raw = payload.get('idSolicitacao')
        ids_solicitacao = extrair_lista_ids_solicitacao(ids_raw)

        if not ids_solicitacao:
            raise ValueError('Campo idSolicitacao é obrigatório para responder a alçada.')

        ds_alcada = payload.get('dsAlcada', '').strip() or None
        cd_user_resposta = payload.get('cdUserResposta', '').strip() or None
        id_status = int(payload.get('idStatus', 2))
        dt_resposta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        InsumosAlcadasPendentes.execute_responder_alcada(
            database=database,
            ids_solicitacao=ids_solicitacao,
            ds_alcada=ds_alcada,
            dt_resposta=dt_resposta,
            cd_user_resposta=cd_user_resposta,
            id_status=id_status
        )
    except Exception as e:
        raise e
