from typing import Optional, List, Any
from dataclasses import dataclass


@dataclass
class GetAlcadasPendentesModel:
    dsGrupo: str
    dsTipoEvento: str
    dsNome: str
    cdMesa: str
    idSolicitacao: Any
    dtSolicitacao: Optional[str] = None


@dataclass
class GetLimiteConsolidadoGrupoModel:
    vlPrazo: float
    vlTerceiros: float
    vlReservaTecnica: float
    dsGrupo: Optional[str] = None


@dataclass
class GetLimiteEmissorModel:
    dsEmissor: str
    vlPrazo: float
    vlTerceiros: float
    vlReservaTecnica: float
    icRunOff: int
    icLimiteMeta: int
    cdRatingEmissor: Optional[str] = None
    vlShareDivida: Optional[float] = None
    dtVencimentoLimiteMeta: Optional[str] = None


@dataclass
class GetRatingVigenteModel:
    dsEntidade: str
    cdRating: str
    tipoEntidade: str
    dtVencimento: Optional[str] = None


@dataclass
class GetDetalhesAlcadaModel:
    dsGrupo: str
    cdRatingGrupo: Optional[str]
    vlShareDividaGrupo: Optional[float]
    dsTipoEvento: str
    cdMesa: str
    limitesGrupoSemMeta: List[dict]
    limitesGrupoComMeta: List[dict]
    limitesEmissores: List[dict]
    limitesVigentesGrupoSemMeta: List[dict]
    limitesVigentesGrupoComMeta: List[dict]
    limitesVigentesEmissores: List[dict]
    ratingsVigentes: List[dict]
