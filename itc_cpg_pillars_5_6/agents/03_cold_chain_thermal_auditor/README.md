# 03 · Cold-Chain Thermal Auditor

- **Enterprise Scope**: ITC Limited — Consumer Packaged Goods (CPG) Trade Marketing & Distribution (TM&D)
- **Functional Area**: Primary Logistics & Plant Dispatch (Factory -> CFA / Depot) (Pillar 06 · Green Logistics & Cold-Chain Assurance)
- **Persona Owner**: **Cold-Chain & Transit QA Lead** (*Dr. Ananya Chatterjee (National Cold-Chain QA Lead — Kolkata & Kapurthala)*)
- **Build Mode**: **`Low-Code Agent Studio`** · **Priority**: `P0`
- **Model Routing (`GlobalGemini`, `location="global"`)**: `gemini-3.1-pro-preview`
- **Reuse & Provenance (`REUSED_AND_TAILORED`)**: `cold_chain_auditor (Live GE: reasoningEngines/8706771171468640256)`, `cold_chain_salvage_repack_advisor`

## 1. Operational Problem Solved in ITC CPG
ITC Master Chef frozen snacks (-18C), Aashirvaad Svasti paneer/curd (2-8C), and Fabelle luxury chocolates (16-20C) suffer mid-highway compressor slips or driver fuel-saving switch-offs. Simple min/max threshold alerts miss cumulative Arrhenius kinetic heat damage.

## 2. Researched 4-Lever Annual Value Attribution (`₹22.6 Cr/yr`)
| Value Lever | Annual Impact (INR) | Attribution Note |
| :--- | :--- | :--- |
| **Productivity** | ₹1.6 Cr/yr | Planner / supervisor / field-manager toil eliminated |
| **Flow & Capital** | — (Load-Bearing Zero) | Dock, CFA wave, transit velocity & inventory turnover |
| **Risk & Leakage** | ₹14.8 Cr/yr | Freight overcharges, detention slabs, OTIF penalties & spoilage |
| **Revenue Recovery** | ₹6.2 Cr/yr | Prevented stockouts, saved cutoffs & protected channel fill |

> **Load-Bearing Zero Discipline**: Does not accelerate fleet transit velocity (Flow = 0); protects consumer food safety & recovers carrier spoilage claims (Risk) while salvaging borderline cool-chain lots before total write-off (Recovery).

## 3. Connected Systems & Human Sign-Off Gate
- **Target System**: SAP Quality Management (SAP QM `BAPI_INSPLOT_SETUSAGEDECISION`) & Carrier Claims Portal
- **Primary Fact Table**: `enterprise_data/lake_full/03_drishti_reefer_iot_thermal_telemetry.csv`
- **Human Gate (`STOPS AT`)**: Never auto-releases thermally abused frozen, dairy, or chocolate lots into unrestricted CFA stock without QA Lead usage decision.

## 4. Mode-Specific Specifications Included
- `studio_specs/gemini_enterprise_agent_studio.yaml`
- `studio_specs/openapi_tools_spec.json`

## 5. Plain-English Business Starter Prompts
1. *"Audit our inbound frozen Master Chef, Svasti dairy, and Fabelle chocolate reefer shipments—which loads breached Mean Kinetic Temperature limits and need quarantine or a carrier spoilage claim?"*
2. *"Inspect the thermal logger strip chart for the Kapurthala-to-Kundli frozen fries shipment and Patna paneer load to check what caused the temperature spike."*
3. *"Create a visual breakdown of carrier spoilage claim values and shelf-life days lost across flagged reefer trips."*
4. *"Stage a quality quarantine hold and carrier claim packet for the abused cold-chain lots."*
