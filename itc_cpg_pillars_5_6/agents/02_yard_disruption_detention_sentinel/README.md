# 02 · Yard Disruption & Detention Sentinel

- **Enterprise Scope**: ITC Limited — Consumer Packaged Goods (CPG) Trade Marketing & Distribution (TM&D)
- **Functional Area**: Primary Logistics & Plant Dispatch (Factory -> CFA / Depot) (Pillar 06 · Green Logistics & Primary Dispatch)
- **Persona Owner**: **Plant Yard & Dispatch Lead** (*Harpreet Singh Gill (ICML Yard Master — Kapurthala & Ranjangaon)*)
- **Build Mode**: **`Low-Code Agent Studio`** · **Priority**: `P0`
- **Model Routing (`GlobalGemini`, `location="global"`)**: `gemini-3.1-pro-preview`
- **Reuse & Provenance (`REUSED_AND_TAILORED`)**: `yard_dock_sequencer (Live GE: reasoningEngines/2295192314953334784)`, `yard_dock_scheduling_agent`

## 1. Operational Problem Solved in ITC CPG
At peak shift handovers, 32-ft containers and frozen reefers queue at ICML weighbridges and blocked stretch-wrap doors beyond the 120-minute free-time slab—triggering Rs 850-Rs 1,350/hr carrier detention charges and diesel burn on waiting reefers.

## 2. Researched 4-Lever Annual Value Attribution (`₹20.9 Cr/yr`)
| Value Lever | Annual Impact (INR) | Attribution Note |
| :--- | :--- | :--- |
| **Productivity** | ₹1.9 Cr/yr | Planner / supervisor / field-manager toil eliminated |
| **Flow & Capital** | ₹7.8 Cr/yr | Dock, CFA wave, transit velocity & inventory turnover |
| **Risk & Leakage** | ₹11.2 Cr/yr | Freight overcharges, detention slabs, OTIF penalties & spoilage |
| **Revenue Recovery** | — (Load-Bearing Zero) | Prevented stockouts, saved cutoffs & protected channel fill |

> **Load-Bearing Zero Discipline**: Does not create incremental retail consumer demand (Revenue Recovery = 0); value is pure carrier detention avoidance (Risk & Leakage) and faster ICML dock turnaround (Flow).

## 3. Connected Systems & Human Sign-Off Gate
- **Target System**: SAP Extended Warehouse Management (SAP EWM) Yard & Weighbridge Gate Console
- **Primary Fact Table**: `enterprise_data/lake_full/02_icml_yard_gate_fastag_dock_detention.csv`
- **Human Gate (`STOPS AT`)**: Never overrides ICML gate security tare-weight discrepancy holds or waives contractual detention claims without Plant Yard Lead approval.

## 4. Mode-Specific Specifications Included
- `studio_specs/gemini_enterprise_agent_studio.yaml`
- `studio_specs/openapi_tools_spec.json`

## 5. Plain-English Business Starter Prompts
1. *"Which trucks waiting inside our Ranjangaon, Kapurthala, and Panchla plant yards have breached or are about to breach free detention time, and which open dock doors should we move them to right now?"*
2. *"Are any frozen or chilled reefer trailers waiting on diesel at the gate that need immediate reassignment to a shore-power dock door?"*
3. *"Chart the detention penalties avoided by vehicle across our active yard bottleneck queue."*
4. *"Stage the dock door reassignments and spotter move instructions for the yard crew."*
