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
            "pipeId": pipe_id,
            "nome": client.cliente_nome,
            "email": client.cliente_email,
            "patrimonio": str(client.valor_patrimonio)
        }

        return {
            "query": mutation,
            "variables": variables
        }

    @staticmethod
    def build_update_card_mutation(
            card_id: str,
            prioridade: str
    ):

        mutation = """
        mutation UpdateCard(
            $cardId: ID!,
            $status: String!,
            $prioridade: String!
        ) {

            updateStatus: updateCardField(input: {
                card_id: $cardId,
                field_id: "status",
                new_value: $status
            }) {
                card {
                    id
                }
            }

            updatePriority: updateCardField(input: {
                card_id: $cardId,
                field_id: "prioridade",
                new_value: $prioridade
            }) {
                card {
                    id
                }
            }

        }
        """.strip()

        variables = {
            "cardId": card_id,
            "status": "Processado",
            "prioridade": prioridade
        }

        return {
            "query": mutation,
            "variables": variables
        }