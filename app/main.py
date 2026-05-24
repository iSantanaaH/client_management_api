from fastapi import FastAPI

from app.schemas.client_schema import ClientCreateSchema
from app.schemas.webhook_schema import PipefyWebhookSchema

app = FastAPI(
    title="Client Management API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Api online"}

@app.post("/clientes")
def create_client(payload: ClientCreateSchema):
    return {
        "message": "Criar Cliente",
        "data": payload
    }

@app.post("/webhooks/pipefy/card-updated")
def pipefy_webhook(payload: PipefyWebhookSchema):
    return {
        "message": "Webhook recebido",
        "data": payload
    }