# 09 · Predictive WD Reorder & Dispatch Agent (ITC TMD)

- **Gemini Enterprise Display Name**: **`Predictive WD Reorder & Dispatch Agent (ITC TMD)`**
- **Functional Area**: Channel & Route-to-Market (GT, MT & Q-Commerce) (Pillar 05 · Wholesale Dealer (WD) Replenishment & FinAgg Credit)
- **Persona Owner**: **Wholesale Dealer (WD) / Stockist Ops Mgr** (*Rajeshwar Rao (TM&D Stockist Operations & DMS Lead — Mumbai, Bengaluru & Kolkata)*)
- **Build Mode**: **`Google ADK + Python Solvers`** · **Priority**: `P0`
- **Model Routing (`GlobalGemini`, `location="global"`)**: `gemini-3.1-pro-preview`

## 1. On-Screen Gemini Enterprise Starter Prompts (4 Authentic Persona Prompts)
1. `"Which wholesale dealers have dropped below four days of stock on fast-moving SKUs and risk running dry in the next 48 hours?"`
2. `"Do Mahavir Agencies, Kaveri Distributors, and Hooghly Enterprises have enough godown space and FinAgg credit room for a top-up load?"`
3. `"Prepare the primary replenishment orders and FinAgg credit drawdowns for dealer confirmation."`
4. `"Simulate a 25% festive demand surge next week. Which wholesale dealers run out of stock first and need higher FinAgg credit headroom?"`

## 2. Operational Problem Solved in ITC CPG
Wholesale Dealers frequently under-order core staples during UNNATI scheme surges (causing kirana stockouts within 48 hours) or hit credit-limit walls mid-week despite having approved FinAgg/SBI supply-chain credit headroom.

## 3. Researched 4-Lever Annual Value Attribution (`₹32.6 Cr/yr`)
| Value Lever | Annual Impact (INR) |
| :--- | :--- |
| **Productivity** | ₹2.6 Cr/yr |
| **Flow & Capital** | ₹10.8 Cr/yr |
| **Risk & Leakage** | — (Load-Bearing Zero) |
| **Revenue Recovery** | ₹19.2 Cr/yr |
