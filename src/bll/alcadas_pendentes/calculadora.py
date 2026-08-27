# Importações de bibliotecas
from typing import List, Dict, Any
import pandas as pd


class CalculadoraLimitesGrupo:

    """
    Classe responsável pela consolidação matemática dos limites de crédito
    dos emissores no limite do grupo econômico por faixa de prazo, com suporte
    às regras de Private Markets e limites meta.
    """

    # _______________________________ Tratamentos Base _______________________________

    @classmethod
    def aplicar_regra_private_markets_consolidado(cls, df: pd.DataFrame) -> pd.DataFrame:
        """
        Para a visão consolidada de todas as mesas: na mesa PRIVATE MARKETS,
        junta vlTerceiros + vlReservaTecnica em vlTerceiros e zera vlReservaTecnica.
        """
        if df.empty:
            return df

        df_copia = df.copy()
        if 'cdMesa' in df_copia.columns:
            mascara_pm = df_copia['cdMesa'].astype(str).str.upper() == 'PRIVATE MARKETS'
            if mascara_pm.any():
                df_copia.loc[mascara_pm, 'vlTerceiros'] = (
                    df_copia.loc[mascara_pm, 'vlTerceiros'].fillna(0) +
                    df_copia.loc[mascara_pm, 'vlReservaTecnica'].fillna(0)
                )
                df_copia.loc[mascara_pm, 'vlReservaTecnica'] = 0.0

        return df_copia

    @classmethod
    def filtrar_base_limite_meta(cls, df: pd.DataFrame, considerar_meta: bool = False) -> pd.DataFrame:
        """
        Filtra a base de dados:
        - Sem meta: retorna linhas com icLimiteMeta == 0.
        - Com meta: se houver emissores com icLimiteMeta == 1, substitui as linhas com
          icLimiteMeta == 0 apenas desses emissores. Se não houver nenhum emissor com meta,
          retorna DataFrame vazio.
        """
        if df.empty:
            return pd.DataFrame()

        if not considerar_meta:
            return df[df['icLimiteMeta'] == 0]

        df_meta = df[df['icLimiteMeta'] == 1]
        if df_meta.empty:
            return pd.DataFrame()

        emissores_com_meta = df_meta['dsEmissor'].dropna().unique()
        df_sem_meta_outros = df[(df['icLimiteMeta'] == 0) & (~df['dsEmissor'].isin(emissores_com_meta))]

        df_result = pd.concat([df_sem_meta_outros, df_meta], ignore_index=True)
        return df_result

    # _______________________________ Consolidação de Prazos _______________________________

    @classmethod
    def consolidar_prazos(cls, df_linhas: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Consolida os limites por prazo somando os emissores.
        Regra: Para um prazo P, se um emissor não tem linha exata em P, mas possui
        linha em prazo maior (P' > P), utiliza o limite do menor prazo maior que P.
        """
        if df_linhas.empty:
            return []

        prazos_unicos = sorted(df_linhas['vlPrazo'].dropna().unique())
        emissores_unicos = df_linhas['dsEmissor'].dropna().unique()
        resultado_consolidado = []

        for prazo in prazos_unicos:
            total_terceiros = 0.0
            total_reserva_tecnica = 0.0

            for emissor in emissores_unicos:
                df_emissor = df_linhas[df_linhas['dsEmissor'] == emissor]

                df_exato = df_emissor[df_emissor['vlPrazo'] == prazo]
                if not df_exato.empty:
                    total_terceiros += float(df_exato['vlTerceiros'].fillna(0).sum())
                    total_reserva_tecnica += float(df_exato['vlReservaTecnica'].fillna(0).sum())
                    continue

                df_superior = df_emissor[df_emissor['vlPrazo'] > prazo]
                if not df_superior.empty:
                    menor_prazo_superior = df_superior['vlPrazo'].min()
                    df_menor_superior = df_superior[df_superior['vlPrazo'] == menor_prazo_superior]
                    total_terceiros += float(df_menor_superior['vlTerceiros'].fillna(0).sum())
                    total_reserva_tecnica += float(df_menor_superior['vlReservaTecnica'].fillna(0).sum())

            resultado_consolidado.append({
                'vlPrazo': float(prazo),
                'vlTerceiros': round(total_terceiros, 2),
                'vlReservaTecnica': round(total_reserva_tecnica, 2)
            })

        return resultado_consolidado

    # _______________________________ Consolidação do Grupo _______________________________

    @classmethod
    def consolidar_grupo_todas_mesas(cls, df: pd.DataFrame, considerar_meta: bool = False) -> List[Dict[str, Any]]:
        """
        Consolida o grupo somando todas as mesas. Aplica a regra de somar Reserva Técnica
        em Terceiros para a mesa PRIVATE MARKETS antes da consolidação.
        """
        if df.empty:
            return []

        df_base = cls.filtrar_base_limite_meta(df, considerar_meta=considerar_meta)
        if df_base.empty:
            return []

        df_pm = cls.aplicar_regra_private_markets_consolidado(df_base)
        return cls.consolidar_prazos(df_pm)

    @classmethod
    def consolidar_grupo_por_mesa(cls, df: pd.DataFrame, considerar_meta: bool = False) -> List[Dict[str, Any]]:
        """
        Consolida o grupo separando por mesa. Para a mesa PRIVATE MARKETS, renomeia
        a coluna Reserva Técnica para vlMultimesas.
        """
        if df.empty or 'cdMesa' not in df.columns:
            return []

        df_base = cls.filtrar_base_limite_meta(df, considerar_meta=considerar_meta)
        if df_base.empty:
            return []

        resultado = []
        mesas_unicas = sorted(df_base['cdMesa'].dropna().unique())

        for mesa in mesas_unicas:
            df_mesa = df_base[df_base['cdMesa'] == mesa]
            linhas_mesa = cls.consolidar_prazos(df_mesa)
            is_pm = str(mesa).upper() == 'PRIVATE MARKETS'

            for linha in linhas_mesa:
                item = {
                    'cdMesa': mesa,
                    'vlPrazo': linha['vlPrazo'],
                    'vlTerceiros': linha['vlTerceiros']
                }
                if is_pm:
                    item['vlMultimesas'] = linha['vlReservaTecnica']
                else:
                    item['vlReservaTecnica'] = linha['vlReservaTecnica']

                resultado.append(item)

        return resultado

    # _______________________________ Consolidação por Emissor _______________________________

    @classmethod
    def consolidar_emissor_todas_mesas(cls, df_emissor: pd.DataFrame, considerar_meta: bool = False) -> List[Dict[str, Any]]:
        """
        Consolida as linhas de um emissor específico somando todas as mesas (com regra de Private Markets).
        """
        if df_emissor.empty:
            return []

        df_base = cls.filtrar_base_limite_meta(df_emissor, considerar_meta=considerar_meta)
        if df_base.empty:
            return []

        df_pm = cls.aplicar_regra_private_markets_consolidado(df_base)
        return cls.consolidar_prazos(df_pm)

    @classmethod
    def consolidar_emissor_por_mesa(cls, df_emissor: pd.DataFrame, considerar_meta: bool = False) -> List[Dict[str, Any]]:
        """
        Consolida as linhas de um emissor específico separando por mesa. Para PRIVATE MARKETS,
        a reserva técnica é renomeada para vlMultimesas.
        """
        if df_emissor.empty or 'cdMesa' not in df_emissor.columns:
            return []

        df_base = cls.filtrar_base_limite_meta(df_emissor, considerar_meta=considerar_meta)
        if df_base.empty:
            return []

        resultado = []
        mesas_unicas = sorted(df_base['cdMesa'].dropna().unique())

        for mesa in mesas_unicas:
            df_mesa = df_base[df_base['cdMesa'] == mesa]
            linhas_mesa = cls.consolidar_prazos(df_mesa)
            is_pm = str(mesa).upper() == 'PRIVATE MARKETS'

            for linha in linhas_mesa:
                item = {
                    'cdMesa': mesa,
                    'vlPrazo': linha['vlPrazo'],
                    'vlTerceiros': linha['vlTerceiros']
                }
                if is_pm:
                    item['vlMultimesas'] = linha['vlReservaTecnica']
                else:
                    item['vlReservaTecnica'] = linha['vlReservaTecnica']

                resultado.append(item)

        return resultado
