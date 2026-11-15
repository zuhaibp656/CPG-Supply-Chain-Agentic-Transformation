# 09 · Predictive WD Reorder & Dispatch Agent

- **Enterprise Scope**: ITC Limited — Consumer Packaged Goods (CPG) Trade Marketing & Distribution (TM&D)
- **Functional Area**: Channel & Route-to-Market (GT, MT & Q-Commerce) (Pillar 05 · Wholesale Dealer (WD) Replenishment & FinAgg Credit)
- **Persona Owner**: **Wholesale Dealer (WD) / Stockist Ops Mgr** (*Rajeshwar Rao (TM&D Stockist Operations & DMS Lead — Mumbai, Bengaluru & Kolkata)*)
- **Build Mode**: **`Low-Code Agent Studio`** · **Priority**: `P0`
- **Model Routing (`GlobalGemini`, `location="global"`)**: `gemini-3.1-pro-preview`
- **Reuse & Provenance (`REUSED_AND_TAILORED`)**: `dms_distributor_stock_balancer`, `store_capacity_agent (Live GE: reasoningEngines/7365119595465670656)`

## 1. Operational Problem Solved in ITC CPG
Wholesale Dealers frequently under-order core staples during UNNATI scheme surges (causing kirana stockouts within 48 hours) or hit credit-limit walls mid-week despite having approved FinAgg/SBI supply-chain credit headroom—while manual push dispatches overflow small urban WD godowns.

## 2. Researched 4-Lever Annual Value Attribution (`₹32.6 Cr/yr`)
| Value Lever | Annual Impact (INR) | Attribution Note |
| :--- | :--- | :--- |
| **Productivity** | ₹2.6 Cr/yr | Planner / supervisor / field-manager toil eliminated |
| **Flow & Capital** | ₹10.8 Cr/yr | Dock, CFA wave, transit velocity & inventory turnover |
| **Risk & Leakage** | — (Load-Bearing Zero) | Freight overcharges, detention slabs, OTIF penalties & spoilage |
| **Revenue Recovery** | ₹19.2 Cr/yr | Prevented stockouts, saved cutoffs & protected channel fill |

> **Load-Bearing Zero Discipline**: Operates within pre-underwritten FinAgg/bank credit limits (Risk = 0); stabilizes WD Days-of-Inventory turnover (Flow), automates DMS order generation (Productivity), and eliminates secondary kirana stockouts (Revenue Recovery).

## 3. Connected Systems & Human Sign-Off Gate
- **Target System**: ITC Distribution Management System (DMS) -> SAP S/4HANA Primary Sales Order (`VA01`) & FinAgg Credit API
- **Primary Fact Table**: `enterprise_data/lake_full/09_wd_stockist_doi_credit_and_reorders.csv`
- **Human Gate (`STOPS AT`)**: Never converts draft primary orders into firm SAP billing without Wholesale Dealer OTP/portal consent or FinAgg/bank credit-line confirmation.

## 4. Mode-Specific Specifications Included
- `studio_specs/gemini_enterprise_agent_studio.yaml`
- `studio_specs/openapi_tools_spec.json`

## 5. Plain-English Business Starter Prompts
1. *"Which Wholesale Dealers are below 4 days of inventory on high-velocity SKUs and risk stocking out within 48 hours, and how many cases should we replenish respecting their godown space and FinAgg credit limit?"*
2. *"Which dealers need an automated FinAgg supply-chain credit drawdown so their urgent replenishment order doesn't get credit-blocked in SAP?"*
3. *"Show a chart of recommended primary replenishment order values across our most stockout-exposed Wholesale Dealers."*
4. *"Stage the predictive Wholesale Dealer replenishment orders in DMS and SAP for dealer confirmation."*
