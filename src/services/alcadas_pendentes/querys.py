
query_get_alcadas_pendentes = lambda database: f"""

    SELECT 
        idSolicitacao,
        CAST(dtSolicitacao AS DATE) AS dtSolicitacao,
        dsGrupo,
        dsProfile,
        dsTipoEvento
    FROM {database}.dbo.tCRS_0018_SolicitacoesAlcada A
    LEFT JOIN {database}.dbo.tCRS_0005_GrupoEconomicoCadastro B ON A.idGrupo = B.idGrupo
    LEFT JOIN {database}.dbo.tCRS_0017_StatusCadastro C ON A.idStatus = C.idStatus
    LEFT JOIN {database}.dbo.tCRS_0015_TipoEventoCadastro D ON A.idTipoEvento = D.idTipoEvento
    WHERE dsStatus = 'Alçada Pendente'

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