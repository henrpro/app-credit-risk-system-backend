# _______________________________ Geral _______________________________

query_get_id_grupo_by_name = lambda database, grupo: f"""

    SELECT idGrupo 
    FROM {database}.dbo.tCRS_0006_GrupoEconomicoCadastro 
    WHERE dsGrupo = '{grupo}'

"""

query_get_emissor_by_name = lambda database, emissor: f"""

    SELECT idEmissor 
    FROM {database}.dbo.tCRS_0007_EmissorCadastro 
    WHERE dsEmissor = '{emissor}'

"""

query_get_eventos_possiveis = lambda database: f"""

    SELECT *
    FROM {database}.dbo.tCRS_0013_TipoEvento

"""

query_get_ratings_distintos = lambda database: f"""

    SELECT *
    FROM {database}.dbo.tCRS_0014_RatingsDistintos

"""

query_get_limites_aprovados_by_grupo = lambda database, grupo, mesa: f"""

    SELECT 
        A.idGrupo,
        A.dsGrupo,
        B.idEmissor,
        B.dsEmissor,
        C.vlPrazo,
        C.vlTerceiros,
        C.vlReservaTecnica,
        F.cdRating AS cdRatingGrupo,
        G.cdRating As cdRatingEmissor
    FROM {database}.dbo.tCRS_0006_GrupoEconomicoCadastro A
    LEFT JOIN {database}.dbo.tCRS_0007_EmissorCadastro B ON A.idGrupo = B.idGrupo
    LEFT JOIN (
        SELECT *
        FROM {database}.dbo.tCRS_0020_LimitesVigentes
        WHERE cdMesa = '{mesa}'
    ) C ON B.idEmissor = C.idEmissor
    LEFT JOIN {database}.dbo.tCRS_0024_RatingsVigentesGrupo D ON A.idGrupo = D.idGrupo
    LEFT JOIN {database}.dbo.tCRS_0025_RatingsVigentesEmissor E ON B.idEmissor = E.idEmissor
    LEFT JOIN {database}.dbo.tCRS_0014_RatingsDistintos F ON D.cdRatingGrupo = F.cdRating
    LEFT JOIN {database}.dbo.tCRS_0014_RatingsDistintos G ON E.cdRating = G.cdRating
    WHERE A.dsGrupo = '{grupo}'
      AND B.icConsomeHolding = 0

"""

query_get_max_id_solicitacao = lambda database: f"""

    SELECT ISNULL(MAX(idSolicitacao), 0) AS max_id 
    FROM {database}.dbo.tCRS_0016_SolicitacoesAlcada

"""

query_get_prorrogacoes_recentes = lambda database, grupo, mesa: f"""

    SELECT *
    FROM {database}.dbo.tCRS_0006_GrupoEconomicoCadastro A
    LEFT JOIN {database}.dbo.tCRS_0016_SolicitacoesAlcada B ON A.idGrupo = B.idGrupo
    LEFT JOIN {database}.dbo.tCRS_0015_StatusAlcada C ON B.idStatus = C.idStatus
    WHERE B.dsTipoEvento = 'Prorrogação'
      AND C.dsStatus = 'Aprovado'
      AND A.dsGrupo = '{grupo}'
      AND B.cdMesa = '{mesa}'
      AND B.dtSolicitacao >= (
          SELECT MAX(A.dtAprovacao)
          FROM {database}.dbo.tCRS_0019_LimitesAprovadosHistorico A
          LEFT JOIN {database}.dbo.tCRS_0016_SolicitacoesAlcada B ON A.idSolicitacao = B.idSolicitacao
          LEFT JOIN {database}.dbo.tCRS_0006_GrupoEconomicoCadastro D ON A.idGrupo = D.idGrupo
          WHERE A.cdMesa = '{mesa}'
            AND D.dsGrupo = '{grupo}'
            AND B.dsTipoEvento IN ('Abertura de Limite', 'Renovação', 'Renovação com Downgrade de Rating', 'Renovação com Upgrade de Rating', 'Renovação com Downgrade de Rating + Run-Off', 'Renovação com Upgrade de Rating + Run-Off')
      )

"""

query_get_disponivel_flexibilizacao = lambda database, grupo, mesa: f"""

    SELECT 
        A.idEmissor,
        B.dsEmissor,
        B.idGrupo,
        C.dsGrupo,
        A.vlPrazo,
        (A.vlLimite - A.vlFlexibilizado) AS vlDisponivelFlex
    FROM {database}.dbo.tCRS_0021_FlexibilizacaoConsumo A
    LEFT JOIN {database}.dbo.tCRS_0007_EmissorCadastro B ON A.idEmissor = B.idEmissor
    LEFT JOIN {database}.dbo.tCRS_0006_GrupoEconomicoCadastro C ON B.idGrupo = C.idGrupo
    WHERE C.dsGrupo = '{grupo}'
      AND A.cdMesa = '{mesa}'
      AND (A.vlLimite - A.vlFlexibilizado) > 0

"""

# _______________________________ Insert _______________________________

query_insert_solicitacao_alcada = lambda database, id_solicitacao, dt_solicitacao, cd_user, cd_mesa, id_grupo, cd_rating_grupo, vl_share_divida, id_status, ds_tipo_evento: f"""

    INSERT INTO {database}.dbo.tCRS_0016_SolicitacoesAlcada (
        idSolicitacao,
        dtSolicitacao,
        cdUser,
        cdMesa,
        idGrupo,
        cdRatingGrupo,
        vlShareDivida,
        idStatus,
        dsTipoEvento
    )
    VALUES (
        {id_solicitacao},
        '{dt_solicitacao}',
        '{cd_user}',
        '{cd_mesa}',
        {id_grupo},
        {f"'{cd_rating_grupo}'" if cd_rating_grupo is not None else 'NULL'},
        {vl_share_divida if vl_share_divida is not None else 'NULL'},
        {id_status},
        '{ds_tipo_evento}'
    )

"""

query_insert_solicitacao_alcada_descricao = lambda database, id_solicitacao, id_emissor, cd_rating, vl_prazo, vl_terceiros, vl_reserva_tecnica, ic_runoff, vl_share_divida, ic_limite_meta, dt_vencimento_limite_meta: f"""

    INSERT INTO {database}.dbo.tCRS_0017_SolicitacoesAlcadaDescricao (
        idSolicitacao,
        idEmissor,
        cdRating,
        vlPrazo,
        vlTerceiros,
        vlReservaTecnica,
        icRunOff,
        vlShareDivida,
        icLimiteMeta,
        dtVencimentoLimiteMeta
    )
    VALUES (
        {id_solicitacao},
        {id_emissor},
        {f"'{cd_rating}'" if cd_rating is not None else 'NULL'},
        {vl_prazo},
        {vl_terceiros},
        {vl_reserva_tecnica},
        {ic_runoff},
        {vl_share_divida if vl_share_divida is not None else 'NULL'},
        {ic_limite_meta},
        {f"'{dt_vencimento_limite_meta}'" if dt_vencimento_limite_meta is not None else 'NULL'}
    )

"""

# _______________________________ Consulta e Delete por ID _______________________________

query_get_solicitacao_cabecalho_by_id = lambda database, id_solicitacao: f"""

    SELECT 
        A.idSolicitacao,
        A.dtSolicitacao,
        A.cdUser,
        A.cdMesa,
        A.idGrupo,
        B.dsGrupo,
        A.cdRatingGrupo,
        A.vlShareDivida,
        A.idStatus,
        A.dsTipoEvento
    FROM {database}.dbo.tCRS_0016_SolicitacoesAlcada A
    LEFT JOIN {database}.dbo.tCRS_0006_GrupoEconomicoCadastro B ON A.idGrupo = B.idGrupo
    WHERE A.idSolicitacao = {id_solicitacao}

"""

query_get_solicitacao_descricao_by_id = lambda database, id_solicitacao: f"""

    SELECT 
        A.idSolicitacao,
        A.idEmissor,
        B.dsEmissor,
        A.cdRating,
        A.vlPrazo,
        A.vlTerceiros,
        A.vlReservaTecnica,
        A.icRunOff,
        A.vlShareDivida,
        A.icLimiteMeta,
        CAST(A.dtVencimentoLimiteMeta AS DATE) AS dtVencimentoLimiteMeta
    FROM {database}.dbo.tCRS_0017_SolicitacoesAlcadaDescricao A
    LEFT JOIN {database}.dbo.tCRS_0007_EmissorCadastro B ON A.idEmissor = B.idEmissor
    WHERE A.idSolicitacao = {id_solicitacao}
    ORDER BY A.idEmissor, A.icLimiteMeta, A.vlPrazo

"""

query_delete_solicitacao_alcada_resposta = lambda database, id_solicitacao: f"""

    DELETE FROM {database}.dbo.tCRS_0018_SolicitacoesAlcadaResposta
    WHERE idSolicitacao = {id_solicitacao}

"""

query_delete_solicitacao_alcada_descricao = lambda database, id_solicitacao: f"""

    DELETE FROM {database}.dbo.tCRS_0017_SolicitacoesAlcadaDescricao
    WHERE idSolicitacao = {id_solicitacao}

"""

query_delete_solicitacao_alcada_cabecalho = lambda database, id_solicitacao: f"""

    DELETE FROM {database}.dbo.tCRS_0016_SolicitacoesAlcada
    WHERE idSolicitacao = {id_solicitacao}

"""


