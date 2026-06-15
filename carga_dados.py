from datetime import datetime
from app.databases.db import save_interaction, init_db

# Garante que o banco e a tabela existam
init_db()

print("[CARGA] Inserindo dados fictícios de jornadas de clientes...")

# Massa de dados simulando interações em momentos diferentes
massa_testes = [
    ("evt_boti_101", "+5511999992222", "Lucas Souza", "Olá! Tem cupom de desconto?", datetime(2026, 6, 14, 10, 0, 0)),
    ("evt_boti_102", "+5511999992222", "Lucas Souza", "Quero o cupom de primeira compra.", datetime(2026, 6, 14, 10, 5, 0)), # Mensagem seguida
    ("evt_boti_103", "+5521988883333", "Maria Fernanda", "Minha base Make B. chegou errada.", datetime(2026, 6, 14, 11, 30, 0)),
    ("evt_boti_104", "+5511977774444", "Weslley Lima", "Quero rastrear meu pedido.", datetime(2026, 6, 14, 14, 15, 0)),
    ("evt_boti_105", "+5511999992222", "Lucas Souza", "Obrigado, consegui usar o cupom!", datetime(2026, 6, 14, 14, 30, 0)), # Outra mensagem mais tarde
]

for event_id, phone, name, text, dt in massa_testes:
    # Simulando o formato mascarado que o worker salvaria
    phone_masked = f"{phone[:5]}*****{phone[-4:]}"
    save_interaction(event_id, phone_masked, name, text, dt)

print("[CARGA] 🏁 Dados populados com sucesso!")