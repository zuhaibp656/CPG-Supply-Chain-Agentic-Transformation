# 06 · EOD Billing & Cutoff Closer Agent

- **Enterprise Scope**: ITC Limited — Consumer Packaged Goods (CPG) Trade Marketing & Distribution (TM&D)
- **Functional Area**: CFA / Depot Operations & Stock Allocation (Pillar 05 · CFA Billing & SAP Cutoff Governance)
- **Persona Owner**: **Depot Dispatch & Billing Supervisor** (*Prakash Kulkarni (CFA Commercial & SAP Billing Lead — Bhiwandi & Dankuni)*)
- **Build Mode**: **`Low-Code + SAP OpenAPI`** · **Priority**: `P0`
- **Model Routing (`GlobalGemini`, `location="global"`)**: `gemini-3.1-pro-preview`
- **Reuse & Provenance (`NEW_ITC_SPECIFIC_BUILD`)**: `eway_bill_gst_transit_auditor (NIC E-Way Bill foundation)`, `New SAP S/4HANA VL02N/VF01/VKM3/IRN EOD Cutoff Engine`

## 1. Operational Problem Solved in ITC CPG
Every evening between 19:30 and the 21:00 IST gate lock (and critically on month-end close), fully loaded trucks sit trapped at CFA gates because SAP outbound deliveries (`VL02N`) fail Post Goods Issue or `VF01` billing due to minor FEFO batch-split variances, unsynced FinAgg dealer credit drawdowns, or hyphen typos in NIC E-Way Bill Part-B vehicle numbers—pushing Crores of billed revenue into the next day/month.

## 2. Researched 4-Lever Annual Value Attribution (`₹29.8 Cr/yr`)
| Value Lever | Annual Impact (INR) | Attribution Note |
| :--- | :--- | :--- |
| **Productivity** | ₹3.4 Cr/yr | Planner / supervisor / field-manager toil eliminated |
| **Flow & Capital** | ₹14.6 Cr/yr | Dock, CFA wave, transit velocity & inventory turnover |
| **Risk & Leakage** | — (Load-Bearing Zero) | Freight overcharges, detention slabs, OTIF penalties & spoilage |
| **Revenue Recovery** | ₹11.8 Cr/yr | Prevented stockouts, saved cutoffs & protected channel fill |

> **Load-Bearing Zero Discipline**: Enforces rather than alters credit/tax risk policy (Risk = 0); unlocks trapped gate-loaded trucks before 21:00/month-end cutoff (Flow & Revenue Recovery) while eliminating manual late-night SAP firefighting (Productivity).

## 3. Connected Systems & Human Sign-Off Gate
- **Target System**: SAP S/4HANA SD/FI OpenAPI (`API_OUTBOUND_DELIVERY_SRV`, `API_BILLING_DOCUMENT_SRV`) & NIC IRP/E-Way API
- **Primary Fact Table**: `enterprise_data/lake_full/06_cfa_sap_eod_billing_irn_eway_cutoff.csv`
- **Human Gate (`STOPS AT`)**: Never releases hard overdue delinquency blocks (`VKM3 >15 days overdue`) without Commercial Finance Controller approval; auto-stages only technical batch-split, FinAgg sync, and Part-B format fixes.

## 4. Mode-Specific Specifications Included
- `studio_specs/gemini_enterprise_agent_studio.yaml`
- `studio_specs/openapi_tools_spec.json`
- `studio_specs/sap_s4hana_sd_ewm_irn_openapi_v3.json`

## 5. Plain-English Business Starter Prompts
1. *"Which loaded trucks at our CFAs are stuck waiting for SAP billing, GST e-Invoice IRN, or E-Way Bill generation before tonight's 21:00 gate cutoff, and which ones can we clear right now?"*
2. *"Separate the technical SAP batch-split, FinAgg credit-sync, and vehicle-number formatting errors we can fix automatically from hard overdue credit holds that need Finance sign-off."*
3. *"Chart the trapped invoice value by outbound delivery ranked by urgency before cutoff."*
4. *"Stage the SAP OpenAPI batch-split, FinAgg sync, and E-Way Bill Part-B fixes for billing supervisor sign-off."*
