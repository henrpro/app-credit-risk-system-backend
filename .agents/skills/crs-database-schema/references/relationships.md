# Relacionamentos e Fluxo de Dados — Banco CRS

Este documento mapeia os relacionamentos conceituais, chaves estrangeiras lógicas e fluxos de dados mais comuns entre as tabelas do CRS no SQL Server.

---

## 1. Diagrama de Relacionamentos Principais

```
[tCRS_0005_SetorCadastro]
        ▲
        │ (idSetor)
[tCRS_0006_GrupoEconomicoCadastro] ◄────┐
        ▲                                │
        │ (idGrupo)                      │ (idGrupo)
[tCRS_0007_EmissorCadastro]              │
        │                                │
        ├─────────┬──────────────────────┴────────────────────────┐
        │         │                                               │
        │         ▼                                               ▼
        │   [tCRS_0016_SolicitacoesAlcada] ◄── [tCRS_0001_UsuarioCadastro]
        │         │                                (cdUser)
        │         ├───────────────────────────────┬───────────────────────────────┐
        │         ▼                               ▼                               ▼
        │   [tCRS_0017_SolicitacoesAlcadaDescricao] [tCRS_0018_SolicitacoesAlcadaResposta] [tCRS_0032_LimitesAprovacao]
        │         │
        │         ▼
        │   [tCRS_0020_LimitesVigentes]
        │   [tCRS_0019_LimitesAprovadosHistorico]
        │
        ├─────────────────────────────┐
        ▼                             ▼
  [tCRS_0025_RatingsVigentesEmissor] [tCRS_0024_RatingsVigentesGrupo]
```

---

## 2. Joins Mais Utilizados no Sistema

### A. Grupo Econômico com Emissores e Setores
```sql
SELECT 
    G.idGrupo,
    G.dsGrupo,
    E.idEmissor,
    E.dsEmissor,
    E.cdCnpj,
    E.icHolding,
    S.dsSetor
FROM {database}.dbo.tCRS_0006_GrupoEconomicoCadastro G
INNER JOIN {database}.dbo.tCRS_0007_EmissorCadastro E ON G.idGrupo = E.idGrupo
INNER JOIN {database}.dbo.tCRS_0005_SetorCadastro S ON E.idSetor = S.idSetor
```

### B. Solicitação de Alçada Completa com Descrição e Resposta
```sql
SELECT 
    S.idSolicitacao,
    S.dtSolicitacao,
    S.cdUser,
    S.cdMesa,
    G.dsGrupo,
    S.cdRatingGrupo,
    ST.dsStatus,
    D.idEmissor,
    E.dsEmissor,
    D.cdRating AS cdRatingEmissor,
    D.vlPrazo,
    D.vlTerceiros,
    D.vlReservaTecnica,
    D.icRunOff,
    R.dsAlcada,
    R.dtResposta,
    R.cdUserResposta
FROM {database}.dbo.tCRS_0016_SolicitacoesAlcada S
INNER JOIN {database}.dbo.tCRS_0006_GrupoEconomicoCadastro G ON S.idGrupo = G.idGrupo
INNER JOIN {database}.dbo.tCRS_0015_StatusAlcada ST ON S.idStatus = ST.idStatus
INNER JOIN {database}.dbo.tCRS_0017_SolicitacoesAlcadaDescricao D ON S.idSolicitacao = D.idSolicitacao
INNER JOIN {database}.dbo.tCRS_0007_EmissorCadastro E ON D.idEmissor = E.idEmissor
LEFT JOIN {database}.dbo.tCRS_0018_SolicitacoesAlcadaResposta R ON S.idSolicitacao = R.idSolicitacao
```

### C. Limites Vigentes por Mesa e Grupo
```sql
SELECT 
    L.cdMesa,
    G.dsGrupo,
    E.dsEmissor,
    L.vlPrazo,
    L.vlTerceiros,
    L.vlReservaTecnica,
    L.icRunOff,
    L.dtAprovacao,
    L.dtVencimento
FROM {database}.dbo.tCRS_0020_LimitesVigentes L
INNER JOIN {database}.dbo.tCRS_0006_GrupoEconomicoCadastro G ON L.idGrupo = G.idGrupo
INNER JOIN {database}.dbo.tCRS_0007_EmissorCadastro E ON L.idEmissor = E.idEmissor
```

### D. Registro de Aprovações Individuais por Alçada
```sql
SELECT 
    A.idSolicitacao,
    A.cdUserAprovador,
    U.dsNome AS dsNomeAprovador,
    A.dsAlcada,
    A.dtAprovacao,
    A.vlPeso
FROM {database}.dbo.tCRS_0032_LimitesAprovacao A
INNER JOIN {database}.dbo.tCRS_0001_UsuarioCadastro U ON A.cdUserAprovador = U.cdUser
WHERE A.idSolicitacao = {id_solicitacao}
```
