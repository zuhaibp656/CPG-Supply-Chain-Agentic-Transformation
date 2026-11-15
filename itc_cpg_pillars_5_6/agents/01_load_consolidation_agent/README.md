# 01 · Load Consolidation Agent

- **Enterprise Scope**: ITC Limited — Consumer Packaged Goods (CPG) Trade Marketing & Distribution (TM&D)
- **Functional Area**: Primary Logistics & Plant Dispatch (Factory -> CFA / Depot) (Pillar 06 · Green Logistics & Primary Dispatch)
- **Persona Owner**: **Primary Transport Planner** (*Raghavendra Kulkarni (Primary Transport Lead — Pune Ranjangaon ICML)*)
- **Build Mode**: **`Low-Code Agent Studio`** · **Priority**: `P0`
- **Model Routing (`GlobalGemini`, `location="global"`)**: `gemini-3.1-pro-preview`
- **Reuse & Provenance (`REUSED_AND_TAILORED`)**: `load_consolidation_agent (Live GE: reasoningEngines/load_consolidation_agent)`, `fleetflow_cpg_tmd 3D Load Studio`

## 1. Operational Problem Solved in ITC CPG
ITC ICML mega-plants ship both high-density Staples (Aashirvaad Atta at ~600 kg/m3, which weights out a 32-ft MXL truck at 45% volume) and ultra-light fragile Foods (Bingo! chips & Sunfeast biscuits at ~90-180 kg/m3, which cube out at 25% payload). Dispatching single-category FTLs wastes 28-36% of primary freight spend.

## 2. Researched 4-Lever Annual Value Attribution (`₹29.4 Cr/yr`)
| Value Lever | Annual Impact (INR) | Attribution Note |
| :--- | :--- | :--- |
| **Productivity** | ₹2.4 Cr/yr | Planner / supervisor / field-manager toil eliminated |
| **Flow & Capital** | — (Load-Bearing Zero) | Dock, CFA wave, transit velocity & inventory turnover |
| **Risk & Leakage** | ₹8.6 Cr/yr | Freight overcharges, detention slabs, OTIF penalties & spoilage |
| **Revenue Recovery** | ₹18.4 Cr/yr | Prevented stockouts, saved cutoffs & protected channel fill |

> **Load-Bearing Zero Discipline**: Flow & working-capital inventory days stay governed by S&OP; value comes from eliminating air-shipping FTLs (Freight Recovery/Savings) and preventing axle-overload fines & carton crush damage (Risk).

## 3. Connected Systems & Human Sign-Off Gate
- **Target System**: SAP Transportation Management (SAP TM) & Zenith Indent Portal
- **Primary Fact Table**: `enterprise_data/lake_full/01_icml_primary_dispatch_waves_and_cartons.csv`
- **Human Gate (`STOPS AT`)**: Never auto-tenders overloaded vehicles violating Central Motor Vehicles Rules (CMVR) Rule 93 axle limits or commits SAP TM shipment cost docs without Primary Transport Planner sign-off.

## 4. Mode-Specific Specifications Included
- `studio_specs/gemini_enterprise_agent_studio.yaml`
- `studio_specs/openapi_tools_spec.json`

## 5. Plain-English Business Starter Prompts
1. *"Which staged dispatches at Ranjangaon and Khordha ICML are weighing out on Atta or cubing out on Bingo! and Sunfeast, and how can we co-load them into fewer 32-foot trucks without crushing fragile cartons?"*
2. *"Show me a visual comparison of freight savings and cube-plus-weight fill rates across today's composite load plans."*
3. *"Verify that our composite Pune-to-Ahmedabad multi-stop load complies with highway front and rear axle weight regulations and reverse-stop unloading order."*
4. *"Stage the recommended composite load consolidation plan in our transport system for planner sign-off."*
