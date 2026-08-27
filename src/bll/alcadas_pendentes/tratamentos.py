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


def obter_detalhes_alcada(database: str, ids_solicitacao_raw: Any) -> Dict[str, Any]:
    """
    Busca os detalhes completos da solicitação de alçada (grupo, emissores, limites solicitados
    com/sem meta e limites vigentes consolidados).
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
        cd_rating_grupo = df_cabecalho['cdRatingGrupo'].dropna().iloc[0] if not df_cabecalho['cdRatingGrupo'].dropna().empty else None
        vl_share_divida_grupo = float(df_cabecalho['vlShareDividaGrupo'].dropna().iloc[0]) if not df_cabecalho['vlShareDividaGrupo'].dropna().empty else None
        ds_tipo_evento = df_cabecalho['dsTipoEvento'].dropna().iloc[0] if not df_cabecalho['dsTipoEvento'].dropna().empty else ''
        cd_mesa = ', '.join(sorted(set(str(m) for m in df_cabecalho['cdMesa'].dropna() if str(m).strip())))

        # 2. Linhas de limite solicitadas (Emissores)
        df_descricao = InsumosAlcadasPendentes.get_detalhes_solicitacao_descricao(database, ids_solicitacao)

        limites_grupo_sem_meta = CalculadoraLimitesGrupo.calcula_consolidado_grupo_sem_limite_meta(df_descricao)
        limites_grupo_com_meta = CalculadoraLimitesGrupo.calcula_consolidado_grupo_com_limite_meta(df_descricao)

        limites_emissores = []
        if not df_descricao.empty:
            for _, row in df_descricao.iterrows():
                limites_emissores.append({
                    'dsEmissor': row.get('dsEmissor'),
                    'cdRatingEmissor': row.get('cdRatingEmissor'),
                    'vlShareDivida': float(row['vlShareDividaEmissor']) if pd.notna(row.get('vlShareDividaEmissor')) else None,
                    'vlPrazo': float(row['vlPrazo']) if pd.notna(row.get('vlPrazo')) else 0.0,
                    'vlTerceiros': float(row['vlTerceiros']) if pd.notna(row.get('vlTerceiros')) else 0.0,
                    'vlReservaTecnica': float(row['vlReservaTecnica']) if pd.notna(row.get('vlReservaTecnica')) else 0.0,
                    'icRunOff': int(row['icRunOff']) if pd.notna(row.get('icRunOff')) else 0,
                    'icLimiteMeta': int(row['icLimiteMeta']) if pd.notna(row.get('icLimiteMeta')) else 0,
                    'dtVencimentoLimiteMeta': str(row['dtVencimentoLimiteMeta']) if pd.notna(row.get('dtVencimentoLimiteMeta')) else None
                })

        # 3. Limites Vigentes do Grupo e Emissores
        df_vigentes = InsumosAlcadasPendentes.get_limites_vigentes_grupo(database, ds_grupo)
        limites_vigentes_grupo_sem_meta = CalculadoraLimitesGrupo.calcula_consolidado_vigentes_sem_limite_meta(df_vigentes)
        limites_vigentes_grupo_com_meta = CalculadoraLimitesGrupo.calcula_consolidado_vigentes_com_limite_meta(df_vigentes)

        limites_vigentes_emissores = []
        if not df_vigentes.empty:
            for _, row in df_vigentes.iterrows():
                limites_vigentes_emissores.append({
                    'cdMesa': row.get('cdMesa'),
                    'dsEmissor': row.get('dsEmissor'),
                    'vlPrazo': float(row['vlPrazo']) if pd.notna(row.get('vlPrazo')) else 0.0,
                    'vlTerceiros': float(row['vlTerceiros']) if pd.notna(row.get('vlTerceiros')) else 0.0,
                    'vlReservaTecnica': float(row['vlReservaTecnica']) if pd.notna(row.get('vlReservaTecnica')) else 0.0,
                    'icRunOff': int(row['icRunOff']) if pd.notna(row.get('icRunOff')) else 0,
                    'icLimiteMeta': int(row['icLimiteMeta']) if pd.notna(row.get('icLimiteMeta')) else 0,
                    'dtVencimento': str(row['dtVencimento']) if pd.notna(row.get('dtVencimento')) else None
                })

        # 4. Ratings Vigentes
        df_ratings = InsumosAlcadasPendentes.get_ratings_vigentes(database, ds_grupo)
        ratings_vigentes = []
        if not df_ratings.empty:
            for _, row in df_ratings.iterrows():
                ratings_vigentes.append({
                    'dsEntidade': row.get('dsEntidade'),
                    'cdRating': row.get('cdRating'),
                    'tipoEntidade': row.get('tipoEntidade'),
                    'dtVencimento': str(row['dtVencimento']) if pd.notna(row.get('dtVencimento')) else None
                })

        return {
            'dsGrupo': ds_grupo,
            'cdRatingGrupo': cd_rating_grupo,
            'vlShareDividaGrupo': vl_share_divida_grupo,
            'dsTipoEvento': ds_tipo_evento,
            'cdMesa': cd_mesa,
            'idsSolicitacao': ids_solicitacao,
            'limitesGrupoSemMeta': limites_grupo_sem_meta,
            'limitesGrupoComMeta': limites_grupo_com_meta,
            'limitesEmissores': limites_emissores,
            'limitesVigentesGrupoSemMeta': limites_vigentes_grupo_sem_meta,
            'limitesVigentesGrupoComMeta': limites_vigentes_grupo_com_meta,
            'limitesVigentesEmissores': limites_vigentes_emissores,
            'ratingsVigentes': ratings_vigentes
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
