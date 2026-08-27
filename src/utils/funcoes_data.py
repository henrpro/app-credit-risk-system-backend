# Importações do projeto
from utils.calendar import feriados

# Importações de bibliotecas
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
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


# Função que recebe uma data e retorna o primeiro dia útil do mês atual
def primeiro_dia_util_mes_atual(data: date):
    data = data.replace(day = 1)
    data = np.busday_offset(data, 0, roll = 'forward', holidays = feriados)
    return _to_date(data)


# Função que recebe uma data e retorna o primeiro dia útil do ano atual
def primeiro_dia_util_ano_atual(data: date):
    data = data.replace(day = 1)
    data = data.replace(month = 1)
    data = np.busday_offset(data, 0, roll = 'forward', holidays = feriados)
    return _to_date(data)


# Função que recebe uma data e retorna o primeiro dia útil do mês anterior
def primeiro_dia_util_mes_anterior(data: date):
    data = data - relativedelta(months = 1)
    data = data.replace(day = 1)
    data = np.busday_offset(data, 0, roll = 'forward', holidays = feriados)
    return _to_date(data)


# Função que recebe uma data e retorna o último dia útil do mês anterior
def ultimo_dia_util_mes_anterior(data: date):
    data = data.replace(day = 1)
    data = np.busday_offset(data, 0, roll = 'forward', holidays = feriados)
    data = np.busday_offset(data, -1, roll = 'backward', holidays = feriados)
    return _to_date(data)


# Função que recebe uma data e retorna o último dia útil do mês atual
def ultimo_dia_util_mes_atual(data: date):
    data = data + relativedelta(months = 1)
    data = data.replace(day = 1)
    data = np.busday_offset(data, 0, roll = 'forward', holidays = feriados)
    data = np.busday_offset(data, -1, roll = 'backward', holidays = feriados)
    return _to_date(data)


# Função que recebe uma data e calcula o vencimento avançando n meses (último dia útil do mês)
def calcula_vencimento_n_meses(data: date, meses: int):
    if isinstance(data, str):
        data = datetime.strptime(data[:10], '%Y-%m-%d').date()
    data = data + relativedelta(months = meses + 1)
    data = data.replace(day = 1)
    data = np.busday_offset(data, 0, roll = 'forward', holidays = feriados)
    data = np.busday_offset(data, -1, roll = 'backward', holidays = feriados)
    return _to_date(data)


# Função que retorna o número de dias úteis entre duas datas
def funcao_du(data_inicial: date, data_final: date):
    dias = np.busday_count(data_inicial, data_final, weekmask='1111100', holidays = feriados)
    return dias


# Função que retorna o número de dias corridos entre duas datas
def funcao_dc(data_inicial: date, data_final: date):
    dias = np.busday_count(data_inicial, data_final, weekmask='1111111')
    return dias


# Função que verifica se determinado dia é útil ou não
def is_business_day(data: date):
    return np.busday_offset(data, 0, roll = 'forward', holidays = feriados) == data


# Função que ajusta uma data para o próximo dia útil caso seja feriado/final de semana
def ajusta_dia_util(data: date):
    return _to_date(np.busday_offset(data, 0, roll='forward', holidays=feriados))


# Função que retorna o n-ésimo dia útil do mês de uma data de referência
def obtem_enesimo_dia_util_do_mes(data_referencia: date, n: int):
    dia = data_referencia.replace(day=1)
    return _to_date(np.busday_offset(dia, n, roll='forward', holidays=feriados))