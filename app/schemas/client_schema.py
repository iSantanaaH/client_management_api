from pydantic import BaseModel, EmailStr
from typing import Optional

class ClientCreateSchema(BaseModel):
    cliente_nome: str
    cliente_email: EmailStr
    tipo_solicitacao: str
    valor_patrimonio: float

class ClientResponseSchema(BaseModel):
    id: int
    cliente_nome: str
    cliente_email: EmailStr
    tipo_solicitacao: str
    valor_patrimonio: float
    status: str
    prioridade: Optional[str]

    class Config:
        from_attributes = True