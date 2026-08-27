# Importações do projeto
from bll.aprovar_limite.calculadora import CalculadoraLimitesGrupo
from services.aprovar_limite.insumos import InsumosAprovarLimite
from utils.funcoes_data import calcula_vencimento_n_meses

# Importações de bibliotecas
from typing import Dict, Any, List
from datetime import date, datetime
import pandas as pd

EVENTOS_PRINCIPAIS_RENOVACAO = [
    'Abertura de Limite',
    'Renovação',
    'Renovação com Downgrade de Rating',
    'Renovação com Upgrade de Rating',
    'Renovação com Downgrade de Rating + Run-Off',
    'Renovação com Upgrade de Rating + Run-Off'
]


def extrair_lista_ids_solicitacao(id_solicitacao_raw: Any) -> List[int]:
    """
    Normaliza a entrada de idSolicitacao para uma lista de inteiros.
    """
    if isinstance(id_solicitacao_raw, list):
        return [int(x) for x in id_solicitacao_raw if str(x).strip().isdigit()]
    if isinstance(id_solicitacao_raw, (int, float)):
        return [int(id_solicitacao_raw)]
    if isinstance(id_solicitacao_raw, str):
        partes = id_solicitacao_raw.split(',')
        return [int(p.strip()) for p in partes if p.strip().isdigit()]
    return []


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


def obter_aprovacoes_pendentes_consolidadas(database: str) -> pd.DataFrame:
    """
    Busca solicitações com status 'Aprovação Pendente' (idStatus = 3) e consolida por Grupo e Tipo de Evento.
    """
    try:
        df = InsumosAprovarLimite.get_aprovacoes_pendentes(database)

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


def obter_detalhes_solicitacao_aprovacao(database: str, ids_solicitacao_raw: Any) -> Dict[str, Any]:
    """
    Retorna a visão detalhada, segregada e enriquecida da solicitação para aprovação.
    """
    try:
        ids_solicitacao = extrair_lista_ids_solicitacao(ids_solicitacao_raw)
        if not ids_solicitacao:
            raise ValueError('Nenhum idSolicitacao informado.')

        # 1. Cabeçalho das solicitações
        df_cabecalho = InsumosAprovarLimite.get_solicitacao_cabecalho(database, ids_solicitacao)
        if df_cabecalho.empty:
            raise ValueError(f'Nenhuma solicitação encontrada para os IDs: {ids_solicitacao}')

        ds_grupo = df_cabecalho['dsGrupo'].dropna().iloc[0]
        cd_rating_grupo = df_cabecalho['cdRatingGrupo'].dropna().iloc[0] if not df_cabecalho['cdRatingGrupo'].dropna().empty else None
        vl_share_divida_grupo = float(df_cabecalho['vlShareDividaGrupo'].dropna().iloc[0]) if not df_cabecalho['vlShareDividaGrupo'].dropna().empty else None
        ds_tipo_evento = df_cabecalho['dsTipoEvento'].dropna().iloc[0] if not df_cabecalho['dsTipoEvento'].dropna().empty else ''

        # 2. Descrição das solicitações (linhas dos emissores)
        df_descricao = InsumosAprovarLimite.get_detalhes_solicitacao_descricao(database, ids_solicitacao)

        limites_grupo_cons_sem_meta = CalculadoraLimitesGrupo.consolidar_grupo_todas_mesas(df_descricao, considerar_meta=False)
        limites_grupo_mesa_sem_meta = CalculadoraLimitesGrupo.consolidar_grupo_por_mesa(df_descricao, considerar_meta=False)
        limites_grupo_cons_com_meta = CalculadoraLimitesGrupo.consolidar_grupo_todas_mesas(df_descricao, considerar_meta=True)
        limites_grupo_mesa_com_meta = CalculadoraLimitesGrupo.consolidar_grupo_por_mesa(df_descricao, considerar_meta=True)

        emissores_solicitados = estruturar_dados_emissores_solicitacao(df_descricao)

        # 3. Limites e Ratings Vigentes
        df_vigentes = InsumosAprovarLimite.get_limites_vigentes_grupo(database, ds_grupo)
        limites_vigentes_cons = CalculadoraLimitesGrupo.consolidar_grupo_todas_mesas(df_vigentes, considerar_meta=False)
        limites_vigentes_mesa = CalculadoraLimitesGrupo.consolidar_grupo_por_mesa(df_vigentes, considerar_meta=False)

        emissores_vigentes = estruturar_dados_emissores_solicitacao(df_vigentes)

        df_ratings_vigentes = InsumosAprovarLimite.get_ratings_vigentes(database, ds_grupo)
        ratings_vigentes_list = df_ratings_vigentes.to_dict(orient='records') if not df_ratings_vigentes.empty else []

        return {
            'dsGrupo': ds_grupo,
            'cdRatingGrupo': cd_rating_grupo,
            'vlShareDividaGrupo': vl_share_divida_grupo,
            'dsTipoEvento': ds_tipo_evento,
            'limitesGrupoConsolidadoSemMeta': limites_grupo_cons_sem_meta,
            'limitesGrupoPorMesaSemMeta': limites_grupo_mesa_sem_meta,
            'limitesGrupoConsolidadoComMeta': limites_grupo_cons_com_meta,
            'limitesGrupoPorMesaComMeta': limites_grupo_mesa_com_meta,
            'emissores': emissores_solicitados,
            'limitesVigentes': {
                'grupoConsolidado': limites_vigentes_cons,
                'grupoPorMesa': limites_vigentes_mesa,
                'emissores': emissores_vigentes
            },
            'ratingsVigentes': ratings_vigentes_list
        }
    except Exception as e:
        raise e


def calcular_data_vencimento_padrao_aprovacao(
    database: str,
    ds_tipo_evento: str,
    df_descricao: pd.DataFrame,
    df_vigentes: pd.DataFrame,
    data_aprovacao: date
) -> str:
    """
    Calcula a data de vencimento padrão da aprovação conforme a regra de evento e rating de emissores.
    """
    if ds_tipo_evento in EVENTOS_PRINCIPAIS_RENOVACAO:
        df_ratings = InsumosAprovarLimite.get_ratings_distintos(database)
        df_baa4 = df_ratings[df_ratings['cdRating'] == 'Baa4']
        id_corte_baa4 = int(df_baa4['idRating'].iloc[0]) if not df_baa4.empty else 999

        rating_map = dict(zip(df_ratings['cdRating'], df_ratings['idRating'])) if not df_ratings.empty else {}
        ratings_emissores = df_descricao['cdRatingEmissor'].dropna().unique()
        ratings_ids = [rating_map.get(r, 999) for r in ratings_emissores]

        todos_baa4_ou_melhor = all(r_id <= id_corte_baa4 for r_id in ratings_ids) if ratings_ids else True

        if todos_baa4_ou_melhor:
            venc = calcula_vencimento_n_meses(data_aprovacao, 11)
        else:
            venc = calcula_vencimento_n_meses(data_aprovacao, 5)

        return venc.strftime('%Y-%m-%d')

    if ds_tipo_evento == 'Prorrogação':
        if not df_vigentes.empty and not df_vigentes['dtVencimento'].dropna().empty:
            venc_vigente_raw = df_vigentes['dtVencimento'].dropna().iloc[0]
            venc = calcula_vencimento_n_meses(venc_vigente_raw, 3)
            return venc.strftime('%Y-%m-%d')
        else:
            venc = calcula_vencimento_n_meses(data_aprovacao, 3)
            return venc.strftime('%Y-%m-%d')

    # Flexibilização e outros eventos: mantém a data de vencimento vigente
    if not df_vigentes.empty and not df_vigentes['dtVencimento'].dropna().empty:
        venc_vigente_raw = str(df_vigentes['dtVencimento'].dropna().iloc[0])[:10]
        return venc_vigente_raw

    return calcula_vencimento_n_meses(data_aprovacao, 11).strftime('%Y-%m-%d')


def processar_decisao_limite(database: str, payload: dict) -> Dict[str, Any]:
    """
    Processa a aprovação ou rejeição do limite.
    - Se 'Rejeitado': atualiza idStatus = 6 em tCRS_0016_SolicitacoesAlcada.
    - Se 'Aprovado': atualiza idStatus = 4, insere em histórico, substitui vigentes
      e trata flexibilização de consumo conforme o tipo de evento.
    """
    try:
        decisao = str(payload.get('decisao') or payload.get('dsStatus') or '').strip().upper()
        ids_solicitacao = extrair_lista_ids_solicitacao(payload.get('idSolicitacao'))

        if not ids_solicitacao:
            raise ValueError('Campo idSolicitacao é obrigatório.')

        if decisao == 'REJEITADO':
            InsumosAprovarLimite.execute_rejeitar_solicitacoes(database, ids_solicitacao, id_status=6)
            return {'message': 'Solicitação de limite rejeitada com sucesso.'}

        if decisao != 'APROVADO':
            raise ValueError(f"Decisão inválida: '{decisao}'. Esperado 'Aprovado' ou 'Rejeitado'.")

        # 1. Carrega dados da solicitação
        df_cabecalho = InsumosAprovarLimite.get_solicitacao_cabecalho(database, ids_solicitacao)
        if df_cabecalho.empty:
            raise ValueError(f'Nenhuma solicitação encontrada para o(s) ID(s): {ids_solicitacao}')

        id_grupo = int(df_cabecalho['idGrupo'].iloc[0])
        ds_grupo = df_cabecalho['dsGrupo'].iloc[0]
        ds_tipo_evento = df_cabecalho['dsTipoEvento'].iloc[0]
        cd_rating_grupo = df_cabecalho['cdRatingGrupo'].dropna().iloc[0] if not df_cabecalho['cdRatingGrupo'].dropna().empty else None
        id_solicitacao_principal = ids_solicitacao[0]
        mesas = sorted(list(set(str(m) for m in df_cabecalho['cdMesa'].dropna() if str(m).strip())))

        df_descricao = InsumosAprovarLimite.get_detalhes_solicitacao_descricao(database, ids_solicitacao)
        df_vigentes = InsumosAprovarLimite.get_limites_vigentes_grupo(database, ds_grupo)

        # 2. Data de aprovação e vencimento padrão
        data_aprovacao_dt = date.today()
        dt_aprovacao_str = data_aprovacao_dt.strftime('%Y-%m-%d')
        dt_vencimento_padrao_str = calcular_data_vencimento_padrao_aprovacao(
            database=database,
            ds_tipo_evento=ds_tipo_evento,
            df_descricao=df_descricao,
            df_vigentes=df_vigentes,
            data_aprovacao=data_aprovacao_dt
        )

        # 3. Geração de registros para Limites (Histórico e Vigentes)
        current_max_id_limite = InsumosAprovarLimite.get_max_id_limite(database)
        limites_historico_params = []
        limites_vigentes_params = []

        for _, row in df_descricao.iterrows():
            current_max_id_limite += 1
            ic_limite_meta = int(row['icLimiteMeta']) if pd.notna(row.get('icLimiteMeta')) else 0

            # Se for limite meta, a data de vencimento vem de dtVencimentoLimiteMeta; caso contrário usa o padrão
            if ic_limite_meta == 1 and pd.notna(row.get('dtVencimentoLimiteMeta')):
                dt_vencimento_linha = str(row['dtVencimentoLimiteMeta'])[:10]
            else:
                dt_vencimento_linha = dt_vencimento_padrao_str

            item = {
                'idSolicitacao': int(row['idSolicitacao']),
                'idLimite': current_max_id_limite,
                'cdMesa': str(row['cdMesa']),
                'idGrupo': id_grupo,
                'idEmissor': int(row['idEmissor']),
                'vlPrazo': float(row['vlPrazo']),
                'vlTerceiros': float(row['vlTerceiros']),
                'vlReservaTecnica': float(row['vlReservaTecnica']),
                'icRunOff': int(row['icRunOff']) if pd.notna(row.get('icRunOff')) else 0,
                'dtAprovacao': dt_aprovacao_str,
                'dtVencimento': dt_vencimento_linha,
                'icLimiteMeta': ic_limite_meta
            }
            limites_historico_params.append(item)
            limites_vigentes_params.append(item)

        # 4. Registros de Rating
        rating_grupo_params = {
            'idSolicitacao': id_solicitacao_principal,
            'idGrupo': id_grupo,
            'cdRatingGrupo': cd_rating_grupo,
            'dtAprovacao': dt_aprovacao_str,
            'dtVencimento': dt_vencimento_padrao_str
        }

        ratings_emissores_params = []
        emissores_unicos = df_descricao[['idEmissor', 'cdRatingEmissor']].drop_duplicates()
        for _, row in emissores_unicos.iterrows():
            ratings_emissores_params.append({
                'idSolicitacao': id_solicitacao_principal,
                'idEmissor': int(row['idEmissor']),
                'cdRating': str(row['cdRatingEmissor']) if pd.notna(row.get('cdRatingEmissor')) else None,
                'dtAprovacao': dt_aprovacao_str,
                'dtVencimento': dt_vencimento_padrao_str
            })

        # 5. Tratamento de Flexibilização de Consumo (tCRS_0021)
        flexibilizacao_params = []
        remover_flex_anterior = False

        if ds_tipo_evento in EVENTOS_PRINCIPAIS_RENOVACAO:
            remover_flex_anterior = True
            for _, row in df_descricao.iterrows():
                is_runoff = int(row['icRunOff']) == 1 if pd.notna(row.get('icRunOff')) else False
                vl_total_aprovado = float(row['vlTerceiros']) + float(row['vlReservaTecnica'])
                vl_limite_flex = round(vl_total_aprovado * (0.01 if is_runoff else 0.10), 2)

                flexibilizacao_params.append({
                    'cdMesa': str(row['cdMesa']),
                    'idEmissor': int(row['idEmissor']),
                    'vlPrazo': int(row['vlPrazo']),
                    'vlFlexibilizado': 0.0,
                    'vlLimite': vl_limite_flex
                })

        elif ds_tipo_evento == 'Flexibilização':
            remover_flex_anterior = False
            for _, row in df_descricao.iterrows():
                cd_mesa_row = str(row['cdMesa'])
                id_emissor_row = int(row['idEmissor'])
                vl_prazo_row = float(row['vlPrazo'])
                vl_aprovado_total = float(row['vlTerceiros']) + float(row['vlReservaTecnica'])

                # Limite vigente anterior para a mesma mesa, emissor e prazo
                df_vig_match = df_vigentes[
                    (df_vigentes['cdMesa'] == cd_mesa_row) &
                    (df_vigentes['idEmissor'] == id_emissor_row) &
                    (df_vigentes['vlPrazo'] == vl_prazo_row)
                ]
                vl_vigente_total = float(df_vig_match['vlTerceiros'].sum() + df_vig_match['vlReservaTecnica'].sum()) if not df_vig_match.empty else 0.0
                delta_flex = max(0.0, round(vl_aprovado_total - vl_vigente_total, 2))

                flexibilizacao_params.append({
                    'cdMesa': cd_mesa_row,
                    'idEmissor': id_emissor_row,
                    'vlPrazo': int(vl_prazo_row),
                    'vlFlexibilizado': 0.0,
                    'vlLimite': delta_flex
                })

        # 6. Execução transacional única
        InsumosAprovarLimite.execute_efetivar_aprovacao_transacional(
            database=database,
            ids_solicitacao=ids_solicitacao,
            id_grupo=id_grupo,
            mesas=mesas,
            limites_historico_params=limites_historico_params,
            limites_vigentes_params=limites_vigentes_params,
            rating_grupo_params=rating_grupo_params,
            ratings_emissores_params=ratings_emissores_params,
            flexibilizacao_params=flexibilizacao_params,
            remover_flexibilizacao_anterior=remover_flex_anterior
        )

        return {
            'message': 'Limite aprovado e efetivado com sucesso.',
            'dtVencimento': dt_vencimento_padrao_str,
            'idStatus': 4
        }
    except Exception as e:
        raise e
