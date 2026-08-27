from dataclasses import dataclass
from typing import Optional


@dataclass
class GetUsuariosCadastradosModel:
    cdUser: str
    dsNome: str
    dsProfile: str


@dataclass
class GetUsuariosModel:
    cdUser: str
    dsNome: str
    cdPassword: str
    dsProfile: str
    dsAlcadaAprovador: Optional[str] = None
    vlPesoAprovacao: Optional[float] = None

