from dataclasses import dataclass
from typing import Optional


@dataclass
class GetSolicitacoesPendentesModel:
    idSolicitacao: int
    dtSolicitacao: str
    dsNome: str
    dsGrupo: str
    dsTipoEvento: str
    dsStatus: str
    dsAlcada: Optional[str] = None
