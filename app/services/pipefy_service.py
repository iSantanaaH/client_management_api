import os

from dotenv import load_dotenv

load_dotenv()

class PipefyService:

    @staticmethod
    def create_card_payload(client):
        pipe_id = os.getenv("PIPEFY_PIPE_ID")

        mutation = """
        mutation CreateCard(
            $pipeId: ID!,
            $nome: String!,
            $email: String!,
            $patrimonio: String!
        ) {
            createCard(input: {
                pipe_id: $pipeId,
                fields_attributes: [
                    {
                        field_id: "nome",
                        field_value: $nome
                    },
                    {
                        field_id: "email",
                        field_value: $email
                    },
                    {
                        field_id: "patrimonio",
                        field_value: $patrimonio
                    }
                ]
            }) {
                card {
                    id
                    title
                }
            }
        }
        """.strip()

        variables = {
            "PIPEFY_PIPE_ID": pipe_id,
            "nome": client.cliente_nome,
            "email": client.cliente_email,
            "patrimonio": str(client.valor_patrimonio)
        }

        return {
            "query": mutation,
            "variables": variables
        }