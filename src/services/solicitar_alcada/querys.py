
# _______________________________ Geral _______________________________

query_get_eventos_possiveis = lambda database: f"""

    SELECT *
    FROM {database}.dbo.tCRS_0015_TipoEventoCadastro

"""

query_get_ratings_distintos = lambda database: f"""

    SELECT *
    FROM {database}.dbo.tCRS_0016_RatingsDistintosCadastro

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
    FROM {database}.dbo.tCRS_0005_GrupoEconomicoCadastro A
    LEFT JOIN {database}.dbo.tCRS_0006_EmissorCadastro B ON A.idGrupo = B.idGrupo
    LEFT JOIN (
        SELECT *
        FROM {database}.dbo.tCRS_0023_LimitesVigentes
        WHERE cdMesa = '{mesa}'
    ) C ON B.idEmissor = C.idEmissor
    LEFT JOIN {database}.dbo.tCRS_0026_RatingsVigentesGrupo D ON A.idGrupo = D.idGrupo
    LEFT JOIN {database}.dbo.tCRS_0027_RatingsVigentesEmissor E ON B.idEmissor = E.idEmissor
    LEFT JOIN {database}.dbo.tCRS_0016_RatingsDistintosCadastro F ON D.idRating = F.idRating
    LEFT JOIN {database}.dbo.tCRS_0016_RatingsDistintosCadastro G ON E.idRating = G.idRating
    WHERE dsGrupo = '{grupo}'
    AND B.icConsomeHolding = 0

"""

query_get_max_id_solicitacao = lambda database: f"""

    SELECT ISNULL(MAX(idSolicitacao), 0) as max_id 
    FROM {database}.dbo.tCRS_0018_SolicitacoesAlcada

"""

query_get_prorrogacoes_recentes = lambda database, grupo, mesa: f"""

    SELECT *
    FROM {database}.dbo.tCRS_0005_GrupoEconomicoCadastro A
    LEFT JOIN {database}.dbo.tCRS_0018_SolicitacoesAlcada B ON A.idGrupo = B.idGrupo
    LEFT JOIN {database}.dbo.tCRS_0017_StatusCadastro C ON B.idStatus = C.idStatus
    LEFT JOIN {database}.dbo.tCRS_0015_TipoEventoCadastro D ON B.idTipoEvento = D.idTipoEvento
    WHERE dsTipoEvento = 'Prorrogação'
    AND dsStatus = 'Aprovado'
    AND dsGrupo = '{grupo}'
    AND dsProfile = '{mesa}'
    AND dtSolicitacao >= (
        SELECT MAX(dtAprovacao)
        FROM {database}.dbo.tCRS_0022_LimitesAprovadosHistorico A
        LEFT JOIN {database}.dbo.tCRS_0018_SolicitacoesAlcada B ON A.idSolicitacao = B.idSolicitacao
        LEFT JOIN {database}.dbo.tCRS_0015_TipoEventoCadastro C ON B.idTipoEvento = C.idTipoEvento
        LEFT JOIN {database}.dbo.tCRS_0005_GrupoEconomicoCadastro D ON A.idGrupo = D.idGrupo
        WHERE A.cdMesa = '{mesa}'
        AND D.dsGrupo = '{grupo}'
        AND C.dsTipoEvento IN ('Abertura de Limite', 'Renovação', 'Renovação com Downgrade de Rating', 'Renovação com Upgrade de Rating', 'Renovação com Downgrade de Rating + Run-Off', 'Renovação com Upgrade de Rating + Run-Off')
    )

"""

query_get_disponivel_flexibilizacao = lambda database, grupo, mesa: f"""

    SELECT 
        A.idEmissor,
        B.dsEmissor,
        B.idGrupo,
        C.dsGrupo,
        A.vlPrazo,
        (vlLimite - vlFlexibilizado) AS vlDisponivelFlex
    FROM {database}.dbo.tCRS_0028_FlexibilizacaoConsumo A
    LEFT JOIN {database}.dbo.tCRS_0006_EmissorCadastro B ON A.idEmissor = B.idEmissor
    LEFT JOIN {database}.dbo.tCRS_0005_GrupoEconomicoCadastro C ON B.idGrupo = C.idGrupo
    WHERE dsGrupo = '{grupo}'
    AND A.cdMesa = '{mesa}'
    AND (vlLimite - vlFlexibilizado) > 0

"""

# _______________________________ Insert _______________________________

query_insert_solicitacao_alcada = lambda database, id_solicitacao, dt_solicitacao, cd_user, ds_profile, id_grupo, id_rating_grupo, vl_share_divida, id_status, id_tipo_evento: f"""

    INSERT INTO {database}.dbo.tCRS_0018_SolicitacoesAlcada (
        idSolicitacao,
        dtSolicitacao,
        cdUser,
        dsProfile,
        idGrupo,
        idRatingGrupo,
        vlShareDivida,
        idStatus,
        idTipoEvento
    )
    VALUES (
        {id_solicitacao},
        {f"'{dt_solicitacao}'"},
        {f"'{cd_user}'"},
        {f"'{ds_profile}'"},
        {id_grupo},
        {id_rating_grupo if id_rating_grupo is not None else 'NULL'},
        {vl_share_divida if vl_share_divida is not None else 'NULL'},
        {id_status},
        {id_tipo_evento}
    )

"""

query_insert_solicitacao_alcada_descricao = lambda database, id_solicitacao, id_emissor, id_rating, vl_prazo, vl_terceiros, vl_reserva_tecnica, ic_runoff, vl_share_divida: f"""

    INSERT INTO {database}.dbo.tCRS_0019_SolicitacoesAlcadaDescricao (
        idSolicitacao,
        idEmissor,
        idRating,
        vlPrazo,
        vlTerceiros,
        vlReservaTecnica,
        icRunOff,
        vlShareDivida
    )
    VALUES (
        {id_solicitacao},
        {id_emissor},
        {id_rating if id_rating is not None else 'NULL'},
        {vl_prazo},
        {vl_terceiros},
        {vl_reserva_tecnica},
        {ic_runoff},
        {vl_share_divida if vl_share_divida is not None else 'NULL'}
    )

"""

query_insert_solicitacao_alcada_limite_meta_descricao = lambda database, id_solicitacao, id_emissor, id_rating, vl_prazo, vl_terceiros, vl_reserva_tecnica, ic_runoff, vl_share_divida, dt_vencimento_limite_meta: f"""

    INSERT INTO {database}.dbo.tCRS_0020_SolicitacoesAlcadaLimiteMetaDescricao (
        idSolicitacao,
        idEmissor,
        idRating,
        vlPrazo,
        vlTerceiros,
        vlReservaTecnica,
        icRunOff,
        vlShareDivida,
        dtVencimentoLimiteMeta
    )
    VALUES (
        {id_solicitacao},
        {id_emissor},
        {id_rating if id_rating is not None else 'NULL'},
        {vl_prazo},
        {vl_terceiros},
        {vl_reserva_tecnica},
        {ic_runoff},
        {vl_share_divida if vl_share_divida is not None else 'NULL'},
        {f"'{dt_vencimento_limite_meta}'"}
    )

"""
