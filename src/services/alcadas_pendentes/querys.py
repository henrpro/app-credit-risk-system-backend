
query_get_alcadas_pendentes = lambda database: f"""

    SELECT 
        idSolicitacao,
        CAST(dtSolicitacao AS DATE) AS dtSolicitacao,
        dsGrupo,
        dsProfile,
        dsTipoEvento
    FROM {database}.dbo.tCRS_0016_SolicitacoesAlcada A
    LEFT JOIN {database}.dbo.tCRS_0006_GrupoEconomicoCadastro B ON A.idGrupo = B.idGrupo
    LEFT JOIN {database}.dbo.tCRS_0015_StatusAlcada C ON A.idStatus = C.idStatus
    LEFT JOIN {database}.dbo.tCRS_0013_TipoEvento D ON A.idTipoEvento = D.idTipoEvento
    WHERE dsStatus = 'Alçada Pendente'

"""

query_get_detalhes_solicitacao = lambda database, idsolicitacao: f"""

    SELECT 
        G.dsTipoEvento,
        dsGrupo,
        f.cdRating AS cdRatingGrupo,
        B.vlShareDivida AS vlShareDividaGrupo,
        dsEmissor,
        E.cdRating AS cdRatingEmissor,
        icRunOff,
        A.vlShareDivida AS vlShareDividaEmissor,
        vlPrazo,
        vlTerceiros,
        vlReservaTecnica
    FROM {database}.dbo.tCRS_0017_SolicitacoesAlcadaDescricao A
    LEFT JOIN {database}.dbo.tCRS_0016_SolicitacoesAlcada B ON A.idSolicitacao = B.idSolicitacao
    LEFT JOIN {database}.dbo.tCRS_0006_GrupoEconomicoCadastro C ON B.idGrupo = C.idGrupo
    LEFT JOIN {database}.dbo.tCRS_0007_EmissorCadastro D ON A.idEmissor = D.idEmissor
    LEFT JOIN {database}.dbo.tCRS_0013_TipoEvento G ON B.idTipoEvento = G.idTipoEvento
    WHERE A.idSolicitacao = {idsolicitacao}

"""

query_get_detalhes_limite_meta_solicitacao = lambda database, idsolicitacao: f"""

    SELECT 
        G.dsTipoEvento,
        dsGrupo,
        f.cdRating AS cdRatingGrupo,
        B.vlShareDivida AS vlShareDividaGrupo,
        dsEmissor,
        E.cdRating AS cdRatingEmissor,
        icRunOff,
        A.vlShareDivida AS vlShareDividaEmissor,
        vlPrazo,
        vlTerceiros,
        vlReservaTecnica
    FROM {database}.dbo.tCRS_0019_SolicitacoesAlcadaDescricao A
    LEFT JOIN {database}.dbo.tCRS_0020_SolicitacoesAlcadaLimiteMetaDescricao B ON A.idSolicitacao = B.idSolicitacao
    LEFT JOIN {database}.dbo.tCRS_0005_GrupoEconomicoCadastro C ON B.idGrupo = C.idGrupo
    LEFT JOIN {database}.dbo.tCRS_0006_EmissorCadastro D ON A.idEmissor = D.idEmissor
    LEFT JOIN {database}.dbo.tCRS_0016_RatingsDistintosCadastro E ON A.idRating = E.idRating
    LEFT JOIN {database}.dbo.tCRS_0016_RatingsDistintosCadastro F ON B.idRatingGrupo = F.idRating
    LEFT JOIN {database}.dbo.tCRS_0015_TipoEventoCadastro G ON B.idTipoEvento = G.idTipoEvento
    WHERE A.idSolicitacao = {idsolicitacao}

"""

query_get_limites_vigentes = lambda database, grupo: f"""

    SELECT 
        cdMesa,
        dsEmissor,
        vlPrazo,
        vlTerceiros,
        vlReservaTecnica,
        icRunOff,
        icLimiteMeta,
        dtVencimento
    FROM {database}.dbo.tCRS_0023_LimitesVigentes A
    LEFT JOIN {database}.dbo.tCRS_0005_GrupoEconomicoCadastro B ON A.idGrupo = B.idGrupo
    LEFT JOIN {database}.dbo.tCRS_0006_EmissorCadastro C ON A.idEmissor = C.idEmissor
    WHERE dsGrupo = '{grupo}'

"""

query_outras_solicitacoes_pendentes = lambda database, grupo, solicitacao: f"""


"""