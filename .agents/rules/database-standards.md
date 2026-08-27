# Padrões de Banco de Dados SQL Server — CRS Backend

Este guia estabelece as diretrizes de acesso, conexões, escrita, leitura e consistência com o Microsoft SQL Server no projeto CRS.

---

## 1. Conexões e Ambientes

As conexões são gerenciadas exclusivamente pela classe [Connections](file:///c:/Users/henri/Documents/Projetos/credit_system/app-credit-risk-system-backend/src/services/connections.py).

- **Servidor SQL Server**: `HENRIQUE\SQLEXPRESS` (via `Trusted_Connection=yes`)
- **Driver ODBC**: Detecção automática de drivers instalados (`ODBC Driver XX for SQL Server`).
- **Bancos por Ambiente**:
  - `dev` -> `CRS_HOMDB`
  - `prod` -> `CRS`

---

## 2. Padrão de Leitura (`SELECT`)

- Utiliza `Connections.get_cnx_select(database)` que retorna uma conexão `pyodbc.Connection`.
- Deve ser consumida sempre dentro de um gerenciador de contexto `with` combinado com `pandas.read_sql`:

```python
@classmethod
def get_dados(cls, database: str):
    try:
        with Connections.get_cnx_select(database) as cnx:
            df = pd.read_sql(query_get_dados(database), cnx)
            return df
    except Exception as e:
        raise e
```

---

## 3. Padrão de Escrita (`INSERT` / `UPDATE` / `DELETE`)

- Utiliza `Connections.get_cnx_insert(database)` que retorna `(engine, cnx)` via SQLAlchemy.
- A execução deve obrigatoriamente estar encapsulada em transação segura `with cnx.begin():` e bloco `finally:` para descarte de recursos:

```python
@classmethod
def execute_operacao(cls, database: str, param1: str, param2: int):
    engine, cnx = Connections.get_cnx_insert(database)
    try:
        with cnx.begin():
            cnx.execute(text(query_operacao(database, param1, param2)))
    except Exception as e:
        raise e
    finally:
        cnx.close()
        engine.dispose()
```

---

## 4. Estrutura de Queries SQL em `querys.py`

- Nomes de query em snake_case com prefixos expressivos: `query_get_...`, `query_insert_...`, `query_update_...`, `query_delete_...`.
- Interpolação explícita de banco: `{database}.dbo.<tabela>`.
- Tratamento explícito de valores `NULL`:
  - Para strings: `{f"'{valor}'" if valor is not None else 'NULL'}`
  - Para numéricos/floats: `{valor if valor is not None else 'NULL'}`
  - Para flags inteiras: `{int(flag)}`

---

## 5. Regras de Integridade e Modelagem

- Sempre utilize a skill [crs-database-schema](file:///c:/Users/henri/Documents/Projetos/credit_system/app-credit-risk-system-backend/.agents/skills/crs-database-schema/SKILL.md) e o arquivo [schema.md](file:///c:/Users/henri/Documents/Projetos/credit_system/app-credit-risk-system-backend/.agents/skills/crs-database-schema/references/schema.md) como fonte de verdade para os nomes das tabelas (`tCRS_0001` a `tCRS_0031`) e seus respectivos campos e chaves.
- Respeite as chaves primárias compostas (ex: `tCRS_0019_LimitesAprovadosHistorico` e `tCRS_0020_LimitesVigentes` possuem PK composta: `idSolicitacao`, `idLimite`, `cdMesa`, `idGrupo`, `idEmissor`, `vlPrazo`, `icLimiteMeta`).
