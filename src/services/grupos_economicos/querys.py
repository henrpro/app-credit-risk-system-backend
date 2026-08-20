
query_get_setores_distintos = lambda database: f"""

    SELECT DISTINCT dsSetor
    FROM {database}.dbo.tCRS_0003_SetorCadastro

"""


query_get_subsetores_distintos = lambda database: f"""

    SELECT DISTINCT dsSubsetor
    FROM {database}.dbo.tCRS_0004_SubsetorCadastro

"""


query_get_grupos_economicos_distintos = lambda database: f"""

    SELECT DISTINCT dsGrupo
    FROM {database}.dbo.tCRS_0005_GrupoEconomicoCadastro

"""


query_get_codigo_emissor_oc3 = lambda emissor: f"""

    --Escrever a query aqui

"""


query_get_codigo_emissor_crims = lambda emissor: f"""

    --Escrever a query aqui

"""


query_get_grupo_economico = lambda database, grupo: f"""

    SELECT 
        dsGrupo,
        cdCnpj,
        idEmissor,
        dsEmissor,
        icHolding,
        icConsomeHolding,
        idEmissorHoldingConsumo,
        dsSetor
    FROM {database}.dbo.tCRS_0005_GrupoEconomicoCadastro A
    LEFT JOIN {database}.dbo.tCRS_0006_EmissorCadastro B ON A.idGrupo = B.idGrupo
    LEFT JOIN {database}.dbo.tCRS_0003_SetorCadastro C ON B.idSetor = C.idSetor
    WHERE dsGrupo = '{grupo}'

"""


query_get_emissores_oc3 = lambda database, id_emissor: f"""

    SELECT DISTINCT cdEmissorOC3
    FROM CRS.dbo.tCRS_0007_EmissorOC3
    WHERE idEmissor = {id_emissor}

"""


query_get_emissores_crims = lambda database, id_emissor: f"""

    SELECT DISTINCT cdEmissorCRIMS
    FROM CRS.dbo.tCRS_0008_EmissorCRIMS
    WHERE idEmissor = {id_emissor}

"""


query_get_ativos_consumo = lambda database, id_emissor: f"""

    SELECT 
        cdAtivo,
        vlPcConsumo
    FROM CRS.dbo.tCRS_0013_MapeamentoConsumoAtivos
    WHERE idEmissor = {id_emissor}

"""


