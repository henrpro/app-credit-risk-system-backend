query_get_solicitacoes_pendentes = lambda database, mesa: f"""

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
    WHERE {"dsProfile IN ('PRIVATE MARKETS', 'MESA CORE')" if mesa == 'ADMIN' else f"dsProfile = '{mesa}'"}
    AND dsStatus IN ('Alçada Pendente', 'Em Discussão', 'Aprovação Pendente')

"""

update_status_aprovacao_pendente = lambda database, idsolicitacao: f"""

    UPDATE {database}.dbo.tCRS_0018_SolicitacoesAlcada
    SET idStatus = 3
    WHERE idSolicitacao = {idsolicitacao}

"""

update_status_cancelar_solicitacao = lambda database, idsolicitacao: f"""

    UPDATE {database}.dbo.tCRS_0018_SolicitacoesAlcada
    SET idStatus = 5
    WHERE idSolicitacao = {idsolicitacao}

"""