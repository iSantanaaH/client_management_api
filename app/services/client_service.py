from app.database.connection import SessionLocal
from app.database.models import Client

class ClientService:
    @staticmethod
    def create_client(data):
        db = SessionLocal()

        try:
            client = Client(
                cliente_nome=data.cliente_nome,
                cliente_email=data.cliente_email,
                tipo_solicitacao=data.tipo_solicitacao,
                valor_patrimonio=data.valor_patrimonio,
            )

            db.add(client)

            db.commit()

            db.refresh(client)

            return client

        finally:
            db.close()
