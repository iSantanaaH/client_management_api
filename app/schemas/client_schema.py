from pydantic import BaseModel, EmailStr, ConfigDict
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

    model_config = ConfigDict(
        from_attributes=True
    )