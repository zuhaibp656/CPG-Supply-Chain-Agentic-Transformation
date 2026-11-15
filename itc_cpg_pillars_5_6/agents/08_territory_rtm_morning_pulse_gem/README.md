# 08 · Territory RTM Morning Pulse Gem

- **Enterprise Scope**: ITC Limited — Consumer Packaged Goods (CPG) Trade Marketing & Distribution (TM&D)
- **Functional Area**: Channel & Route-to-Market (GT, MT & Q-Commerce) (Pillar 05 · UNNATI eB2B & Vajra Field Route-to-Market)
- **Persona Owner**: **Area Distribution / RTM Manager** (*Siddharth Banerjee (TM&D Area Manager — Pune, Lucknow & Kolkata Clusters)*)
- **Build Mode**: **`No-Code Gemini Gem`** · **Priority**: `P1`
- **Model Routing (`GlobalGemini`, `location="global"`)**: `gemini-3.8-flash`
- **Reuse & Provenance (`NEW_TAILORED_ITC_GEM`)**: `field_beat_distributor_sync_agent (RTM Beat Foundation)`, `New Grounded UNNATI eB2B + Vajra SFA Morning Pulse Gem`

## 1. Operational Problem Solved in ITC CPG
Area Distribution Managers start every morning juggling four disconnected spreadsheets: overnight UNNATI kirana app orders, yesterday's Vajra salesman beat strike rates, Wholesale Dealer stockout lines, and active trade schemes—missing urgent morning beat course-corrections before salesmen leave at 08:30.

## 2. Researched 4-Lever Annual Value Attribution (`₹19.8 Cr/yr`)
| Value Lever | Annual Impact (INR) | Attribution Note |
| :--- | :--- | :--- |
| **Productivity** | ₹4.2 Cr/yr | Planner / supervisor / field-manager toil eliminated |
| **Flow & Capital** | — (Load-Bearing Zero) | Dock, CFA wave, transit velocity & inventory turnover |
| **Risk & Leakage** | — (Load-Bearing Zero) | Freight overcharges, detention slabs, OTIF penalties & spoilage |
| **Revenue Recovery** | ₹15.6 Cr/yr | Prevented stockouts, saved cutoffs & protected channel fill |

> **Load-Bearing Zero Discipline**: Pure commercial & field-force morning intelligence Gem (Flow = 0, Risk = 0); saves 6+ hours/week per Area Manager assembling DMS/SFA trackers (Productivity) and lifts secondary beat strike rate & kirana fill (Revenue Recovery).

## 3. Connected Systems & Human Sign-Off Gate
- **Target System**: ITC Vajra SFA Beat Console & UNNATI eB2B Campaign Broadcast
- **Primary Fact Table**: `enterprise_data/lake_full/08_unnati_eb2b_vajra_sfa_morning_pulse.csv`
- **Human Gate (`STOPS AT`)**: Advisory No-Code Gemini Gem by design—synthesizes morning beat priorities and drafts WhatsApp/Vajra nudges, never mutating trade scheme budgets or HR attendance records.

## 4. Mode-Specific Specifications Included
- `studio_specs/gemini_enterprise_agent_studio.yaml`
- `studio_specs/openapi_tools_spec.json`
- `studio_specs/gemini_gem_blueprint_and_knowledge_pack.md`

## 5. Plain-English Business Starter Prompts
1. *"Give me my 7:30 AM Territory Morning Pulse—where did UNNATI kirana orders surge overnight, which Vajra salesman beats had low strike rates yesterday, and which Wholesale Dealers have stockouts?"*
2. *"Draft crisp morning action notes for my Area Sales Executives in Pune, Lucknow, and South Kolkata before the 8:30 AM beat flag-off."*
3. *"Chart secondary revenue at stake across territories by stockout and beat productivity gap."*
4. *"Stage the morning Vajra beat priority nudges for Area Manager review."*
