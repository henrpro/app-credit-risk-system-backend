from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class GetSolicitacoesPendentesModel:
    idSolicitacao: int
    dtSolicitacao: date
    dsNome: str
    dsProfile: str
    dsGrupo: str
    dsTipoEvento: str
    dsStatus: str
    dsAlcada: Optional[str] = None
