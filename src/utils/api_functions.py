from unicodedata import normalize
from datetime import datetime
import pandas as pd 


# Formato de data padrão que deve ser retornado via API
_FMT_DATA_BD = '%Y-%m-%d'
funcao_lambda = (lambda x: datetime.strptime(x, _FMT_DATA_BD).date() if isinstance(x, str) else x)

def apply_model_dataclass(df: pd.DataFrame, model):

    """
    Função que aplica um modelo de dataclass em um DataFrame.
    O retorno da função é uma lista de instâncias do modelo.
    """
    
    # Aplica o modelo de dataclass no DataFrame
    return [model(**df.iloc[i].to_dict()) for i in range(len(df))]
    
