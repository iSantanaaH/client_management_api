import uuid
from fastapi.testclient import TestClient
from app.main import app

from app.database.connection import SessionLocal
from app.database.models.client_model import Client

client = TestClient(app)


def test_client_init():
    payload = {
        "cliente_nome": "Micael",
        "cliente_email": f"{uuid.uuid4()}@gmail.com",
        "tipo_solicitacao": "Teste",
        "valor_patrimonio": 100000
    }

    response = client.post(
        "/clientes",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Cliente criado com sucesso"

    db_session = SessionLocal()

    try:

        client_db = (
            db_session.query(Client)
            .filter(Client.cliente_email == payload["cliente_email"])
            .first()
        )

        assert client_db is not None

        assert client_db.cliente_nome == payload["cliente_nome"]
        assert client_db.cliente_email == payload["cliente_email"]
        assert client_db.valor_patrimonio == payload["valor_patrimonio"]

        db_session.delete(client_db)
        db_session.commit()

    finally:
        db_session.close()
