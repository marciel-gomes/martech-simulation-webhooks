import duckdb
import os
from datetime import datetime

DATABASE_PATH = os.getenv("DATABASE_PATH", "martech_events.db")

def get_db_connection():
    """Retorna uma conexão com o banco de dados analítico DuckDB."""
    return duckdb.connect(DATABASE_PATH)

def init_db():
    """Cria a estrutura de tabelas caso não exista."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Criando a tabela de eventos de Martech (Tabela Fato de Ingestão)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_whatsapp_interactions (
            event_id VARCHAR PRIMARY KEY,
            phone_number_masked VARCHAR,
            customer_name VARCHAR,
            message_text VARCHAR,
            interaction_timestamp TIMESTAMP,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.close()
    print("[DATABASE] Tabela fact_whatsapp_interactions inicializada com sucesso.")

def save_interaction(event_id: str, phone_masked: str, name: str, text: str, timestamp: datetime):
    """Persiste o evento purificado no banco analítico."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO fact_whatsapp_interactions 
            (event_id, phone_number_masked, customer_name, message_text, interaction_timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (event_id, phone_masked, name, text, timestamp))
        conn.commit()
    except duckdb.ConstraintException:
        # Garante idempotência: se o evento já existir, ignora para não duplicar dados
        print(f"[DATABASE] ⚠️ Evento {event_id} já processado. Ignorando (Idempotência).")
    finally:
        conn.close()
