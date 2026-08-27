# _______________________________ Geral _______________________________

query_get_solicitacoes_pendentes = lambda database, mesa: f"""

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
      AND C.dsStatus IN ('Alçada Pendente', 'Em Discussão', 'Aprovação Pendente')

"""

# _______________________________ Update _______________________________

update_status_aprovacao_pendente = lambda database, idsolicitacao: f"""

    UPDATE {database}.dbo.tCRS_0016_SolicitacoesAlcada
    SET idStatus = 3
    WHERE idSolicitacao = {idsolicitacao}

"""

update_status_cancelar_solicitacao = lambda database, idsolicitacao: f"""

    UPDATE {database}.dbo.tCRS_0016_SolicitacoesAlcada
    SET idStatus = 5
    WHERE idSolicitacao = {idsolicitacao}

"""