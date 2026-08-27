# _______________________________ Geral _______________________________

query_get_aprovacoes_pendentes = lambda database: f"""

    SELECT 
        A.idSolicitacao,
        CAST(A.dtSolicitacao AS DATE) AS dtSolicitacao,
        B.dsGrupo,
        A.cdMesa,
        A.dsTipoEvento,
        E.dsNome
    FROM {database}.dbo.tCRS_0016_SolicitacoesAlcada A
    LEFT JOIN {database}.dbo.tCRS_0006_GrupoEconomicoCadastro B ON A.idGrupo = B.idGrupo
    LEFT JOIN {database}.dbo.tCRS_0015_StatusAlcada C ON A.idStatus = C.idStatus
    LEFT JOIN {database}.dbo.tCRS_0001_UsuarioCadastro E ON A.cdUser = E.cdUser
    WHERE C.dsStatus = 'Aprovação Pendente'
       OR A.idStatus = 3

"""

query_get_solicitacao_cabecalho = lambda database, ids_solicitacao_str: f"""

    SELECT 
        A.idSolicitacao,
        A.dtSolicitacao,
        A.cdUser,
        A.cdMesa,
        A.idGrupo,
        B.dsGrupo,
        A.cdRatingGrupo,
        A.vlShareDivida AS vlShareDividaGrupo,
        A.dsTipoEvento
    FROM {database}.dbo.tCRS_0016_SolicitacoesAlcada A
    LEFT JOIN {database}.dbo.tCRS_0006_GrupoEconomicoCadastro B ON A.idGrupo = B.idGrupo
    WHERE A.idSolicitacao IN ({ids_solicitacao_str})

"""

query_get_detalhes_solicitacao_descricao = lambda database, ids_solicitacao_str: f"""

    SELECT 
        A.idSolicitacao,
        B.cdMesa,
        A.idEmissor,
        D.dsEmissor,
        A.cdRating AS cdRatingEmissor,
        A.vlPrazo,
        A.vlTerceiros,
        A.vlReservaTecnica,
        A.icRunOff,
        A.vlShareDivida AS vlShareDividaEmissor,
        A.icLimiteMeta,
        CAST(A.dtVencimentoLimiteMeta AS DATE) AS dtVencimentoLimiteMeta
    FROM {database}.dbo.tCRS_0017_SolicitacoesAlcadaDescricao A
    LEFT JOIN {database}.dbo.tCRS_0016_SolicitacoesAlcada B ON A.idSolicitacao = B.idSolicitacao
    LEFT JOIN {database}.dbo.tCRS_0007_EmissorCadastro D ON A.idEmissor = D.idEmissor
    WHERE A.idSolicitacao IN ({ids_solicitacao_str})

"""

query_get_ratings_distintos = lambda database: f"""

    SELECT 
        idRating,
        cdRating
    FROM {database}.dbo.tCRS_0014_RatingsDistintos

"""

query_get_max_id_limite = lambda database: f"""

    SELECT ISNULL(MAX(idLimite), 0) AS max_id
    FROM (
        SELECT idLimite FROM {database}.dbo.tCRS_0019_LimitesAprovadosHistorico
        UNION ALL
        SELECT idLimite FROM {database}.dbo.tCRS_0020_LimitesVigentes
    ) AS T

"""

query_get_limites_vigentes_grupo = lambda database, grupo: f"""

    SELECT 
        A.idSolicitacao,
        A.idLimite,
        A.cdMesa,
        A.idGrupo,
        B.dsGrupo,
        A.idEmissor,
        C.dsEmissor,
        A.vlPrazo,
        A.vlTerceiros,
        A.vlReservaTecnica,
        A.icRunOff,
        A.icLimiteMeta,
        CAST(A.dtVencimento AS DATE) AS dtVencimento
    FROM {database}.dbo.tCRS_0020_LimitesVigentes A
    LEFT JOIN {database}.dbo.tCRS_0006_GrupoEconomicoCadastro B ON A.idGrupo = B.idGrupo
    LEFT JOIN {database}.dbo.tCRS_0007_EmissorCadastro C ON A.idEmissor = C.idEmissor
    WHERE B.dsGrupo = '{grupo}'

"""

query_get_ratings_vigentes_grupo = lambda database, grupo: f"""

    SELECT 
        B.dsGrupo AS dsEntidade,
        A.cdRatingGrupo AS cdRating,
        'Grupo' AS tipoEntidade,
        CAST(A.dtVencimento AS DATE) AS dtVencimento
    FROM {database}.dbo.tCRS_0024_RatingsVigentesGrupo A
    LEFT JOIN {database}.dbo.tCRS_0006_GrupoEconomicoCadastro B ON A.idGrupo = B.idGrupo
    WHERE B.dsGrupo = '{grupo}'

"""

query_get_ratings_vigentes_emissores = lambda database, grupo: f"""

    SELECT 
        C.dsEmissor AS dsEntidade,
        A.cdRating AS cdRating,
        'Emissor' AS tipoEntidade,
        CAST(A.dtVencimento AS DATE) AS dtVencimento
    FROM {database}.dbo.tCRS_0025_RatingsVigentesEmissor A
    LEFT JOIN {database}.dbo.tCRS_0007_EmissorCadastro C ON A.idEmissor = C.idEmissor
    LEFT JOIN {database}.dbo.tCRS_0006_GrupoEconomicoCadastro B ON C.idGrupo = B.idGrupo
    WHERE B.dsGrupo = '{grupo}'

"""

query_get_flexibilizacao_consumo_grupo = lambda database, id_grupo: f"""

    SELECT 
        A.cdMesa,
        A.idEmissor,
        B.dsEmissor,
        A.vlPrazo,
        A.vlFlexibilizado,
        A.vlLimite
    FROM {database}.dbo.tCRS_0021_FlexibilizacaoConsumo A
    LEFT JOIN {database}.dbo.tCRS_0007_EmissorCadastro B ON A.idEmissor = B.idEmissor
    WHERE B.idGrupo = {id_grupo}

"""

# _______________________________ Execução SQL _______________________________

query_update_status_solicitacao = lambda database, id_solicitacao, id_status: f"""

    UPDATE {database}.dbo.tCRS_0016_SolicitacoesAlcada
    SET idStatus = {id_status}
    WHERE idSolicitacao = {id_solicitacao}

"""

query_insert_limite_aprovado_historico = lambda database, id_solicitacao, id_limite, cd_mesa, id_grupo, id_emissor, vl_prazo, vl_terceiros, vl_reserva_tecnica, ic_runoff, dt_aprovacao, dt_vencimento, ic_limite_meta: f"""

    INSERT INTO {database}.dbo.tCRS_0019_LimitesAprovadosHistorico (
        idSolicitacao,
        idLimite,
        cdMesa,
        idGrupo,
        idEmissor,
        vlPrazo,
        vlTerceiros,
        vlReservaTecnica,
        icRunOff,
        dtAprovacao,
        dtVencimento,
        icLimiteMeta
    )
    VALUES (
        {id_solicitacao},
        {id_limite},
        '{cd_mesa}',
        {id_grupo},
        {id_emissor},
        {vl_prazo},
        {vl_terceiros},
        {vl_reserva_tecnica},
        {ic_runoff},
        '{dt_aprovacao}',
        '{dt_vencimento}',
        {ic_limite_meta}
    )

"""

query_delete_limites_vigentes_by_grupo_mesa = lambda database, id_grupo, cd_mesa: f"""

    DELETE FROM {database}.dbo.tCRS_0020_LimitesVigentes
    WHERE idGrupo = {id_grupo}
      AND cdMesa = '{cd_mesa}'

"""

query_insert_limite_vigente = lambda database, id_solicitacao, id_limite, cd_mesa, id_grupo, id_emissor, vl_prazo, vl_terceiros, vl_reserva_tecnica, ic_runoff, dt_aprovacao, dt_vencimento, ic_limite_meta: f"""

    INSERT INTO {database}.dbo.tCRS_0020_LimitesVigentes (
        idSolicitacao,
        idLimite,
        cdMesa,
        idGrupo,
        idEmissor,
        vlPrazo,
        vlTerceiros,
        vlReservaTecnica,
        icRunOff,
        dtAprovacao,
        dtVencimento,
        icLimiteMeta
    )
    VALUES (
        {id_solicitacao},
        {id_limite},
        '{cd_mesa}',
        {id_grupo},
        {id_emissor},
        {vl_prazo},
        {vl_terceiros},
        {vl_reserva_tecnica},
        {ic_runoff},
        '{dt_aprovacao}',
        '{dt_vencimento}',
        {ic_limite_meta}
    )

"""

query_insert_rating_grupo_historico = lambda database, id_solicitacao, id_grupo, cd_rating_grupo, dt_aprovacao, dt_vencimento: f"""

    INSERT INTO {database}.dbo.tCRS_0022_RatingsAprovadosGrupoHistorico (
        idSolicitacao,
        idGrupo,
        cdRatingGrupo,
        dtAprovacao,
        dtVencimento
    )
    VALUES (
        {id_solicitacao},
        {id_grupo},
        {f"'{cd_rating_grupo}'" if cd_rating_grupo is not None else 'NULL'},
        '{dt_aprovacao}',
        '{dt_vencimento}'
    )

"""

query_delete_rating_vigente_grupo = lambda database, id_grupo: f"""

    DELETE FROM {database}.dbo.tCRS_0024_RatingsVigentesGrupo
    WHERE idGrupo = {id_grupo}

"""

query_insert_rating_vigente_grupo = lambda database, id_solicitacao, id_grupo, cd_rating_grupo, dt_aprovacao, dt_vencimento: f"""

    INSERT INTO {database}.dbo.tCRS_0024_RatingsVigentesGrupo (
        idSolicitacao,
        idGrupo,
        cdRatingGrupo,
        dtAprovacao,
        dtVencimento
    )
    VALUES (
        {id_solicitacao},
        {id_grupo},
        {f"'{cd_rating_grupo}'" if cd_rating_grupo is not None else 'NULL'},
        '{dt_aprovacao}',
        '{dt_vencimento}'
    )

"""

query_insert_rating_emissor_historico = lambda database, id_solicitacao, id_emissor, cd_rating, dt_aprovacao, dt_vencimento: f"""

    INSERT INTO {database}.dbo.tCRS_0023_RatingsAprovadosEmissorHistorico (
        idSolicitacao,
        idEmissor,
        cdRating,
        dtAprovacao,
        dtVencimento
    )
    VALUES (
        {id_solicitacao},
        {id_emissor},
        {f"'{cd_rating}'" if cd_rating is not None else 'NULL'},
        '{dt_aprovacao}',
        '{dt_vencimento}'
    )

"""

query_delete_ratings_vigentes_emissores_grupo = lambda database, id_grupo: f"""

    DELETE A
    FROM {database}.dbo.tCRS_0025_RatingsVigentesEmissor A
    INNER JOIN {database}.dbo.tCRS_0007_EmissorCadastro B ON A.idEmissor = B.idEmissor
    WHERE B.idGrupo = {id_grupo}

"""

query_insert_rating_vigente_emissor = lambda database, id_solicitacao, id_emissor, cd_rating, dt_aprovacao, dt_vencimento: f"""

    INSERT INTO {database}.dbo.tCRS_0025_RatingsVigentesEmissor (
        idSolicitacao,
        idEmissor,
        cdRating,
        dtAprovacao,
        dtVencimento
    )
    VALUES (
        {id_solicitacao},
        {id_emissor},
        {f"'{cd_rating}'" if cd_rating is not None else 'NULL'},
        '{dt_aprovacao}',
        '{dt_vencimento}'
    )

"""

query_delete_flexibilizacao_consumo_grupo = lambda database, id_grupo: f"""

    DELETE A
    FROM {database}.dbo.tCRS_0021_FlexibilizacaoConsumo A
    INNER JOIN {database}.dbo.tCRS_0007_EmissorCadastro B ON A.idEmissor = B.idEmissor
    WHERE B.idGrupo = {id_grupo}

"""

query_insert_flexibilizacao_consumo = lambda database, cd_mesa, id_emissor, vl_prazo, vl_flexibilizado, vl_limite: f"""

    INSERT INTO {database}.dbo.tCRS_0021_FlexibilizacaoConsumo (
        cdMesa,
        idEmissor,
        vlPrazo,
        vlFlexibilizado,
        vlLimite
    )
    VALUES (
        '{cd_mesa}',
        {id_emissor},
        {vl_prazo},
        {vl_flexibilizado},
        {vl_limite}
    )

"""
