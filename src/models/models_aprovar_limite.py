from typing import Optional, Any
from dataclasses import dataclass


@dataclass
class GetAprovacoesPendentesModel:
    dsGrupo: str
    dsTipoEvento: str
    dsNome: str
    cdMesa: str
    idSolicitacao: Any
    dtSolicitacao: Optional[str] = None
