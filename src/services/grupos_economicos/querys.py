
query_get_grupos_economicos_distintos = lambda database: f"""

    SELECT DISTINCT dsGrupo
    FROM {database}.dbo.tCRS_0005_GrupoEconomicoCadastro

"""


query_get_setores_distintos = lambda database: f"""

    SELECT DISTINCT dsSetor
    FROM {database}.dbo.tCRS_0003_SetorCadastro

"""


query_get_subsetores_distintos = lambda database: f"""

    SELECT DISTINCT dsSubsetor
    FROM {database}.dbo.tCRS_0004_SubsetorCadastro

"""


query_get_grupo_economico = lambda database, grupo: f"""

    SELECT 
        dsGrupo,
        cdCnpj,
        dsEmissor,
        icHolding,
        icConsomeHolding,
        idEmissorHoldingConsumo,
        dsSetor,
        dsSubsetor
    FROM {database}.dbo.tCRS_0005_GrupoEconomicoCadastro A
    LEFT JOIN {database}.dbo.tCRS_0006_EmissorCadastro B ON A.idGrupo = B.idGrupo
    LEFT JOIN {database}.dbo.tCRS_0003_SetorCadastro C ON B.idSetor = C.idSetor
    LEFT JOIN {database}.dbo.tCRS_0004_SubsetorCadastro D ON B.idSubsetor = D.idSubsetor
    WHERE dsGrupo = '{grupo}'

"""
