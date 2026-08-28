# Dicionário de Dados SQL Server — Modelagem CRS

Este documento lista todas as 31 tabelas do banco de dados `[CRS].[dbo]`, contendo chaves primárias, colunas, tipos de dados e descrições técnicas.

---

### 0001 — `tCRS_0001_UsuarioCadastro`
**Chave Primária (PK)**: `cdUser`
- `cdUser` VARCHAR(100) NOT NULL — Login único do usuário
- `dsNome` VARCHAR(100) NOT NULL — Nome completo do usuário
- `cdPassword` VARCHAR(100) NOT NULL — Senha de autenticação
- `idProfile` INT NOT NULL — Chave estrangeira para `tCRS_0002_ProfileAcesso`
- `dsAlcadaAprovador` VARCHAR(30) NULL — Nível/tipo de alçada do aprovador (se aplicável)
- `vlPesoAprovacao` FLOAT NULL — Peso do voto na aprovação de solicitações

---

### 0002 — `tCRS_0002_ProfileAcesso`
**Chave Primária (PK)**: `idProfile`
- `idProfile` INT NOT NULL — Identificador sequencial do perfil
- `dsProfile` VARCHAR(30) NOT NULL — Descrição do perfil de acesso (ex: Mesa, Risco, Gestor, Admin)

---

### 0003 — `tCRS_0003_ProcessoCadastro`
**Chave Primária (PK)**: `idProcesso`
- `idProcesso` INT NOT NULL — Identificador do processo batch/rotina
- `dsNome` VARCHAR(100) NOT NULL — Nome da rotina
- `dsDescricao` VARCHAR(200) NOT NULL — Detalhamento do processo
- `dsPeriodicidade` VARCHAR(200) NOT NULL — Descrição da frequência de execução
- `cdTipoPeriodicidade` VARCHAR(30) NOT NULL — Código da periodicidade (Diário, Mensal, Intraday)
- `dsHorarioExecucao` VARCHAR(20) NULL — Horário previsto para disparo
- `cdDiaMesExecucao` INT NULL — Dia do mês para execução (quando aplicável)

---

### 0004 — `tCRS_0004_ExecucaoControle`
**Sem PK definida**
- `idProcesso` INT NOT NULL — Referência ao processo em `tCRS_0003`
- `cdServidor` VARCHAR(50) NOT NULL — Nome do host/servidor que executou
- `dsHoraInicio` DATETIME2 NULL — Data e hora de início
- `dsHoraFim` DATETIME2 NULL — Data e hora de término
- `ic_Trava` INT NULL — Flag de bloqueio concorrente (1 = travado, 0 = liberado)
- `dsStatus` VARCHAR(50) NULL — Status da execução (Sucesso, Erro, Em Execução)
- `idExecucao` BIGINT NULL — Identificador de rastreamento do log de execução

---

### 0005 — `tCRS_0005_SetorCadastro`
**Chave Primária (PK)**: `idSetor`
- `idSetor` BIGINT NOT NULL — Identificador do setor de atuação
- `dsSetor` VARCHAR(100) NOT NULL — Nome do setor da economia (ex: Energia, Varejo, Financeiro)

---

### 0006 — `tCRS_0006_GrupoEconomicoCadastro`
**Chave Primária (PK)**: `idGrupo`
- `idGrupo` BIGINT NOT NULL — Identificador do Grupo Econômico
- `dsGrupo` VARCHAR(100) NOT NULL — Razão social / Nome do Grupo Econômico

---

### 0007 — `tCRS_0007_EmissorCadastro`
**Chave Primária (PK)**: `idEmissor`
- `idEmissor` BIGINT NOT NULL — Identificador da empresa emissora
- `cdCnpj` VARCHAR(30) NULL — CNPJ da empresa
- `dsEmissor` VARCHAR(200) NOT NULL — Razão social / Nome fantasia do emissor
- `icHolding` INT NOT NULL — Flag se o emissor é a holding do grupo (1/0)
- `icConsomeHolding` INT NOT NULL — Flag se o limite consome da holding (1/0)
- `idEmissorHoldingConsumo` BIGINT NULL — ID da holding a ser consumida
- `idGrupo` BIGINT NOT NULL — Referência a `tCRS_0006_GrupoEconomicoCadastro`
- `idSetor` BIGINT NOT NULL — Referência a `tCRS_0005_SetorCadastro`

---

### 0008 — `tCRS_0008_EmissorOC3`
**Sem PK definida**
- `idEmissor` BIGINT NOT NULL — Referência a `tCRS_0007_EmissorCadastro`
- `cdEmissorOC3` VARCHAR(50) NOT NULL — Código equivalente do emissor no sistema OC3

---

### 0009 — `tCRS_0009_EmissorCRIMS`
**Sem PK definida**
- `idEmissor` BIGINT NOT NULL — Referência a `tCRS_0007_EmissorCadastro`
- `cdEmissorCRIMS` VARCHAR(50) NOT NULL — Código equivalente do emissor no sistema CRIMS

---

### 0010 — `tCRS_0010_TipoLastroFIDC`
**Chave Primária (PK)**: `idTipoLastro`
- `idTipoLastro` BIGINT NOT NULL — Identificador do tipo de lastro
- `dsTipoLastro` VARCHAR(50) NOT NULL — Descrição do lastro (ex: Duplicatas, Cartão, CCB)

---

### 0011 — `tCRS_0011_Senioridade`
**Chave Primária (PK)**: `idSenioridade`
- `idSenioridade` BIGINT NOT NULL — Identificador da cota/senioridade
- `dsSenioridade` VARCHAR(100) NOT NULL — Descrição (Sênior, Mezanino, Subordinada)
- `vlOrdem` BIGINT NOT NULL — Ordem de subordinação/preferência

---

### 0012 — `tCRS_0012_CadastroFIDC`
**Sem PK definida**
- `cdTicker` VARCHAR(15) NOT NULL — Código do ticker do FIDC na B3 / Cetip
- `idEmissor` BIGINT NOT NULL — Referência a `tCRS_0007_EmissorCadastro`
- `idTipoLastro` BIGINT NOT NULL — Referência a `tCRS_0010_TipoLastroFIDC`
- `idSenioridade` BIGINT NOT NULL — Referência a `tCRS_0011_Senioridade`

---

### 0013 — `tCRS_0013_TipoEvento`
**Chave Primária (PK)**: `idTipoEvento`
- `idTipoEvento` BIGINT NOT NULL — Identificador do evento
- `dsTipoEvento` VARCHAR(100) NOT NULL — Ex: Abertura de Limite, Renovação, Prorrogação, Upgrade, Downgrade

---

### 0014 — `tCRS_0014_RatingsDistintos`
**Chave Primária (PK)**: `idRating`
- `idRating` BIGINT NOT NULL — Identificador do rating
- `cdRating` VARCHAR(10) NOT NULL — Notação do rating (ex: AAA, AA+, A, BBB, etc.)

---

### 0015 — `tCRS_0015_StatusAlcada`
**Chave Primária (PK)**: `idStatus`
- `idStatus` INT NOT NULL — Identificador do status
- `dsStatus` VARCHAR(30) NOT NULL — Status da solicitação (ex: Pendente, Aprovado, Reprovado)

---

### 0016 — `tCRS_0016_SolicitacoesAlcada`
**Chave Primária (PK)**: `idSolicitacao`
- `idSolicitacao` BIGINT NOT NULL — Identificador sequencial da solicitação de limite
- `dtSolicitacao` DATETIME2 NOT NULL — Data e hora da solicitação
- `cdUser` VARCHAR(100) NOT NULL — Usuário solicitante
- `cdMesa` VARCHAR(100) NOT NULL — Mesa solicitante
- `idGrupo` BIGINT NOT NULL — Grupo econômico analisado
- `cdRatingGrupo` VARCHAR(15) NOT NULL — Rating atribuído ao grupo
- `vlShareDivida` FLOAT NULL — Percentual de participação da dívida
- `idStatus` INT NOT NULL — Status atual da solicitação (`tCRS_0015`)
- `dsTipoEvento` VARCHAR(100) NOT NULL — Tipo de evento da solicitação (`tCRS_0013`)

---

### 0017 — `tCRS_0017_SolicitacoesAlcadaDescricao`
**Chave Primária Composta (PK)**: `idSolicitacao`, `idEmissor`, `vlPrazo`, `icLimiteMeta`
- `idSolicitacao` BIGINT NOT NULL — Referência à solicitação pai
- `idEmissor` BIGINT NOT NULL — Emissor contemplado
- `cdRating` VARCHAR(15) NOT NULL — Rating do emissor
- `vlPrazo` BIGINT NOT NULL — Prazo em dias/meses
- `vlTerceiros` FLOAT NOT NULL — Limite solicitado para recursos de terceiros
- `vlReservaTecnica` FLOAT NOT NULL — Limite solicitado para reserva técnica
- `icRunOff` INT NOT NULL — Indicador de Run-off (1 = Sim, 0 = Não)
- `vlShareDivida` FLOAT NULL — Share de dívida do emissor
- `icLimiteMeta` INT NOT NULL — Indicador se é limite meta futuro (1/0)
- `dtVencimentoLimiteMeta` DATETIME2 NOT NULL — Data de vigência para limite meta

---

### 0018 — `tCRS_0018_SolicitacoesAlcadaResposta`
**Chave Primária (PK)**: `idSolicitacao`
- `idSolicitacao` BIGINT NOT NULL — Referência à solicitação
- `dsAlcada` VARCHAR(30) NULL — Nível da alçada deliberadora
- `dtResposta` DATETIME2 NOT NULL — Data e hora da deliberação
- `cdUserResposta` VARCHAR(30) NULL — Usuário aprovador/reprovador

---

### 0019 — `tCRS_0019_LimitesAprovadosHistorico`
**Chave Primária Composta (PK)**: `idSolicitacao`, `idLimite`, `cdMesa`, `idGrupo`, `idEmissor`, `vlPrazo`, `icLimiteMeta`
- `idSolicitacao` BIGINT NOT NULL — Solicitação de origem
- `idLimite` BIGINT NOT NULL — Identificador do limite
- `cdMesa` VARCHAR(100) NOT NULL — Mesa proprietária
- `idGrupo` BIGINT NOT NULL — Grupo econômico
- `idEmissor` BIGINT NOT NULL — Emissor
- `vlPrazo` BIGINT NOT NULL — Prazo
- `vlTerceiros` FLOAT NOT NULL — Valor aprovado para terceiros
- `vlReservaTecnica` FLOAT NOT NULL — Valor aprovado para reserva técnica
- `icRunOff` INT NOT NULL — Flag de run-off
- `dtAprovacao` DATETIME2 NOT NULL — Data de aprovação
- `dtVencimento` DATETIME2 NOT NULL — Data de expiração do limite
- `icLimiteMeta` INT NOT NULL — Flag de limite meta

---

### 0020 — `tCRS_0020_LimitesVigentes`
**Chave Primária Composta (PK)**: `idSolicitacao`, `idLimite`, `cdMesa`, `idGrupo`, `idEmissor`, `vlPrazo`, `icLimiteMeta`
- `idSolicitacao` BIGINT NOT NULL — Solicitação que gerou a vigência
- `idLimite` BIGINT NOT NULL — Identificador do limite
- `cdMesa` VARCHAR(100) NOT NULL — Mesa associada
- `idGrupo` BIGINT NOT NULL — Grupo
- `idEmissor` BIGINT NOT NULL — Emissor
- `vlPrazo` BIGINT NOT NULL — Prazo
- `vlTerceiros` FLOAT NOT NULL — Limite atual de terceiros
- `vlReservaTecnica` FLOAT NOT NULL — Limite atual de reserva técnica
- `icRunOff` INT NOT NULL — Flag de run-off
- `dtAprovacao` DATETIME2 NOT NULL — Data de início da vigência
- `dtVencimento` DATETIME2 NOT NULL — Data de término da vigência
- `icLimiteMeta` INT NOT NULL — Flag de limite meta

---

### 0021 — `tCRS_0021_FlexibilizacaoConsumo`
**Chave Primária Composta (PK)**: `cdMesa`, `idEmissor`, `vlPrazo`
- `cdMesa` VARCHAR(100) NOT NULL — Mesa
- `idEmissor` BIGINT NOT NULL — Emissor
- `vlPrazo` INT NOT NULL — Prazo
- `vlFlexibilizado` FLOAT NOT NULL — Valor consumido flexibilizado
- `vlLimite` FLOAT NOT NULL — Limite total alocado para flexibilização

---

### 0022 — `tCRS_0022_RatingsAprovadosGrupoHistorico`
**Chave Primária Composta (PK)**: `idSolicitacao`, `idGrupo`
- `idSolicitacao` BIGINT NOT NULL
- `idGrupo` BIGINT NOT NULL
- `cdRatingGrupo` VARCHAR(15) NULL
- `dtAprovacao` DATETIME2 NOT NULL
- `dtVencimento` DATETIME2 NOT NULL

---

### 0023 — `tCRS_0023_RatingsAprovadosEmissorHistorico`
**Chave Primária Composta (PK)**: `idSolicitacao`, `idEmissor`
- `idSolicitacao` BIGINT NOT NULL
- `idEmissor` BIGINT NOT NULL
- `cdRating` VARCHAR(15) NULL
- `dtAprovacao` DATETIME2 NOT NULL
- `dtVencimento` DATETIME2 NOT NULL

---

### 0024 — `tCRS_0024_RatingsVigentesGrupo`
**Chave Primária (PK)**: `idGrupo`
- `idSolicitacao` BIGINT NOT NULL
- `idGrupo` BIGINT NOT NULL
- `cdRatingGrupo` VARCHAR(15) NULL
- `dtAprovacao` DATETIME2 NOT NULL
- `dtVencimento` DATETIME2 NOT NULL

---

### 0025 — `tCRS_0025_RatingsVigentesEmissor`
**Chave Primária (PK)**: `idEmissor`
- `idSolicitacao` BIGINT NOT NULL
- `idEmissor` BIGINT NOT NULL
- `cdRating` VARCHAR(15) NOT NULL
- `dtAprovacao` DATETIME2 NOT NULL
- `dtVencimento` DATETIME2 NOT NULL

---

### 0026 — `tCRS_0026_MapeamentoManagers`
**Chave Primária (PK)**: `dsManager`
- `dsManager` VARCHAR(100) NOT NULL — Nome/identificador da carteira/manager externo
- `cdMesa` VARCHAR(100) NOT NULL — Mesa interna correspondente no CRS

---

### 0027 — `tCRS_0027_MapeamentoProdutos`
**Chave Primária (PK)**: `cdProdutoOC3`
- `cdProdutoOC3` VARCHAR(30) NOT NULL — Código do produto no sistema OC3
- `icCaptura` INT NOT NULL — Indicador se deve ser capturado pelo CRS (1/0)

---

### 0028 — `tCRS_0028_MapeamentoAtivosConsumo`
**Sem PK definida**
- `cdTicker` VARCHAR(30) NOT NULL — Código do ticker do ativo
- `idEmissor` BIGINT NULL — Emissor direto
- `idEmissorConsumo` BIGINT NULL — Emissor real onde deve recair o consumo
- `vlPcConsumo` FLOAT NULL — Percentual de consumo alocado (ex: 1.0 para 100%)

---

### 0029 — `tCRS_0029_PosicaoRaw`
**Sem PK definida**
- `dtPosicao` DATETIME2 NOT NULL — Data base da posição
- `cdCarteira` VARCHAR(100) NOT NULL — Código da carteira de investimento
- `dsManager` VARCHAR(100) NOT NULL — Nome do gestor/manager
- `cdAtivo` VARCHAR(30) NOT NULL — Identificador do papel/ativo
- `cd_rfTipo` VARCHAR(30) NOT NULL — Tipo de renda fixa / produto
- `dtVencimento` DATETIME2 NULL — Data de vencimento do papel
- `vlQuantidade` FLOAT NOT NULL — Quantidade de cotas/títulos
- `vlVolumeFin` FLOAT NOT NULL — Volume financeiro total

---

### 0030 — `tCRS_0030_AnaliticoTerceirosPosicao`
**Sem PK definida**
- `dtPosicao` DATETIME2 NOT NULL — Data da posição
- `cdCarteira` VARCHAR(100) NOT NULL — Código da carteira de terceiros
- `dsManager` VARCHAR(100) NOT NULL — Gestor/manager
- `cdAtivo` VARCHAR(30) NOT NULL — Ativo
- `cd_rfTipo` VARCHAR(30) NOT NULL — Tipo do ativo
- `dtVencimento` DATETIME2 NULL — Vencimento
- `vlQuantidade` FLOAT NOT NULL — Quantidade
- `vlVolumeFin` FLOAT NOT NULL — Volume financeiro

---

### 0031 — `tCRS_0031_ExecucaoControleLimites`
**Chave Primária Composta (PK)**: `dtDatabase`, `cdControle`, `vlPrazo`, `idGrupo`, `idEmissor`
- `dtDatabase` DATETIME2 NOT NULL — Data base de processamento do enquadramento
- `cdControle` VARCHAR(30) NOT NULL — Tipo de controle de risco
- `vlPrazo` BIGINT NOT NULL — Faixa de prazo
- `idGrupo` BIGINT NOT NULL — Grupo econômico
- `idEmissor` BIGINT NOT NULL — Emissor
- `vlExposicao` FLOAT NOT NULL — Volume financeiro em risco / exposição total
- `vlDisponivel` FLOAT NOT NULL — Margem disponível de limite

---

### 0032 — `tCRS_0032_LimitesAprovacao`
**Sem PK definida**
- `idSolicitacao` BIGINT NOT NULL — Identificador da solicitação de crédito (`tCRS_0016_SolicitacoesAlcada`)
- `cdUserAprovador` VARCHAR(100) NOT NULL — Login/código do usuário aprovador (`tCRS_0001_UsuarioCadastro`)
- `dsAlcada` VARCHAR(100) NOT NULL — Alçada de deliberação (`Mesa de Gestão`, `Comitê de Crédito IAM`, `Comitê Superior de Crédito`)
- `dtAprovacao` DATETIME2 NOT NULL — Data e hora do registro da aprovação individual
- `vlPeso` FLOAT NOT NULL — Peso ponderado do voto/aprovação do usuário

