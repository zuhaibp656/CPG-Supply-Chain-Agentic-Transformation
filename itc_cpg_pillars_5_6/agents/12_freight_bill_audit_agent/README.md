# 12 · Freight Bill Audit Agent

- **Enterprise Scope**: ITC Limited — Consumer Packaged Goods (CPG) Trade Marketing & Distribution (TM&D)
- **Functional Area**: Fleet, Carrier & Freight Governance (Pillar 06 · Multimodal Freight Audit, POD & Claims Settlement)
- **Persona Owner**: **Freight Bill & Claims Controller** (*Subhashish Mukherjee (National Freight Audit & Commercial Claims Controller — Kolkata)*)
- **Build Mode**: **`Multimodal + Agent Studio`** · **Priority**: `P0`
- **Model Routing (`GlobalGemini`, `location="global"`)**: `gemini-3.1-pro-preview`
- **Reuse & Provenance (`REUSED_AND_TAILORED`)**: `freight_bill_audit_agent (Live GE: reasoningEngines/8272173807427387392)`, `osd_freight_claims_agent (Live GE: reasoningEngines/5496125750106914816)`

## 1. Operational Problem Solved in ITC CPG
Indian CPG freight settlement requires reconciling paper-heavy Lorry Receipts (Bilty), rubber-stamped CFA Proof-of-Delivery (POD) slips with handwritten wet/crushed carton remarks, contracted diesel escalation pegs, and GPS-verified gate detention hours. Manual 5% sampling misses duplicate LR billings, inflated 8-12 hour detention claims, and unrecovered POD shortages.

## 2. Researched 4-Lever Annual Value Attribution (`₹25.5 Cr/yr`)
| Value Lever | Annual Impact (INR) | Attribution Note |
| :--- | :--- | :--- |
| **Productivity** | ₹3.9 Cr/yr | Planner / supervisor / field-manager toil eliminated |
| **Flow & Capital** | — (Load-Bearing Zero) | Dock, CFA wave, transit velocity & inventory turnover |
| **Risk & Leakage** | ₹21.6 Cr/yr | Freight overcharges, detention slabs, OTIF penalties & spoilage |
| **Revenue Recovery** | — (Load-Bearing Zero) | Prevented stockouts, saved cutoffs & protected channel fill |

> **Load-Bearing Zero Discipline**: Post-delivery financial & multimodal claims audit (Flow = 0, Revenue Recovery = 0); recovers 3.8-5.2% of freight spend from duplicate LRs, detention padding, and POD damage claims (Risk & Leakage) while replacing manual paper-bilty checking (Productivity).

## 3. Connected Systems & Human Sign-Off Gate
- **Target System**: SAP S/4HANA FI-AP (`MIRO` / `FB60` Short-Pay Voucher & GST RCM Ledger) + Carrier Dispute Portal
- **Primary Fact Table**: `enterprise_data/lake_full/12_freight_lr_pod_invoices_and_claims.csv`
- **Human Gate (`STOPS AT`)**: Never releases bank NEFT/RTGS payouts or posts final carrier debit notes without Freight Bill Controller sign-off; blocks 100% of duplicate Lorry Receipt claims.

## 4. Mode-Specific Specifications Included
- `studio_specs/gemini_enterprise_agent_studio.yaml`
- `studio_specs/openapi_tools_spec.json`
- `studio_specs/multimodal_ocr_4way_match_pipeline.yaml`

## 5. Plain-English Business Starter Prompts
1. *"Audit our pending carrier freight invoices against contracted lane rates, diesel fuel pegs, GPS detention logs, and scanned Proof of Delivery receipts—where are we being overcharged?"*
2. *"Inspect the scanned Lorry Receipt, stamped POD, and invoice for LR-TCI-882910 and LR-HWK-771024 to verify the crushed Dark Fantasy cartons and check for duplicate billing."*
3. *"Create a chart comparing carrier billed amounts versus verified net payable and overcharge recovery by invoice."*
4. *"Stage the short-pay SAP vouchers, duplicate-LR block, and POD damage debit notes for controller sign-off."*
