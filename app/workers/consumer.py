import asyncio
import random
from datetime import datetime
from app.databases.db import save_interaction  # <-- Importa a persistência

sqs_queue_simulation = asyncio.Queue()
dlq_queue_simulation = []
MAX_RETRIES = 3

async def send_to_salesforce_mock(event_id: str, customer_name: str) -> bool:
    await asyncio.sleep(0.5)
    return random.choices([True, False], weights=[85, 15])[0] # Aumentei a chance de sucesso para o teste do banco

async def martech_worker_consumer():
    print("[WORKER] Iniciado e escutando eventos de Martech...")
    
    while True:
        event_data = await sqs_queue_simulation.get()
        
        event_id = event_data.get("event_id")
        customer_name = event_data.get("customer_name")
        phone_number_masked = event_data.get("phone_number_masked")
        message_text = event_data.get("message_text")
        # Trata o timestamp vindo da API
        timestamp_str = event_data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00")) if isinstance(timestamp_str, str) else timestamp_str
        
        retries = event_data.get("retries", 0)
        
        success = await send_to_salesforce_mock(event_id, customer_name)
        
        if success:
            # --- SALVANDO NO BANCO ANALÍTICO ---
            save_interaction(event_id, phone_number_masked, customer_name, message_text, timestamp)
            print(f"[WORKER] ✅ Sucesso e Persistência Concluída para o evento {event_id}.")
        else:
            if retries < MAX_RETRIES - 1:
                event_data["retries"] = retries + 1
                await sqs_queue_simulation.put(event_data)
            else:
                dlq_queue_simulation.append(event_data)
                print(f"[WORKER] 🚨 CRÍTICO: Evento {event_id} enviado para a DLQ.")
        
        sqs_queue_simulation.task_done()
