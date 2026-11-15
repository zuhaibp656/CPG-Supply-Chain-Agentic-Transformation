# 10 · Dynamic Rerouter

- **Enterprise Scope**: ITC Limited — Consumer Packaged Goods (CPG) Trade Marketing & Distribution (TM&D)
- **Functional Area**: Fleet, Carrier & Freight Governance (Pillar 06 · Green Logistics, Fleet & Live Route Governance)
- **Persona Owner**: **Fleet & Route Dispatch Lead** (*Vikramaditya Menon (Central Zenith Fleet Control Tower Lead — Mumbai, Bengaluru & Kolkata)*)
- **Build Mode**: **`Low-Code + Maps Platform`** · **Priority**: `P0`
- **Model Routing (`GlobalGemini`, `location="global"`)**: `gemini-3.1-pro-preview`
- **Reuse & Provenance (`REUSED_AND_TAILORED`)**: `fleetflow_dispatch (Live GE: reasoningEngines/1064147210658119680)`, `port_drayage_orchestrator (Curfew Orchestrator)`

## 1. Operational Problem Solved in ITC CPG
En-route highway landslides (NH-48 Khandala Ghat), urban waterlogging (Bengaluru ORR), police heavy-vehicle curfews (08:00-21:00 Kolkata/Mumbai), commercial EV low battery State-of-Charge, and expiring midnight NIC E-Way Bills cause severe delivery misses and Section 129 GST transit penalties (200% of tax).

## 2. Researched 4-Lever Annual Value Attribution (`₹22.0 Cr/yr`)
| Value Lever | Annual Impact (INR) | Attribution Note |
| :--- | :--- | :--- |
| **Productivity** | ₹1.7 Cr/yr | Planner / supervisor / field-manager toil eliminated |
| **Flow & Capital** | ₹11.5 Cr/yr | Dock, CFA wave, transit velocity & inventory turnover |
| **Risk & Leakage** | ₹8.8 Cr/yr | Freight overcharges, detention slabs, OTIF penalties & spoilage |
| **Revenue Recovery** | — (Load-Bearing Zero) | Prevented stockouts, saved cutoffs & protected channel fill |

> **Load-Bearing Zero Discipline**: Protects already-sold in-transit dispatches (Revenue Recovery = 0); cuts highway/curfew dwell & empty detour km (Flow) and prevents Section 129 GST E-Way Bill expiry fines (Risk).

## 3. Connected Systems & Human Sign-Off Gate
- **Target System**: Zenith Fleet Control Tower + Google Maps Routes Matrix v2 + NIC E-Way Bill Part-B API
- **Primary Fact Table**: `enterprise_data/lake_full/10_zenith_fleet_gps_traffic_and_ev_routes.csv`
- **Human Gate (`STOPS AT`)**: Never routes heavy multi-axle trucks onto weight-restricted bridges/no-entry police zones or files statutory NIC E-Way Bill extensions without Fleet Lead confirmation.

## 4. Mode-Specific Specifications Included
- `studio_specs/gemini_enterprise_agent_studio.yaml`
- `studio_specs/openapi_tools_spec.json`
- `studio_specs/google_maps_routes_matrix_v2_spec.json`

## 5. Plain-English Business Starter Prompts
1. *"Which in-transit primary trucks and urban Green Logistics EV vans are delayed by highway blockages, waterlogging, or city no-entry curfews right now, and what is the fastest safe reroute?"*
2. *"Are any delayed trucks within 4 hours of their NIC E-Way Bill expiring, or do any commercial EV vans need a fast-charging stop added to finish their beat?"*
3. *"Chart the transit minutes saved across all active fleet reroutes."*
4. *"Stage the updated Google Maps route diversions, EV charger stop, and E-Way Bill extension alert in Zenith."*
