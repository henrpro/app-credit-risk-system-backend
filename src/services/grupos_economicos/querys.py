
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
        dsSetor,
        dsSubsetor
    FROM {database}.dbo.tCRS_0005_GrupoEconomicoCadastro A
    LEFT JOIN {database}.dbo.tCRS_0006_EmissorCadastro B ON A.idGrupo = B.idGrupo
    LEFT JOIN {database}.dbo.tCRS_0003_SetorCadastro C ON B.idSetor = C.idSetor
    LEFT JOIN {database}.dbo.tCRS_0004_SubsetorCadastro D ON B.idSubsetor = D.idSubsetor
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


query_insert_grupo_economico = lambda database, id_grupo, ds_grupo: f"""

    INSERT INTO {database}.dbo.tCRS_0005_GrupoEconomicoCadastro (idGrupo, dsGrupo)
    VALUES ({id_grupo}, '{ds_grupo}')

"""


query_get_max_id_grupo = lambda database: f"""

    SELECT ISNULL(MAX(idGrupo), 0) as max_id 
    FROM {database}.dbo.tCRS_0005_GrupoEconomicoCadastro

"""

query_get_max_id_emissor = lambda database: f"""

    SELECT ISNULL(MAX(idEmissor), 0) as max_id 
    FROM {database}.dbo.tCRS_0006_EmissorCadastro

"""


query_get_id_emissor_by_name = lambda database, ds_emissor, exclude_id_emissor=None: f"""
    SELECT idEmissor 
    FROM {database}.dbo.tCRS_0006_EmissorCadastro
    WHERE dsEmissor = '{ds_emissor}'
    {f"AND idEmissor != {exclude_id_emissor}" if exclude_id_emissor else ""}
"""


query_get_id_emissor_by_cnpj = lambda database, cd_cnpj, exclude_id_emissor=None: f"""
    SELECT idEmissor 
    FROM {database}.dbo.tCRS_0006_EmissorCadastro
    WHERE cdCnpj = '{cd_cnpj}'
    {f"AND idEmissor != {exclude_id_emissor}" if exclude_id_emissor else ""}
"""


query_get_id_grupo_by_name = lambda database, ds_grupo, exclude_id_grupo=None: f"""

    SELECT idGrupo 
    FROM {database}.dbo.tCRS_0005_GrupoEconomicoCadastro
    WHERE dsGrupo = '{ds_grupo}'
    {f"AND idGrupo != {exclude_id_grupo}" if exclude_id_grupo else ""}
    
"""


query_get_id_setor_by_name = lambda database, ds_setor: f"""

    SELECT idSetor 
    FROM {database}.dbo.tCRS_0003_SetorCadastro
    WHERE dsSetor = '{ds_setor}'

"""


query_get_id_subsetor_by_name = lambda database, ds_subsetor: f"""

    SELECT idSubsetor 
    FROM {database}.dbo.tCRS_0004_SubsetorCadastro
    WHERE dsSubsetor = '{ds_subsetor}'

"""


query_insert_emissor = lambda database, id_emissor, cd_cnpj, ds_emissor, ic_holding, ic_consome_holding, id_holding, id_grupo, id_setor, id_subsetor: f"""

    INSERT INTO {database}.dbo.tCRS_0006_EmissorCadastro (idEmissor, cdCnpj, dsEmissor, icHolding, icConsomeHolding, idEmissorHoldingConsumo, idGrupo, idSetor, idSubsetor)
    VALUES ({id_emissor}, {'NULL' if not cd_cnpj else f"'{cd_cnpj}'"}, '{ds_emissor}', {ic_holding}, {ic_consome_holding}, {id_holding if id_holding else 'NULL'}, {id_grupo}, {id_setor if id_setor else 'NULL'}, {id_subsetor if id_subsetor else 'NULL'})

"""


query_update_holding_consumo = lambda database, ds_emissor, id_holding: f"""
    
    UPDATE {database}.dbo.tCRS_0006_EmissorCadastro
    SET idEmissorHoldingConsumo = {id_holding if id_holding else 'NULL'}
    WHERE dsEmissor = '{ds_emissor}'

"""


query_insert_emissor_oc3 = lambda database, id_emissor, cd_oc3: f"""
    
    INSERT INTO {database}.dbo.tCRS_0007_EmissorOC3 (idEmissor, cdEmissorOC3)
    VALUES ({id_emissor}, '{cd_oc3}')

"""


query_insert_emissor_crims = lambda database, id_emissor, cd_crims: f"""
    
    INSERT INTO {database}.dbo.tCRS_0008_EmissorCRIMS (idEmissor, cdEmissorCRIMS)
    VALUES ({id_emissor}, '{cd_crims}')

"""


query_clear_holding_consumo_by_grupo = lambda database, id_grupo: f"""
    
    UPDATE {database}.dbo.tCRS_0006_EmissorCadastro
    SET idEmissorHoldingConsumo = NULL
    WHERE idGrupo = {id_grupo}

"""


query_delete_emissores_oc3_by_grupo = lambda database, id_grupo: f"""
    
    DELETE 
    FROM {database}.dbo.tCRS_0007_EmissorOC3
    WHERE idEmissor IN (SELECT idEmissor FROM {database}.dbo.tCRS_0006_EmissorCadastro WHERE idGrupo = {id_grupo})

"""


query_delete_emissores_crims_by_grupo = lambda database, id_grupo: f"""
    
    DELETE 
    FROM {database}.dbo.tCRS_0008_EmissorCRIMS
    WHERE idEmissor IN (SELECT idEmissor FROM {database}.dbo.tCRS_0006_EmissorCadastro WHERE idGrupo = {id_grupo})

"""


query_delete_emissores_by_grupo = lambda database, id_grupo: f"""
    
    DELETE 
    FROM {database}.dbo.tCRS_0006_EmissorCadastro
    WHERE idGrupo = {id_grupo}

"""


query_delete_grupo = lambda database, id_grupo: f"""

    DELETE 
    FROM {database}.dbo.tCRS_0005_GrupoEconomicoCadastro
    WHERE idGrupo = {id_grupo}

"""


query_delete_emissor_oc3 = lambda database, id_emissor: f"""

    DELETE 
    FROM {database}.dbo.tCRS_0007_EmissorOC3
    WHERE idEmissor = {id_emissor}

"""


query_delete_emissor_crims = lambda database, id_emissor: f"""

    DELETE 
    FROM {database}.dbo.tCRS_0008_EmissorCRIMS
    WHERE idEmissor = {id_emissor}

"""


query_delete_emissor_cadastro = lambda database, id_emissor: f"""

    DELETE 
    FROM {database}.dbo.tCRS_0006_EmissorCadastro
    WHERE idEmissor = {id_emissor}

"""


query_delete_grupo_economico_cadastro = lambda database, id_grupo: f"""
    
    DELETE FROM {database}.dbo.tCRS_0005_GrupoEconomicoCadastro
    WHERE idGrupo = {id_grupo}

"""
