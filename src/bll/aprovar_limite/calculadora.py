# Importações de bibliotecas
from typing import List, Dict, Any
import pandas as pd


class CalculadoraLimitesGrupo:

    @staticmethod
    def _preparar_base_calculo(df_solicitacao: pd.DataFrame, considerar_meta: bool = False) -> pd.DataFrame:
        """
        Prepara a base de cálculo filtrando limite meta conforme a regra:
        - Para NÃO considerar limite meta (considerar_meta = False): icLimiteMeta == 0.
        - Para considerar limite meta (considerar_meta = True): se houver algum emissor com
          icLimiteMeta == 1, remove as linhas com icLimiteMeta == 0 apenas daquele emissor.
          Se nenhum emissor tiver meta, retorna DataFrame vazio.
        """
        if df_solicitacao.empty:
            return pd.DataFrame()

        df = df_solicitacao.copy()
        if 'icLimiteMeta' not in df.columns:
            df['icLimiteMeta'] = 0

        df['icLimiteMeta'] = df['icLimiteMeta'].fillna(0).astype(int)

        if not considerar_meta:
            return df[df['icLimiteMeta'] == 0]

        emissores_com_meta = set(df[df['icLimiteMeta'] == 1]['idEmissor'].unique())
        if not emissores_com_meta:
            return pd.DataFrame()

        condicao_remover_sem_meta = (df['idEmissor'].isin(emissores_com_meta)) & (df['icLimiteMeta'] == 0)
        df_filtrado = df[~condicao_remover_sem_meta]
        return df_filtrado

    @staticmethod
    def _calcular_limites_consolidados_prazos(df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Calcula a consolidação dos prazos do grupo somando os emissores.
        Regra de prazos: para um prazo P, se um emissor não tem linha em P,
        ele herda o valor do menor prazo maior que P cadastrado para ele.
        """
        if df.empty:
            return []

        prazos_distintos = sorted(df['vlPrazo'].dropna().unique())
        emissores_distintos = df['idEmissor'].dropna().unique()
        resultado = []

        for prazo in prazos_distintos:
            soma_terceiros = 0.0
            soma_reserva = 0.0

            for emissor in emissores_distintos:
                df_emissor = df[df['idEmissor'] == emissor]
                linha_exata = df_emissor[df_emissor['vlPrazo'] == prazo]

                if not linha_exata.empty:
                    soma_terceiros += float(linha_exata['vlTerceiros'].sum())
                    soma_reserva += float(linha_exata['vlReservaTecnica'].sum())
                else:
                    prazos_maiores = df_emissor[df_emissor['vlPrazo'] > prazo]
                    if not prazos_maiores.empty:
                        menor_prazo_maior = prazos_maiores['vlPrazo'].min()
                        linha_herdada = prazos_maiores[prazos_maiores['vlPrazo'] == menor_prazo_maior]
                        soma_terceiros += float(linha_herdada['vlTerceiros'].sum())
                        soma_reserva += float(linha_herdada['vlReservaTecnica'].sum())

            resultado.append({
                'vlPrazo': float(prazo),
                'vlTerceiros': round(soma_terceiros, 2),
                'vlReservaTecnica': round(soma_reserva, 2)
            })

        return resultado

    @classmethod
    def consolidar_grupo_todas_mesas(cls, df_solicitacao: pd.DataFrame, considerar_meta: bool = False) -> List[Dict[str, Any]]:
        """
        Gera a tabela de consolidado do grupo considerando todas as mesas:
        Para a mesa PRIVATE MARKETS, junta vlTerceiros e vlReservaTecnica na coluna
        vlTerceiros, deixando vlReservaTecnica como 0, e depois consolida as mesas.
        """
        df_base = cls._preparar_base_calculo(df_solicitacao, considerar_meta)
        if df_base.empty:
            return []

        df_ajustado = df_base.copy()
        if 'cdMesa' in df_ajustado.columns:
            mascara_pm = df_ajustado['cdMesa'].str.upper() == 'PRIVATE MARKETS'
            df_ajustado.loc[mascara_pm, 'vlTerceiros'] = (
                df_ajustado.loc[mascara_pm, 'vlTerceiros'].fillna(0) +
                df_ajustado.loc[mascara_pm, 'vlReservaTecnica'].fillna(0)
            )
            df_ajustado.loc[mascara_pm, 'vlReservaTecnica'] = 0.0

        return cls._calcular_limites_consolidados_prazos(df_ajustado)

    @classmethod
    def consolidar_grupo_por_mesa(cls, df_solicitacao: pd.DataFrame, considerar_meta: bool = False) -> List[Dict[str, Any]]:
        """
        Gera a tabela de consolidado do grupo por mesa:
        Para a mesa PRIVATE MARKETS, a coluna Reserva Técnica é renomeada para vlMultimesas.
        """
        df_base = cls._preparar_base_calculo(df_solicitacao, considerar_meta)
        if df_base.empty:
            return []

        if 'cdMesa' not in df_base.columns:
            df_base['cdMesa'] = 'MESA PADRAO'

        resultado_por_mesa = []
        mesas_distintas = sorted(df_base['cdMesa'].dropna().unique())

        for mesa in mesas_distintas:
            df_mesa = df_base[df_base['cdMesa'] == mesa]
            consolidados_mesa = cls._calcular_limites_consolidados_prazos(df_mesa)

            for linha in consolidados_mesa:
                item = {
                    'cdMesa': mesa,
                    'vlPrazo': linha['vlPrazo'],
                    'vlTerceiros': linha['vlTerceiros']
                }
                if str(mesa).upper() == 'PRIVATE MARKETS':
                    item['vlMultimesas'] = linha['vlReservaTecnica']
                else:
                    item['vlReservaTecnica'] = linha['vlReservaTecnica']

                resultado_por_mesa.append(item)

        return resultado_por_mesa
