

# _______________________________ Geral _______________________________

query_get_grupos_economicos_distintos = lambda database: f"""

    SELECT DISTINCT dsGrupo
    FROM {database}.dbo.tCRS_0006_GrupoEconomicoCadastro

"""

query_get_setores_distintos = lambda database: f"""

    SELECT DISTINCT dsSetor
    FROM {database}.dbo.tCRS_0005_SetorCadastro

"""


query_get_id_setor_by_name = lambda database, ds_setor: f"""

    SELECT idSetor 
    FROM {database}.dbo.tCRS_0005_SetorCadastro
    WHERE dsSetor = '{ds_setor}'

"""

query_get_id_grupo_by_name = lambda database, ds_grupo, exclude_id_grupo=None: f"""

    SELECT idGrupo 
    FROM {database}.dbo.tCRS_0006_GrupoEconomicoCadastro
    WHERE dsGrupo = '{ds_grupo}'
    {f"AND idGrupo != {exclude_id_grupo}" if exclude_id_grupo else ""}
    
"""

query_get_id_emissor_by_name = lambda database, ds_emissor, exclude_id_emissor=None: f"""

    SELECT idEmissor 
    FROM {database}.dbo.tCRS_0007_EmissorCadastro
    WHERE dsEmissor = '{ds_emissor}'
    {f"AND idEmissor != {exclude_id_emissor}" if exclude_id_emissor else ""}

"""

query_get_max_id_grupo = lambda database: f"""

    SELECT ISNULL(MAX(idGrupo), 0) as max_id 
    FROM {database}.dbo.tCRS_0006_GrupoEconomicoCadastro

"""

query_get_max_id_emissor = lambda database: f"""

    SELECT ISNULL(MAX(idEmissor), 0) as max_id 
    FROM {database}.dbo.tCRS_0007_EmissorCadastro

"""

# _______________________________ Cadastrar Grupo _______________________________

query_get_codigo_emissor_oc3 = lambda emissor: f"""

    --Escrever a query aqui

"""

query_get_codigo_emissor_crims = lambda emissor: f"""

    --Escrever a query aqui

"""

query_insert_grupo_economico = lambda database, id_grupo, ds_grupo: f"""

    INSERT INTO {database}.dbo.tCRS_0006_GrupoEconomicoCadastro (idGrupo, dsGrupo)
    VALUES ({id_grupo}, '{ds_grupo}')

"""

query_insert_emissor = lambda database, id_emissor, cd_cnpj, ds_emissor, ic_holding, ic_consome_holding, id_holding, id_grupo, id_setor: f"""

    INSERT INTO {database}.dbo.tCRS_0007_EmissorCadastro (idEmissor, cdCnpj, dsEmissor, icHolding, icConsomeHolding, idEmissorHoldingConsumo, idGrupo, idSetor)
    VALUES ({id_emissor}, {'NULL' if not cd_cnpj else f"'{cd_cnpj}'"}, '{ds_emissor}', {ic_holding}, {ic_consome_holding}, {id_holding if id_holding else 'NULL'}, {id_grupo}, {id_setor if id_setor else 'NULL'})

"""

query_insert_emissor_oc3 = lambda database, id_emissor, cd_oc3: f"""
    
    INSERT INTO {database}.dbo.tCRS_0008_EmissorOC3 (idEmissor, cdEmissorOC3)
    VALUES ({id_emissor}, '{cd_oc3}')

"""

query_insert_emissor_crims = lambda database, id_emissor, cd_crims: f"""
    
    INSERT INTO {database}.dbo.tCRS_0009_EmissorCRIMS (idEmissor, cdEmissorCRIMS)
    VALUES ({id_emissor}, '{cd_crims}')

"""

query_update_holding_consumo = lambda database, id_emissor, id_holding: f"""
    
    UPDATE {database}.dbo.tCRS_0007_EmissorCadastro
    SET idEmissorHoldingConsumo = {id_holding if id_holding else 'NULL'}
    WHERE idEmissor = {id_emissor}

"""

# _______________________________ Consultar Grupo _______________________________

query_get_grupo_economico = lambda database, grupo: f"""

    SELECT 
        A.idGrupo,
        A.dsGrupo,
        B.cdCnpj,
        B.idEmissor,
        B.dsEmissor,
        B.icHolding,
        B.icConsomeHolding,
        B.idEmissorHoldingConsumo,
        dsSetor
    FROM {database}.dbo.tCRS_0006_GrupoEconomicoCadastro A
    LEFT JOIN {database}.dbo.tCRS_0007_EmissorCadastro B ON A.idGrupo = B.idGrupo
    LEFT JOIN {database}.dbo.tCRS_0005_SetorCadastro C ON B.idSetor = C.idSetor
    WHERE dsGrupo = '{grupo}'

"""

query_get_emissores_oc3 = lambda database, id_emissor: f"""

    SELECT DISTINCT cdEmissorOC3
    FROM {database}.dbo.tCRS_0008_EmissorOC3
    WHERE idEmissor = {id_emissor}

"""

query_get_emissores_crims = lambda database, id_emissor: f"""

    SELECT DISTINCT cdEmissorCRIMS
    FROM {database}.dbo.tCRS_0009_EmissorCRIMS
    WHERE idEmissor = {id_emissor}

"""

query_get_ativos_consumo = lambda database, id_emissor: f"""

    SELECT 
        cdTicker,
        vlPcConsumo
    FROM {database}.dbo.tCRS_0028_MapeamentoAtivosConsumo
    WHERE idEmissor = {id_emissor}

"""

# _______________________________ Atualizar Grupo _____________________________

query_get_ids_emissores_by_grupo = lambda database, id_grupo: f"""

    SELECT idEmissor
    FROM {database}.dbo.tCRS_0007_EmissorCadastro
    WHERE idGrupo = {id_grupo}

"""

query_delete_emissor_oc3 = lambda database, id_emissor: f"""

    DELETE 
    FROM {database}.dbo.tCRS_0008_EmissorOC3
    WHERE idEmissor = {id_emissor}

"""

query_delete_emissor_crims = lambda database, id_emissor: f"""

    DELETE 
    FROM {database}.dbo.tCRS_0009_EmissorCRIMS
    WHERE idEmissor = {id_emissor}

"""

query_delete_emissor_fidc = lambda database, id_emissor: f"""

    DELETE 
    FROM {database}.dbo.tCRS_0012_CadastroFIDC
    WHERE idEmissor = {id_emissor}

"""

query_delete_emissor_solicitacoes_descricao = lambda database, id_emissor: f"""

    DELETE 
    FROM {database}.dbo.tCRS_0017_SolicitacoesAlcadaDescricao
    WHERE idEmissor = {id_emissor}

"""

query_delete_emissor_limites_historico = lambda database, id_emissor: f"""

    DELETE 
    FROM {database}.dbo.tCRS_0019_LimitesAprovadosHistorico
    WHERE idEmissor = {id_emissor}

"""

query_delete_emissor_limites_vigentes = lambda database, id_emissor: f"""

    DELETE 
    FROM {database}.dbo.tCRS_0020_LimitesVigentes
    WHERE idEmissor = {id_emissor}

"""

query_delete_emissor_flexibilizacao = lambda database, id_emissor: f"""

    DELETE 
    FROM {database}.dbo.tCRS_0021_FlexibilizacaoConsumo
    WHERE idEmissor = {id_emissor}

"""

query_delete_emissor_ratings_historico = lambda database, id_emissor: f"""

    DELETE 
    FROM {database}.dbo.tCRS_0023_RatingsAprovadosEmissorHistorico
    WHERE idEmissor = {id_emissor}

"""

query_delete_emissor_ratings_vigentes = lambda database, id_emissor: f"""

    DELETE 
    FROM {database}.dbo.tCRS_0025_RatingsVigentesEmissor
    WHERE idEmissor = {id_emissor}

"""

query_delete_emissor_mapeamento_ativos = lambda database, id_emissor: f"""

    DELETE 
    FROM {database}.dbo.tCRS_0028_MapeamentoAtivosConsumo
    WHERE idEmissor = {id_emissor} OR idEmissorConsumo = {id_emissor}

"""

query_delete_emissor_controle_limites = lambda database, id_emissor: f"""

    DELETE 
    FROM {database}.dbo.tCRS_0031_ExecucaoControleLimites
    WHERE idEmissor = {id_emissor}

"""

query_update_reset_holding_dependentes = lambda database, id_emissor: f"""

    UPDATE {database}.dbo.tCRS_0007_EmissorCadastro
    SET idEmissorHoldingConsumo = NULL,
        icConsomeHolding = 0
    WHERE idEmissorHoldingConsumo = {id_emissor}

"""

query_delete_emissor_cadastro = lambda database, id_emissor: f"""

    DELETE 
    FROM {database}.dbo.tCRS_0007_EmissorCadastro
    WHERE idEmissor = {id_emissor}

"""

query_transfer_emissor_grupo = lambda database, id_emissor, id_grupo_destino: f"""

    UPDATE {database}.dbo.tCRS_0007_EmissorCadastro
    SET idGrupo = {id_grupo_destino},
        idEmissorHoldingConsumo = NULL,
        icConsomeHolding = 0
    WHERE idEmissor = {id_emissor}

"""

query_transfer_emissor_limites_historico = lambda database, id_emissor, id_grupo_destino: f"""

    UPDATE {database}.dbo.tCRS_0019_LimitesAprovadosHistorico
    SET idGrupo = {id_grupo_destino}
    WHERE idEmissor = {id_emissor}

"""

query_transfer_emissor_limites_vigentes = lambda database, id_emissor, id_grupo_destino: f"""

    UPDATE {database}.dbo.tCRS_0020_LimitesVigentes
    SET idGrupo = {id_grupo_destino}
    WHERE idEmissor = {id_emissor}

"""

query_transfer_emissor_controle_limites = lambda database, id_emissor, id_grupo_destino: f"""

    UPDATE {database}.dbo.tCRS_0031_ExecucaoControleLimites
    SET idGrupo = {id_grupo_destino}
    WHERE idEmissor = {id_emissor}

"""

# _______________________________ Deletar Grupo _______________________________

query_delete_emissores_oc3_by_grupo = lambda database, id_grupo: f"""
    
    DELETE 
    FROM {database}.dbo.tCRS_0008_EmissorOC3
    WHERE idEmissor IN (SELECT idEmissor FROM {database}.dbo.tCRS_0007_EmissorCadastro WHERE idGrupo = {id_grupo})

"""

query_delete_emissores_crims_by_grupo = lambda database, id_grupo: f"""
    
    DELETE 
    FROM {database}.dbo.tCRS_0009_EmissorCRIMS
    WHERE idEmissor IN (SELECT idEmissor FROM {database}.dbo.tCRS_0007_EmissorCadastro WHERE idGrupo = {id_grupo})

"""

query_delete_emissores_fidc_by_grupo = lambda database, id_grupo: f"""
    
    DELETE 
    FROM {database}.dbo.tCRS_0012_CadastroFIDC
    WHERE idEmissor IN (SELECT idEmissor FROM {database}.dbo.tCRS_0007_EmissorCadastro WHERE idGrupo = {id_grupo})

"""

query_delete_solicitacoes_descricao_by_grupo = lambda database, id_grupo: f"""
    
    DELETE 
    FROM {database}.dbo.tCRS_0017_SolicitacoesAlcadaDescricao
    WHERE idEmissor IN (SELECT idEmissor FROM {database}.dbo.tCRS_0007_EmissorCadastro WHERE idGrupo = {id_grupo})
       OR idSolicitacao IN (SELECT idSolicitacao FROM {database}.dbo.tCRS_0016_SolicitacoesAlcada WHERE idGrupo = {id_grupo})

"""

query_delete_solicitacoes_resposta_by_grupo = lambda database, id_grupo: f"""
    
    DELETE 
    FROM {database}.dbo.tCRS_0018_SolicitacoesAlcadaResposta
    WHERE idSolicitacao IN (SELECT idSolicitacao FROM {database}.dbo.tCRS_0016_SolicitacoesAlcada WHERE idGrupo = {id_grupo})

"""

query_delete_limites_historico_by_grupo = lambda database, id_grupo: f"""
    
    DELETE 
    FROM {database}.dbo.tCRS_0019_LimitesAprovadosHistorico
    WHERE idGrupo = {id_grupo}
       OR idEmissor IN (SELECT idEmissor FROM {database}.dbo.tCRS_0007_EmissorCadastro WHERE idGrupo = {id_grupo})

"""

query_delete_limites_vigentes_by_grupo = lambda database, id_grupo: f"""
    
    DELETE 
    FROM {database}.dbo.tCRS_0020_LimitesVigentes
    WHERE idGrupo = {id_grupo}
       OR idEmissor IN (SELECT idEmissor FROM {database}.dbo.tCRS_0007_EmissorCadastro WHERE idGrupo = {id_grupo})

"""

query_delete_flexibilizacao_by_grupo = lambda database, id_grupo: f"""
    
    DELETE 
    FROM {database}.dbo.tCRS_0021_FlexibilizacaoConsumo
    WHERE idEmissor IN (SELECT idEmissor FROM {database}.dbo.tCRS_0007_EmissorCadastro WHERE idGrupo = {id_grupo})

"""

query_delete_ratings_grupo_historico = lambda database, id_grupo: f"""
    
    DELETE 
    FROM {database}.dbo.tCRS_0022_RatingsAprovadosGrupoHistorico
    WHERE idGrupo = {id_grupo}

"""

query_delete_ratings_emissor_historico_by_grupo = lambda database, id_grupo: f"""
    
    DELETE 
    FROM {database}.dbo.tCRS_0023_RatingsAprovadosEmissorHistorico
    WHERE idEmissor IN (SELECT idEmissor FROM {database}.dbo.tCRS_0007_EmissorCadastro WHERE idGrupo = {id_grupo})

"""

query_delete_ratings_grupo_vigentes = lambda database, id_grupo: f"""
    
    DELETE 
    FROM {database}.dbo.tCRS_0024_RatingsVigentesGrupo
    WHERE idGrupo = {id_grupo}

"""

query_delete_ratings_emissor_vigentes_by_grupo = lambda database, id_grupo: f"""
    
    DELETE 
    FROM {database}.dbo.tCRS_0025_RatingsVigentesEmissor
    WHERE idEmissor IN (SELECT idEmissor FROM {database}.dbo.tCRS_0007_EmissorCadastro WHERE idGrupo = {id_grupo})

"""

query_delete_mapeamento_ativos_by_grupo = lambda database, id_grupo: f"""
    
    DELETE 
    FROM {database}.dbo.tCRS_0028_MapeamentoAtivosConsumo
    WHERE idEmissor IN (SELECT idEmissor FROM {database}.dbo.tCRS_0007_EmissorCadastro WHERE idGrupo = {id_grupo})
       OR idEmissorConsumo IN (SELECT idEmissor FROM {database}.dbo.tCRS_0007_EmissorCadastro WHERE idGrupo = {id_grupo})

"""

query_delete_controle_limites_by_grupo = lambda database, id_grupo: f"""
    
    DELETE 
    FROM {database}.dbo.tCRS_0031_ExecucaoControleLimites
    WHERE idGrupo = {id_grupo}
       OR idEmissor IN (SELECT idEmissor FROM {database}.dbo.tCRS_0007_EmissorCadastro WHERE idGrupo = {id_grupo})

"""

query_delete_solicitacoes_by_grupo = lambda database, id_grupo: f"""
    
    DELETE 
    FROM {database}.dbo.tCRS_0016_SolicitacoesAlcada
    WHERE idGrupo = {id_grupo}

"""

query_update_reset_holding_by_grupo = lambda database, id_grupo: f"""

    UPDATE {database}.dbo.tCRS_0007_EmissorCadastro
    SET idEmissorHoldingConsumo = NULL,
        icConsomeHolding = 0
    WHERE idEmissorHoldingConsumo IN (SELECT idEmissor FROM {database}.dbo.tCRS_0007_EmissorCadastro WHERE idGrupo = {id_grupo})

"""

query_delete_emissores_by_grupo = lambda database, id_grupo: f"""
    
    DELETE 
    FROM {database}.dbo.tCRS_0007_EmissorCadastro
    WHERE idGrupo = {id_grupo}

"""

query_delete_grupo = lambda database, id_grupo: f"""

    DELETE 
    FROM {database}.dbo.tCRS_0006_GrupoEconomicoCadastro
    WHERE idGrupo = {id_grupo}

"""

































