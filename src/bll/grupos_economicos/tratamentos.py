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
            'dsSetor': row.get('dsSetor', '')
        })
        
    return pd.DataFrame(lista_emissores)


def cadastrar_novo_grupo_economico(database: str, payload: dict):

    """
    Função que realiza o cadastro de um novo grupo econômico no banco de dados.
    """

    try:
        # Extrai os dados do payload
        ds_grupo = str(payload.get('dsGrupo') or '').strip()
        emissores = payload.get('emissores', [])
        
        # 1. Verifica se o grupo já existe
        if InsumosGruposEconomicos.get_id_grupo_by_name(database, ds_grupo):
            raise ValueError(f"Já existe um grupo econômico cadastrado com o nome '{ds_grupo}'.")
            
        # 2. Verifica se os emissores já existem
        for emissor in emissores:
            nome = str(emissor.get('dsEmissor') or '').strip()
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

            # Buscamos o idSetor para os valores recebidos
            id_setor = InsumosGruposEconomicos.get_id_setor_by_name(database, emissor.get('dsSetor')) if emissor.get('dsSetor') else None
            
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
                id_setor
            )
            
            # Inserimos os emissores OC3 e CRIMS associados ao emissor
            for oc3 in emissor.get('cdEmissoresOC3', []):
                InsumosGruposEconomicos.execute_insert_emissor_oc3(database, max_id_emissor, oc3)
            for crims in emissor.get('cdEmissoresCRIMS', []):
                InsumosGruposEconomicos.execute_insert_emissor_crims(database, max_id_emissor, crims)
                
        # Segunda passagem para atualizar a holding após todos os emissores existirem
        for emissor in emissores:
            id_emissor = InsumosGruposEconomicos.get_emissor_by_name(database, str(emissor.get('dsEmissor') or '').strip())
            emissor_holding = emissor.get('dsEmissorHoldingConsumo')
            id_emissor_holding = InsumosGruposEconomicos.get_emissor_by_name(database, emissor_holding) if emissor_holding else None
            InsumosGruposEconomicos.execute_update_holding_consumo(database, id_emissor, id_emissor_holding)

    except Exception as e:
        raise e


def update_grupo_economico(database: str, payload: dict):

    """
    Função que atualiza os dados de um determinado grupo econômico
    """

    try:
        # Começamos extraindo os dados do payload
        id_grupo = int(payload.get('idGrupo'))
        ds_grupo = str(payload.get('dsGrupo') or '').strip()
        emissores = payload.get('emissores', [])

        # Validamos se já existe algum grupo com este nome em outro id
        id_existente_nome = InsumosGruposEconomicos.get_id_grupo_by_name(database, ds_grupo, exclude_id=id_grupo)
        if id_existente_nome:
            raise ValueError(f"Já existe um grupo econômico cadastrado com o nome '{ds_grupo}'.")

        # Deletamos e inserimos o grupo econômico
        InsumosGruposEconomicos.execute_delete_grupo_economico(database, id_grupo)
        InsumosGruposEconomicos.execute_insert_grupo_economico(database, id_grupo, ds_grupo)

        # Identificamos e deletamos os emissores removidos em cascata
        ids_emissores_atuais = InsumosGruposEconomicos.get_ids_emissores_by_grupo(database, id_grupo)
        ids_emissores_payload = [int(emissor.get('idEmissor')) for emissor in emissores if emissor.get('idEmissor')]
        ids_para_deletar = set(ids_emissores_atuais) - set(ids_emissores_payload)

        for id_emissor_del in ids_para_deletar:
            InsumosGruposEconomicos.execute_delete_emissor_completo(database, id_emissor_del)

        # Buscamos o maior id emissor para o caso de novos emissores
        max_id_emissor = InsumosGruposEconomicos.get_max_id_emissor(database)

        # Separamos emissores que serão transferidos para outro grupo dos que permanecem
        emissores_do_grupo = []

        for emissor in emissores:
            id_emissor = emissor.get('idEmissor')
            ds_grupo_destino = str(emissor.get('dsGrupoDestino') or '').strip()
            id_grupo_destino = emissor.get('idGrupoDestino')

            # Se houver grupo de destino diferente do atual, transfere o emissor
            if ds_grupo_destino and ds_grupo_destino != ds_grupo:
                id_destino = int(id_grupo_destino) if id_grupo_destino else InsumosGruposEconomicos.get_id_grupo_by_name(database, ds_grupo_destino)
                if id_destino and id_destino != id_grupo and id_emissor:
                    InsumosGruposEconomicos.execute_transferir_emissor_grupo(database, int(id_emissor), id_destino)
                    continue

            emissores_do_grupo.append(emissor)

        # Iteramos pelos emissores que permanecem no grupo
        for emissor in emissores_do_grupo:
            nome = str(emissor.get('dsEmissor') or '').strip()
            id_emissor = emissor.get('idEmissor')

            # Se não existir id_emissor no payload, geramos um novo
            if not id_emissor:
                max_id_emissor += 1
                id_emissor = max_id_emissor
                emissor['idEmissor'] = id_emissor
            else:
                id_emissor = int(id_emissor)

            # Validamos se já existe algum outro emissor com este nome
            id_existente_nome = InsumosGruposEconomicos.get_emissor_by_name(database, nome, exclude_id=id_emissor)
            if id_existente_nome:
                raise ValueError(f"Já existe um emissor cadastrado com o nome '{nome}'.")

            # Buscamos o idSetor para os valores recebidos
            id_setor = InsumosGruposEconomicos.get_id_setor_by_name(database, emissor.get('dsSetor')) if emissor.get('dsSetor') else None
            
            # Deletamos o emissor oc3, crims e cadastro antes de reinserir
            InsumosGruposEconomicos.execute_delete_emissor_oc3(database, id_emissor)
            InsumosGruposEconomicos.execute_delete_emissor_crims(database, id_emissor)
            InsumosGruposEconomicos.execute_delete_emissor_cadastro(database, id_emissor)

            # Inserimos o emissor
            InsumosGruposEconomicos.execute_insert_emissor(
                database, 
                id_emissor, 
                emissor.get('cdCnpj', ''), 
                nome, 
                emissor.get('icHolding', 0), 
                emissor.get('icConsomeHolding', 0), 
                None, 
                id_grupo, 
                id_setor
            )

            # Reinserimos o emissor oc3 e crims
            for oc3 in emissor.get('cdEmissoresOC3', []):
                InsumosGruposEconomicos.execute_insert_emissor_oc3(database, id_emissor, oc3)
            for crims in emissor.get('cdEmissoresCRIMS', []):
                InsumosGruposEconomicos.execute_insert_emissor_crims(database, id_emissor, crims)

        # Segunda passagem para atualizar a holding após todos os emissores existirem
        for emissor in emissores_do_grupo:
            id_emissor = int(emissor.get('idEmissor'))
            id_emissor_holding = emissor.get('idEmissorHoldingConsumo')
            if id_emissor_holding:
                id_emissor_holding = int(id_emissor_holding)
            else:
                id_emissor_holding = None

            InsumosGruposEconomicos.execute_update_holding_consumo(database, id_emissor, id_emissor_holding)

    except Exception as e:
        raise e