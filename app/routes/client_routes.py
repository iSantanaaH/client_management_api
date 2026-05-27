from fastapi import APIRouter

from app.schemas.client_schema import ClientCreateSchema
from app.services.client_service import ClientService

router = APIRouter()

@router.post("/clientes")
def create_client(payload: ClientCreateSchema):

    result = ClientService.create_client(payload)

    return {
        "message": "Cliente criado",
        "data": result
    }