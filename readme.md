# 🚀 Martech Ingestion Pipeline - Simulação 

Este projeto simula uma arquitetura de alta performance para ingestão assíncrona de eventos de conversas do WhatsApp (Meta API), focada no ecossistema de Martech e integração com CRMs (Salesforce).

## 🛠️ Tecnologias e Conceitos Aplicados
- **FastAPI & Uvicorn**: Ingestão de webhooks em alta performance com respostas na casa dos milissegundos.
- **Pydantic**: Validação estrita de contratos de dados na borda da aplicação.
- **Arquitetura Orientada a Eventos (EDA)**: Desacoplamento completo entre a API e serviços terceiros através de mensageria assíncrona (`asyncio.Queue` simulando AWS SQS).
- **Resiliência & Failover**: Implementação de políticas de Retry e Dead Letter Queue (DLQ).
- **Governança & LGPD**: Mascaramento e higienização de dados sensíveis (PII) antes da persistência.
- **SQL Analítico (DuckDB & Pandas)**: Armazenamento e tratamento de jornadas através de Window Functions (`ROW_NUMBER() OVER`).

## 📐 Arquitetura do Sistema
O dado flui da seguinte forma:
`Meta Webhook -> FastAPI -> Fila Assíncrona (SQS) -> Worker Consumidor -> Validação/Retry -> DuckDB (Tabela Fato)`

## 🏃‍♂️ Como Rodar o Projeto
1. Instale as dependências: `pip install -r requirements.txt`
2. Inicie a aplicação: `python main.py`
3. Acesse a documentação viva e teste pelo Swagger: `http://127.0.0.1:8000/docs`
4. Execute as queries analíticas: `python queries_teste.py`