from pydantic import BaseModel, EmailStr
from datetime import datetime

class PipefyWebhookSchema(BaseModel):
    event_id: str
    card_ir: str
    cliente_email: EmailStr
    timestamp: datetime