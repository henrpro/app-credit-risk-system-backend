# Templates Padrão por Camada — CRS Backend

Utilize estes modelos como base direta para implementação de novos módulos.

---

### Camada 1: Model (`src/models/models_<exemplo>.py`)

```python
from dataclasses import dataclass
from typing import Optional


@dataclass
class GetExemploModel:
    idItem: int
    dsNome: str
    vlValor: float
    dsDescricao: Optional[str] = None
```

---

### Camada 2: Querys (`src/services/<exemplo>/querys.py`)

```python
# _______________________________ Geral _______________________________

query_get_exemplos = lambda database: f"""

    SELECT 
        idItem,
        dsNome,
        vlValor,
        dsDescricao
    FROM {database}.dbo.tCRS_XXXX_ExemploCadastro

"""

query_insert_exemplo = lambda database, nome, valor, descricao: f"""

    INSERT INTO {database}.dbo.tCRS_XXXX_ExemploCadastro (
        dsNome,
        vlValor,
        dsDescricao
    )
    VALUES (
        '{nome}',
        {valor},
        {f"'{descricao}'" if descricao is not None else 'NULL'}
    )

"""
```

---

### Camada 3: Insumos (`src/services/<exemplo>/insumos.py`)

```python
# Importações do projeto
from services.exemplo.querys import *
from services.connections import Connections

# Importações de bibliotecas
from sqlalchemy import text
import pandas as pd


class InsumosExemplo:

    # _______________________________ Geral _______________________________

    @classmethod
    def get_exemplos(cls, database: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_exemplos(database), cnx)
                return df
        except Exception as e:
            raise e

    # _______________________________ Execução SQL _______________________________

    @classmethod
    def execute_insert_exemplo(cls, database: str, nome: str, valor: float, descricao: str = None):
        engine, cnx = Connections.get_cnx_insert(database)
        try:
            with cnx.begin():
                cnx.execute(text(query_insert_exemplo(database, nome, valor, descricao)))
        except Exception as e:
            raise e
        finally:
            cnx.close()
            engine.dispose()
```

---

### Camada 4: BLL (`src/bll/<exemplo>/tratamentos.py`)

```python
# Importações do projeto
from services.exemplo.insumos import InsumosExemplo


def salvar_exemplo(database: str, payload: dict):
    """
    Regra de negócio para validação e gravação do exemplo.
    """
    try:
        nome = payload.get('dsNome', '').strip()
        valor = float(payload.get('vlValor', 0.0))
        descricao = payload.get('dsDescricao', '').strip() or None

        InsumosExemplo.execute_insert_exemplo(
            database=database,
            nome=nome,
            valor=valor,
            descricao=descricao
        )
    except Exception as e:
        raise e
```

---

### Camada 5: Blueprint (`src/blueprints/<exemplo>/routes.py`)

```python
# Importações do projeto
from models.models_exemplo import GetExemploModel
from bll.exemplo.tratamentos import salvar_exemplo
from services.exemplo.insumos import InsumosExemplo
from utils.api_functions import apply_model_dataclass

# Importações de bibliotecas
from flask import Blueprint, jsonify, current_app, request
import pandas as pd

# Cria a blueprint
exemplo = Blueprint('exemplo', __name__)

# _______________________________ Rotas _______________________________

@exemplo.route('/consultar-exemplos', methods=['GET'])
def consultar_exemplos():
    try:
        database = current_app.config['DATABASE']
        df = InsumosExemplo.get_exemplos(database)
        dados = apply_model_dataclass(df, GetExemploModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter exemplos': str(e)}), 500


@exemplo.route('/salvar-exemplo', methods=['POST'])
def salvar_novo_exemplo():
    try:
        database = current_app.config['DATABASE']
        payload = request.json
        salvar_exemplo(database, payload)
        return jsonify({'message': 'Exemplo salvo com sucesso.'}), 200
    except Exception as e:
        return jsonify({'Erro ao salvar exemplo': str(e)}), 500
```
