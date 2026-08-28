# Diretrizes e Identidade de Desenvolvimento — Credit Risk System (CRS)

Este documento define os princípios inegociáveis de engenharia de software, padrões estéticos de código e a identidade de desenvolvimento do projeto **Credit Risk System (CRS Backend)**.

---

## 1. Princípios Fundamentais (Tolerância Zero)

- **Tolerância Zero a Código Desorganizado**: Código sem estrutura, com imports bagunçados, sem tratamento de exceção ou misturando responsabilidades de camadas não é aceito sob nenhuma hipótese.
- **Lógica Linear e Direta (Sem Funções Aninhadas)**: Proibido criar funções dentro de funções (`nested functions`/`closures` desnecessárias). O fluxo de execução deve ser linear, plano, claro e direto ao ponto.
- **Identidade e Consistência Estética**: Cada arquivo gerado deve ser indistinguível do código escrito pelo autor original.
- **Rigor na Arquitetura em 5 Camadas**: A separação de responsabilidades deve ser seguida estritamente (`models` -> `services/querys` -> `services/insumos` -> `bll` -> `blueprints`).
- **Visibilidade Integral do Banco de Dados**: O banco SQL Server (`CRS` em produção e `CRS_HOMDB` em desenvolvimento) possui modelagem estrita com 32 tabelas catalogadas (`tCRS_0001` a `tCRS_0032`).

---

## 2. Regra Visual e Estética de Importações (Pirâmide Invertida)

Os blocos de imports devem ser estritamente divididos e ordenados em **ordem decrescente de tamanho da linha (número de caracteres)**:

```python
# Importações do projeto
from models.models_gestao_de_usuarios import GetUsuariosCadastradosModel, GetUsuariosModel
from bll.gestao_de_usuarios.tratamentos import realizar_cadastro_usuario
from services.gestao_de_usuarios.insumos import InsumosGestaoUsuarios
from utils.api_functions import apply_model_dataclass

# Importações de bibliotecas
from flask import Blueprint, jsonify, current_app, request
import pandas as pd
```

> **Regras de Imports:**
> 1. Bloco `# Importações do projeto` sempre vem primeiro.
> 2. Bloco `# Importações de bibliotecas` sempre vem em seguida.
> 3. Em cada bloco, as linhas mais longas ficam no topo e as mais curtas na base (ordem decrescente de caracteres).

---

## 3. Divisores de Seção e Estilo Visual

Utilize separadores com sublinhados para delimitar seções lógicas nos arquivos:

```python
# _______________________________ Nome_Da_Secao _______________________________
```

Exemplos de seções padrão:
- `services/<modulo>/querys.py`: `# _______________________________ Geral _______________________________`, `# _______________________________ Insert _______________________________`
- `services/<modulo>/insumos.py`: `# _______________________________ Geral _______________________________`, `# _______________________________ Execução SQL _______________________________`
- `blueprints/<modulo>/routes.py`: `# _______________________________ Rotas _______________________________` ou agrupamentos por entidade.

---

## 4. Convenção de Nomenclatura do Domínio CRS

Os campos de banco de dados e atributos de models seguem os prefixos padronizados do SQL Server:
- `cd...` (Código/Identificador textual ou chave alfanumérica): `cdUser`, `cdMesa`, `cdRating`, `cdTicker`, `cdPassword`
- `ds...` (Descrição/Texto/Nome/Status): `dsNome`, `dsProfile`, `dsDescricao`, `dsEmissor`, `dsStatus`, `dsAlcadaAprovador`
- `id...` (Identificador numérico/ID): `idProfile`, `idGrupo`, `idEmissor`, `idSolicitacao`, `idStatus`, `idTipoEvento`
- `vl...` (Valor numérico/Monetário/Peso/Percentual/Prazo): `vlPrazo`, `vlTerceiros`, `vlReservaTecnica`, `vlShareDivida`, `vlPesoAprovacao`, `vlFlexibilizado`
- `dt...` (Data/DataHora): `dtSolicitacao`, `dtResposta`, `dtAprovacao`, `dtVencimento`, `dtDatabase`, `dtPosicao`
- `ic...` (Indicador/Flag booleana 0 ou 1): `icRunOff`, `icLimiteMeta`, `icHolding`, `icConsomeHolding`, `icCaptura`, `ic_Trava`

---

## 5. Estrutura do Workspace de Agentes

Consulte as regras e skills especializadas sempre que for atuar no projeto:
- **Regras de Arquitetura**: [architecture-standards.md](file:///c:/Users/henri/Documents/Projetos/credit_system/app-credit-risk-system-backend/.agents/rules/architecture-standards.md)
- **Padrões de Banco SQL Server**: [database-standards.md](file:///c:/Users/henri/Documents/Projetos/credit_system/app-credit-risk-system-backend/.agents/rules/database-standards.md)
- **Qualidade de Código**: [code-quality.md](file:///c:/Users/henri/Documents/Projetos/credit_system/app-credit-risk-system-backend/.agents/rules/code-quality.md)
- **Skill do Banco CRS (tCRS_0001 a 0031)**: [crs-database-schema](file:///c:/Users/henri/Documents/Projetos/credit_system/app-credit-risk-system-backend/.agents/skills/crs-database-schema/SKILL.md)
- **Skill de Criação de Módulos**: [crs-module-scaffolder](file:///c:/Users/henri/Documents/Projetos/credit_system/app-credit-risk-system-backend/.agents/skills/crs-module-scaffolder/SKILL.md)
