import duckdb

conn = duckdb.connect("martech_events.db")

print("\n--- CENÁRIO 1: Volumetria de interações por cliente para campanhas de marketing ---")
# Mostra quem são os clientes mais ativos (Engajamento)
query_1 = """
    SELECT 
        customer_name, 
        COUNT(event_id) as total_interactions,
        MAX(interaction_timestamp) as last_interaction
    FROM fact_whatsapp_interactions
    GROUP BY customer_name
    ORDER BY total_interactions DESC;
"""
print(conn.execute(query_1).fetchdf())


print("\n--- CENÁRIO 2: Deduplicação e Encontrar a Última Mensagem (Função de Janela / Window Function) ---")
# Em Martech, o cliente pode mandar várias mensagens seguidas. 
# O BigQuery/Athena cobra por dados processados. Como pegar apenas a ÚLTIMA interação real de cada cliente?
query_2 = """
    WITH ranked_interactions AS (
        SELECT 
            event_id,
            customer_name,
            phone_number_masked,
            message_text,
            interaction_timestamp,
            ROW_NUMBER() OVER(PARTITION BY phone_number_masked ORDER BY interaction_timestamp DESC) as rn
        FROM fact_whatsapp_interactions
    )
    SELECT 
        customer_name,
        phone_number_masked,
        message_text,
        interaction_timestamp
    FROM ranked_interactions
    WHERE rn = 1;
"""
print(conn.execute(query_2).fetchdf())

conn.close()
