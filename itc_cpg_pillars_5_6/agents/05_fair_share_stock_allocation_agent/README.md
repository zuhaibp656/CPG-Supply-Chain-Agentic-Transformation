# 05 · Fair-Share Stock Allocation Agent

- **Enterprise Scope**: ITC Limited — Consumer Packaged Goods (CPG) Trade Marketing & Distribution (TM&D)
- **Functional Area**: CFA / Depot Operations & Stock Allocation (Pillar 05 · CFA Operations & Stock Allocation)
- **Persona Owner**: **Customer Service & Logistics (CS&L) Lead** (*Meenakshi Sundaram (Zonal CS&L Head — Bengaluru & Southern Hub)*)
- **Build Mode**: **`Low-Code Agent Studio`** · **Priority**: `P0`
- **Model Routing (`GlobalGemini`, `location="global"`)**: `gemini-3.1-pro-preview`
- **Reuse & Provenance (`REUSED_AND_TAILORED`)**: `echelon_inventory_allocator`, `dynamic_order_promising_atp`, `atp_order_promising_agent`

## 1. Operational Problem Solved in ITC CPG
When a high-velocity SKU like Sunfeast Dark Fantasy 300g is constrained at a State CFA (e.g., 2,400 cases available vs 3,650 ordered), standard SAP First-In-First-Out (FIFO) lets early Modern Trade bulk orders consume 100% of stock—starving 18 General Trade Wholesale Dealers and UNNATI kiranas or triggering steep 8% Quick-Commerce OTIF penalties.

## 2. Researched 4-Lever Annual Value Attribution (`₹27.4 Cr/yr`)
| Value Lever | Annual Impact (INR) | Attribution Note |
| :--- | :--- | :--- |
| **Productivity** | ₹1.8 Cr/yr | Planner / supervisor / field-manager toil eliminated |
| **Flow & Capital** | — (Load-Bearing Zero) | Dock, CFA wave, transit velocity & inventory turnover |
| **Risk & Leakage** | ₹9.1 Cr/yr | Freight overcharges, detention slabs, OTIF penalties & spoilage |
| **Revenue Recovery** | ₹16.5 Cr/yr | Prevented stockouts, saved cutoffs & protected channel fill |

> **Load-Bearing Zero Discipline**: Allocates already-manufactured scarce stock (Flow = 0); shields steep Modern Trade/Q-Comm OTIF chargebacks (Risk) and preserves high-margin UNNATI/General Trade sell-through (Revenue Recovery).

## 3. Connected Systems & Human Sign-Off Gate
- **Target System**: SAP S/4HANA Advanced Available-to-Promise (aATP) & Order Rationing Engine
- **Primary Fact Table**: `enterprise_data/lake_full/05_csl_shortage_orders_and_channel_allocations.csv`
- **Human Gate (`STOPS AT`)**: Never zeroes out General Trade baseline territory floors or overrides contractual key-account allocation commitments without CS&L Lead approval.

## 4. Mode-Specific Specifications Included
- `studio_specs/gemini_enterprise_agent_studio.yaml`
- `studio_specs/openapi_tools_spec.json`

## 5. Plain-English Business Starter Prompts
1. *"We only have 2,400 cases of Sunfeast Dark Fantasy 300g at Nelamangala Bengaluru CFA against 3,650 cases of competing orders—how should we ration stock fairly across Quick-Commerce, Modern Trade, UNNATI kiranas, and Wholesale Dealers?"*
2. *"Compare our Linear Programming fair-share split against standard First-In-First-Out allocation so we see how much penalty and margin we save without starving General Trade."*
3. *"Plot the recommended case allocation and fill rate across each channel."*
4. *"Stage the approved fair-share allocation quantities into SAP Available-to-Promise for release."*
