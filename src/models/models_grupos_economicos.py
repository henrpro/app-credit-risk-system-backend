from dataclasses import dataclass


@dataclass
class GetSetoresModel:
    dsSetor: str

@dataclass
class GetSubsetoresModel:
    dsSubsetor: str

@dataclass
class GetGruposEconomicosDistintosModel:
    dsGrupo: str

@dataclass
class GetEmissoresOC3Model:
    cdCnpj: str
    cdEmissor: str
    dsEmissor: str

@dataclass
class GetEmissoresCRIMSModel:
    cdCnpj: str
    cdEmissor: str
    dsEmissor: str

@dataclass
class GetGruposEconomicosModel:
    dsGrupo: str
    cdCnpj: str
    idEmissor: int
    dsEmissor: str
    cdEmissoresOC3: list
    cdEmissoresCRIMS: list
    cdAtivosConsumos: dict
    icHolding: int
    icConsomeHolding: int
    idEmissorHoldingConsumo: int
    dsSetor: str
    dsSubsetor: str