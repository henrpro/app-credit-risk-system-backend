# Importações de bibliotecas
import pandas as pd

class CalculadoraLimitesGrupo:

    """
    Classe que consolida os limites do emissores para montar o limite do grupo
    """

    def __init__(self, dados: pd.DataFrame): 
        self.dados = dados

    def calcula_consolidado_grupo_sem_limite_meta(self):
        # Começamos pegando apenas os limites não meta
        dados = self.dados[self.dados['icLimiteMeta'] == 0]

        # Montamos o dataframe do grupo
        grupo = dados[['dsGrupo', 'vlPrazo']].drop_duplicates()
        grupo[['vlTerceiros', 'vlReservaTecnica']] = None

        # Iteramos pelos emissores
        