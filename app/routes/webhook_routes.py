from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.webhook_schema import (
    PipefyWebhookSchema
)

from app.database.connection import get_db

from app.services.webhook_service import (
    process_webhook
)

router = APIRouter()


@router.post(
    "/webhooks/pipefy/card-updated"
)
def receive_pipefy_webhook(
        payload: PipefyWebhookSchema,
        db: Session = Depends(get_db)
):
    return process_webhook(payload, db)