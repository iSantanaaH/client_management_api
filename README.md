# Client Management API

API desenvolvida para processamento de clientes e integração via webhook utilizando FastAPI.

---

# Tecnologias utilizadas

* Python 3.12+
* FastAPI
* SQLAlchemy
* PostgreSQL
* Uvicorn

---

# Como executar o projeto localmente

## 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd client_management_api
```

---

## 2. Criar e ativar ambiente virtual

### Linux/macOS

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 4. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/client_management_db
PIPEFY_PIPE_ID=123456
```

---

## 5. Executar a aplicação

```bash
uvicorn app.main:app --reload
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:8000
```

---

# Documentação automática da API

Swagger:

```text
http://127.0.0.1:8000/docs
```

Redoc:

```text
http://127.0.0.1:8000/redoc
```

---

# Executando os testes

```bash
python -m pytest
```

---

# Exemplos de requisição

## 1. Criar cliente

```bash
curl -X POST "http://127.0.0.1:8000/clientes" \
-H "Content-Type: application/json" \
-d '{
  "cliente_nome": "Micael",
  "cliente_email": "micael23@gmail.com",
  "tipo_solicitacao": "Financiamento",
  "valor_patrimonio": 100000
}'
```

---

## 2. Processar webhook

```bash
curl -X POST "http://127.0.0.1:8000/webhooks/pipefy/card-updated" \
-H "Content-Type: application/json" \
-d '{
  "event_id": "evt_001",
  "card_id": "card_123",
  "cliente_email": "micael23@gmail.com",
  "timestamp": "2026-05-18T12:00:00Z"
}'
```

---

# Visão de Produção (AWS)

Em um cenário de produção, essa aplicação poderia ser escalada utilizando serviços da AWS para garantir maior disponibilidade, desempenho e capacidade de processamento conforme o volume de requisições aumentasse.

Uma possível arquitetura seria utilizar o AWS API Gateway como porta de entrada da API, recebendo as requisições HTTP e encaminhando para funções AWS Lambda responsáveis pelas regras de negócio da aplicação.

Nesse modelo, cada fluxo poderia ser separado em funções específicas, como:

* criação de clientes
* processamento de webhooks
* integrações externas
* validações de dados

Isso permitiria que a aplicação escalasse automaticamente conforme a demanda, sem necessidade de gerenciar servidores manualmente.

Para persistência dos dados, o PostgreSQL atual poderia ser migrado para um Amazon RDS PostgreSQL, mantendo a estrutura relacional já utilizada no projeto e facilitando consultas SQL e integridade dos dados.

Em cenários com alto volume de eventos, principalmente relacionados a webhooks, também seria possível utilizar o Amazon DynamoDB para armazenamento de eventos e controle de idempotência, aproveitando sua baixa latência e escalabilidade horizontal.

Outra melhoria importante seria o processamento assíncrono dos webhooks utilizando Amazon SQS. Nesse fluxo:

1. a API recebe o webhook
2. o evento é enviado para uma fila
3. uma função Lambda consome essa fila
4. o processamento acontece separadamente

Isso ajuda a evitar sobrecarga na API principal e aumenta a resiliência da aplicação em momentos de pico.

Para monitoramento e observabilidade, serviços como Amazon CloudWatch poderiam ser utilizados para logs, métricas e acompanhamento de falhas da aplicação.

Com essa arquitetura, o sistema conseguiria lidar melhor com crescimento de tráfego, múltiplos webhooks simultâneos e processamento distribuído, mantendo boa disponibilidade e escalabilidade.

