# 🌿 FarmaFlow

Sistema modular de gestão para redes farmacêuticas. Integra operações, logística, caixa, estoque, financeiro e gestão em um único ambiente — construído do zero, módulo por módulo.

---

## 💡 Origem do Projeto

FarmaFlow nasceu da observação direta da operação de uma farmácia. Processos manuais, comunicação via WhatsApp, conferências em papel e erros descobertos tarde demais — na porta do cliente.

O sistema foi projetado para eliminar esses gargalos um módulo de cada vez, integrando todos os setores num banco de dados central.

---

## 🏗️ Arquitetura

Todos os módulos compartilham um único banco de dados central (`farmaflow.db`), permitindo que dados fluam entre setores sem repasse manual.

```
farmaflow/
│
├── banco.py              # Banco central — todas as tabelas e funções
├── farmaflow.db          # Banco de dados SQLite gerado automaticamente
│
├── caixa.py              # Módulo 02 — Caixa e Conferência
│
└── [módulos futuros]
    ├── entregas.py       # Módulo 01 — Entregas (migração em andamento)
    ├── estoque.py        # Módulo 03 — Estoque
    ├── financeiro.py     # Módulo 04 — Financeiro
    ├── rh.py             # Módulo 05 — RH e Equipe
    └── gerencial.py      # Módulo 06 — Painel Gerencial
```

---

## ✅ Módulos

### ✅ Módulo 01 — Entregas
Controla o ciclo completo de entregas: registro, acompanhamento em tempo real, cronômetro de saída e relatório diário.

**Funcionalidades:**
- Numeração automática de pedidos (`ENT-001`, `ENT-002`...)
- Fluxo de status: Aguardando Retirada → Em Rota → Entregue / Devolvido / Pendente
- Histórico de cada mudança de status com horário
- Cronômetro regressivo de 5 minutos com alerta visual e sonoro
- Relatório diário com percentual no prazo e saídas registradas

---

### ✅ Módulo 02 — Caixa e Conferência
Elimina o repasse manual entre o caixa e o entregador. Cria registro formal de cada pedido conferido e conecta automaticamente com o módulo de entregas.

**Funcionalidades:**
- Registro de pedidos pela operadora com itens, valor e forma de pagamento
- Formas de pagamento: Pago, Dinheiro, Pix, Cartão na Entrega
- Campo de troco condicional — aparece apenas quando necessário
- Confirmação de recebimento pelo entregador com registro de horário
- Tabela de pedidos do dia com status de confirmação em tempo real
- Rastreabilidade completa: quem registrou, quem confirmou e quando

---

### 🔜 Módulo 03 — Estoque
Controle de entradas e saídas, alertas de nível crítico e rastreamento por setor.

### 🔜 Módulo 04 — Financeiro
Registro de custos por categoria, comparação com orçamento e identificação de desvios.

### 🔜 Módulo 05 — RH e Equipe
Gestão de colaboradores, jornada e indicadores de performance.

### 🔜 Módulo 06 — Painel Gerencial
Dashboard central com dados em tempo real de todos os módulos — elimina a conferência manual do gestor.

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|------------|-----|
| Python 3.11 | Linguagem principal |
| Tkinter | Interface gráfica desktop |
| SQLite | Banco de dados central |

Sem dependências externas. Roda diretamente com Python instalado.

---

## ▶️ Como Executar

**Pré-requisito:** Python 3.8 ou superior instalado.

```bash
# Clone o repositório
git clone https://github.com/WilliandosSantos89/farmaflow.git

# Acesse a pasta
cd farmaflow

# Execute o módulo desejado
python caixa.py
```

O banco de dados é criado automaticamente na primeira execução.

---

## 🗺️ Roadmap

- [x] Módulo 01 — Entregas
- [x] Módulo 02 — Caixa e Conferência
- [ ] Migração do Módulo 01 para o repositório FarmaFlow
- [ ] Módulo 03 — Estoque
- [ ] Módulo 04 — Financeiro
- [ ] Módulo 05 — RH e Equipe
- [ ] Módulo 06 — Painel Gerencial
- [ ] Sistema web com notificação ao cliente
- [ ] Otimização de rota no mapa

---

## 👤 Autor

**Willian dos Santos**
Desenvolvedor em formação | ADS | Administração
[LinkedIn](https://www.linkedin.com/in/willian-dos-santos) • [GitHub](https://github.com/WilliandosSantos89)