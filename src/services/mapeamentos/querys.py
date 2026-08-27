# ________________________________ Mapeamento Managers ______________________________

query_get_mapeamento_managers = lambda database: f"""

    SELECT 
        dsManager,
        cdMesa
    FROM {database}.dbo.tCRS_0026_MapeamentoManagers

"""

query_get_managers_sem_mapeamento = lambda database: f"""

    SELECT DISTINCT A.dsManager
    FROM {database}.dbo.tCRS_0029_PosicaoRaw A
    LEFT JOIN {database}.dbo.tCRS_0026_MapeamentoManagers B ON A.dsManager = B.dsManager
    WHERE B.cdMesa IS NULL

"""

query_insert_mapeamento_manager = lambda database, manager, mesa: f"""

    INSERT INTO {database}.dbo.tCRS_0026_MapeamentoManagers (dsManager, cdMesa)
    VALUES ('{manager}', '{mesa}')

"""

query_delete_mapeamento_manager = lambda database, manager: f"""

    DELETE
    FROM {database}.dbo.tCRS_0026_MapeamentoManagers
    WHERE dsManager = '{manager}'

"""


# ________________________________ Mapeamento Tipo Produto ______________________________

query_get_mapeamento_produtos = lambda database: f"""

    SELECT 
        cdProdutoOC3,
        icCaptura
    FROM {database}.dbo.tCRS_0027_MapeamentoProdutos

"""

query_get_produtos_sem_mapeamento = lambda database: f"""

    SELECT DISTINCT A.cd_rfTipo AS cdProdutoOC3
    FROM {database}.dbo.tCRS_0029_PosicaoRaw A
    LEFT JOIN {database}.dbo.tCRS_0027_MapeamentoProdutos B ON A.cd_rfTipo = B.cdProdutoOC3
    WHERE B.icCaptura IS NULL

"""

query_insert_mapeamento_produto = lambda database, cd_produto_oc3, ic_captura: f"""

    INSERT INTO {database}.dbo.tCRS_0027_MapeamentoProdutos (cdProdutoOC3, icCaptura)
    VALUES ('{cd_produto_oc3}', {ic_captura})

"""

query_delete_mapeamento_produto = lambda database, cd_produto_oc3: f"""

    DELETE
    FROM {database}.dbo.tCRS_0027_MapeamentoProdutos
    WHERE cdProdutoOC3 = '{cd_produto_oc3}'

"""


# ________________________________ Mapeamento Ativo Consumo ______________________________

query_get_mapeamento_ativos = lambda database: f"""

    SELECT 
        A.cdTicker,
        A.idEmissor,
        B.dsEmissor,
        A.idEmissorConsumo,
        C.dsEmissor AS dsEmissorConsumo,
        A.vlPcConsumo
    FROM {database}.dbo.tCRS_0028_MapeamentoAtivosConsumo A
    LEFT JOIN {database}.dbo.tCRS_0007_EmissorCadastro B ON A.idEmissor = B.idEmissor
    LEFT JOIN {database}.dbo.tCRS_0007_EmissorCadastro C ON A.idEmissorConsumo = C.idEmissor

"""

query_get_ativos_sem_mapeamento = lambda database: f"""

    SELECT DISTINCT A.cdAtivo AS cdTicker
    FROM {database}.dbo.tCRS_0029_PosicaoRaw A
    LEFT JOIN {database}.dbo.tCRS_0028_MapeamentoAtivosConsumo B ON A.cdAtivo = B.cdTicker
    WHERE B.idEmissorConsumo IS NULL

"""

query_insert_mapeamento_ativo = lambda database, cd_ticker, id_emissor, id_emissor_consumo, vl_pc_consumo: f"""

    INSERT INTO {database}.dbo.tCRS_0028_MapeamentoAtivosConsumo (cdTicker, idEmissor, idEmissorConsumo, vlPcConsumo)
    VALUES ('{cd_ticker}', {id_emissor}, {id_emissor_consumo}, {vl_pc_consumo})

"""

query_delete_mapeamento_ativo = lambda database, cd_ticker: f"""

    DELETE
    FROM {database}.dbo.tCRS_0028_MapeamentoAtivosConsumo
    WHERE cdTicker = '{cd_ticker}'

"""

query_get_emissores_cadastrados = lambda database: f"""

    SELECT 
        idEmissor,
        dsEmissor
    FROM {database}.dbo.tCRS_0007_EmissorCadastro
    ORDER BY dsEmissor

"""