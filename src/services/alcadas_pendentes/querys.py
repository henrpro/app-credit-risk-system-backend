# _______________________________ Geral _______________________________

query_get_alcadas_pendentes = lambda database: f"""

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
    WHERE C.dsStatus = 'Alçada Pendente'
       OR A.idStatus = 1

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

query_get_limites_vigentes_grupo = lambda database, grupo: f"""

    SELECT 
        A.cdMesa,
        B.dsGrupo,
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

# _______________________________ Execução SQL _______________________________

query_insert_resposta_alcada = lambda database, id_solicitacao, ds_alcada, dt_resposta, cd_user_resposta: f"""

    INSERT INTO {database}.dbo.tCRS_0018_SolicitacoesAlcadaResposta (
        idSolicitacao,
        dsAlcada,
        dtResposta,
        cdUserResposta
    )
    VALUES (
        {id_solicitacao},
        {f"'{ds_alcada}'" if ds_alcada is not None else 'NULL'},
        '{dt_resposta}',
        {f"'{cd_user_resposta}'" if cd_user_resposta is not None else 'NULL'}
    )

"""

query_update_status_solicitacao = lambda database, id_solicitacao, id_status: f"""

    UPDATE {database}.dbo.tCRS_0016_SolicitacoesAlcada
    SET idStatus = {id_status}
    WHERE idSolicitacao = {id_solicitacao}

"""