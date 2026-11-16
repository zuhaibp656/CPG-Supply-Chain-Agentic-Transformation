# 04 · CFA Wave & Bay Orchestrator (ITC TMD)

- **Gemini Enterprise Display Name**: **`CFA Wave & Bay Orchestrator (ITC TMD)`**
- **Functional Area**: CFA / Depot Operations & Stock Allocation (Pillar 05 · CFA Operations & Omnichannel Fulfillment)
- **Persona Owner**: **Depot / CFA Operations Manager** (*Suresh Deshpande (Regional Mother CFA Manager — Bhiwandi & Kundli)*)
- **Build Mode**: **`Google ADK + Python Solvers`** · **Priority**: `P0`
- **Model Routing (`GlobalGemini`, `location="global"`)**: `gemini-3.1-pro-preview`

## 1. On-Screen Gemini Enterprise Starter Prompts (4 Authentic Persona Prompts)
1. `"How are morning pick waves and loading bays tracking at Bhiwandi and Kundli, and will any wave miss its dispatch cutoff?"`
2. `"Are any Blinkit or Zepto orders picking older stock that could get rejected at their dock for having less than 75% shelf life?"`
3. `"Swap those older compliant batches to General Trade beats, rebalance the pickers across bays, and stage the updated wave plan."`
4. `"Simulate shifting four General Trade pickers to Quick-Commerce bays at Bhiwandi before noon. How much dispatch revenue is protected before cutoff?"`

## 2. Operational Problem Solved in ITC CPG
State CFAs simultaneously pick rapid Quick-Commerce waves (strict 75% Minimum Remaining Shelf-Life gate, 10:30 cutoff), Modern Trade pallets, and General Trade Wholesale Dealer loads (55% MRSL gate). Unbalanced bays miss morning cutoffs while blind picking sends older batches to Quick-Commerce.

## 3. Researched 4-Lever Annual Value Attribution (`₹21.1 Cr/yr`)
| Value Lever | Annual Impact (INR) |
| :--- | :--- |
| **Productivity** | ₹3.8 Cr/yr |
| **Flow & Capital** | ₹9.4 Cr/yr |
| **Risk & Leakage** | ₹7.9 Cr/yr |
| **Revenue Recovery** | — (Load-Bearing Zero) |
