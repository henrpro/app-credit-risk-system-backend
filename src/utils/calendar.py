# Importações de bibliotecas
from pandas.tseries.holiday import AbstractHolidayCalendar, GoodFriday, Holiday, Easter, Day
from datetime import datetime

# Classe contendos os feriados da B3
class Calendario_Anbima(AbstractHolidayCalendar):
    rules = [
        Holiday('Confraternização Universal', month = 1, day = 1),
        Holiday('Segunda-Feira de Carnaval', month = 1, day = 1, offset = [Easter(), Day(-48)]),
        Holiday('Terça-Feira de Carnaval', month = 1, day = 1, offset = [Easter(), Day(-47)]),
        GoodFriday,
        Holiday('Corpus Christi', month = 1, day = 1, offset=[Easter(), Day(60)]),
        Holiday('Tiradentes', month = 4, day = 21),
        Holiday('Dia do Trabalho', month = 5, day = 1),
        Holiday('Independência do Brasil', month = 9, day = 7),
        Holiday('Nossa Senhora Aparecida', month = 10, day = 12),
        Holiday('Finados', month = 11, day = 2),
        Holiday('Proclamação da República', month = 11, day = 15),
        Holiday('Consciência Negra', month = 11, day = 20),
        Holiday('Natal', month = 12, day = 25)
    ]

# Lista de feriados
anbima_calendar = Calendario_Anbima()
feriados_anbima = anbima_calendar.holidays(datetime(1900,1,1), datetime(2100,12,31))

feriados = []
for feriado in feriados_anbima:
    feriados.append(datetime.strftime(feriado, '%Y-%m-%d'))