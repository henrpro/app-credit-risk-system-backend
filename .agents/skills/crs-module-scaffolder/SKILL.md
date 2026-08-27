---
name: crs-module-scaffolder
description: >-
  Utilize esta skill sempre que for criar um novo módulo, endpoint, regra de negócio
  ou consulta no backend do CRS, garantindo a criação de todas as 5 camadas
  (Models, Querys, Insumos, BLL e Blueprints) e respeito rigoroso aos padrões de código.
---

# Guia de Construção de Módulos — CRS Backend

Esta skill guia o desenvolvimento de novas funcionalidades, endpoints e tabelas no backend do CRS.

---

## 1. Passo a Passo para Criar um Novo Módulo

Sempre que implementar uma nova funcionalidade (ex: `gestao_de_limites`), crie os arquivos na seguinte ordem:

1. **Model** (`src/models/models_<modulo>.py`):
   - Criar as dataclasses com tipos explícitos (`@dataclass`).
2. **Querys** (`src/services/<modulo>/querys.py`):
   - Criar as funções lambda recebendo `database: str` e parâmetros.
   - Referenciar `{database}.dbo.<tabela>`.
3. **Insumos** (`src/services/<modulo>/insumos.py`):
   - Criar a classe `Insumos<NomeModulo>` com métodos de classe (`@classmethod`).
   - Usar `Connections.get_cnx_select` para leitura e `Connections.get_cnx_insert` para escrita com transação explícita.
4. **BLL** (`src/bll/<modulo>/tratamentos.py`):
   - Implementar regras de negócio, validações e orquestração de insumos.
5. **Blueprint** (`src/blueprints/<modulo>/routes.py`):
   - Criar `Blueprint('<modulo>', __name__)`.
   - Definir rotas com injeção de `database = current_app.config['DATABASE']`, conversão via `apply_model_dataclass` e tratamento `try...except`.
6. **Registro em `src/app.py`**:
   - Importar e registrar a blueprint com `app.register_blueprint(<modulo>, url_prefix='/v1/<kebab-case-modulo>')`.

---

## 2. Checklists Obrigatórios de Qualidade

Antes de finalizar qualquer arquivo, verifique:

- [ ] **Lógica Linear (Sem Funções Aninhadas)**: Lógica sequencial e direta, sem declarações de `def` dentro de outro `def`.
- [ ] **Imports em Pirâmide Invertida**: Linhas ordenadas por tamanho decrescente de caracteres dentro de `# Importações do projeto` e `# Importações de bibliotecas`.
- [ ] **Separadores de Seção**: Uso de `# _______________________________ Nome _______________________________`.
- [ ] **Tratamento de Exceções**: Bloco `try...except Exception as e:` em todas as rotas com retorno `status 500`.
- [ ] **DataClasses**: Todas as rotas de consulta utilizam `apply_model_dataclass(df, Model)`.
- [ ] **Fechamento de Conexões**: Operações de escrita fecham conexão e descartam engine em bloco `finally:`.

---

## 3. Templates Prontos

Consulte [examples/standard-module-template.md](./examples/standard-module-template.md) para copiar o esqueleto pronto de cada camada.
