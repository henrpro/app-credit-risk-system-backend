# _______________________________ Geral _______________________________

query_get_solicitacoes_finalizadas = lambda database, mesa: f"""

    SELECT
        A.idSolicitacao,
        CAST(A.dtSolicitacao AS DATE) AS dtSolicitacao,
        E.dsNome,
        A.cdMesa AS dsProfile,
        B.dsGrupo,
        A.dsTipoEvento,
        C.dsStatus,
        F.dsAlcada
    FROM {database}.dbo.tCRS_0016_SolicitacoesAlcada A
    LEFT JOIN {database}.dbo.tCRS_0006_GrupoEconomicoCadastro B ON A.idGrupo = B.idGrupo
    LEFT JOIN {database}.dbo.tCRS_0015_StatusAlcada C ON A.idStatus = C.idStatus 
    LEFT JOIN {database}.dbo.tCRS_0001_UsuarioCadastro E ON A.cdUser = E.cdUser
    LEFT JOIN {database}.dbo.tCRS_0018_SolicitacoesAlcadaResposta F ON A.idSolicitacao = F.idSolicitacao
    WHERE {"A.cdMesa IN ('PRIVATE MARKETS', 'MESA CORE')" if mesa == 'ADMIN' else f"A.cdMesa = '{mesa}'"}
      AND (C.dsStatus IN ('Aprovado', 'Rejeitado') OR A.idStatus IN (4, 6))

"""

query_get_solicitacao_cabecalho = lambda database, id_solicitacao: f"""

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
    WHERE A.idSolicitacao = {id_solicitacao}

"""

query_get_descricao_solicitacao = lambda database, id_solicitacao: f"""

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
    WHERE A.idSolicitacao = {id_solicitacao}

"""