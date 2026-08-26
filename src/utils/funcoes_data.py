# Importações do projeto
from utils.calendar import feriados

# Importações de bibliotecas
from datetime import date
import numpy as np

"""
Arquivo para montar funções envolvendo datas.
O objeto feriados é uma lista contendo os feriados da B3.
"""

def _to_date(np_date):
    return np_date.astype('datetime64[D]').item()

# Função que retorna n dias úteis para trás de uma determinada data
def dias_uteis_atras(dias: int, data_chamada: date):
    data_chamada = _to_date(np.busday_offset(data_chamada, 0, roll = 'forward', holidays = feriados))
    data = np.busday_offset(data_chamada, -dias, roll = 'backward', holidays = feriados)
    return _to_date(data)