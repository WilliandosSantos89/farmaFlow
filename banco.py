import sqlite3
from datetime import date, datetime

def conectar():
    return sqlite3.connect("farmaflow.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # ── MÓDULO 01 — ENTREGAS ─────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entregas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_pedido TEXT NOT NULL,
            cliente TEXT NOT NULL,
            endereco TEXT NOT NULL,
            regiao TEXT,
            horario_previsto TEXT,
            horario_real TEXT,
            status TEXT NOT NULL,
            acompanhamento TEXT,
            data TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entrega_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            horario TEXT NOT NULL,
            FOREIGN KEY (entrega_id) REFERENCES entregas(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros_saida (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entregador TEXT,
            horario_inicio TEXT NOT NULL,
            horario_saida TEXT,
            saiu_no_prazo INTEGER,
            data TEXT NOT NULL
        )
    """)

    # ── MÓDULO 02 — CAIXA E CONFERÊNCIA ──────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos_caixa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_pedido TEXT NOT NULL,
            operadora TEXT NOT NULL,
            itens TEXT NOT NULL,
            valor_total REAL NOT NULL,
            forma_pagamento TEXT NOT NULL,
            troco REAL,
            horario_registro TEXT NOT NULL,
            data TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS confirmacoes_recebimento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            entregador TEXT NOT NULL,
            horario_confirmacao TEXT NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos_caixa(id)
        )
    """)

    conn.commit()
    conn.close()

# ── MÓDULO 01 — FUNÇÕES ──────────────────────────────────────
def gerar_numero_pedido():
    conn = conectar()
    cursor = conn.cursor()
    hoje = date.today().isoformat()
    cursor.execute("SELECT COUNT(*) FROM entregas WHERE data = ?", (hoje,))
    total = cursor.fetchone()[0]
    conn.close()
    return f"ENT-{str(total + 1).zfill(3)}"

def registrar_historico(entrega_id, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO historico_status (entrega_id, status, horario)
        VALUES (?, ?, ?)
    """, (entrega_id, status, datetime.now().strftime("%H:%M")))
    conn.commit()
    conn.close()

def iniciar_cronometro(entregador=""):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO registros_saida (entregador, horario_inicio, data)
        VALUES (?, ?, ?)
    """, (entregador, datetime.now().strftime("%H:%M:%S"), date.today().isoformat()))
    registro_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return registro_id

def registrar_saida(registro_id, saiu_no_prazo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE registros_saida
        SET horario_saida = ?, saiu_no_prazo = ?
        WHERE id = ?
    """, (datetime.now().strftime("%H:%M:%S"), 1 if saiu_no_prazo else 0, registro_id))
    conn.commit()
    conn.close()

# ── MÓDULO 02 — FUNÇÕES ──────────────────────────────────────
def registrar_pedido_caixa(numero_pedido, operadora, itens,
                            valor_total, forma_pagamento, troco=0):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pedidos_caixa
        (numero_pedido, operadora, itens, valor_total,
         forma_pagamento, troco, horario_registro, data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        numero_pedido, operadora, itens, valor_total,
        forma_pagamento, troco,
        datetime.now().strftime("%H:%M"),
        date.today().isoformat()
    ))
    pedido_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return pedido_id

def confirmar_recebimento(pedido_id, entregador):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO confirmacoes_recebimento
        (pedido_id, entregador, horario_confirmacao, data)
        VALUES (?, ?, ?, ?)
    """, (
        pedido_id, entregador,
        datetime.now().strftime("%H:%M"),
        date.today().isoformat()
    ))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabelas()
    print("Banco FarmaFlow criado com sucesso.")