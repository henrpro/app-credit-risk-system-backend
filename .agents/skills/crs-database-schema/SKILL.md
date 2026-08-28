---
name: crs-database-schema
description: >-
  Consulte esta skill sempre que precisar entender a estrutura de dados, tabelas,
  colunas, chaves primárias e relacionamentos do banco de dados SQL Server do CRS
  (Credit Risk System), abrangendo as tabelas tCRS_0001 a tCRS_0032.
---

# Catálogo e Modelagem de Dados do CRS (SQL Server)

Esta skill fornece o mapa completo e detalhado da modelagem relacional do sistema de risco de crédito (**CRS**), dividida em 32 tabelas no SQL Server (`[CRS].[dbo]`).

---

## 1. Visão Geral dos Domínios do Banco

O banco de dados está segmentado nos seguintes domínios:

| Domínio | Tabelas | Finalidade |
| :--- | :--- | :--- |
| **Acesso & Autenticação** | `tCRS_0001`, `tCRS_0002` | Usuários, senhas, perfis de acesso, pesos de aprovação e alçadas. |
| **Processos & Batches** | `tCRS_0003`, `tCRS_0004` | Cadastros de jobs periódicos, travas, status e histórico de execução. |
| **Entidades de Crédito** | `tCRS_0005` a `tCRS_0009` | Setores, Grupos Econômicos, Emissores e mapeamentos de IDs externos (OC3, CRIMS). |
| **Estrutura de FIDCs** | `tCRS_0010` a `tCRS_0012` | Tipos de lastro, senioridades e cadastro de ativos FIDC (Tickers). |
| **Workflow de Alçadas & Aprovações** | `tCRS_0013` a `tCRS_0018`, `tCRS_0032` | Tipos de evento, ratings, status, solicitações de crédito, descrições, respostas de comitê e registros individuais de aprovação de limites. |
| **Limites de Crédito** | `tCRS_0019` a `tCRS_0021` | Histórico de limites aprovados, limites vigentes consolidados e flexibilização de consumo. |
| **Ratings de Crédito** | `tCRS_0022` a `tCRS_0025` | Histórico e vigência de ratings tanto a nível de Grupo quanto de Emissor. |
| **Mapeamento & Posicionamento** | `tCRS_0026` a `tCRS_0030` | Mapeamentos de Managers (mesas), produtos OC3, ativos de consumo, posições brutas e analítico de terceiros. |
| **Controle de Enquadramento** | `tCRS_0031` | Acompanhamento diário de exposição vs disponível por grupo/emissor/prazo. |

---

## 2. Documentação Detalhada

Para consultar o dicionário exaustivo de cada tabela, tipos de colunas, PKs simples e compostas:
- Consulte o arquivo [references/schema.md](./references/schema.md).

Para consultar os relacionamentos, foreign keys conceituais e diagramas de joins mais utilizados:
- Consulte o arquivo [references/relationships.md](./references/relationships.md).
