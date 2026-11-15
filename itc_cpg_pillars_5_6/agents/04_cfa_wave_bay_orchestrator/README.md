# 04 · CFA Wave & Bay Orchestrator

- **Enterprise Scope**: ITC Limited — Consumer Packaged Goods (CPG) Trade Marketing & Distribution (TM&D)
- **Functional Area**: CFA / Depot Operations & Stock Allocation (Pillar 05 · CFA Operations & Omnichannel Fulfillment)
- **Persona Owner**: **Depot / CFA Operations Manager** (*Suresh Deshpande (Regional Mother CFA Manager — Bhiwandi & Kundli)*)
- **Build Mode**: **`Low-Code Agent Studio`** · **Priority**: `P0`
- **Model Routing (`GlobalGemini`, `location="global"`)**: `gemini-3.1-pro-preview`
- **Reuse & Provenance (`REUSED_AND_TAILORED`)**: `wave_fulfillment_copilot`, `fefo_shelf_life_allocator`, `warehouse_slotting_agent`

## 1. Operational Problem Solved in ITC CPG
State CFAs simultaneously pick rapid Quick-Commerce waves (strict 75% Minimum Remaining Shelf-Life gate, 10:30 cutoff), Modern Trade pallets, and General Trade Wholesale Dealer loads (55% MRSL gate). Unbalanced bays miss morning cutoffs while blind picking sends older batches to Quick-Commerce (causing instant dock rejection) and wastes ultra-fresh batches on General Trade.

## 2. Researched 4-Lever Annual Value Attribution (`₹21.1 Cr/yr`)
| Value Lever | Annual Impact (INR) | Attribution Note |
| :--- | :--- | :--- |
| **Productivity** | ₹3.8 Cr/yr | Planner / supervisor / field-manager toil eliminated |
| **Flow & Capital** | ₹9.4 Cr/yr | Dock, CFA wave, transit velocity & inventory turnover |
| **Risk & Leakage** | ₹7.9 Cr/yr | Freight overcharges, detention slabs, OTIF penalties & spoilage |
| **Revenue Recovery** | — (Load-Bearing Zero) | Prevented stockouts, saved cutoffs & protected channel fill |

> **Load-Bearing Zero Discipline**: Executes existing booked orders faster and cleaner without altering commercial demand; drives picker throughput (Productivity), bay velocity (Flow), and zero shelf-life rejections (Risk).

## 3. Connected Systems & Human Sign-Off Gate
- **Target System**: SAP Extended Warehouse Management (SAP EWM) Pick-Wave & Loading Bay Controller
- **Primary Fact Table**: `enterprise_data/lake_full/04_cfa_wms_pick_waves_fefo_and_bays.csv`
- **Human Gate (`STOPS AT`)**: Never dispatches batches violating customer Minimum Remaining Shelf-Life (MRSL) gates or overrides cold-room safety capacity without CFA Manager sign-off.

## 4. Mode-Specific Specifications Included
- `studio_specs/gemini_enterprise_agent_studio.yaml`
- `studio_specs/openapi_tools_spec.json`

## 5. Plain-English Business Starter Prompts
1. *"Which pick waves and loading bays at Bhiwandi and Kundli CFAs are congested or about to miss morning dispatch cutoffs, and are any Quick-Commerce orders picking batches that will fail the 75% shelf-life rule?"*
2. *"Show how we can swap batch allocations between Quick-Commerce and General Trade waves so fresh stock protects Blinkit/Zepto while older compliant stock moves through Wholesale Dealers."*
3. *"Generate a chart of protected dispatch value across our rebalanced CFA pick waves."*
4. *"Stage the bay reassignments, picker shifts, and FEFO batch swaps in the warehouse system."*
