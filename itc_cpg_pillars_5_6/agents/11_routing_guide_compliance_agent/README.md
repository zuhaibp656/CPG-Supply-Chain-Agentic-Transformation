# 11 · Routing Guide Compliance Agent

- **Enterprise Scope**: ITC Limited — Consumer Packaged Goods (CPG) Trade Marketing & Distribution (TM&D)
- **Functional Area**: Fleet, Carrier & Freight Governance (Pillar 06 · Transport Procurement & Carrier Waterfall Governance)
- **Persona Owner**: **Transport Procurement Manager** (*Kavita Krishnamurthy (National Freight Procurement Lead — ITC TM&D HQ Kolkata)*)
- **Build Mode**: **`No-Code Gemini Gem`** · **Priority**: `P1`
- **Model Routing (`GlobalGemini`, `location="global"`)**: `gemini-3.8-flash`
- **Reuse & Provenance (`REUSED_AND_TAILORED`)**: `freight_control_tower (Live GE: reasoningEngines/1933778444856852480)`

## 1. Operational Problem Solved in ITC CPG
ITC negotiates annual L1/L2/L3 waterfall rate cards across hundreds of ICML-to-CFA lanes, yet local dispatchers frequently bypass L2 backup carriers during evening rush and book ad-hoc spot-market brokers at 28-40% freight premiums—leaking Crores annually.

## 2. Researched 4-Lever Annual Value Attribution (`₹16.9 Cr/yr`)
| Value Lever | Annual Impact (INR) | Attribution Note |
| :--- | :--- | :--- |
| **Productivity** | ₹1.5 Cr/yr | Planner / supervisor / field-manager toil eliminated |
| **Flow & Capital** | — (Load-Bearing Zero) | Dock, CFA wave, transit velocity & inventory turnover |
| **Risk & Leakage** | ₹15.4 Cr/yr | Freight overcharges, detention slabs, OTIF penalties & spoilage |
| **Revenue Recovery** | — (Load-Bearing Zero) | Prevented stockouts, saved cutoffs & protected channel fill |

> **Load-Bearing Zero Discipline**: Pure freight procurement & contract-compliance governance Gem (Flow = 0, Revenue Recovery = 0); eliminates maverick spot-market rate leakage (Risk & Leakage) and automates lane compliance audits (Productivity).

## 3. Connected Systems & Human Sign-Off Gate
- **Target System**: SAP TM / Zenith Carrier Waterfall Guide & Monthly Transporter Allocation Scorecard
- **Primary Fact Table**: `enterprise_data/lake_full/11_carrier_routing_guide_tenders_and_spot.csv`
- **Human Gate (`STOPS AT`)**: Advisory & governance No-Code Gem—flags maverick spot indents and drafts L1/L2 carrier show-cause or rate-reindexing memos, never altering signed annual transport contracts unilaterally.

## 4. Mode-Specific Specifications Included
- `studio_specs/gemini_enterprise_agent_studio.yaml`
- `studio_specs/openapi_tools_spec.json`
- `studio_specs/gemini_gem_blueprint_and_knowledge_pack.md`

## 5. Plain-English Business Starter Prompts
1. *"Which primary lanes are leaking the most money into expensive spot-market trucks instead of following our L1 and L2 contracted carrier routing guide?"*
2. *"Distinguish lanes where dispatch planners bypassed our L2 backup carrier from lanes where both L1 and L2 transporters rejected tenders due to capacity or backhaul issues."*
3. *"Show a chart of monthly maverick spot-freight leakage across our top non-compliant lanes."*
4. *"Draft carrier compliance notices and stage TMS waterfall lock recommendations for procurement review."*
