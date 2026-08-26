
# Importações do projeto
from services.grupos_economicos.insumos import InsumosGruposEconomicos
from services.solicitar_alcada.insumos import InsumosSolicitarAlcada

# Importações de bibliotecas
from datetime import date


def obtem_eventos_disponiveis(database: str, grupo: str, mesa: str):

    """
    Função que busca os eventos disponíveis para um determinado grupo econômico
    """

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


def realiza_insert_solicitacao_alcada(database: str, payload: dict):

    """
    Realiza o insert da solicitação de alçada, seus emissores, linhas de limite e limites meta.
    """

    try:
        # Extrai e valida o grupo econômico
        ds_grupo = payload.get('dsGrupo', '').strip()
        id_grupo = InsumosGruposEconomicos.get_id_grupo_by_name(database, ds_grupo)

        # Mapeamento de ratings
        df_ratings = InsumosSolicitarAlcada.get_ratings_distintos(database)
        mapeamento_ratings = dict(zip(df_ratings['cdRating'], df_ratings['idRating'])) if not df_ratings.empty else {}

        # Mapeamento de tipo de evento
        df_eventos = InsumosSolicitarAlcada.get_eventos_possiveis(database)
        mapeamento_eventos = dict(zip(df_eventos['dsTipoEvento'], df_eventos['idTipoEvento'])) if not df_eventos.empty else {}
        
        # Tipo de evento sendo solicitado, data e status 
        id_tipo_evento = mapeamento_eventos.get(payload.get('dsTipoEvento'))
        dt_solicitacao = date.today()
        id_status = 1

        # Dados do solicitante
        user = payload.get('cdUser')
        profile = payload.get('dsProfile')

        # Dados do grupo econômico solicitado
        rating_grupo = payload.get('cdRatingGrupo')
        id_rating_grupo = mapeamento_ratings.get(rating_grupo) 
        vl_share_divida = payload.get('vlShareDivida')
        vl_share_divida = float(vl_share_divida) if vl_share_divida not in (None, "") else None

        # Buscamos o max id solicitacao
        id_solicitacao = InsumosSolicitarAlcada.get_max_id_solicitacao(database) + 1

        # Inserimos os dados da solicitação do grupo econômico
        InsumosSolicitarAlcada.execute_insert_solicitacao_alcada(
            database=database,
            id_solicitacao=id_solicitacao,
            dt_solicitacao=dt_solicitacao,
            cd_user=user,
            ds_profile=profile,
            id_grupo=id_grupo,
            id_rating_grupo=id_rating_grupo,
            vl_share_divida=vl_share_divida,
            id_status=id_status,
            id_tipo_evento=id_tipo_evento
        )

        # Iteramos os emissores e inserimos as linhas e limites meta
        for emissor in payload.get('emissores', []):
            # Começamos buscando o emissor e seu id
            ds_emissor = emissor.get('dsEmissor', '').strip()
            id_emissor = InsumosGruposEconomicos.get_emissor_by_name(database, ds_emissor)

            # Agora buscamos o rating, share da dívida e se o emissor está em run-off
            cd_rating_emissor = emissor.get('cdRating')
            id_rating_emissor = mapeamento_ratings.get(cd_rating_emissor)
            vl_share_divida_emissor = emissor.get('vlShareDivida')
            vl_share_divida_emissor = float(vl_share_divida_emissor) if vl_share_divida_emissor not in (None, "") else None
            ic_runoff = emissor.get('icRunOff', 0)

            # Inserção das linhas de limite solicitadas para o emissor
            for linha in emissor.get('linhas', []):
                # Buscamos o prazo, valor terceiros e RT
                vl_prazo = linha.get('vlPrazo')
                vl_terceiros = linha.get('vlTerceiros', 0.0)
                vl_reserva_tecnica = linha.get('vlReservaTecnica', 0.0)

                # Inserimos os dados para o emissor
                InsumosSolicitarAlcada.execute_insert_solicitacao_alcada_descricao(
                    database=database,
                    id_solicitacao=id_solicitacao,
                    id_emissor=id_emissor,
                    id_rating=id_rating_emissor,
                    vl_prazo=vl_prazo,
                    vl_terceiros=vl_terceiros,
                    vl_reserva_tecnica=vl_reserva_tecnica,
                    ic_runoff=ic_runoff,
                    vl_share_divida=vl_share_divida_emissor
                )

            # Começamos buscando os dados de limite meta
            meta = emissor.get('meta')

            # Se tiver limite meta preenchido 
            if meta and isinstance(meta, dict) and meta.get('rows'):
                # Buscamos a data de vencimento do limite meta, rating e share da dívida
                dt_vencimento_meta = meta.get('dtVencimento')
                cd_rating_meta = meta.get('cdRating')
                id_rating_meta = mapeamento_ratings.get(cd_rating_meta)
                vl_share_divida_meta = meta.get('shareDivida')
                vl_share_divida_meta = float(vl_share_divida_meta) if vl_share_divida_meta not in (None, "") else None
                ic_runoff_meta = meta.get('icRunOff', ic_runoff)

                # Iteramos pelas linhas do limite meta
                for row in meta.get('rows', []):
                    # Buscamos o prazo, valor terceiros e RT
                    vl_prazo_meta = row.get('prazo') if row.get('prazo') is not None else row.get('vlPrazo')
                    vl_terceiros_meta = row.get('terceirosProposto') if row.get('terceirosProposto') is not None else row.get('vlTerceiros', 0.0)
                    vl_reserva_tecnica_meta = row.get('rtProposto') if row.get('rtProposto') is not None else row.get('vlReservaTecnica', 0.0)

                    # Inserimos os dados para o emissor
                    InsumosSolicitarAlcada.execute_insert_solicitacao_alcada_limite_meta_descricao(
                        database=database,
                        id_solicitacao=id_solicitacao,
                        id_emissor=id_emissor,
                        id_rating=id_rating_meta,
                        vl_prazo=vl_prazo_meta,
                        vl_terceiros=vl_terceiros_meta,
                        vl_reserva_tecnica=vl_reserva_tecnica_meta,
                        ic_runoff=ic_runoff_meta,
                        vl_share_divida=vl_share_divida_meta,
                        dt_vencimento_limite_meta=dt_vencimento_meta
                    )

    except Exception as e:
        raise e



