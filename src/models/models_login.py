from dataclasses import dataclass

@dataclass
class GetLoginModel:
    cdUser: str
    cdPassword: str
    dsProfile: str