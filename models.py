from pydantic import BaseModel, Field
from typing import Optional, List

class CasoBase(BaseModel):
    descricao: str = Field(..., example="Assédio verbal na saída do evento.")
    latitude: float = Field(..., example=-23.550520)
    longitude: float = Field(..., example=-46.633308)

class CasoCreate(CasoBase):
    user_id: str

class Caso(CasoBase):
    id: str
    data_ocorrencia: str
    bo_solicitado: bool

class UnidadeApoio(BaseModel):
    id: int
    nome: str
    tipo: str
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    latitude: float
    longitude: float
    distancia_km: float

class UnidadeApoioCreate(BaseModel):
    nome: str
    tipo: str
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    latitude: float
    longitude: float

class RiscoZona(BaseModel):
    latitude: float
    longitude: float
    contagem: int
    caso_ids: List[str]

class BODados(BaseModel):
    nome_completo: str
    cpf: str = Field(..., example="123.456.789-00")
    detalhes_adicionais: Optional[str] = None 