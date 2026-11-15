# 07 · MT / Q-Comm Slot & OTIF Copilot

- **Enterprise Scope**: ITC Limited — Consumer Packaged Goods (CPG) Trade Marketing & Distribution (TM&D)
- **Functional Area**: Channel & Route-to-Market (GT, MT & Q-Commerce) (Pillar 05 · Modern Trade & Quick-Commerce Fulfillment)
- **Persona Owner**: **Modern Trade & Q-Comm Logistics Lead** (*Neha Kapoor (National MT & Quick-Commerce Supply Lead — Gurugram & Mumbai)*)
- **Build Mode**: **`Low-Code Agent Studio`** · **Priority**: `P0`
- **Model Routing (`GlobalGemini`, `location="global"`)**: `gemini-3.1-pro-preview`
- **Reuse & Provenance (`REUSED_AND_TAILORED`)**: `otif_penalty_shield (Live GE: reasoningEngines/3448113819560181760)`, `modern_trade_dock_slot_booker`

## 1. Operational Problem Solved in ITC CPG
Blinkit, Zepto, Swiggy Instamart, DMart, and Reliance enforce 15-to-30-minute dock arrival tolerances and strict 75% Minimum Remaining Shelf-Life gates. Missing a slot by 20 minutes or sending a 68%-MRSL batch triggers full truck turn-away, 5-10% PO chargebacks, and dark-store out-of-stocks.

## 2. Researched 4-Lever Annual Value Attribution (`₹28.4 Cr/yr`)
| Value Lever | Annual Impact (INR) | Attribution Note |
| :--- | :--- | :--- |
| **Productivity** | ₹2.1 Cr/yr | Planner / supervisor / field-manager toil eliminated |
| **Flow & Capital** | — (Load-Bearing Zero) | Dock, CFA wave, transit velocity & inventory turnover |
| **Risk & Leakage** | ₹12.4 Cr/yr | Freight overcharges, detention slabs, OTIF penalties & spoilage |
| **Revenue Recovery** | ₹13.9 Cr/yr | Prevented stockouts, saved cutoffs & protected channel fill |

> **Load-Bearing Zero Discipline**: Operates within existing inventory pools (Flow = 0); directly blocks 5-10% retailer OTIF chargebacks (Risk) and prevents full-PO dock refusals & dark-store delistings (Revenue Recovery).

## 3. Connected Systems & Human Sign-Off Gate
- **Target System**: Retailer EDI 856 ASN & Partner Appointment Portals (Blinkit, Zepto, Instamart, DMart, Reliance)
- **Primary Fact Table**: `enterprise_data/lake_full/07_mt_qcomm_asn_dock_slots_and_otif.csv`
- **Human Gate (`STOPS AT`)**: Never accepts contractual penalty waivers that alter commercial trade terms or commits premium dedicated air/express recovery above Rs 25,000 without MT Logistics Lead approval.

## 4. Mode-Specific Specifications Included
- `studio_specs/gemini_enterprise_agent_studio.yaml`
- `studio_specs/openapi_tools_spec.json`

## 5. Plain-English Business Starter Prompts
1. *"Which of today's Blinkit, Zepto, Instamart, and DMart dispatches are at risk of missing their dock appointment slot or failing the 75% shelf-life check?"*
2. *"Check open partner-portal reschedule slots and pre-dispatch batch swaps to protect our On-Time In-Full score and avoid chargebacks."*
3. *"Show a visual chart of at-risk chargeback deductions shielded across Modern Trade and Quick-Commerce accounts."*
4. *"Stage the slot rebooking requests on the Blinkit and DMart portals and flag the Zepto batch swap."*
