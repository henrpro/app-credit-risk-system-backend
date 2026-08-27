# Padrões de Arquitetura em Camadas — CRS Backend

O backend do Credit Risk System é estruturado rigorosamente em **5 camadas**, garantindo total desacoplamento entre HTTP, regras de negócio e persistência SQL Server.

---

## Fluxo de Execução

```
[ HTTP Request ]
       │
       ▼
1. Blueprints (`src/blueprints/<modulo>/routes.py`)
       │
       ▼
2. BLL (`src/bll/<modulo>/tratamentos.py`)
       │
       ▼
3. Services Insumos (`src/services/<modulo>/insumos.py`)
       │
       ▼
4. Services Querys (`src/services/<modulo>/querys.py`)
       │
       ▼
[ SQL Server Database ] (CRS / CRS_HOMDB)
       │
       ▼ (DataFrame / Raw Result)
5. Models (`src/models/models_<modulo>.py`)
       │
       ▼
[ HTTP Response JSON ]
```

---

## Responsabilidade de Cada Camada

### 1. `src/models/models_<modulo>.py`
- Define as estruturas de dados tipadas retornadas pela API utilizando `@dataclass`.
- Utiliza tipagens explícitas: `str`, `int`, `float`, `Optional[str] = None`, `Optional[float] = None`, etc.
- Os nomes dos atributos devem bater exatamente com as colunas retornadas nas queries SQL (ou DataFrames Pandas).

```python
from dataclasses import dataclass
from typing import Optional


@dataclass
class GetUsuariosCadastradosModel:
    cdUser: str
    dsNome: str
    dsProfile: str
```

---

### 2. `src/services/<modulo>/querys.py`
- Contém todas as instruções SQL (SELECT, INSERT, UPDATE, DELETE).
- Toda query deve ser definida como uma função `lambda` que recebe `database: str` como primeiro argumento, além dos parâmetros de filtro/valores.
- As tabelas são sempre referenciadas como `{database}.dbo.<nome_tabela>`.
- Separe as queries em seções lógicas com `# _______________________________ Nome_Secao _______________________________`.

```python
# _______________________________ Geral _______________________________

query_get_usuarios_cadastrados = lambda database: f"""

    SELECT DISTINCT
        cdUser,
        dsNome,
        dsProfile
    FROM {database}.dbo.tCRS_0001_UsuarioCadastro A
    LEFT JOIN {database}.dbo.tCRS_0002_ProfileAcesso B ON A.idProfile = B.idProfile

"""
```

---

### 3. `src/services/<modulo>/insumos.py`
- Centraliza a comunicação com o banco através da classe `Insumos<PascalCaseModulo>`.
- Todos os métodos são de classe (`@classmethod`).
- Consultas de leitura (`SELECT`) usam `Connections.get_cnx_select(database)` e retornam um `pandas.DataFrame`.
- Operações de escrita (`INSERT`/`UPDATE`/`DELETE`) usam `Connections.get_cnx_insert(database)` com transação explícita `with cnx.begin(): cnx.execute(text(...))` e finalização com `cnx.close()` e `engine.dispose()`.

```python
# Importações do projeto
from services.gestao_de_usuarios.querys import *
from services.connections import Connections

# Importações de bibliotecas
from sqlalchemy import text
import pandas as pd


class InsumosGestaoUsuarios:

    # _______________________________ Geral _______________________________

    @classmethod
    def get_usuarios_cadastrados(cls, database: str):
        try:
            with Connections.get_cnx_select(database) as cnx:
                df = pd.read_sql(query_get_usuarios_cadastrados(database), cnx)
                return df
        except Exception as e:
            raise e
```

---

### 4. `src/bll/<modulo>/tratamentos.py`
- Business Logic Layer (Regras de negócio, validações, orquestrações).
- **Lógica Linear e Direta**: Código sequencial, limpo e legível, sem funções dentro de funções (`nested functions`).
- Executa extração e sanitização de payloads (`strip()`, casting, tratamento de nulos).
- Realiza validações de integridade antes de persistir (ex: checar se usuário/registro existe, deletar e reinserir se necessário).
- Não gera JSON nem faz conexão direta de banco; delega tudo para a camada de `Insumos`.

---

### 5. `src/blueprints/<modulo>/routes.py`
- Endpoints Flask (GET, POST).
- Recupera o banco ativo via `database = current_app.config['DATABASE']`.
- Lê parâmetros de requisição (`request.args.to_dict()` para GET, `request.json` para POST).
- Converte DataFrames em instâncias de dataclass usando `apply_model_dataclass(df, Model)` de `utils.api_functions`.
- Retorna JSON via `jsonify([ob.__dict__ for ob in dados])` ou mensagens de sucesso `jsonify({'message': '...'}), 200`.
- Trata erros com bloco `try...except` retornando status HTTP 500: `jsonify({'Erro ao <acao>': str(e)}), 500`.

---

### 6. `src/app.py`
- Registra cada blueprint com o prefixo versionado `/v1/<kebab-case-modulo>`.
