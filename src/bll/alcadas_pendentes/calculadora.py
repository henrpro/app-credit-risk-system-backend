# Importações de bibliotecas
from typing import List, Dict, Any
import pandas as pd


class CalculadoraLimitesGrupo:

    """
    Classe responsável pela consolidação matemática dos limites de crédito
    dos emissores no limite do grupo econômico por faixa de prazo.
    """

    # _______________________________ Métodos de Consolidação _______________________________

    @classmethod
    def consolidar_prazos(cls, df_linhas: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Consolida os limites por prazo.
        Regra: Para um prazo P, se um emissor não tem linha exata em P, mas possui
        linha em prazo maior (P' > P), utiliza o limite do menor prazo maior que P.
        """
        if df_linhas.empty:
            return []

        # Prazos distintos ordenados
        prazos_unicos = sorted(df_linhas['vlPrazo'].dropna().unique())
        emissores_unicos = df_linhas['dsEmissor'].dropna().unique()
        resultado_consolidado = []

        for prazo in prazos_unicos:
            total_terceiros = 0.0
            total_reserva_tecnica = 0.0

            for emissor in emissores_unicos:
                df_emissor = df_linhas[df_linhas['dsEmissor'] == emissor]
                
                # Linha exata para o prazo
                df_exato = df_emissor[df_emissor['vlPrazo'] == prazo]
                if not df_exato.empty:
                    total_terceiros += float(df_exato['vlTerceiros'].fillna(0).sum())
                    total_reserva_tecnica += float(df_exato['vlReservaTecnica'].fillna(0).sum())
                    continue

                # Linhas com prazo superior (P' > P)
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

    @classmethod
    def calcula_consolidado_grupo_sem_limite_meta(cls, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Consolida os limites do grupo considerando apenas linhas com icLimiteMeta == 0.
        """
        if df.empty:
            return []

        df_sem_meta = df[df['icLimiteMeta'] == 0]
        return cls.consolidar_prazos(df_sem_meta)

    @classmethod
    def calcula_consolidado_grupo_com_limite_meta(cls, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Consolida os limites do grupo considerando limite meta.
        Regra: Se um emissor possui linhas com icLimiteMeta == 1, as linhas icLimiteMeta == 0
        daquele emissor são substituídas pelas linhas com meta.
        """
        if df.empty:
            return []

        emissores_com_meta = df[df['icLimiteMeta'] == 1]['dsEmissor'].unique()
        df_sem_meta_outros = df[(df['icLimiteMeta'] == 0) & (~df['dsEmissor'].isin(emissores_com_meta))]
        df_com_meta = df[df['icLimiteMeta'] == 1]
        
        df_final = pd.concat([df_sem_meta_outros, df_com_meta], ignore_index=True)
        return cls.consolidar_prazos(df_final)

    @classmethod
    def calcula_consolidado_vigentes_sem_limite_meta(cls, df_vigentes: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Consolida os limites vigentes do grupo considerando apenas icLimiteMeta == 0.
        """
        if df_vigentes.empty:
            return []

        df_sem_meta = df_vigentes[df_vigentes['icLimiteMeta'] == 0]
        return cls.consolidar_prazos(df_sem_meta)

    @classmethod
    def calcula_consolidado_vigentes_com_limite_meta(cls, df_vigentes: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Consolida os limites vigentes do grupo substituindo linhas de emissores que possuem meta.
        """
        if df_vigentes.empty:
            return []

        emissores_com_meta = df_vigentes[df_vigentes['icLimiteMeta'] == 1]['dsEmissor'].unique()
        df_sem_meta_outros = df_vigentes[(df_vigentes['icLimiteMeta'] == 0) & (~df_vigentes['dsEmissor'].isin(emissores_com_meta))]
        df_com_meta = df_vigentes[df_vigentes['icLimiteMeta'] == 1]

        df_final = pd.concat([df_sem_meta_outros, df_com_meta], ignore_index=True)
        return cls.consolidar_prazos(df_final)
