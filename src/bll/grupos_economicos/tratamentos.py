# Importações do projeto
from models.models_grupos_economicos import GetSetoresModel, GetSubsetoresModel, GetGruposEconomicosDistintosModel, GetGruposEconomicosModel
from services.grupos_economicos.insumos import InsumosGruposEconomicos
from utils.api_functions import apply_model_dataclass


# Importações de bibliotecas
import pandas as pd


def obtem_setores_distintos(database: str):
    """
    Função que busca todos os setores cadastrados no banco de dados.
    """
    return InsumosGruposEconomicos.get_setores_distintos(database)


def obtem_subsetores_distintos(database: str):
    """
    Função que busca todos os subsetores cadastrados no banco de dados.
    """
    return InsumosGruposEconomicos.get_subsetores_distintos(database)


def obtem_grupos_economicos_distintos(database: str):
    """
    Função que obtem a lista de grupos econômicos distintos cadastrados na ferramenta
    """
    return InsumosGruposEconomicos.get_grupos_economicos_distintos(database)


def obtem_codigo_emissor_oc3(emissor: str):
    """
    Função que obtem a lista de emissores OC3 com nome similar ao chamado.
    """
    # return InsumosGruposEconomicos.get_codigo_emissor_oc3(emissor)
    return pd.DataFrame({
        'cd_Emissor': ['RUMO', 'GASC', 'COSAN', 'TESOURO']
    })


def obtem_codigo_emissor_crims(emissor: str):
    """
    Função que obtem a lista de emissores CRIMS com nome similar ao chamado.
    """
    # return InsumosGruposEconomicos.get_codigo_emissor_crims(emissor)
    return pd.DataFrame({
        'cd_Emissor': ['RUMO', 'GASC', 'COSAN', 'TESOURO']
    })


def obtem_grupo_economico(database: str, grupo: str):

    """
    Função que obtem a estrutura de um determinado grupo economico no banco de dados
    """

    # Começamos obtendo o grupo e seus emissores
    df = InsumosGruposEconomicos.get_grupo_economico(database, grupo)

    # Para cada emissor do grupo pegamos os códigos OC3 e CRIMS associados ao emissor e os ativos que consomem do emissor
    for idx, row in df.iterrows():
        codigos_oc3 = InsumosGruposEconomicos.get_emissores_oc3(database, row['idEmissor'])
        codigos_crims = InsumosGruposEconomicos.get_emissores_crims(database, row['idEmissor'])
        ativos = InsumosGruposEconomicos.get_ativos_consumo(database, row['idEmissor'])



def registrar_grupo_economico():

    """
    Função que registra um grupo econômico novo no banco de dados
    """


def atualizar_grupo_economico():

    """

    """


def deletar_grupo_economico():

    """
    Deleta um grupo econômicos cadastrado
    """