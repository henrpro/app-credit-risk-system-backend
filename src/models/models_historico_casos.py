from dataclasses import dataclass
from typing import Optional


@dataclass
class GetSolicitacoesFinalizadasModel:
    idSolicitacao: int
    dtSolicitacao: str
    dsNome: str
    dsProfile: str
    dsGrupo: str
    dsTipoEvento: str
    dsStatus: str
    dsAlcada: Optional[str] = None
