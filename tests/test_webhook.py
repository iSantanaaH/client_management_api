import datetime
import uuid
from fastapi.testclient import TestClient
from app.main import app

from app.database.connection import SessionLocal
from app.database.models.client_model import Client
from app.database.models.webhook_event_model import WebhookEvent

client = TestClient(app)


def test_webhook_define_high_priority():
    unique_email = f"{uuid.uuid4()}@gmail.com"

    db_session = SessionLocal()

    try:

        new_client = Client(
            cliente_nome="Micael",
            cliente_email=unique_email,
            tipo_solicitacao="Teste",
            valor_patrimonio=300000,
            status="Aguardando análise",
        )

        db_session.add(new_client)
        db_session.commit()

        payload = {
            "event_id": str(uuid.uuid4()),
            "cliente_email": unique_email,
            "card_id": str(uuid.uuid4()),
            "timestamp": str(datetime.datetime.now())
        }

        response = client.post(
            "/webhooks/pipefy/card-updated",
            json=payload
        )

        assert response.status_code == 200

        response_data = response.json()

        assert (
                response_data["message"]
                == "Webhook processado com sucesso"
        )

        updated_client = (
            db_session.query(Client)
            .filter(Client.cliente_email == unique_email)
            .first()
        )

        assert updated_client is not None

        assert (
                updated_client.prioridade
                == "prioridade_alta"
        )

        assert updated_client.status == "Processado"

        webhook_event = (
            db_session.query(WebhookEvent)
            .filter(WebhookEvent.event_id
                    == payload["event_id"]
                    )
            .first()
        )

        assert webhook_event is not None

        db_session.delete(webhook_event)
        db_session.delete(updated_client)

        db_session.commit()

    finally:
        db_session.close()


def test_webhook_duplicate_event_id():

    unique_email = f"{uuid.uuid4()}@gmail.com"

    db_session = SessionLocal()

    try:

        new_client = Client(
            cliente_nome="Micael",
            cliente_email=unique_email,
            tipo_solicitacao="Teste",
            valor_patrimonio=300000,
            status="Aguardando análise",
        )

        db_session.add(new_client)
        db_session.commit()

        duplicated_event_id = str(uuid.uuid4())

        payload = {
            "event_id": duplicated_event_id,
            "cliente_email": unique_email,
            "card_id": str(uuid.uuid4()),
            "timestamp": str(datetime.datetime.now())
        }

        first_response = client.post(
            "/webhooks/pipefy/card-updated",
            json=payload
        )

        second_response = client.post(
            "/webhooks/pipefy/card-updated",
            json=payload
        )

        assert first_response.status_code == 200

        second_response_data = second_response.json()

        assert (
                second_response_data["message"]
                == "Evento já processado"
        )

        webhook_event = (
            db_session.query(WebhookEvent)
            .filter(
                WebhookEvent.event_id
                == duplicated_event_id
            )
            .first()
        )

        if webhook_event:
            db_session.delete(webhook_event)

        db_session.delete(new_client)

        db_session.commit()

    finally:
        db_session.close()