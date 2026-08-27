# Diretrizes de Qualidade e Estilo de Código — CRS Backend

Este documento resume as regras de qualidade, formatação e boas práticas a serem seguidas estritamente em todo o projeto.

---

## 1. Regra de Ouro das Importações (Pirâmide Invertida)

Cada arquivo Python deve agrupar seus imports em dois blocos, ordenados estritamente do **mais longo para o mais curto** em quantidade de caracteres por linha:

```python
# Importações do projeto
from models.models_mapeamentos import GetMapeamentoManagersModel, GetManagersSemMapeamentoModel
from bll.mapeamentos.tratamentos import salvar_mapeamento_manager, deletar_mapeamento_manager
from services.mapeamentos.insumos import InsumosMapeamentos
from utils.api_functions import apply_model_dataclass

# Importações de bibliotecas
from flask import Blueprint, jsonify, current_app, request
import pandas as pd
```

> **Atenção:**
> - Nunca misture bibliotecas externas com módulos internos do projeto.
> - Verifique visualmente e por contagem de caracteres o formato de funil/pirâmide invertida em cada bloco.

---

## 2. Divisores de Seção

- Utilize linhas de comentário no padrão `# _______________________________ Nome_Secao _______________________________`.
- Exemplo:
  ```python
  # ________________________________ Mapeamento Managers ______________________________
  ```

---

## 3. Tratamento de Exceções e Respostas HTTP

- Todo endpoint em `blueprints` deve estar encapsulado em `try...except Exception as e:`.
- O retorno em caso de falha deve ter status code `500` e mensagem explicativa no padrão:
  ```python
  except Exception as e:
      return jsonify({'Erro ao <descrever a ação em português>': str(e)}), 500
  ```
- Operações de sucesso de mutação (`POST`) devem retornar:
  ```python
  return jsonify({'message': '<Mensagem amigável de sucesso>.'}), 200
  ```

---

## 4. Tipagem e DataClasses

- Todos os models devem utilizar o decorator `@dataclass`.
- Atributos opcionais devem ser declarados com `Optional[tipo] = None` e sempre ao final da classe (após atributos obrigatórios).
- Datas devem ser tratadas conforme os utilitários de [api_functions.py](file:///c:/Users/henri/Documents/Projetos/credit_system/app-credit-risk-system-backend/src/utils/api_functions.py).

---

## 5. Lógica Linear e Proibição de Funções Aninhadas

- **Lógica Plana e Sequencial**: O código deve ter leitura fluida de cima para baixo, sem aninhamentos desnecessários de blocos condicionais ou loops profundos.
- **Sem Nested Functions**: NUNCA declare `def` dentro de outro `def`. Se uma função auxiliar for necessária, declare-a no escopo do módulo ou na camada apropriada (`utils`, `bll`, `services`).

---

## 6. Anti-Patterns Proibidos

❌ Declarar funções aninhadas (`nested functions` / funções dentro de funções).  
❌ Escrever SQL inline dentro de rotas em `blueprints` ou regras em `bll`.  
❌ Retornar dicionários manuais da rota sem passar pela dataclass do model.  
❌ Deixar de fechar conexões SQL ou de dar dispose na engine em operações de escrita.  
❌ Imports fora de ordem ou misturados sem os comentários de cabeçalho.  
❌ Nomes genéricos de variáveis como `x`, `temp`, `data1`.  
