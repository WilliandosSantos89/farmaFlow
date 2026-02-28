import tkinter as tk
from tkinter import messagebox, ttk
from banco import (conectar, criar_tabelas, registrar_pedido_caixa,
                   confirmar_recebimento, gerar_numero_pedido)
from datetime import date

COR_FUNDO      = "#f4f6f9"
COR_PRIMARIA   = "#2d6a4f"
COR_SECUNDARIA = "#40916c"
COR_TEXTO      = "#1b1b1b"
COR_BRANCO     = "#ffffff"
COR_ALERTA     = "#e07b00"
FONTE_TITULO   = ("Segoe UI", 16, "bold")
FONTE_NORMAL   = ("Segoe UI", 10)
FONTE_BTN      = ("Segoe UI", 10, "bold")

FORMAS_PAGAMENTO = ["Pago", "Dinheiro", "Cartão na Entrega"]
OPERADORAS       = ["Operadora 1", "Operadora 2", "Operadora 3"]
ENTREGADORES     = ["Entregador 1", "Entregador 2", "Entregador 3"]


class AppCaixa:
    def __init__(self, root):
        self.root = root
        self.root.title("FarmaFlow — Caixa e Conferência")
        self.root.configure(bg=COR_FUNDO)
        self.root.resizable(False, False)
        criar_tabelas()
        self.tela_principal()

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ── TELA PRINCIPAL ───────────────────────────────────────
    def tela_principal(self):
        self.limpar_tela()
        self.root.geometry("500x380")

        tk.Label(self.root, text="Caixa e Conferência",
                 font=FONTE_TITULO, bg=COR_FUNDO,
                 fg=COR_PRIMARIA).pack(pady=25)

        tk.Label(self.root, text="FarmaFlow — Módulo 02",
                 font=FONTE_NORMAL, bg=COR_FUNDO,
                 fg="#888").pack()

        botoes = [
            ("📋  Registrar Pedido",          self.tela_registrar_pedido),
            ("✔   Confirmar Recebimento",      self.tela_confirmar_recebimento),
            ("📊  Pedidos do Dia",             self.tela_pedidos_dia),
        ]

        for texto, comando in botoes:
            tk.Button(self.root, text=texto, command=comando,
                      font=FONTE_BTN, bg=COR_PRIMARIA,
                      fg=COR_BRANCO, width=28, pady=8,
                      relief="flat", cursor="hand2",
                      activebackground=COR_SECUNDARIA,
                      activeforeground=COR_BRANCO).pack(pady=7)

    # ── TELA REGISTRAR PEDIDO ────────────────────────────────
    def tela_registrar_pedido(self):
        self.limpar_tela()
        self.root.geometry("500x640")

        tk.Label(self.root, text="Registrar Pedido",
                 font=FONTE_TITULO, bg=COR_FUNDO,
                 fg=COR_PRIMARIA).pack(pady=15)

        frame = tk.Frame(self.root, bg=COR_FUNDO)
        frame.pack(padx=30, fill="x")

        campos = {}

        def campo(label, chave, valor_inicial=""):
            tk.Label(frame, text=label, font=FONTE_NORMAL,
                     bg=COR_FUNDO, fg=COR_TEXTO,
                     anchor="w").pack(fill="x", pady=(8, 0))
            var = tk.StringVar(value=valor_inicial)
            entry = tk.Entry(frame, textvariable=var,
                             font=FONTE_NORMAL, relief="solid", bd=1)
            entry.pack(fill="x", ipady=5)
            campos[chave] = entry
            return entry

        def combo(label, chave, valores, padrao):
            tk.Label(frame, text=label, font=FONTE_NORMAL,
                     bg=COR_FUNDO, fg=COR_TEXTO,
                     anchor="w").pack(fill="x", pady=(8, 0))
            var = tk.StringVar(value=padrao)
            cb = ttk.Combobox(frame, textvariable=var,
                              values=valores, state="readonly",
                              font=FONTE_NORMAL)
            cb.pack(fill="x", ipady=5)
            campos[chave] = cb
            return var

        # número do pedido automático
        tk.Label(frame, text="Número do Pedido", font=FONTE_NORMAL,
                 bg=COR_FUNDO, fg=COR_TEXTO, anchor="w").pack(fill="x", pady=(8, 0))
        num_var = tk.StringVar(value=gerar_numero_pedido())
        tk.Entry(frame, textvariable=num_var, font=FONTE_NORMAL,
                 relief="solid", bd=1, state="disabled",
                 disabledforeground="#555",
                 disabledbackground="#e8ece8").pack(fill="x", ipady=5)

        op_var  = combo("Operadora",          "operadora",       OPERADORAS,       OPERADORAS[0])
        campo("Itens do Pedido",              "itens")
        campo("Valor Total (R$)",             "valor_total")
        fp_var  = combo("Forma de Pagamento", "forma_pagamento", FORMAS_PAGAMENTO, FORMAS_PAGAMENTO[0])

        # troco só aparece se pagamento for dinheiro
        troco_label = tk.Label(frame, text="Troco (R$)", font=FONTE_NORMAL,
                               bg=COR_FUNDO, fg=COR_TEXTO, anchor="w")
        troco_entry = tk.Entry(frame, font=FONTE_NORMAL, relief="solid", bd=1)

        def atualizar_troco(*args):
            if fp_var.get() == "Dinheiro":
                troco_label.pack(fill="x", pady=(8, 0))
                troco_entry.pack(fill="x", ipady=5)
            else:
                troco_label.pack_forget()
                troco_entry.pack_forget()

        fp_var.trace("w", atualizar_troco)

        def salvar():
            itens      = campos["itens"].get().strip()
            valor_str  = campos["valor_total"].get().strip()

            if not itens or not valor_str:
                messagebox.showwarning("Atenção", "Preencha itens e valor.")
                return

            try:
                valor = float(valor_str.replace(",", "."))
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido. Use números.")
                return

            troco = 0.0
            if fp_var.get() == "Dinheiro":
                try:
                    troco = float(troco_entry.get().replace(",", ".") or "0")
                except ValueError:
                    troco = 0.0

            pedido_id = registrar_pedido_caixa(
                numero_pedido    = num_var.get(),
                operadora        = op_var.get(),
                itens            = itens,
                valor_total      = valor,
                forma_pagamento  = fp_var.get(),
                troco            = troco
            )

            messagebox.showinfo("Sucesso",
                f"Pedido {num_var.get()} registrado!\nAguardando confirmação do entregador.")
            self.tela_principal()

        tk.Button(frame, text="✔  Salvar Pedido", command=salvar,
                  font=FONTE_BTN, bg=COR_PRIMARIA, fg=COR_BRANCO,
                  width=25, pady=8, relief="flat",
                  cursor="hand2").pack(pady=15)

        tk.Button(frame, text="← Voltar", command=self.tela_principal,
                  font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_PRIMARIA,
                  relief="flat", cursor="hand2").pack(pady=(0, 15))

    # ── TELA CONFIRMAR RECEBIMENTO ───────────────────────────
    def tela_confirmar_recebimento(self):
        self.limpar_tela()
        self.root.geometry("600x480")

        tk.Label(self.root, text="Confirmar Recebimento",
                 font=FONTE_TITULO, bg=COR_FUNDO,
                 fg=COR_PRIMARIA).pack(pady=15)

        frame = tk.Frame(self.root, bg=COR_FUNDO)
        frame.pack(fill="both", expand=True, padx=15)

        colunas = ("ID", "Pedido", "Itens", "Valor", "Pagamento", "Troco")
        tabela = ttk.Treeview(frame, columns=colunas,
                              show="headings", height=10)

        larguras = [40, 80, 200, 70, 110, 60]
        for col, larg in zip(colunas, larguras):
            tabela.heading(col, text=col)
            tabela.column(col, width=larg, anchor="center")

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.numero_pedido, p.itens,
                   p.valor_total, p.forma_pagamento, p.troco
            FROM pedidos_caixa p
            WHERE p.data = ?
            AND p.id NOT IN (
                SELECT pedido_id FROM confirmacoes_recebimento
            )
            ORDER BY p.id ASC
        """, (date.today().isoformat(),))
        for row in cursor.fetchall():
            tabela.insert("", "end", values=row)
        conn.close()

        tabela.pack(fill="both", expand=True)

        tk.Label(self.root, text="Entregador", font=FONTE_NORMAL,
                 bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=(10, 0))
        ent_var = tk.StringVar(value=ENTREGADORES[0])
        ttk.Combobox(self.root, textvariable=ent_var,
                     values=ENTREGADORES, state="readonly",
                     font=FONTE_NORMAL, width=25).pack()

        def confirmar():
            selecionado = tabela.selection()
            if not selecionado:
                messagebox.showwarning("Atenção", "Selecione um pedido.")
                return
            pedido_id = tabela.item(selecionado[0])["values"][0]
            numero    = tabela.item(selecionado[0])["values"][1]
            confirmar_recebimento(pedido_id, ent_var.get())
            messagebox.showinfo("Confirmado",
                f"Pedido {numero} confirmado por {ent_var.get()}!")
            self.tela_confirmar_recebimento()

        tk.Button(self.root, text="✔  Confirmar Recebimento",
                  command=confirmar,
                  font=FONTE_BTN, bg=COR_PRIMARIA, fg=COR_BRANCO,
                  width=25, pady=6, relief="flat",
                  cursor="hand2").pack(pady=10)

        tk.Button(self.root, text="← Voltar", command=self.tela_principal,
                  font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_PRIMARIA,
                  relief="flat", cursor="hand2").pack()

    # ── TELA PEDIDOS DO DIA ──────────────────────────────────
    def tela_pedidos_dia(self):
        self.limpar_tela()
        self.root.geometry("700x480")

        tk.Label(self.root, text="Pedidos do Dia",
                 font=FONTE_TITULO, bg=COR_FUNDO,
                 fg=COR_PRIMARIA).pack(pady=15)

        frame = tk.Frame(self.root, bg=COR_FUNDO)
        frame.pack(fill="both", expand=True, padx=15)

        colunas = ("Pedido", "Operadora", "Valor", "Pagamento", "Confirmado por", "Horário")
        tabela = ttk.Treeview(frame, columns=colunas,
                              show="headings", height=12)

        larguras = [80, 110, 70, 110, 130, 70]
        for col, larg in zip(colunas, larguras):
            tabela.heading(col, text=col)
            tabela.column(col, width=larg, anchor="center")

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.numero_pedido, p.operadora, p.valor_total,
                   p.forma_pagamento,
                   COALESCE(c.entregador, '⏳ Pendente'),
                   p.horario_registro
            FROM pedidos_caixa p
            LEFT JOIN confirmacoes_recebimento c ON c.pedido_id = p.id
            WHERE p.data = ?
            ORDER BY p.id ASC
        """, (date.today().isoformat(),))
        for row in cursor.fetchall():
            tabela.insert("", "end", values=row)
        conn.close()

        tabela.pack(fill="both", expand=True)

        tk.Button(self.root, text="← Voltar", command=self.tela_principal,
                  font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_PRIMARIA,
                  relief="flat", cursor="hand2").pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    AppCaixa(root)
    root.mainloop()