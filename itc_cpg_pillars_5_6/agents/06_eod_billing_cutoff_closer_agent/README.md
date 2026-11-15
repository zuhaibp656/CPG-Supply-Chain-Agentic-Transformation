# 06 · EOD Billing & Cutoff Closer Agent (ITC TMD)

- **Gemini Enterprise Display Name**: **`EOD Billing & Cutoff Closer Agent (ITC TMD)`**
- **Functional Area**: CFA / Depot Operations & Stock Allocation (Pillar 05 · CFA Billing & SAP Cutoff Governance)
- **Persona Owner**: **Depot Dispatch & Billing Supervisor** (*Prakash Kulkarni (CFA Commercial & SAP Billing Lead — Bhiwandi & Dankuni)*)
- **Build Mode**: **`Low-Code + SAP OpenAPI`** · **Priority**: `P0`
- **Model Routing (`GlobalGemini`, `location="global"`)**: `gemini-3.1-pro-preview`

## 1. On-Screen Gemini Enterprise Starter Prompts (3 Authentic Persona Prompts)
1. `"Which loaded trucks at our depots are still unbilled before tonight's 9 PM SAP cutoff, and what is holding each one up?"`
2. `"Separate the deliveries we can clear right away, like batch splits, FinAgg credit sync, or E-Way Bill typos, from overdue credit holds."`
3. `"Clear the fixable SAP delivery, e-Invoice, and E-Way Bill errors for my sign-off and flag the overdue account to Finance."`

## 2. Operational Problem Solved in ITC CPG
Every evening before the 21:00 IST gate lock, loaded trucks sit trapped at CFA gates because SAP outbound deliveries (`VL02N`) fail Post Goods Issue or `VF01` billing due to FEFO batch-split variances, unsynced FinAgg dealer credit drawdowns, or hyphen typos in NIC E-Way Bill Part-B vehicle numbers.

## 3. Researched 4-Lever Annual Value Attribution (`₹29.8 Cr/yr`)
| Value Lever | Annual Impact (INR) |
| :--- | :--- |
| **Productivity** | ₹3.4 Cr/yr |
| **Flow & Capital** | ₹14.6 Cr/yr |
| **Risk & Leakage** | — (Load-Bearing Zero) |
| **Revenue Recovery** | ₹11.8 Cr/yr |
