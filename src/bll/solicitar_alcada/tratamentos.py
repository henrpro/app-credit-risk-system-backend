# Importações do projeto
from services.solicitar_alcada.insumos import InsumosSolicitarAlcada

# Importações de bibliotecas
from datetime import date
import pandas as pd


def obtem_eventos_disponiveis(database: str, grupo: str, mesa: str) -> pd.DataFrame:
    """
    Função que busca os eventos disponíveis para um determinado grupo econômico.
    """
    try:
        # Começamos obtendo os eventos distintos do banco de dados
        df_eventos = InsumosSolicitarAlcada.get_eventos_possiveis(database)

        # Buscamos os limites aprovados para o grupo econômico e a mesa
        df_limites = InsumosSolicitarAlcada.get_limites_aprovados_by_grupo(database, grupo, mesa)

        # Verificamos se há algum limite vigente para a mesa no grupo
        tem_limite_vigente = not df_limites.empty and df_limites['vlTerceiros'].notna().any()

        if not tem_limite_vigente:
            # Se a mesa não tem nenhum limite aprovado no grupo, o único evento disponível é 'Abertura de Limite'
            df_eventos = df_eventos[df_eventos['dsTipoEvento'] == 'Abertura de Limite']
        else:
            # Se a mesa já possui limite aprovado, removemos 'Abertura de Limite'
            df_eventos = df_eventos[df_eventos['dsTipoEvento'] != 'Abertura de Limite']

            # Verificamos se a mesa já prorrogou o grupo; se sim, retiramos 'Prorrogação' da lista
            df_prorrogacoes = InsumosSolicitarAlcada.get_prorrogacoes_recentes(database, grupo, mesa)
            if not df_prorrogacoes.empty:
                df_eventos = df_eventos[df_eventos['dsTipoEvento'] != 'Prorrogação']

        # Verificamos se é possível flexibilizar o grupo (com aumento de LMAX)
        df_flexibilizacao = InsumosSolicitarAlcada.get_disponivel_flexibilizacao(database, grupo, mesa)
        if df_flexibilizacao.empty:
            df_eventos = df_eventos[df_eventos['dsTipoEvento'] != 'Flexibilização']

        return df_eventos.reset_index(drop=True)
    except Exception as e:
        raise e


def realiza_insert_solicitacao_alcada(database: str, payload: dict):
    """
    Realiza o insert transacional da solicitação de alçada, seus emissores, linhas de limite e limites meta.
    """
    try:
        # Começamos extraindo e validando o grupo econômico
        ds_grupo = payload.get('dsGrupo', '').strip()
        id_grupo = InsumosSolicitarAlcada.get_id_grupo_by_name(database, ds_grupo)
        if not id_grupo:
            raise ValueError(f"Grupo econômico '{ds_grupo}' não encontrado.")

        # Tipo de evento sendo solicitado, data e status inicial
        ds_tipo_evento = payload.get('dsTipoEvento', '').strip()
        dt_solicitacao = date.today().strftime('%Y-%m-%d')
        id_status = 1

        # Dados do solicitante
        user = payload.get('cdUser')
        profile = payload.get('dsProfile')

        # Dados do grupo econômico solicitado
        cd_rating_grupo = payload.get('cdRatingGrupo')
        vl_share_divida_raw = payload.get('vlShareDivida')
        vl_share_divida = float(vl_share_divida_raw) / 100 if vl_share_divida_raw not in (None, "") else None

        # Buscamos o próximo id de solicitação
        id_solicitacao = InsumosSolicitarAlcada.get_max_id_solicitacao(database) + 1

        # Montamos o dicionário de parâmetros do cabeçalho da solicitação
        solicitacao_params = {
            'idSolicitacao': id_solicitacao,
            'dtSolicitacao': dt_solicitacao,
            'cdUser': user,
            'cdMesa': profile,
            'idGrupo': id_grupo,
            'cdRatingGrupo': cd_rating_grupo,
            'vlShareDivida': vl_share_divida,
            'idStatus': id_status,
            'dsTipoEvento': ds_tipo_evento
        }

        linhas_descricao_params = []

        # Iteramos os emissores e montamos as linhas e limites meta
        for emissor in payload.get('emissores', []):
            # Começamos buscando o emissor e seu id
            ds_emissor = emissor.get('dsEmissor', '').strip()
            id_emissor = InsumosSolicitarAlcada.get_emissor_by_name(database, ds_emissor)
            if not id_emissor:
                raise ValueError(f"Emissor '{ds_emissor}' não encontrado.")

            # Agora buscamos o rating, share da dívida e se o emissor está em run-off
            cd_rating_emissor = emissor.get('cdRating')
            vl_share_raw = emissor.get('vlShareDivida')
            vl_share_divida_emissor = float(vl_share_raw) / 100 if vl_share_raw not in (None, "") else None
            ic_runoff = int(emissor.get('icRunOff', 0))

            # Inserção das linhas de limite solicitadas para o emissor
            for linha in emissor.get('linhas', []):
                # Buscamos o prazo, valor terceiros e RT
                vl_prazo = float(linha.get('vlPrazo'))
                vl_terceiros = float(linha.get('vlTerceiros', 0.0))
                vl_reserva_tecnica = float(linha.get('vlReservaTecnica', 0.0))

                # Guardamos os dados para a descrição do emissor
                linhas_descricao_params.append({
                    'idSolicitacao': id_solicitacao,
                    'idEmissor': id_emissor,
                    'cdRating': cd_rating_emissor,
                    'vlPrazo': vl_prazo,
                    'vlTerceiros': vl_terceiros,
                    'vlReservaTecnica': vl_reserva_tecnica,
                    'icRunOff': ic_runoff,
                    'vlShareDivida': vl_share_divida_emissor,
                    'icLimiteMeta': 0,
                    'dtVencimentoLimiteMeta': None
                })

            # Começamos buscando os dados de limite meta
            meta = emissor.get('meta')

            # Se tiver limite meta preenchido
            if meta and isinstance(meta, dict) and meta.get('rows'):
                # Buscamos a data de vencimento do limite meta, rating e share da dívida
                dt_vencimento_meta = meta.get('dtVencimento')
                cd_rating_meta = meta.get('cdRating', cd_rating_emissor)
                vl_share_meta_raw = meta.get('shareDivida')
                vl_share_divida_meta = float(vl_share_meta_raw) / 100 if vl_share_meta_raw not in (None, "") else vl_share_divida_emissor
                ic_runoff_meta = int(meta.get('icRunOff', ic_runoff))

                # Iteramos pelas linhas do limite meta
                for row in meta.get('rows', []):
                    # Buscamos o prazo, valor terceiros e RT
                    vl_prazo_meta = float(row.get('prazo') if row.get('prazo') is not None else row.get('vlPrazo'))
                    vl_terceiros_meta = float(row.get('terceirosProposto') if row.get('terceirosProposto') is not None else row.get('vlTerceiros', 0.0))
                    vl_reserva_tecnica_meta = float(row.get('rtProposto') if row.get('rtProposto') is not None else row.get('vlReservaTecnica', 0.0))

                    # Guardamos os dados de limite meta para o emissor
                    linhas_descricao_params.append({
                        'idSolicitacao': id_solicitacao,
                        'idEmissor': id_emissor,
                        'cdRating': cd_rating_meta,
                        'vlPrazo': vl_prazo_meta,
                        'vlTerceiros': vl_terceiros_meta,
                        'vlReservaTecnica': vl_reserva_tecnica_meta,
                        'icRunOff': ic_runoff_meta,
                        'vlShareDivida': vl_share_divida_meta,
                        'icLimiteMeta': 1,
                        'dtVencimentoLimiteMeta': dt_vencimento_meta
                    })

        # Executamos a inserção completa no banco em transação única
        InsumosSolicitarAlcada.execute_insert_solicitacao_completa(
            database=database,
            solicitacao_params=solicitacao_params,
            linhas_descricao_params=linhas_descricao_params
        )
    except Exception as e:
        raise e


def obtem_detalhes_solicitacao_completa(database: str, id_solicitacao: int) -> dict:
    """
    Busca todos os dados de uma solicitação de alçada (cabeçalho, emissores, linhas e limite meta) pelo idSolicitacao.
    """
    try:
        # 1. Busca cabeçalho
        df_cab = InsumosSolicitarAlcada.get_solicitacao_cabecalho_by_id(database, id_solicitacao)
        if df_cab.empty:
            raise ValueError(f"Solicitação #{id_solicitacao} não encontrada.")

        cab = df_cab.iloc[0]

        # 2. Busca linhas de descrição
        df_desc = InsumosSolicitarAlcada.get_solicitacao_descricao_by_id(database, id_solicitacao)

        emissores_dict = {}

        for _, row in df_desc.iterrows():
            id_emissor = int(row['idEmissor'])
            ds_emissor = row['dsEmissor']
            cd_rating = row['cdRating'] if pd.notna(row['cdRating']) else ''
            vl_share = float(row['vlShareDivida']) if pd.notna(row['vlShareDivida']) else None
            ic_runoff = int(row['icRunOff']) if pd.notna(row['icRunOff']) else 0
            ic_meta = int(row['icLimiteMeta']) if pd.notna(row['icLimiteMeta']) else 0

            if id_emissor not in emissores_dict:
                emissores_dict[id_emissor] = {
                    'idEmissor': id_emissor,
                    'dsEmissor': ds_emissor,
                    'cdRating': cd_rating,
                    'vlShareDivida': vl_share,
                    'icRunOff': ic_runoff,
                    'linhas': [],
                    'meta': None
                }

            if ic_meta == 0:
                # Linha normal da proposta
                emissores_dict[id_emissor]['linhas'].append({
                    'vlPrazo': int(row['vlPrazo']) if pd.notna(row['vlPrazo']) else 0,
                    'vlTerceiros': float(row['vlTerceiros']) if pd.notna(row['vlTerceiros']) else 0.0,
                    'vlReservaTecnica': float(row['vlReservaTecnica']) if pd.notna(row['vlReservaTecnica']) else 0.0
                })
            else:
                # Linha de limite meta
                if emissores_dict[id_emissor]['meta'] is None:
                    dt_venc = str(row['dtVencimentoLimiteMeta']) if pd.notna(row['dtVencimentoLimiteMeta']) else ''
                    emissores_dict[id_emissor]['meta'] = {
                        'dtVencimento': dt_venc,
                        'cdRating': cd_rating,
                        'shareDivida': vl_share,
                        'icRunOff': ic_runoff,
                        'rows': []
                    }

                emissores_dict[id_emissor]['meta']['rows'].append({
                    'prazo': int(row['vlPrazo']) if pd.notna(row['vlPrazo']) else 0,
                    'terceirosProposto': float(row['vlTerceiros']) if pd.notna(row['vlTerceiros']) else 0.0,
                    'rtProposto': float(row['vlReservaTecnica']) if pd.notna(row['vlReservaTecnica']) else 0.0
                })

        return {
            'idSolicitacao': int(cab['idSolicitacao']),
            'dtSolicitacao': str(cab['dtSolicitacao']) if pd.notna(cab['dtSolicitacao']) else '',
            'cdUser': str(cab['cdUser']) if pd.notna(cab['cdUser']) else '',
            'cdMesa': str(cab['cdMesa']) if pd.notna(cab['cdMesa']) else '',
            'idGrupo': int(cab['idGrupo']) if pd.notna(cab['idGrupo']) else None,
            'dsGrupo': str(cab['dsGrupo']) if pd.notna(cab['dsGrupo']) else '',
            'cdRatingGrupo': str(cab['cdRatingGrupo']) if pd.notna(cab['cdRatingGrupo']) else '',
            'vlShareDividaGrupo': float(cab['vlShareDivida']) if pd.notna(cab['vlShareDivida']) else None,
            'idStatus': int(cab['idStatus']) if pd.notna(cab['idStatus']) else 1,
            'dsTipoEvento': str(cab['dsTipoEvento']) if pd.notna(cab['dsTipoEvento']) else '',
            'emissores': list(emissores_dict.values())
        }
    except Exception as e:
        raise e


def realiza_update_solicitacao_alcada(database: str, payload: dict):
    """
    Atualiza uma solicitação de alçada existente deletando os registros anteriores e reinserindo com o mesmo idSolicitacao.
    """
    try:
        # Começamos extraindo e validando o idSolicitacao
        id_solicitacao_raw = payload.get('idSolicitacao')
        if not id_solicitacao_raw:
            raise ValueError("ID da solicitação não informado para atualização.")

        id_solicitacao = int(id_solicitacao_raw)

        # Validamos o grupo econômico
        ds_grupo = payload.get('dsGrupo', '').strip()
        id_grupo = InsumosSolicitarAlcada.get_id_grupo_by_name(database, ds_grupo)
        if not id_grupo:
            raise ValueError(f"Grupo econômico '{ds_grupo}' não encontrado.")

        # Tipo de evento sendo solicitado, data e status (sempre retorna para status 1 - Enviado / Alçada Pendente)
        ds_tipo_evento = payload.get('dsTipoEvento', '').strip()
        dt_solicitacao = date.today().strftime('%Y-%m-%d')
        id_status = 1

        # Dados do solicitante
        user = payload.get('cdUser')
        profile = payload.get('dsProfile')

        # Dados do grupo econômico solicitado
        cd_rating_grupo = payload.get('cdRatingGrupo')
        vl_share_divida_raw = payload.get('vlShareDivida')
        vl_share_divida = float(vl_share_divida_raw) / 100 if vl_share_divida_raw not in (None, "") else None

        # Montamos o dicionário de parâmetros do cabeçalho da solicitação
        solicitacao_params = {
            'idSolicitacao': id_solicitacao,
            'dtSolicitacao': dt_solicitacao,
            'cdUser': user,
            'cdMesa': profile,
            'idGrupo': id_grupo,
            'cdRatingGrupo': cd_rating_grupo,
            'vlShareDivida': vl_share_divida,
            'idStatus': id_status,
            'dsTipoEvento': ds_tipo_evento
        }

        linhas_descricao_params = []

        # Iteramos os emissores e montamos as linhas e limites meta
        for emissor in payload.get('emissores', []):
            ds_emissor = emissor.get('dsEmissor', '').strip()
            id_emissor = InsumosSolicitarAlcada.get_emissor_by_name(database, ds_emissor)
            if not id_emissor:
                raise ValueError(f"Emissor '{ds_emissor}' não encontrado.")

            cd_rating_emissor = emissor.get('cdRating')
            vl_share_raw = emissor.get('vlShareDivida')
            vl_share_divida_emissor = float(vl_share_raw) / 100 if vl_share_raw not in (None, "") else None
            ic_runoff = int(emissor.get('icRunOff', 0))

            # Inserção das linhas de limite solicitadas para o emissor
            for linha in emissor.get('linhas', []):
                vl_prazo = float(linha.get('vlPrazo'))
                vl_terceiros = float(linha.get('vlTerceiros', 0.0))
                vl_reserva_tecnica = float(linha.get('vlReservaTecnica', 0.0))

                linhas_descricao_params.append({
                    'idSolicitacao': id_solicitacao,
                    'idEmissor': id_emissor,
                    'cdRating': cd_rating_emissor,
                    'vlPrazo': vl_prazo,
                    'vlTerceiros': vl_terceiros,
                    'vlReservaTecnica': vl_reserva_tecnica,
                    'icRunOff': ic_runoff,
                    'vlShareDivida': vl_share_divida_emissor,
                    'icLimiteMeta': 0,
                    'dtVencimentoLimiteMeta': None
                })

            # Dados de limite meta
            meta = emissor.get('meta')
            if meta and isinstance(meta, dict) and meta.get('rows'):
                dt_vencimento_meta = meta.get('dtVencimento')
                cd_rating_meta = meta.get('cdRating', cd_rating_emissor)
                vl_share_meta_raw = meta.get('shareDivida')
                vl_share_divida_meta = float(vl_share_meta_raw) / 100 if vl_share_meta_raw not in (None, "") else vl_share_divida_emissor
                ic_runoff_meta = int(meta.get('icRunOff', ic_runoff))

                for row in meta.get('rows', []):
                    vl_prazo_meta = float(row.get('prazo') if row.get('prazo') is not None else row.get('vlPrazo'))
                    vl_terceiros_meta = float(row.get('terceirosProposto') if row.get('terceirosProposto') is not None else row.get('vlTerceiros', 0.0))
                    vl_reserva_tecnica_meta = float(row.get('rtProposto') if row.get('rtProposto') is not None else row.get('vlReservaTecnica', 0.0))

                    linhas_descricao_params.append({
                        'idSolicitacao': id_solicitacao,
                        'idEmissor': id_emissor,
                        'cdRating': cd_rating_meta,
                        'vlPrazo': vl_prazo_meta,
                        'vlTerceiros': vl_terceiros_meta,
                        'vlReservaTecnica': vl_reserva_tecnica_meta,
                        'icRunOff': ic_runoff_meta,
                        'vlShareDivida': vl_share_divida_meta,
                        'icLimiteMeta': 1,
                        'dtVencimentoLimiteMeta': dt_vencimento_meta
                    })

        # Executamos o update via exclusão e reinserção atômica no banco
        InsumosSolicitarAlcada.execute_update_solicitacao_completa(
            database=database,
            id_solicitacao=id_solicitacao,
            solicitacao_params=solicitacao_params,
            linhas_descricao_params=linhas_descricao_params
        )
    except Exception as e:
        raise e

