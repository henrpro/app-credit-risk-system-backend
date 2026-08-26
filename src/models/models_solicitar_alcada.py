from dataclasses import dataclass

@dataclass
class GetTipoEventosModel:
    idTipoEvento: int
    dsTipoEvento: str


@dataclass
class GetRatingsDistintosModel:
    idRating: int
    cdRating: str

@dataclass
class GetLimitesGrupoEconomicoModel:
    idGrupo: int
    dsGrupo: str
    idEmissor: int
    dsEmissor: str
    vlPrazo: float
    vlTerceiros: float
    vlReservaTecnica: float
    cdRatingGrupo: str
    cdRatingEmissor: str

@dataclass
class GetDisponivelFlexibilizacaoModel:
    idGrupo: int
    dsGrupo: str
    idEmissor: int
    dsEmissor: str
    vlPrazo: float
    vlDisponivelFlex: float