from fastapi import FastAPI

from app.schemas.client_schema import ClientCreateSchema
from app.schemas.webhook_schema import PipefyWebhookSchema

# Database Connection
from app.database.connection import Base, engine
from app.database.models import Client
from app.services.client_service import ClientService

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Client Management API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Api online"}

@app.post("/clientes")
def create_client(payload: ClientCreateSchema):
    result = ClientService.create_client(payload)

    return {
        "message": "Cliente criado",
        "data": result
    }

@app.post("/webhooks/pipefy/card-updated")
def pipefy_webhook(payload: PipefyWebhookSchema):
    return {
        "message": "Webhook recebido",
        "data": payload
    }