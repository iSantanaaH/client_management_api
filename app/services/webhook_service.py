from sqlalchemy.orm import Session

from app.database.models.client_model import Client
from app.database.models.webhook_event_model import WebhookEvent

from app.services.pipefy_service import (
    PipefyService,
)


def process_webhook(payload, db: Session):

    # 1. Verificar idempotência
    existing_event = (
        db.query(WebhookEvent)
        .filter(
            WebhookEvent.event_id == payload.event_id
        )
        .first()
    )

    if existing_event:
        return {
            "message": "Evento já processado"
        }

    # 2. Buscar cliente
    client = (
        db.query(Client)
        .filter(
            Client.cliente_email == payload.cliente_email
        )
        .first()
    )

    if not client:
        return {
            "message": "Cliente não encontrado"
        }

    # 3. Regra de negócio
    if client.valor_patrimonio >= 200000:
        prioridade = "prioridade_alta"
    else:
        prioridade = "prioridade_normal"

    # 4. Montar mutation GraphQL
    graphql_mutation = PipefyService.build_update_card_mutation(
        payload.card_id,
        prioridade
    )

    print(graphql_mutation)

    # 5. Atualizar cliente
    client.status = "Processado"
    client.prioridade = prioridade

    # 6. Salvar evento processado
    event = WebhookEvent(
        event_id=payload.event_id
    )

    db.add(event)

    db.commit()

    return {
        "message": "Webhook processado com sucesso",
        "prioridade": prioridade
    }