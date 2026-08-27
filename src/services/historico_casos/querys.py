query_get_solicitacoes_finalizadas = lambda database, mesa: f"""

    SELECT
        A.idSolicitacao,
        CAST(dtSolicitacao AS DATE) AS dtSolicitacao,
        E.dsNome,
        A.dsProfile,
        dsGrupo,
        dsTipoEvento,
        dsStatus,
        F.dsAlcada
    FROM {database}.dbo.tCRS_0018_SolicitacoesAlcada A
    LEFT JOIN {database}.dbo.tCRS_0005_GrupoEconomicoCadastro B ON A.idGrupo = B.idGrupo
    LEFT JOIN {database}.dbo.tCRS_0017_StatusCadastro C ON A.idStatus = C.idStatus 
    LEFT JOIN {database}.dbo.tCRS_0015_TipoEventoCadastro D ON A.idTipoEvento = D.idTipoEvento
    LEFT JOIN {database}.dbo.tCRS_0001_UsuarioCadastro E ON A.cdUser = E.cdUser
    LEFT JOIN {database}.dbo.tCRS_0021_SolicitacoesAlcadaResposta F ON A.idSolicitacao = F.idSolicitacao
    WHERE dsProfile = '{mesa}'
    AND dsStatus IN ('Aprovado', 'Rejeitado')

"""

query_get_descricao_solicitacao = lambda database, idsolicitacao: f"""

    SELECT 
        dsGrupo,
        E.cdRating AS cdRatingGrupo,
        A.vlShareDivida AS vlShareDividaGrupo,
        dsEmissor,
        F.cdRating AS cdRatingEmissor,
        B.vlShareDivida AS vlShareDividaEmissor,
        vlPrazo,
        vlTerceiros,
        vlReservaTecnica,
        icRunOff,
        icLimiteMeta,
        dtVencimentoLimiteMeta
    FROM {database}.dbo.tCRS_0018_SolicitacoesAlcada A
    LEFT JOIN {database}.dbo.tCRS_0019_SolicitacoesAlcadaDescricao B ON A.idSolicitacao = B.idSolicitacao
    LEFT JOIN {database}.dbo.tCRS_0005_GrupoEconomicoCadastro C ON A.idGrupo = C.idGrupo 
    LEFT JOIN {database}.dbo.tCRS_0006_EmissorCadastro D ON B.idEmissor = D.idEmissor
    LEFT JOIN {database}.dbo.tCRS_0016_RatingsDistintosCadastro E ON A.idRatingGrupo = E.idRating
    LEFT JOIN {database}.dbo.tCRS_0016_RatingsDistintosCadastro F ON B.idRating = F.idRating
    WHERE A.idSolicitacao = {idsolicitacao}

"""