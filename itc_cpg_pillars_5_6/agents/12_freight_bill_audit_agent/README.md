# 12 · Freight Bill Audit Agent (ITC TMD)

- **Gemini Enterprise Display Name**: **`Freight Bill Audit Agent (ITC TMD)`**
- **Functional Area**: Fleet, Carrier & Freight Governance (Pillar 06 · Multimodal Freight Audit, POD & Claims Settlement)
- **Persona Owner**: **Freight Bill & Claims Controller** (*Subhashish Mukherjee (National Freight Audit & Commercial Claims Controller — Kolkata)*)
- **Build Mode**: **`Multimodal + Agent Studio`** · **Priority**: `P0`
- **Model Routing (`GlobalGemini`, `location="global"`)**: `gemini-3.1-pro-preview`

## 1. On-Screen Gemini Enterprise Starter Prompts (3 Authentic Persona Prompts)
1. `"Audit this week's pending transporter freight bills. Where do billed rates, fuel surcharges, or detention hours disagree with our contracts and GPS logs?"`
2. `"Check the scanned lorry receipts and stamped delivery slips on LR-TCI-882910 and LR-HWK-771024 for damaged cartons or duplicate billing."`
3. `"Block the duplicate bill and stage short-pay vouchers deducting the unverified detention and damaged Dark Fantasy cartons."`

## 2. Operational Problem Solved in ITC CPG
Indian CPG freight settlement requires reconciling paper-heavy Lorry Receipts (Bilty), rubber-stamped CFA Proof-of-Delivery (POD) slips with handwritten wet/crushed carton remarks, contracted diesel escalation pegs, and GPS-verified gate detention hours.

## 3. Researched 4-Lever Annual Value Attribution (`₹25.5 Cr/yr`)
| Value Lever | Annual Impact (INR) |
| :--- | :--- |
| **Productivity** | ₹3.9 Cr/yr |
| **Flow & Capital** | — (Load-Bearing Zero) |
| **Risk & Leakage** | ₹21.6 Cr/yr |
| **Revenue Recovery** | — (Load-Bearing Zero) |
