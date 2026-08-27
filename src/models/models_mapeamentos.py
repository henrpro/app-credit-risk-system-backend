from dataclasses import dataclass
from typing import Optional

@dataclass
class GetMapeamentoManagersModel:
    dsManager: str
    cdMesa: str


@dataclass
class GetManagersSemMapeamentoModel:
    dsManager: str


@dataclass
class GetMapeamentoProdutosModel:
    cdProdutoOC3: str
    icCaptura: int


@dataclass
class GetProdutosSemMapeamentoModel:
    cdProdutoOC3: str


@dataclass
class GetMapeamentoAtivosModel:
    cdTicker: str
    idEmissor: int
    dsEmissor: Optional[str] = None
    idEmissorConsumo: Optional[int] = None
    dsEmissorConsumo: Optional[str] = None
    vlPcConsumo: Optional[float] = None


@dataclass
class GetAtivosSemMapeamentoModel:
    cdTicker: str


@dataclass
class GetEmissoresCadastradosModel:
    idEmissor: int
    dsEmissor: str
