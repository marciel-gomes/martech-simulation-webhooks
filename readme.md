Projeto_001-Webhooks/
│
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── webhook.py      <-- Onde o passo 1 vai acontecer (FastAPI)
│   ├── workers/
│   │   └── consumer.py     <-- Simulação do worker assíncrono (Passo 3)
│   ├── core/
│   │   └── config.py       <-- Configurações e variáveis de ambiente
│   └── database/
│       └── db.py           <-- Conexão e queries analíticas (Passo 4)
│

** Requirements.txt
* fastapi==0.111.0: Framework para construir APIs web rápidas e modernas baseadas em tipos padrão do Python.
* uvicorn==0.30.1: Servidor web assíncrono (ASGI) de alta performance que roda a aplicação web do FastAPI.
* pydantic==2.7.4: Biblioteca de validação de dados e gerenciamento de configurações estruturadas usando tipagem de dados.
* python-dotenv==1.0.1: Ferramenta que lê variáveis de ambiente de um arquivo .env para proteger dados sensíveis.
* duckdb==1.0.0: Banco de dados analítico (OLAP) embutido, focado em alta velocidade para consultas e ciência de dados.
* pytest==8.2.2: Framework de testes automatizados que simplifica a escrita de códigos de verificação de erros.


