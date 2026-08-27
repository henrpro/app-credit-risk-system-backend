# Importações do projeto
from services.mapeamentos.insumos import InsumosMapeamentos


# ________________________________ Mapeamento Managers ______________________________

def salvar_mapeamento_manager(database: str, payload: dict):

    """
    Função que cadastra ou atualiza o mapeamento de um manager para uma mesa.
    Se o mapeamento já existir para o manager, deleta e reinsere.
    """

    try:
        manager = payload.get('dsManager', '').strip()
        mesa = payload.get('cdMesa', '').strip()
        
        # Deleta mapeamento existente se houver
        InsumosMapeamentos.execute_delete_mapeamento_manager(database, manager)

        # Insere o novo mapeamento
        InsumosMapeamentos.execute_insert_mapeamento_manager(database, manager, mesa)
    except Exception as e:
        raise e


def deletar_mapeamento_manager(database: str, payload: dict):

    """
    Função que remove o mapeamento de um manager.
    """

    try:
        manager = payload.get('dsManager', '').strip()
        InsumosMapeamentos.execute_delete_mapeamento_manager(database, manager)
    except Exception as e:
        raise e


# ________________________________ Mapeamento Tipo Produto ______________________________

def salvar_mapeamento_produto(database: str, payload: dict):

    """
    Função que cadastra ou atualiza o mapeamento de um tipo de produto OC3.
    Se o mapeamento já existir para o produto, deleta e reinsere.
    """

    try:
        cd_produto_oc3 = payload.get('cdProdutoOC3', '').strip()
        ic_captura = int(payload.get('icCaptura', 1))

        # Deleta mapeamento existente se houver
        InsumosMapeamentos.execute_delete_mapeamento_produto(database, cd_produto_oc3)

        # Insere o novo mapeamento
        InsumosMapeamentos.execute_insert_mapeamento_produto(database, cd_produto_oc3, ic_captura)
    except Exception as e:
        raise e


def deletar_mapeamento_produto(database: str, payload: dict):

    """
    Função que remove o mapeamento de um tipo de produto OC3.
    """

    try:
        cd_produto_oc3 = payload.get('cdProdutoOC3', '').strip()
        InsumosMapeamentos.execute_delete_mapeamento_produto(database, cd_produto_oc3)
    except Exception as e:
        raise e


# ________________________________ Mapeamento Ativo Consumo ______________________________

def salvar_mapeamento_ativo(database: str, payload: dict):

    """
    Função que cadastra ou atualiza o mapeamento de um ativo de consumo.
    Se o mapeamento já existir para o ticker, deleta e reinsere.
    """

    try:
        cd_ticker = payload.get('cdTicker', '').strip()
        id_emissor = int(payload['idEmissor'])
        id_emissor_consumo = int(payload['idEmissorConsumo'])
        vl_pc_consumo = float(payload.get('vlPcConsumo', 1.0))

        # Deleta mapeamento existente se houver
        InsumosMapeamentos.execute_delete_mapeamento_ativo(database, cd_ticker)

        # Insere o novo mapeamento
        InsumosMapeamentos.execute_insert_mapeamento_ativo(database, cd_ticker, id_emissor, id_emissor_consumo, vl_pc_consumo)
    except Exception as e:
        raise e


def deletar_mapeamento_ativo(database: str, payload: dict):

    """
    Função que remove o mapeamento de um ativo de consumo.
    """

    try:
        cd_ticker = payload.get('cdTicker', '').strip()
        InsumosMapeamentos.execute_delete_mapeamento_ativo(database, cd_ticker)
    except Exception as e:
        raise e
