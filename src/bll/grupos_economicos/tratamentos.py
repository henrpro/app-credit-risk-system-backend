# Importações do projeto
from services.grupos_economicos.insumos import InsumosGruposEconomicos
from utils.api_functions import apply_model_dataclass

# Importações de bibliotecas
import pandas as pd


def obtem_grupo_economico(database: str, grupo: str):

    """
    Função que obtem a estrutura de um determinado grupo economico no banco de dados
    """
    
    lista_emissores = []

    # Começamos obtendo o grupo e seus emissores
    df = InsumosGruposEconomicos.get_grupo_economico(database, grupo)

    # Para cada emissor do grupo pegamos os códigos OC3 e CRIMS associados ao emissor e os ativos que consomem do emissor
    for idx, row in df.iterrows():
        codigos_oc3 = InsumosGruposEconomicos.get_emissores_oc3_by_emissor(database, row['idEmissor'])
        codigos_crims = InsumosGruposEconomicos.get_emissores_crims_by_emissor(database, row['idEmissor'])
        ativos = InsumosGruposEconomicos.get_ativos_consumo(database, row['idEmissor'])
        
        # Estrutura de dados conforme GetGruposEconomicosModel
        lista_emissores.append({
            'idGrupo': row.get('idGrupo', ''),
            'dsGrupo': row.get('dsGrupo', ''),
            'cdCnpj': row.get('cdCnpj', ''),
            'idEmissor': row.get('idEmissor', 0),
            'dsEmissor': row.get('dsEmissor', ''),
            'cdEmissoresOC3': codigos_oc3['cdEmissorOC3'].tolist() if not codigos_oc3.empty else [],
            'cdEmissoresCRIMS': codigos_crims['cdEmissorCRIMS'].tolist() if not codigos_crims.empty else [],
            'cdAtivosConsumos': dict(zip(ativos['cdAtivo'], ativos['vlPcConsumo'])) if not ativos.empty else {},
            'icHolding': row.get('icHolding', 0),
            'icConsomeHolding': row.get('icConsomeHolding', 0),
            'idEmissorHoldingConsumo': row.get('idEmissorHoldingConsumo', 0),
            'dsSetor': row.get('dsSetor', ''),
            'dsSubsetor': row.get('dsSubsetor', '')
        })
        
    return pd.DataFrame(lista_emissores)


def cadastrar_novo_grupo_economico(database: str, payload: dict):

    """
    Função que realiza o cadastro de um novo grupo econômico no banco de dados.
    """

    try:
        # Extrai os dados do payload
        ds_grupo = payload.get('dsGrupo', '').strip()
        emissores = payload.get('emissores', [])
        
        # 1. Verifica se o grupo já existe
        if InsumosGruposEconomicos.get_id_grupo_by_name(database, ds_grupo):
            raise ValueError(f"Já existe um grupo econômico cadastrado com o nome '{ds_grupo}'.")
            
        # 2. Verifica se os emissores já existem (por nome ou CNPJ)
        for emissor in emissores:
            nome = emissor.get('dsEmissor', '').strip()
            
            if InsumosGruposEconomicos.get_emissor_by_name(database, nome):
                raise ValueError(f"Já existe um emissor cadastrado com o nome '{nome}'.")

        # Começamos criando um novo id e inserindo o grupo
        id_grupo = InsumosGruposEconomicos.get_max_id_grupo(database) + 1
        
        # Inserimos o grupo econômico no banco de dados
        InsumosGruposEconomicos.execute_insert_grupo_economico(database, id_grupo, ds_grupo)

        # Buscamos a lista de emissores e o max id emissor
        max_id_emissor = InsumosGruposEconomicos.get_max_id_emissor(database)

        for emissor in emissores:
            max_id_emissor += 1

            # Buscamos o idSetor e o idSubsetor para os valores recebidos
            id_setor = InsumosGruposEconomicos.get_id_setor_by_name(database, emissor.get('dsSetor')) if emissor.get('dsSetor') else None
            id_subsetor = InsumosGruposEconomicos.get_id_subsetor_by_name(database, emissor.get('dsSubsetor')) if emissor.get('dsSubsetor') else None
            
            # Inserimos o emissor na tabela de cadastro de emissores
            InsumosGruposEconomicos.execute_insert_emissor(
                database, 
                max_id_emissor, 
                emissor.get('cdCnpj', ''), 
                emissor.get('dsEmissor', ''), 
                emissor.get('icHolding', 0), 
                emissor.get('icConsomeHolding', 0), 
                None, 
                id_grupo, 
                id_setor, 
                id_subsetor
            )
            
            # Inserimos os emissores OC3 e CRIMS associados ao emissor
            for oc3 in emissor.get('cdEmissoresOC3', []):
                InsumosGruposEconomicos.execute_insert_emissor_oc3(database, max_id_emissor, oc3)
            for crims in emissor.get('cdEmissoresCRIMS', []):
                InsumosGruposEconomicos.execute_insert_emissor_crims(database, max_id_emissor, crims)
                
        # Segunda passagem para atualizar a holding após todos os emissores existirem
        for emissor in emissores:
            emissor_holding = emissor.get('dsEmissorHoldingConsumo')
            id_emissor_holding = InsumosGruposEconomicos.get_emissor_by_name(database, emissor_holding)
            InsumosGruposEconomicos.execute_update_holding_consumo(database, emissor.get('dsEmissor', ''), id_emissor_holding)

    except Exception as e:
        raise e


def update_grupo_economico(database: str, payload: dict):

    """
    Função que atualiza os dados de um determinado grupo econômico
    """

    try:
        # Começamos extraindo os dados do payload e buscando o id_emissor
        ds_grupo = payload.get('dsGrupo', '').strip()
        emissores = payload.get('emissores', [])
        id_grupo = InsumosGruposEconomicos.get_id_grupo_by_name(database, ds_grupo)

        # Deletamos e inserimos o grupo econômico
        InsumosGruposEconomicos.execute_delete_grupo_economico(database, id_grupo)
        InsumosGruposEconomicos.execute_insert_grupo_economico(database, id_grupo, ds_grupo)

        # Iteramos pelos emissores do grupo
        for emissor in emissores:
            nome = emissor.get('dsEmissor', '').strip()

            # Buscamos o id_emissor
            id_emissor = InsumosGruposEconomicos.get_emissor_by_name(database, nome)

            # Se não existir buscamos o max id emissor
            if not id_emissor:
                id_emissor = InsumosGruposEconomicos.get_max_id_emissor(database) + 1

            # Validamos se já existe algum emissor com este nome
            id_existente_nome = InsumosGruposEconomicos.get_emissor_by_name(database, nome)
            if id_existente_nome and id_existente_nome != id_emissor:
                raise ValueError(f"Já existe um emissor cadastrado com o nome '{nome}'.")

            # Buscamos o idSetor e o idSubsetor para os valores recebidos
            id_setor = InsumosGruposEconomicos.get_id_setor_by_name(database, emissor.get('dsSetor')) if emissor.get('dsSetor') else None
            id_subsetor = InsumosGruposEconomicos.get_id_subsetor_by_name(database, emissor.get('dsSubsetor')) if emissor.get('dsSubsetor') else None
            
            # Deletamos o emissor oc3, crims e cadastro antes de reinserir
            InsumosGruposEconomicos.execute_delete_emissor_oc3(database, id_emissor)
            InsumosGruposEconomicos.execute_delete_emissor_crims(database, id_emissor)
            InsumosGruposEconomicos.execute_delete_emissor_cadastro(database, id_emissor)

            # Excluímos e reinserimos o emissor
            InsumosGruposEconomicos.execute_insert_emissor(
                database, 
                id_emissor, 
                emissor.get('cdCnpj', ''), 
                emissor.get('dsEmissor', ''), 
                emissor.get('icHolding', 0), 
                emissor.get('icConsomeHolding', 0), 
                None, 
                id_grupo, 
                id_setor, 
                id_subsetor
            )

            # Reinserimos o emissor oc3 e crims
            for oc3 in emissor.get('cdEmissoresOC3', []):
                InsumosGruposEconomicos.execute_insert_emissor_oc3(database, id_emissor, oc3)
            for crims in emissor.get('cdEmissoresCRIMS', []):
                InsumosGruposEconomicos.execute_insert_emissor_crims(database, id_emissor, crims)


        # Segunda passagem para atualizar a holding após todos os emissores existirem
        for emissor in emissores:
            emissor_holding = emissor.get('dsEmissorHoldingConsumo')
            id_emissor_holding = InsumosGruposEconomicos.get_emissor_by_name(database, emissor_holding)
            InsumosGruposEconomicos.execute_update_holding_consumo(database, emissor.get('dsEmissor', ''), id_emissor_holding)

    except Exception as e:
        raise e