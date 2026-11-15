#!/usr/bin/env python3
"""Builds all 12 ITC Limited CPG Pillars 5 & 6 Distribution, CFA, RTM & Freight Agents,
mode-specific Studio/SAP/Maps/Gem/Multimodal specifications, research matrix, and pytest suites."""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Dict, List

SUITE_ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = SUITE_ROOT / "agents"
SEEDS_DIR = SUITE_ROOT / "enterprise_data" / "seeds"

AGENTS_CATALOG: List[Dict[str, Any]] = [
    {
        "num": "01",
        "slug": "01_load_consolidation_agent",
        "agent_id": "itc_load_consolidation_agent",
        "class_prefix": "LoadConsolidation",
        "functional_area": "Primary Logistics & Plant Dispatch (Factory -> CFA / Depot)",
        "itc_pillar": "Pillar 06 · Green Logistics & Primary Dispatch",
        "persona": "Primary Transport Planner",
        "persona_named": "Raghavendra Kulkarni (Primary Transport Lead — Pune Ranjangaon ICML)",
        "agent_name": "Load Consolidation Agent",
        "build_mode": "Low-Code Agent Studio",
        "priority": "P0",
        "default_model": "gemini-3.1-pro-preview",
        "table_stem": "01_icml_primary_dispatch_waves_and_cartons",
        "reuse_status": "REUSED_AND_TAILORED",
        "reused_from_agents": ["load_consolidation_agent (Live GE: reasoningEngines/load_consolidation_agent)", "fleetflow_cpg_tmd 3D Load Studio"],
        "target_system": "SAP Transportation Management (SAP TM) & Zenith Indent Portal",
        "stops_at": "Never auto-tenders overloaded vehicles violating Central Motor Vehicles Rules (CMVR) Rule 93 axle limits or commits SAP TM shipment cost docs without Primary Transport Planner sign-off.",
        "problem_statement": "ITC ICML mega-plants ship both high-density Staples (Aashirvaad Atta at ~600 kg/m3, which weights out a 32-ft MXL truck at 45% volume) and ultra-light fragile Foods (Bingo! chips & Sunfeast biscuits at ~90-180 kg/m3, which cube out at 25% payload). Dispatching single-category FTLs wastes 28-36% of primary freight spend.",
        "special_tool_name": "verify_cmvr_rule93_axle_and_crush_physics",
        "special_tool_doc": "Verifies Central Motor Vehicles Rules (CMVR) Rule 93 front steering (<=7,500 kg) & rear drive (<=11,500 kg) axle weights and top-tier carton crush limits (<=85 kg on Bingo! / <=155 kg on Sunfeast).",
        "chart_label_key": "composite_load_id",
        "chart_value_key": "freight_saved_inr",
        "headline_kpi_key": "net_freight_savings_display",
        "rows_key": "composite_load_plans",
        "levers_inr_cr": {"productivity": 2.4, "flow": 0.0, "risk": 8.6, "recovery": 18.4, "zero_rationale": "Flow & working-capital inventory days stay governed by S&OP; value comes from eliminating air-shipping FTLs (Freight Recovery/Savings) and preventing axle-overload fines & carton crush damage (Risk)."},
        "starter_prompts": [
            "Which staged dispatches at Ranjangaon and Khordha ICML are weighing out on Atta or cubing out on Bingo! and Sunfeast, and how can we co-load them into fewer 32-foot trucks without crushing fragile cartons?",
            "Show me a visual comparison of freight savings and cube-plus-weight fill rates across today's composite load plans.",
            "Verify that our composite Pune-to-Ahmedabad multi-stop load complies with highway front and rear axle weight regulations and reverse-stop unloading order.",
            "Stage the recommended composite load consolidation plan in our transport system for planner sign-off."
        ],
    },
    {
        "num": "02",
        "slug": "02_yard_disruption_detention_sentinel",
        "agent_id": "itc_yard_disruption_detention_sentinel",
        "class_prefix": "YardDisruptionDetention",
        "functional_area": "Primary Logistics & Plant Dispatch (Factory -> CFA / Depot)",
        "itc_pillar": "Pillar 06 · Green Logistics & Primary Dispatch",
        "persona": "Plant Yard & Dispatch Lead",
        "persona_named": "Harpreet Singh Gill (ICML Yard Master — Kapurthala & Ranjangaon)",
        "agent_name": "Yard Disruption & Detention Sentinel",
        "build_mode": "Low-Code Agent Studio",
        "priority": "P0",
        "default_model": "gemini-3.1-pro-preview",
        "table_stem": "02_icml_yard_gate_fastag_dock_detention",
        "reuse_status": "REUSED_AND_TAILORED",
        "reused_from_agents": ["yard_dock_sequencer (Live GE: reasoningEngines/2295192314953334784)", "yard_dock_scheduling_agent"],
        "target_system": "SAP Extended Warehouse Management (SAP EWM) Yard & Weighbridge Gate Console",
        "stops_at": "Never overrides ICML gate security tare-weight discrepancy holds or waives contractual detention claims without Plant Yard Lead approval.",
        "problem_statement": "At peak shift handovers, 32-ft containers and frozen reefers queue at ICML weighbridges and blocked stretch-wrap doors beyond the 120-minute free-time slab—triggering Rs 850-Rs 1,350/hr carrier detention charges and diesel burn on waiting reefers.",
        "special_tool_name": "evaluate_reefer_shore_power_and_slab_clock",
        "special_tool_doc": "Ranks waiting ICML yard trailers by remaining minutes to carrier detention slab breach and flags frozen/chilled reefers burning diesel without shore-power dock seals.",
        "chart_label_key": "vehicle_reg_no",
        "chart_value_key": "detention_avoided_inr",
        "headline_kpi_key": "total_detention_charges_avoided_display",
        "rows_key": "sequenced_dock_moves",
        "levers_inr_cr": {"productivity": 1.9, "flow": 7.8, "risk": 11.2, "recovery": 0.0, "zero_rationale": "Does not create incremental retail consumer demand (Revenue Recovery = 0); value is pure carrier detention avoidance (Risk & Leakage) and faster ICML dock turnaround (Flow)."},
        "starter_prompts": [
            "Which trucks waiting inside our Ranjangaon, Kapurthala, and Panchla plant yards have breached or are about to breach free detention time, and which open dock doors should we move them to right now?",
            "Are any frozen or chilled reefer trailers waiting on diesel at the gate that need immediate reassignment to a shore-power dock door?",
            "Chart the detention penalties avoided by vehicle across our active yard bottleneck queue.",
            "Stage the dock door reassignments and spotter move instructions for the yard crew."
        ],
    },
    {
        "num": "03",
        "slug": "03_cold_chain_thermal_auditor",
        "agent_id": "itc_cold_chain_thermal_auditor",
        "class_prefix": "ColdChainThermalAuditor",
        "functional_area": "Primary Logistics & Plant Dispatch (Factory -> CFA / Depot)",
        "itc_pillar": "Pillar 06 · Green Logistics & Cold-Chain Assurance",
        "persona": "Cold-Chain & Transit QA Lead",
        "persona_named": "Dr. Ananya Chatterjee (National Cold-Chain QA Lead — Kolkata & Kapurthala)",
        "agent_name": "Cold-Chain Thermal Auditor",
        "build_mode": "Low-Code Agent Studio",
        "priority": "P0",
        "default_model": "gemini-3.1-pro-preview",
        "table_stem": "03_drishti_reefer_iot_thermal_telemetry",
        "reuse_status": "REUSED_AND_TAILORED",
        "reused_from_agents": ["cold_chain_auditor (Live GE: reasoningEngines/8706771171468640256)", "cold_chain_salvage_repack_advisor"],
        "target_system": "SAP Quality Management (SAP QM `BAPI_INSPLOT_SETUSAGEDECISION`) & Carrier Claims Portal",
        "stops_at": "Never auto-releases thermally abused frozen, dairy, or chocolate lots into unrestricted CFA stock without QA Lead usage decision.",
        "problem_statement": "ITC Master Chef frozen snacks (-18C), Aashirvaad Svasti paneer/curd (2-8C), and Fabelle luxury chocolates (16-20C) suffer mid-highway compressor slips or driver fuel-saving switch-offs. Simple min/max threshold alerts miss cumulative Arrhenius kinetic heat damage.",
        "special_tool_name": "inspect_drishti_strip_chart_multimodal",
        "special_tool_doc": "Performs multimodal OCR & strip-chart inspection on scanned Drishti BLE thermal logger printouts (`DOC-STRIP-SHP-CLD-*.png`) to corroborate carrier negligence claims.",
        "chart_label_key": "shipment_id",
        "chart_value_key": "carrier_spoilage_claim_inr",
        "headline_kpi_key": "recoverable_carrier_claims_display",
        "rows_key": "thermal_audit_ledger",
        "levers_inr_cr": {"productivity": 1.6, "flow": 0.0, "risk": 14.8, "recovery": 6.2, "zero_rationale": "Does not accelerate fleet transit velocity (Flow = 0); protects consumer food safety & recovers carrier spoilage claims (Risk) while salvaging borderline cool-chain lots before total write-off (Recovery)."},
        "starter_prompts": [
            "Audit our inbound frozen Master Chef, Svasti dairy, and Fabelle chocolate reefer shipments—which loads breached Mean Kinetic Temperature limits and need quarantine or a carrier spoilage claim?",
            "Inspect the thermal logger strip chart for the Kapurthala-to-Kundli frozen fries shipment and Patna paneer load to check what caused the temperature spike.",
            "Create a visual breakdown of carrier spoilage claim values and shelf-life days lost across flagged reefer trips.",
            "Stage a quality quarantine hold and carrier claim packet for the abused cold-chain lots."
        ],
    },
    {
        "num": "04",
        "slug": "04_cfa_wave_bay_orchestrator",
        "agent_id": "itc_cfa_wave_bay_orchestrator",
        "class_prefix": "CfaWaveBayOrchestrator",
        "functional_area": "CFA / Depot Operations & Stock Allocation",
        "itc_pillar": "Pillar 05 · CFA Operations & Omnichannel Fulfillment",
        "persona": "Depot / CFA Operations Manager",
        "persona_named": "Suresh Deshpande (Regional Mother CFA Manager — Bhiwandi & Kundli)",
        "agent_name": "CFA Wave & Bay Orchestrator",
        "build_mode": "Low-Code Agent Studio",
        "priority": "P0",
        "default_model": "gemini-3.1-pro-preview",
        "table_stem": "04_cfa_wms_pick_waves_fefo_and_bays",
        "reuse_status": "REUSED_AND_TAILORED",
        "reused_from_agents": ["wave_fulfillment_copilot", "fefo_shelf_life_allocator", "warehouse_slotting_agent"],
        "target_system": "SAP Extended Warehouse Management (SAP EWM) Pick-Wave & Loading Bay Controller",
        "stops_at": "Never dispatches batches violating customer Minimum Remaining Shelf-Life (MRSL) gates or overrides cold-room safety capacity without CFA Manager sign-off.",
        "problem_statement": "State CFAs simultaneously pick rapid Quick-Commerce waves (strict 75% Minimum Remaining Shelf-Life gate, 10:30 cutoff), Modern Trade pallets, and General Trade Wholesale Dealer loads (55% MRSL gate). Unbalanced bays miss morning cutoffs while blind picking sends older batches to Quick-Commerce (causing instant dock rejection) and wastes ultra-fresh batches on General Trade.",
        "special_tool_name": "validate_channel_fefo_mrsl_batch_swaps",
        "special_tool_doc": "Identifies cross-channel batch swaps inside the CFA so >=75%-shelf-life batches serve Quick-Commerce/Modern Trade while 55-74% batches clear cleanly through high-velocity General Trade beats.",
        "chart_label_key": "cfa_wave_id",
        "chart_value_key": "protected_dispatch_value_inr",
        "headline_kpi_key": "protected_dispatch_revenue_display",
        "rows_key": "wave_orchestration_plan",
        "levers_inr_cr": {"productivity": 3.8, "flow": 9.4, "risk": 7.9, "recovery": 0.0, "zero_rationale": "Executes existing booked orders faster and cleaner without altering commercial demand; drives picker throughput (Productivity), bay velocity (Flow), and zero shelf-life rejections (Risk)."},
        "starter_prompts": [
            "Which pick waves and loading bays at Bhiwandi and Kundli CFAs are congested or about to miss morning dispatch cutoffs, and are any Quick-Commerce orders picking batches that will fail the 75% shelf-life rule?",
            "Show how we can swap batch allocations between Quick-Commerce and General Trade waves so fresh stock protects Blinkit/Zepto while older compliant stock moves through Wholesale Dealers.",
            "Generate a chart of protected dispatch value across our rebalanced CFA pick waves.",
            "Stage the bay reassignments, picker shifts, and FEFO batch swaps in the warehouse system."
        ],
    },
    {
        "num": "05",
        "slug": "05_fair_share_stock_allocation_agent",
        "agent_id": "itc_fair_share_stock_allocation_agent",
        "class_prefix": "FairShareStockAllocation",
        "functional_area": "CFA / Depot Operations & Stock Allocation",
        "itc_pillar": "Pillar 05 · CFA Operations & Stock Allocation",
        "persona": "Customer Service & Logistics (CS&L) Lead",
        "persona_named": "Meenakshi Sundaram (Zonal CS&L Head — Bengaluru & Southern Hub)",
        "agent_name": "Fair-Share Stock Allocation Agent",
        "build_mode": "Low-Code Agent Studio",
        "priority": "P0",
        "default_model": "gemini-3.1-pro-preview",
        "table_stem": "05_csl_shortage_orders_and_channel_allocations",
        "reuse_status": "REUSED_AND_TAILORED",
        "reused_from_agents": ["echelon_inventory_allocator", "dynamic_order_promising_atp", "atp_order_promising_agent"],
        "target_system": "SAP S/4HANA Advanced Available-to-Promise (aATP) & Order Rationing Engine",
        "stops_at": "Never zeroes out General Trade baseline territory floors or overrides contractual key-account allocation commitments without CS&L Lead approval.",
        "problem_statement": "When a high-velocity SKU like Sunfeast Dark Fantasy 300g is constrained at a State CFA (e.g., 2,400 cases available vs 3,650 ordered), standard SAP First-In-First-Out (FIFO) lets early Modern Trade bulk orders consume 100% of stock—starving 18 General Trade Wholesale Dealers and UNNATI kiranas or triggering steep 8% Quick-Commerce OTIF penalties.",
        "special_tool_name": "compare_ortools_lp_vs_naive_fifo_rationing",
        "special_tool_doc": "Compares Google OR-Tools Linear Programming fair-share allocation against naive SAP FIFO order consumption across margin, OTIF penalties, and kirana breadth.",
        "chart_label_key": "channel_name",
        "chart_value_key": "fair_share_lp_cases",
        "headline_kpi_key": "net_economic_advantage_display",
        "rows_key": "channel_allocations",
        "levers_inr_cr": {"productivity": 1.8, "flow": 0.0, "risk": 9.1, "recovery": 16.5, "zero_rationale": "Allocates already-manufactured scarce stock (Flow = 0); shields steep Modern Trade/Q-Comm OTIF chargebacks (Risk) and preserves high-margin UNNATI/General Trade sell-through (Revenue Recovery)."},
        "starter_prompts": [
            "We only have 2,400 cases of Sunfeast Dark Fantasy 300g at Nelamangala Bengaluru CFA against 3,650 cases of competing orders—how should we ration stock fairly across Quick-Commerce, Modern Trade, UNNATI kiranas, and Wholesale Dealers?",
            "Compare our Linear Programming fair-share split against standard First-In-First-Out allocation so we see how much penalty and margin we save without starving General Trade.",
            "Plot the recommended case allocation and fill rate across each channel.",
            "Stage the approved fair-share allocation quantities into SAP Available-to-Promise for release."
        ],
    },
    {
        "num": "06",
        "slug": "06_eod_billing_cutoff_closer_agent",
        "agent_id": "itc_eod_billing_cutoff_closer_agent",
        "class_prefix": "EodBillingCutoffCloser",
        "functional_area": "CFA / Depot Operations & Stock Allocation",
        "itc_pillar": "Pillar 05 · CFA Billing & SAP Cutoff Governance",
        "persona": "Depot Dispatch & Billing Supervisor",
        "persona_named": "Prakash Kulkarni (CFA Commercial & SAP Billing Lead — Bhiwandi & Dankuni)",
        "agent_name": "EOD Billing & Cutoff Closer Agent",
        "build_mode": "Low-Code + SAP OpenAPI",
        "priority": "P0",
        "default_model": "gemini-3.1-pro-preview",
        "table_stem": "06_cfa_sap_eod_billing_irn_eway_cutoff",
        "reuse_status": "NEW_ITC_SPECIFIC_BUILD",
        "reused_from_agents": ["eway_bill_gst_transit_auditor (NIC E-Way Bill foundation)", "New SAP S/4HANA VL02N/VF01/VKM3/IRN EOD Cutoff Engine"],
        "target_system": "SAP S/4HANA SD/FI OpenAPI (`API_OUTBOUND_DELIVERY_SRV`, `API_BILLING_DOCUMENT_SRV`) & NIC IRP/E-Way API",
        "stops_at": "Never releases hard overdue delinquency blocks (`VKM3 >15 days overdue`) without Commercial Finance Controller approval; auto-stages only technical batch-split, FinAgg sync, and Part-B format fixes.",
        "problem_statement": "Every evening between 19:30 and the 21:00 IST gate lock (and critically on month-end close), fully loaded trucks sit trapped at CFA gates because SAP outbound deliveries (`VL02N`) fail Post Goods Issue or `VF01` billing due to minor FEFO batch-split variances, unsynced FinAgg dealer credit drawdowns, or hyphen typos in NIC E-Way Bill Part-B vehicle numbers—pushing Crores of billed revenue into the next day/month.",
        "special_tool_name": "validate_sap_openapi_bapi_and_nic_payload",
        "special_tool_doc": "Validates exact SAP S/4HANA OData/BAPI payloads (`ConfirmBatchSplitAndPGI`, `Z_API_SD_FINAGG_SYNC`, `Z_API_GST_EWAYBILL_PARTB_RETRY`) and separates hard Finance credit stops.",
        "chart_label_key": "outbound_delivery_no",
        "chart_value_key": "invoice_value_inr",
        "headline_kpi_key": "same_day_revenue_unlockable_display",
        "rows_key": "prioritized_cutoff_queue",
        "levers_inr_cr": {"productivity": 3.4, "flow": 14.6, "risk": 0.0, "recovery": 11.8, "zero_rationale": "Enforces rather than alters credit/tax risk policy (Risk = 0); unlocks trapped gate-loaded trucks before 21:00/month-end cutoff (Flow & Revenue Recovery) while eliminating manual late-night SAP firefighting (Productivity)."},
        "starter_prompts": [
            "Which loaded trucks at our CFAs are stuck waiting for SAP billing, GST e-Invoice IRN, or E-Way Bill generation before tonight's 21:00 gate cutoff, and which ones can we clear right now?",
            "Separate the technical SAP batch-split, FinAgg credit-sync, and vehicle-number formatting errors we can fix automatically from hard overdue credit holds that need Finance sign-off.",
            "Chart the trapped invoice value by outbound delivery ranked by urgency before cutoff.",
            "Stage the SAP OpenAPI batch-split, FinAgg sync, and E-Way Bill Part-B fixes for billing supervisor sign-off."
        ],
    },
    {
        "num": "07",
        "slug": "07_mt_qcomm_slot_otif_copilot",
        "agent_id": "itc_mt_qcomm_slot_otif_copilot",
        "class_prefix": "MtQcommSlotOtifCopilot",
        "functional_area": "Channel & Route-to-Market (GT, MT & Q-Commerce)",
        "itc_pillar": "Pillar 05 · Modern Trade & Quick-Commerce Fulfillment",
        "persona": "Modern Trade & Q-Comm Logistics Lead",
        "persona_named": "Neha Kapoor (National MT & Quick-Commerce Supply Lead — Gurugram & Mumbai)",
        "agent_name": "MT / Q-Comm Slot & OTIF Copilot",
        "build_mode": "Low-Code Agent Studio",
        "priority": "P0",
        "default_model": "gemini-3.1-pro-preview",
        "table_stem": "07_mt_qcomm_asn_dock_slots_and_otif",
        "reuse_status": "REUSED_AND_TAILORED",
        "reused_from_agents": ["otif_penalty_shield (Live GE: reasoningEngines/3448113819560181760)", "modern_trade_dock_slot_booker"],
        "target_system": "Retailer EDI 856 ASN & Partner Appointment Portals (Blinkit, Zepto, Instamart, DMart, Reliance)",
        "stops_at": "Never accepts contractual penalty waivers that alter commercial trade terms or commits premium dedicated air/express recovery above Rs 25,000 without MT Logistics Lead approval.",
        "problem_statement": "Blinkit, Zepto, Swiggy Instamart, DMart, and Reliance enforce 15-to-30-minute dock arrival tolerances and strict 75% Minimum Remaining Shelf-Life gates. Missing a slot by 20 minutes or sending a 68%-MRSL batch triggers full truck turn-away, 5-10% PO chargebacks, and dark-store out-of-stocks.",
        "special_tool_name": "scan_retailer_portal_open_appointment_windows",
        "special_tool_doc": "Checks live Blinkit, Zepto, Instamart, DMart, and Reliance appointment portals for open same-day swap slots and pre-dispatch MRSL compliance.",
        "chart_label_key": "account_name",
        "chart_value_key": "chargeback_shielded_inr",
        "headline_kpi_key": "total_otif_penalties_shielded_display",
        "rows_key": "slot_and_otif_actions",
        "levers_inr_cr": {"productivity": 2.1, "flow": 0.0, "risk": 12.4, "recovery": 13.9, "zero_rationale": "Operates within existing inventory pools (Flow = 0); directly blocks 5-10% retailer OTIF chargebacks (Risk) and prevents full-PO dock refusals & dark-store delistings (Revenue Recovery)."},
        "starter_prompts": [
            "Which of today's Blinkit, Zepto, Instamart, and DMart dispatches are at risk of missing their dock appointment slot or failing the 75% shelf-life check?",
            "Check open partner-portal reschedule slots and pre-dispatch batch swaps to protect our On-Time In-Full score and avoid chargebacks.",
            "Show a visual chart of at-risk chargeback deductions shielded across Modern Trade and Quick-Commerce accounts.",
            "Stage the slot rebooking requests on the Blinkit and DMart portals and flag the Zepto batch swap."
        ],
    },
    {
        "num": "08",
        "slug": "08_territory_rtm_morning_pulse_gem",
        "agent_id": "itc_territory_rtm_morning_pulse_gem",
        "class_prefix": "TerritoryRtmMorningPulseGem",
        "functional_area": "Channel & Route-to-Market (GT, MT & Q-Commerce)",
        "itc_pillar": "Pillar 05 · UNNATI eB2B & Vajra Field Route-to-Market",
        "persona": "Area Distribution / RTM Manager",
        "persona_named": "Siddharth Banerjee (TM&D Area Manager — Pune, Lucknow & Kolkata Clusters)",
        "agent_name": "Territory RTM Morning Pulse Gem",
        "build_mode": "No-Code Gemini Gem",
        "priority": "P1",
        "default_model": "gemini-3.8-flash",
        "table_stem": "08_unnati_eb2b_vajra_sfa_morning_pulse",
        "reuse_status": "NEW_TAILORED_ITC_GEM",
        "reused_from_agents": ["field_beat_distributor_sync_agent (RTM Beat Foundation)", "New Grounded UNNATI eB2B + Vajra SFA Morning Pulse Gem"],
        "target_system": "ITC Vajra SFA Beat Console & UNNATI eB2B Campaign Broadcast",
        "stops_at": "Advisory No-Code Gemini Gem by design—synthesizes morning beat priorities and drafts WhatsApp/Vajra nudges, never mutating trade scheme budgets or HR attendance records.",
        "problem_statement": "Area Distribution Managers start every morning juggling four disconnected spreadsheets: overnight UNNATI kirana app orders, yesterday's Vajra salesman beat strike rates, Wholesale Dealer stockout lines, and active trade schemes—missing urgent morning beat course-corrections before salesmen leave at 08:30.",
        "special_tool_name": "generate_0730_ase_whatsapp_and_vajra_brief",
        "special_tool_doc": "Synthesizes a crisp, plain-English 07:30 IST Area Sales Executive (ASE) beat action card pairing overnight UNNATI surges with Vajra strike-rate gaps.",
        "chart_label_key": "territory_name",
        "chart_value_key": "revenue_at_stake_inr",
        "headline_kpi_key": "overnight_unnati_digital_gmv_display",
        "rows_key": "morning_territory_briefing",
        "levers_inr_cr": {"productivity": 4.2, "flow": 0.0, "risk": 0.0, "recovery": 15.6, "zero_rationale": "Pure commercial & field-force morning intelligence Gem (Flow = 0, Risk = 0); saves 6+ hours/week per Area Manager assembling DMS/SFA trackers (Productivity) and lifts secondary beat strike rate & kirana fill (Revenue Recovery)."},
        "starter_prompts": [
            "Give me my 7:30 AM Territory Morning Pulse—where did UNNATI kirana orders surge overnight, which Vajra salesman beats had low strike rates yesterday, and which Wholesale Dealers have stockouts?",
            "Draft crisp morning action notes for my Area Sales Executives in Pune, Lucknow, and South Kolkata before the 8:30 AM beat flag-off.",
            "Chart secondary revenue at stake across territories by stockout and beat productivity gap.",
            "Stage the morning Vajra beat priority nudges for Area Manager review."
        ],
    },
    {
        "num": "09",
        "slug": "09_predictive_wd_reorder_dispatch_agent",
        "agent_id": "itc_predictive_wd_reorder_dispatch_agent",
        "class_prefix": "PredictiveWdReorderDispatch",
        "functional_area": "Channel & Route-to-Market (GT, MT & Q-Commerce)",
        "itc_pillar": "Pillar 05 · Wholesale Dealer (WD) Replenishment & FinAgg Credit",
        "persona": "Wholesale Dealer (WD) / Stockist Ops Mgr",
        "persona_named": "Rajeshwar Rao (TM&D Stockist Operations & DMS Lead — Mumbai, Bengaluru & Kolkata)",
        "agent_name": "Predictive WD Reorder & Dispatch Agent",
        "build_mode": "Low-Code Agent Studio",
        "priority": "P0",
        "default_model": "gemini-3.1-pro-preview",
        "table_stem": "09_wd_stockist_doi_credit_and_reorders",
        "reuse_status": "REUSED_AND_TAILORED",
        "reused_from_agents": ["dms_distributor_stock_balancer", "store_capacity_agent (Live GE: reasoningEngines/7365119595465670656)"],
        "target_system": "ITC Distribution Management System (DMS) -> SAP S/4HANA Primary Sales Order (`VA01`) & FinAgg Credit API",
        "stops_at": "Never converts draft primary orders into firm SAP billing without Wholesale Dealer OTP/portal consent or FinAgg/bank credit-line confirmation.",
        "problem_statement": "Wholesale Dealers frequently under-order core staples during UNNATI scheme surges (causing kirana stockouts within 48 hours) or hit credit-limit walls mid-week despite having approved FinAgg/SBI supply-chain credit headroom—while manual push dispatches overflow small urban WD godowns.",
        "special_tool_name": "verify_finagg_credit_and_godown_cube_fit",
        "special_tool_doc": "Checks each Wholesale Dealer's open credit limit, FinAgg/SBI dealer-finance drawdown eligibility, and physical godown case capacity before staging primary SAP replenishment.",
        "chart_label_key": "wd_name",
        "chart_value_key": "order_billing_value_inr",
        "headline_kpi_key": "total_auto_replenishment_billing_display",
        "rows_key": "wd_dispatch_recommendations",
        "levers_inr_cr": {"productivity": 2.6, "flow": 10.8, "risk": 0.0, "recovery": 19.2, "zero_rationale": "Operates within pre-underwritten FinAgg/bank credit limits (Risk = 0); stabilizes WD Days-of-Inventory turnover (Flow), automates DMS order generation (Productivity), and eliminates secondary kirana stockouts (Revenue Recovery)."},
        "starter_prompts": [
            "Which Wholesale Dealers are below 4 days of inventory on high-velocity SKUs and risk stocking out within 48 hours, and how many cases should we replenish respecting their godown space and FinAgg credit limit?",
            "Which dealers need an automated FinAgg supply-chain credit drawdown so their urgent replenishment order doesn't get credit-blocked in SAP?",
            "Show a chart of recommended primary replenishment order values across our most stockout-exposed Wholesale Dealers.",
            "Stage the predictive Wholesale Dealer replenishment orders in DMS and SAP for dealer confirmation."
        ],
    },
    {
        "num": "10",
        "slug": "10_dynamic_rerouter",
        "agent_id": "itc_dynamic_rerouter",
        "class_prefix": "DynamicRerouter",
        "functional_area": "Fleet, Carrier & Freight Governance",
        "itc_pillar": "Pillar 06 · Green Logistics, Fleet & Live Route Governance",
        "persona": "Fleet & Route Dispatch Lead",
        "persona_named": "Vikramaditya Menon (Central Zenith Fleet Control Tower Lead — Mumbai, Bengaluru & Kolkata)",
        "agent_name": "Dynamic Rerouter",
        "build_mode": "Low-Code + Maps Platform",
        "priority": "P0",
        "default_model": "gemini-3.1-pro-preview",
        "table_stem": "10_zenith_fleet_gps_traffic_and_ev_routes",
        "reuse_status": "REUSED_AND_TAILORED",
        "reused_from_agents": ["fleetflow_dispatch (Live GE: reasoningEngines/1064147210658119680)", "port_drayage_orchestrator (Curfew Orchestrator)"],
        "target_system": "Zenith Fleet Control Tower + Google Maps Routes Matrix v2 + NIC E-Way Bill Part-B API",
        "stops_at": "Never routes heavy multi-axle trucks onto weight-restricted bridges/no-entry police zones or files statutory NIC E-Way Bill extensions without Fleet Lead confirmation.",
        "problem_statement": "En-route highway landslides (NH-48 Khandala Ghat), urban waterlogging (Bengaluru ORR), police heavy-vehicle curfews (08:00-21:00 Kolkata/Mumbai), commercial EV low battery State-of-Charge, and expiring midnight NIC E-Way Bills cause severe delivery misses and Section 129 GST transit penalties (200% of tax).",
        "special_tool_name": "evaluate_maps_routes_ev_soc_and_eway_clock",
        "special_tool_doc": "Combines Google Maps Routes Matrix v2 live congestion deltas with commercial EV DC fast-charger waypoints, city no-entry curfews, and NIC E-Way Bill remaining hours.",
        "chart_label_key": "vehicle_reg_no",
        "chart_value_key": "net_minutes_saved",
        "headline_kpi_key": "protected_in_transit_cargo_display",
        "rows_key": "reroute_execution_plan",
        "levers_inr_cr": {"productivity": 1.7, "flow": 11.5, "risk": 8.8, "recovery": 0.0, "zero_rationale": "Protects already-sold in-transit dispatches (Revenue Recovery = 0); cuts highway/curfew dwell & empty detour km (Flow) and prevents Section 129 GST E-Way Bill expiry fines (Risk)."},
        "starter_prompts": [
            "Which in-transit primary trucks and urban Green Logistics EV vans are delayed by highway blockages, waterlogging, or city no-entry curfews right now, and what is the fastest safe reroute?",
            "Are any delayed trucks within 4 hours of their NIC E-Way Bill expiring, or do any commercial EV vans need a fast-charging stop added to finish their beat?",
            "Chart the transit minutes saved across all active fleet reroutes.",
            "Stage the updated Google Maps route diversions, EV charger stop, and E-Way Bill extension alert in Zenith."
        ],
    },
    {
        "num": "11",
        "slug": "11_routing_guide_compliance_agent",
        "agent_id": "itc_routing_guide_compliance_agent",
        "class_prefix": "RoutingGuideCompliance",
        "functional_area": "Fleet, Carrier & Freight Governance",
        "itc_pillar": "Pillar 06 · Transport Procurement & Carrier Waterfall Governance",
        "persona": "Transport Procurement Manager",
        "persona_named": "Kavita Krishnamurthy (National Freight Procurement Lead — ITC TM&D HQ Kolkata)",
        "agent_name": "Routing Guide Compliance Agent",
        "build_mode": "No-Code Gemini Gem",
        "priority": "P1",
        "default_model": "gemini-3.8-flash",
        "table_stem": "11_carrier_routing_guide_tenders_and_spot",
        "reuse_status": "REUSED_AND_TAILORED",
        "reused_from_agents": ["freight_control_tower (Live GE: reasoningEngines/1933778444856852480)"],
        "target_system": "SAP TM / Zenith Carrier Waterfall Guide & Monthly Transporter Allocation Scorecard",
        "stops_at": "Advisory & governance No-Code Gem—flags maverick spot indents and drafts L1/L2 carrier show-cause or rate-reindexing memos, never altering signed annual transport contracts unilaterally.",
        "problem_statement": "ITC negotiates annual L1/L2/L3 waterfall rate cards across hundreds of ICML-to-CFA lanes, yet local dispatchers frequently bypass L2 backup carriers during evening rush and book ad-hoc spot-market brokers at 28-40% freight premiums—leaking Crores annually.",
        "special_tool_name": "diagnose_planner_bypass_vs_carrier_rejection",
        "special_tool_doc": "Separates maverick planner waterfall bypasses (where L2 was skipped) from genuine L1+L2 carrier capacity rejections requiring lane rate-card re-indexing.",
        "chart_label_key": "lane_description",
        "chart_value_key": "monthly_spot_leakage_inr",
        "headline_kpi_key": "annualized_recoverable_freight_display",
        "rows_key": "waterfall_compliance_findings",
        "levers_inr_cr": {"productivity": 1.5, "flow": 0.0, "risk": 15.4, "recovery": 0.0, "zero_rationale": "Pure freight procurement & contract-compliance governance Gem (Flow = 0, Revenue Recovery = 0); eliminates maverick spot-market rate leakage (Risk & Leakage) and automates lane compliance audits (Productivity)."},
        "starter_prompts": [
            "Which primary lanes are leaking the most money into expensive spot-market trucks instead of following our L1 and L2 contracted carrier routing guide?",
            "Distinguish lanes where dispatch planners bypassed our L2 backup carrier from lanes where both L1 and L2 transporters rejected tenders due to capacity or backhaul issues.",
            "Show a chart of monthly maverick spot-freight leakage across our top non-compliant lanes.",
            "Draft carrier compliance notices and stage TMS waterfall lock recommendations for procurement review."
        ],
    },
    {
        "num": "12",
        "slug": "12_freight_bill_audit_agent",
        "agent_id": "itc_freight_bill_audit_agent",
        "class_prefix": "FreightBillAudit",
        "functional_area": "Fleet, Carrier & Freight Governance",
        "itc_pillar": "Pillar 06 · Multimodal Freight Audit, POD & Claims Settlement",
        "persona": "Freight Bill & Claims Controller",
        "persona_named": "Subhashish Mukherjee (National Freight Audit & Commercial Claims Controller — Kolkata)",
        "agent_name": "Freight Bill Audit Agent",
        "build_mode": "Multimodal + Agent Studio",
        "priority": "P0",
        "default_model": "gemini-3.1-pro-preview",
        "table_stem": "12_freight_lr_pod_invoices_and_claims",
        "reuse_status": "REUSED_AND_TAILORED",
        "reused_from_agents": [
            "freight_bill_audit_agent (Live GE: reasoningEngines/8272173807427387392)",
            "osd_freight_claims_agent (Live GE: reasoningEngines/5496125750106914816)"
        ],
        "target_system": "SAP S/4HANA FI-AP (`MIRO` / `FB60` Short-Pay Voucher & GST RCM Ledger) + Carrier Dispute Portal",
        "stops_at": "Never releases bank NEFT/RTGS payouts or posts final carrier debit notes without Freight Bill Controller sign-off; blocks 100% of duplicate Lorry Receipt claims.",
        "problem_statement": "Indian CPG freight settlement requires reconciling paper-heavy Lorry Receipts (Bilty), rubber-stamped CFA Proof-of-Delivery (POD) slips with handwritten wet/crushed carton remarks, contracted diesel escalation pegs, and GPS-verified gate detention hours. Manual 5% sampling misses duplicate LR billings, inflated 8-12 hour detention claims, and unrecovered POD shortages.",
        "special_tool_name": "audit_multimodal_lr_pod_and_carrier_invoice",
        "special_tool_doc": "Runs multimodal OCR & visual inspection across scanned Lorry Receipts (`DOC-LR-*.png`), stamped PODs (`DOC-POD-*.png`), and Carrier Tax Invoices (`DOC-FINV-*.png`) for 4-way match.",
        "chart_label_key": "freight_invoice_id",
        "chart_value_key": "overcharge_and_pod_recovery_inr",
        "headline_kpi_key": "total_recovered_display",
        "rows_key": "freight_audit_vouchers",
        "levers_inr_cr": {"productivity": 3.9, "flow": 0.0, "risk": 21.6, "recovery": 0.0, "zero_rationale": "Post-delivery financial & multimodal claims audit (Flow = 0, Revenue Recovery = 0); recovers 3.8-5.2% of freight spend from duplicate LRs, detention padding, and POD damage claims (Risk & Leakage) while replacing manual paper-bilty checking (Productivity)."},
        "starter_prompts": [
            "Audit our pending carrier freight invoices against contracted lane rates, diesel fuel pegs, GPS detention logs, and scanned Proof of Delivery receipts—where are we being overcharged?",
            "Inspect the scanned Lorry Receipt, stamped POD, and invoice for LR-TCI-882910 and LR-HWK-771024 to verify the crushed Dark Fantasy cartons and check for duplicate billing.",
            "Create a chart comparing carrier billed amounts versus verified net payable and overcharge recovery by invoice.",
            "Stage the short-pay SAP vouchers, duplicate-LR block, and POD damage debit notes for controller sign-off."
        ],
    },
]


def render_tools_py(meta: Dict[str, Any]) -> str:
    slug = meta["slug"]
    aid = meta["agent_id"]
    t_stem = meta["table_stem"]
    target_sys = meta["target_system"]
    stops_at = meta["stops_at"]
    spec_fn = meta["special_tool_name"]
    spec_doc = meta["special_tool_doc"]
    lbl_k = meta["chart_label_key"]
    val_k = meta["chart_value_key"]
    kpi_k = meta["headline_kpi_key"]
    rows_k = meta["rows_key"]

    return f'''"""Deterministic Python Tools for {meta['agent_name']} ({slug}) — ITC Limited CPG Pillars 5 & 6."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

AGENT_DIR = Path(__file__).resolve().parents[1]
SUITE_ROOT = AGENT_DIR.parents[1]
if str(SUITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SUITE_ROOT))

from common.itc_data_loader import (
    format_inr,
    inspect_multimodal_document,
    load_backbone,
    query_domain_table,
    stage_governed_enterprise_action,
)
from common.solvers import SOLVER_REGISTRY
from common.a2ui_and_cockpit import (
    build_a2ui_vega_and_canvas,
    export_verified_csv,
    render_interactive_cockpit_html,
)

AGENT_SLUG = "{slug}"
AGENT_ID = "{aid}"
AGENT_NAME = "{meta['agent_name']}"
PERSONA_TITLE = "{meta['persona']}"
FUNCTIONAL_AREA = "{meta['functional_area']}"
BUILD_MODE = "{meta['build_mode']}"
TARGET_SYSTEM = "{target_sys}"
STOPS_AT_BOUNDARY = "{stops_at}"
PRIMARY_TABLE = "{t_stem}"


def query_itc_enterprise_records(search_filter: str = "", limit: int = 30) -> Dict[str, Any]:
    """Queries ITC CPG enterprise records for {meta['agent_name']} from the 405 MB TM&D lake (or container seeds)."""
    return query_domain_table(PRIMARY_TABLE, search_filter=search_filter, limit=limit, agent_dir=AGENT_DIR)


def query_itc_master_network_backbone(entity_type: str = "all", search_filter: str = "") -> Dict[str, Any]:
    """Queries ITC Master Backbone: ICML mega-plants, State CFAs, Wholesale Dealers (WDs), SKUs, and Carriers."""
    bb = load_backbone()
    needle = (search_filter or "").strip().lower()
    mapping = {{
        "icml": bb.get("icml_plants", []),
        "cfa": bb.get("cfa_depots", []),
        "sku": bb.get("sku_master", []),
        "wd": bb.get("wholesale_dealers", []),
        "carrier": bb.get("carriers", []),
    }}
    if entity_type.lower() in mapping:
        items = mapping[entity_type.lower()]
        if needle:
            items = [x for x in items if needle in str(x).lower()]
        return {{"entity_type": entity_type, "count": len(items), "records": items[:25]}}
    return {{"counts": bb.get("counts", {{}}), "systems_landscape": bb.get("systems_landscape", [])}}


def run_deterministic_optimization_solver(search_filter: str = "") -> Dict[str, Any]:
    """Executes the exact deterministic mathematical/OR-Tools/physics solver for {meta['agent_name']}."""
    queried = query_domain_table(PRIMARY_TABLE, search_filter=search_filter, limit=40, agent_dir=AGENT_DIR)
    solver_fn = SOLVER_REGISTRY[AGENT_SLUG]
    result = solver_fn(queried.get("records", []))
    result["agent_id"] = AGENT_ID
    result["agent_name"] = AGENT_NAME
    result["build_mode"] = BUILD_MODE
    result["using_full_enterprise_lake"] = queried.get("using_full_enterprise_lake", False)
    return result


def {spec_fn}(reference_id: str = "") -> Dict[str, Any]:
    """{spec_doc}"""
    if AGENT_SLUG in ("03_cold_chain_thermal_auditor", "12_freight_bill_audit_agent"):
        default_doc = "DOC-STRIP-SHP-CLD-70001.png" if "03_" in AGENT_SLUG else "DOC-POD-882910.png"
        doc_name = reference_id if (reference_id and ".png" in reference_id.lower()) else default_doc
        ocr = inspect_multimodal_document(doc_name)
        solved = run_deterministic_optimization_solver("")
        return {{
            "tool": "{spec_fn}",
            "multimodal_vision_verification": ocr,
            "headline_recovery_or_claim": solved.get("{kpi_k}"),
            "top_audited_items": solved.get("{rows_k}", [])[:3],
        }}
    solved = run_deterministic_optimization_solver(reference_id)
    return {{
        "tool": "{spec_fn}",
        "reference_filter": reference_id or "ALL_PRIORITY_EXCEPTIONS",
        "headline_impact_inr": solved.get("{kpi_k}"),
        "verified_diagnostics": solved.get("{rows_k}", [])[:4],
        "human_gate_boundary": STOPS_AT_BOUNDARY,
    }}


def stage_governed_erp_or_portal_action(
    target_record_id: str,
    proposed_action: str,
    rationale: str = "",
    idempotency_key: str = "",
) -> Dict[str, Any]:
    """Stages a policy-checked write-back to {target_sys} with idempotency & human sign-off."""
    return stage_governed_enterprise_action(
        agent_id=AGENT_ID,
        target_system=TARGET_SYSTEM,
        action_type=proposed_action,
        target_record_id=target_record_id,
        payload={{"proposed_action": proposed_action, "agent_slug": AGENT_SLUG}},
        rationale=rationale or f"Deterministic recommendation from {{AGENT_NAME}}",
        stops_at_boundary=STOPS_AT_BOUNDARY,
        idempotency_key=idempotency_key,
    )


def render_a2ui_visual_chart_and_canvas(search_filter: str = "") -> Dict[str, Any]:
    """Renders A2UI v0.9 visual-only VegaChart card + side-panel RichTable Canvas."""
    solved = run_deterministic_optimization_solver(search_filter)
    rows = solved.get("{rows_k}", [])
    return build_a2ui_vega_and_canvas(
        agent_title=AGENT_NAME,
        subtitle=f"{{FUNCTIONAL_AREA}} · Headline Impact: {{solved.get('{kpi_k}', 'Verified')}}",
        rows=rows,
        label_key="{lbl_k}",
        value_key="{val_k}",
        value_title_inr="Verified Impact / Metric (₹ INR)",
    )


def export_atomic_schedule_csv(search_filter: str = "") -> Dict[str, Any]:
    """Exports an atomic RFC-4180 CSV schedule ready for Google Sheets or SAP upload."""
    solved = run_deterministic_optimization_solver(search_filter)
    rows = solved.get("{rows_k}", [])
    out_dir = AGENT_DIR / "artifacts_out"
    return export_verified_csv(AGENT_SLUG, rows, out_dir)


def generate_interactive_html_cockpit(search_filter: str = "") -> Dict[str, Any]:
    """Compiles a self-contained Light-Theme Default Interactive HTML5 Cockpit for {meta['agent_name']}."""
    solved = run_deterministic_optimization_solver(search_filter)
    rows = solved.get("{rows_k}", [])
    out_dir = AGENT_DIR / "artifacts_out"
    return render_interactive_cockpit_html(
        agent_slug=AGENT_SLUG,
        agent_title=AGENT_NAME,
        persona_title=PERSONA_TITLE,
        functional_area=FUNCTIONAL_AREA,
        headline_metric_label="Verified Deterministic Impact",
        headline_metric_value=str(solved.get("{kpi_k}", "₹0")),
        rows=rows,
        output_dir=out_dir,
    )


ALL_TOOLS = [
    query_itc_enterprise_records,
    query_itc_master_network_backbone,
    run_deterministic_optimization_solver,
    {spec_fn},
    stage_governed_erp_or_portal_action,
    render_a2ui_visual_chart_and_canvas,
    export_atomic_schedule_csv,
    generate_interactive_html_cockpit,
]
'''


def render_agent_py(meta: Dict[str, Any]) -> str:
    slug = meta["slug"]
    aid = meta["agent_id"]
    cls = meta["class_prefix"]
    rows_k = meta["rows_key"]
    kpi_k = meta["headline_kpi_key"]

    return f'''"""Google ADK + GlobalGemini Agent for {meta['agent_name']} ({slug}) — ITC Limited CPG Pillars 5 & 6."""
from __future__ import annotations

import importlib.util as _ilu
import os
import sys as _sys
from functools import cached_property
from pathlib import Path as _Path
from typing import Any, Callable, Dict, List, Optional

try:
    from . import tools
except ImportError:
    _t_spec = _ilu.spec_from_file_location(f"{slug}_tools", _Path(__file__).resolve().parent / "tools.py")
    assert _t_spec and _t_spec.loader
    tools = _ilu.module_from_spec(_t_spec)  # type: ignore
    _t_spec.loader.exec_module(tools)  # type: ignore

AGENT_ID = "{aid}"
AGENT_SLUG = "{slug}"
AGENT_DISPLAY_NAME = "{meta['agent_name']}"
FUNCTIONAL_AREA = "{meta['functional_area']}"
PERSONA_OWNER = "{meta['persona']}"
NAMED_PERSONA = "{meta['persona_named']}"
BUILD_MODE = "{meta['build_mode']}"
DEFAULT_MODEL = "{meta['default_model']}"

_WRITE_TOOLS = {{
    "stage_governed_erp_or_portal_action": ["target_record_id", "proposed_action"],
}}

SYSTEM_INSTRUCTION = """You are the **{meta['agent_name']}**, built in `{meta['build_mode']}` mode for **{meta['persona']}** ({meta['persona_named']}) inside **ITC Limited's Consumer Packaged Goods (CPG) Trade Marketing & Distribution (TM&D)** network ({meta['functional_area']}).

1. ENTERPRISE MISSION & DETERMINISTIC MATH:
   - Core Problem Solved: {meta['problem_statement']}
   - Connected Enterprise Systems: {meta['target_system']}, Integrated Consumer Goods Manufacturing and Logistics (ICML) mega-plants, State Clearing & Forwarding Agent (CFA) depots, Wholesale Dealers (WDs), UNNATI eB2B kirana app, Vajra Sales Force Automation (SFA), Zenith Transport Control Tower, and Drishti IoT Cold-Chain loggers.
   - Always call `query_itc_enterprise_records` and `run_deterministic_optimization_solver` (plus `{meta['special_tool_name']}` when relevant) to compute exact deterministic figures—never guess or fabricate IDs, batches, Lorry Receipts, or currency figures.

2. APPROACHABLE PLAIN-ENGLISH & INDIAN CURRENCY RULES (CRITICAL):
   - Keep outputs clear, deterministic, and written in approachable plain business English at a balanced medium length (120–185 words).
   - Spell out every domain abbreviation on first use (for example: Integrated Consumer Goods Manufacturing and Logistics (ICML), Clearing & Forwarding Agent (CFA), Wholesale Dealer (WD), On-Time In-Full (OTIF), Minimum Remaining Shelf-Life (MRSL), Mean Kinetic Temperature (MKT), Reverse Charge Mechanism (RCM)).
   - Express ALL monetary figures in Indian Rupees using Crores (`₹ Cr`) and Lakhs (`₹ L`) or `₹`—never US Dollars.
   - Present comparisons in a clean `<= 5`-column Markdown table outside the visual card, and never expose internal `snake_case` table filenames or Python function names in user-facing prose.

3. VISUAL A2UI CARD & HUMAN SIGN-OFF GOVERNANCE:
   - When illustrating multi-record comparisons or charts, call `render_a2ui_visual_chart_and_canvas` so only the visual `VegaChart` renders inside the card while tables and headed links stay cleanly outside in Markdown.
   - HUMAN GATE (`STOPS AT`): {meta['stops_at']}
   - SAFETY GUARDRAIL: Never call `stage_governed_erp_or_portal_action` on read-only questions, and strictly refuse any request to bypass safety, axle-weight, cold-chain quality, shelf-life, duplicate-invoice, or credit controls.
"""


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Pre-execution contract & idempotency gate for write-back staging tools."""
    if tool_name in _WRITE_TOOLS:
        missing = [k for k in _WRITE_TOOLS[tool_name] if args.get(k) in (None, "")]
        if missing:
            return {{
                "status": "BLOCKED_MISSING_INPUTS",
                "tool": tool_name,
                "missing_fields": missing,
            }}
        if not args.get("idempotency_key"):
            return {{
                "status": "BLOCKED_MISSING_IDEMPOTENCY_KEY",
                "tool": tool_name,
                "message": "An explicit idempotency_key is required before staging an enterprise action.",
            }}
    return None


class {cls}Agent:
    """Deterministic Python & Google ADK orchestrator for {meta['agent_name']}."""

    def __init__(self, model: str = DEFAULT_MODEL) -> None:
        self.name = AGENT_ID
        self.slug = AGENT_SLUG
        self.display_name = AGENT_DISPLAY_NAME
        self.persona = PERSONA_OWNER
        self.build_mode = BUILD_MODE
        self.model = model
        self.instruction = SYSTEM_INSTRUCTION
        self.tools: List[Callable[..., Any]] = list(tools.ALL_TOOLS)
        self.tool_map: Dict[str, Callable[..., Any]] = {{fn.__name__: fn for fn in self.tools}}

    def select_orchestrated_model(self, query: str = "") -> Dict[str, str]:
        """Routes complex multi-constraint optimization/multimodal audits to Gemini 3.1 Pro and fast pulse queries to Gemini 3.8 Flash."""
        q_low = (query or "").lower()
        deep_keywords = ("optimize", "consolidate", "ration", "allocate", "arrhenius", "mkt", "multimodal", "pod", "sap", "reroute", "simulate")
        chosen = "gemini-3.1-pro-preview" if (DEFAULT_MODEL == "gemini-3.1-pro-preview" or any(k in q_low for k in deep_keywords)) else "gemini-3.8-flash"
        return {{
            "selected_model": chosen,
            "endpoint_location": "global",
            "build_mode": BUILD_MODE,
        }}

    def run_scenario(self, user_query: str = "") -> Dict[str, Any]:
        """Executes deterministic data retrieval, solver math, and A2UI spec generation end-to-end."""
        routing = self.select_orchestrated_model(user_query)
        solved = tools.run_deterministic_optimization_solver("")
        special = tools.{meta['special_tool_name']}("")
        a2ui = tools.render_a2ui_visual_chart_and_canvas("")
        rows = solved.get("{rows_k}", [])[:4]

        # Build concise <=5-column plain-English Markdown summary table
        if rows:
            cols = list(rows[0].keys())[:4]
            hdr = "| " + " | ".join(c.replace("_", " ").title() for c in cols) + " |"
            sep = "| " + " | ".join(":---" for _ in cols) + " |"
            body = "\\n".join("| " + " | ".join(str(r.get(c, "")) for c in cols) + " |" for r in rows)
            md_table = f"{{hdr}}\\n{{sep}}\\n{{body}}"
        else:
            md_table = "| Status | Impact |\\n| :--- | :--- |\\n| Verified | ₹0 |"

        headline_val = solved.get("{kpi_k}", "Verified")
        markdown = (
            f"**{meta['agent_name']}** completed a deterministic review across **ITC Limited's Trade Marketing & Distribution (TM&D)** "
            f"network for **{meta['persona']}**, identifying **{{headline_val}}** in verified operational value.\\n\\n"
            f"{{md_table}}\\n\\n"
            f"- **Connected System Boundary**: {meta['target_system']}\\n"
            f"- **Human Sign-Off Gate**: {meta['stops_at']}"
        )
        return {{
            "agent_id": AGENT_ID,
            "agent_name": AGENT_DISPLAY_NAME,
            "persona": PERSONA_OWNER,
            "build_mode": BUILD_MODE,
            "model_routing": routing,
            "headline_impact": headline_val,
            "solver_output": solved,
            "special_diagnostic": special,
            "a2ui_surface": a2ui,
            "markdown": markdown,
        }}


try:
    from google.adk.agents import Agent
    from google.adk.models import Gemini
    from google.genai import Client, types

    class GlobalGemini(Gemini):
        """Routes Gemini 3.1 Pro and Gemini 3.8 Flash calls to the global Vertex AI endpoint (`location='global'`)."""

        @cached_property
        def api_client(self) -> Client:
            return Client(
                vertexai=True,
                project=os.environ.get("GOOGLE_CLOUD_PROJECT", "zuhaibp-ai"),
                location="global",
                http_options=types.HttpOptions(
                    headers=self._tracking_headers(),
                    retry_options=self.retry_options,
                ),
            )

    root_agent = Agent(
        name=AGENT_ID,
        model=GlobalGemini(
            model=DEFAULT_MODEL,
            retry_options=types.HttpRetryOptions(attempts=3),
        ),
        description=f"[ITC CPG · {meta['functional_area']}] {meta['agent_name']} for {meta['persona']} ({meta['build_mode']})",
        instruction=SYSTEM_INSTRUCTION,
        tools=list(tools.ALL_TOOLS),
    )
except Exception:
    root_agent = {cls}Agent()  # type: ignore


def create_adk_app() -> Any:
    """Deferred factory for `AdkApp(agent=root_agent)` AFTER `vertexai.init(project=..., location=...)`."""
    from vertexai.preview.reasoning_engines import AdkApp
    return AdkApp(agent=root_agent)
'''


def write_mode_specific_specs(agent_dir: Path, meta: Dict[str, Any]) -> List[str]:
    specs_dir = agent_dir / "studio_specs"
    specs_dir.mkdir(parents=True, exist_ok=True)
    created = []

    # 1. Declarative Agent Studio YAML (all 12 agents)
    yaml_text = f"""# Gemini Enterprise Agent Studio Declarative Specification — ITC Limited CPG
apiVersion: gemini-enterprise.cloud.google.com/v1
kind: DeclarativeAgent
metadata:
  agent_id: {meta['agent_id']}
  slug: {meta['slug']}
  display_name: "{meta['agent_name']}"
  build_mode: "{meta['build_mode']}"
  functional_area: "{meta['functional_area']}"
  itc_pillar: "{meta['itc_pillar']}"
  persona_owner: "{meta['persona']}"
  named_leader: "{meta['persona_named']}"
  priority_tier: "{meta['priority']}"
spec:
  model_routing:
    endpoint: global
    default_model: {meta['default_model']}
    escalation_model: gemini-3.1-pro-preview
    workhorse_model: gemini-3.8-flash
  enterprise_data_lake_table: "enterprise_data/lake_full/{meta['table_stem']}.csv"
  target_system_of_record: "{meta['target_system']}"
  human_signoff_boundary: "{meta['stops_at']}"
  deterministic_tools:
    - query_itc_enterprise_records
    - query_itc_master_network_backbone
    - run_deterministic_optimization_solver
    - {meta['special_tool_name']}
    - stage_governed_erp_or_portal_action
    - render_a2ui_visual_chart_and_canvas
    - export_atomic_schedule_csv
    - generate_interactive_html_cockpit
  starter_prompts:
""" + "\n".join(f'    - "{p}"' for p in meta["starter_prompts"]) + "\n"
    (specs_dir / "gemini_enterprise_agent_studio.yaml").write_text(yaml_text, encoding="utf-8")
    created.append("studio_specs/gemini_enterprise_agent_studio.yaml")

    # 2. OpenAPI v3 Tool Connector Spec (all 12 agents)
    openapi_obj = {
        "openapi": "3.0.3",
        "info": {
            "title": f"ITC CPG TM&D — {meta['agent_name']} Connector API",
            "version": "1.0.0",
            "description": f"Mode: {meta['build_mode']} | Target System: {meta['target_system']}",
        },
        "paths": {
            f"/v1/itc-tmd/{meta['slug']}/records": {
                "get": {
                    "operationId": "query_itc_enterprise_records",
                    "summary": f"Fetch live {meta['agent_name']} operational records",
                }
            },
            f"/v1/itc-tmd/{meta['slug']}/solve": {
                "post": {
                    "operationId": "run_deterministic_optimization_solver",
                    "summary": f"Run deterministic solver for {meta['agent_name']}",
                }
            },
            f"/v1/itc-tmd/{meta['slug']}/stage-action": {
                "post": {
                    "operationId": "stage_governed_erp_or_portal_action",
                    "summary": f"Stage human-gated write-back in {meta['target_system']}",
                }
            },
        },
    }
    (specs_dir / "openapi_tools_spec.json").write_text(json.dumps(openapi_obj, indent=2), encoding="utf-8")
    created.append("studio_specs/openapi_tools_spec.json")

    # 3. Mode-Specific Deep Artifacts matching the table's exact Build Mode column!
    if meta["build_mode"] == "Low-Code + SAP OpenAPI":
        sap_spec = {
            "openapi": "3.0.3",
            "info": {
                "title": "ITC SAP S/4HANA SD / EWM / FinAgg / NIC GST Cutoff OpenAPI Bundle",
                "version": "2026.11",
                "description": "Resolves EOD 21:00 IST CFA billing cutoff blockers across VL02N, VF01, VKM3 FinAgg Credit & NIC E-Way Part-B.",
            },
            "paths": {
                "/sap/opu/odata/sap/API_OUTBOUND_DELIVERY_SRV/ConfirmBatchSplitAndPGI": {
                    "post": {"summary": "Reconciles FEFO batch split lines on picked CFA deliveries and posts Goods Issue (VL02N)."}
                },
                "/sap/opu/odata/sap/Z_API_SD_FINAGG_SYNC_AND_VF01_BILLING": {
                    "post": {"summary": "Syncs approved FinAgg/SBI dealer credit-line drawdowns into VKM3 and triggers VF01 GST invoice."}
                },
                "/sap/opu/odata/sap/Z_API_GST_EWAYBILL_PARTB_RETRY": {
                    "post": {"summary": "Normalizes vehicle registration number formatting and generates NIC E-Way Bill Part-B."}
                },
            },
        }
        (specs_dir / "sap_s4hana_sd_ewm_irn_openapi_v3.json").write_text(json.dumps(sap_spec, indent=2), encoding="utf-8")
        created.append("studio_specs/sap_s4hana_sd_ewm_irn_openapi_v3.json")

    elif meta["build_mode"] == "Low-Code + Maps Platform":
        maps_spec = {
            "platform": "Google Maps Platform Routes Preferred v2 + WeatherNext 3 + NIC E-Way API",
            "endpoints": [
                {
                    "api": "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix",
                    "routingPreference": "TRAFFIC_AWARE_OPTIMAL",
                    "travelMode": "DRIVE",
                    "extraComputations": ["TOLLS", "FUEL_CONSUMPTION"],
                },
                {
                    "api": "https://routes.googleapis.com/directions/v2:computeRoutes",
                    "ev_green_logistics_profile": {
                        "vehicle_types": ["Tata Ace EV 4W", "Euler HiLoad EV 3W"],
                        "min_soc_arrival_pct": 18.0,
                        "dc_fast_charger_network": ["BESCOM", "Tata Power EZ Charge", "Magenta ChargeGrid"],
                    },
                },
            ],
            "curfew_geofences": [
                "Mumbai MMR / Thane Heavy Vehicle Window (08:00-11:00 & 17:00-21:00 IST)",
                "Kolkata Police Vidyasagar Setu Goods Restriction (08:00-21:00 IST)",
            ],
        }
        (specs_dir / "google_maps_routes_matrix_v2_spec.json").write_text(json.dumps(maps_spec, indent=2), encoding="utf-8")
        created.append("studio_specs/google_maps_routes_matrix_v2_spec.json")

    elif meta["build_mode"] == "No-Code Gemini Gem":
        gem_md = f"""# No-Code Gemini Gem Blueprint — {meta['agent_name']}

## 1. Gem Identity & Persona Grounding
- **Gem Name**: `{meta['agent_name']}`
- **Target User**: `{meta['persona']}` ({meta['persona_named']})
- **Recommended Model**: `Gemini 3.8 Flash` (`gemini-3.8-flash` via Global Endpoint for sub-2-second morning turnaround)

## 2. Copy-Paste Gemini Gem System Instructions
```text
You are the {meta['agent_name']} for ITC Limited's Trade Marketing & Distribution (TM&D) organization, supporting the {meta['persona']}.
1. Ground every answer strictly in the attached ITC TM&D connected sheets / BigQuery views ({meta['table_stem']}).
2. Open with a crisp 2-sentence executive summary quantifying impact in Indian Rupees (Crores `₹ Cr` and Lakhs `₹ L`), spelling out domain abbreviations on first use.
3. Present prioritized exceptions in a clean <=5-column table sorted by financial exposure, followed by 3 concrete field or procurement actions before 09:00 AM IST.
4. Never fabricate territory codes, Wholesale Dealer names, or carrier tender IDs, and never mutate contracts or ERP ledgers directly.
```

## 3. Connected Grounding Knowledge Pack
- **Primary Fact Sheet**: `enterprise_data/seeds/{meta['table_stem']}.json` (linked to 405 MB full CSV lake)
- **Master Network Reference**: `enterprise_data/seeds/00_itc_network_backbone.json`
"""
        (specs_dir / "gemini_gem_blueprint_and_knowledge_pack.md").write_text(gem_md, encoding="utf-8")
        created.append("studio_specs/gemini_gem_blueprint_and_knowledge_pack.md")

    elif meta["build_mode"] == "Multimodal + Agent Studio":
        mm_yaml = """# Multimodal Vision + Agent Studio 4-Way Freight Audit Pipeline
pipeline_id: itc_multimodal_lr_pod_invoice_auditor_v1
vision_model: gemini-3.1-pro-preview
endpoint_location: global
document_classes:
  - class_id: lorry_receipt_bilty
    sample_files: ["DOC-LR-882910.png", "DOC-LR-771024.png", "DOC-LR-664319.png"]
    extracted_fields: ["lr_number", "consignor_icml", "consignee_cfa", "vehicle_reg_no", "manifested_cases", "contract_rate_ref"]
  - class_id: stamped_cfa_pod_receipt
    sample_files: ["DOC-POD-882910.png", "DOC-POD-771024.png", "DOC-POD-664319.png"]
    extracted_fields: ["gate_in_ist", "gate_out_ist", "verified_detention_hrs", "good_cases_received", "handwritten_osd_damage_cases", "rubber_stamp_verdict"]
  - class_id: carrier_gst_freight_invoice
    sample_files: ["DOC-FINV-9041.png", "DOC-FINV-9042.png", "DOC-FINV-9043.png"]
    extracted_fields: ["freight_invoice_id", "billed_base_inr", "billed_fsc_pct", "billed_detention_hrs", "gst_rcm_flag"]
reconciliation_rules:
  - Block 100% if `lr_number` matches an already settled SAP FI-AP voucher (`DUPLICATE_LR_BLOCK`).
  - Cap billable detention to `max(0, min(pod_dwell_hrs, zenith_gps_dwell_hrs) - 2.0_free_hrs)`.
  - Deduct scanned POD crushed/wet carton debit (`cases_short * case_mrp_realization`) before short-pay voucher staging.
"""
        (specs_dir / "multimodal_ocr_4way_match_pipeline.yaml").write_text(mm_yaml, encoding="utf-8")
        created.append("studio_specs/multimodal_ocr_4way_match_pipeline.yaml")

    return created


def render_test_smoke_py(meta: Dict[str, Any]) -> str:
    cls = meta["class_prefix"]
    spec_fn = meta["special_tool_name"]
    rows_k = meta["rows_key"]
    kpi_k = meta["headline_kpi_key"]

    return f'''"""Comprehensive Pytest Suite for {meta['agent_name']} ({meta['slug']})."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parents[1]
SUITE_ROOT = AGENT_DIR.parents[1]
if str(SUITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SUITE_ROOT))

_tools_spec = importlib.util.spec_from_file_location("{meta['slug']}_tools", AGENT_DIR / "app" / "tools.py")
assert _tools_spec and _tools_spec.loader
tools = importlib.util.module_from_spec(_tools_spec)
_tools_spec.loader.exec_module(tools)

_agent_spec = importlib.util.spec_from_file_location("{meta['slug']}_agent", AGENT_DIR / "app" / "agent.py")
assert _agent_spec and _agent_spec.loader
agent_mod = importlib.util.module_from_spec(_agent_spec)
sys.modules["tools"] = tools
_agent_spec.loader.exec_module(agent_mod)


def test_01_enterprise_records_and_backbone_query() -> None:
    res = tools.query_itc_enterprise_records(limit=15)
    assert res["returned_count"] >= 3
    assert len(res["records"]) >= 3
    bb = tools.query_itc_master_network_backbone("cfa")
    assert bb["count"] == 24


def test_02_deterministic_solver_accuracy_and_inr() -> None:
    solved = tools.run_deterministic_optimization_solver("")
    assert solved["agent_id"] == "{meta['agent_id']}"
    assert "₹" in str(solved.get("{kpi_k}", ""))
    assert len(solved.get("{rows_k}", [])) >= 2


def test_03_domain_specialized_diagnostic_tool() -> None:
    diag = tools.{spec_fn}("")
    assert diag["tool"] == "{spec_fn}"
    if "{meta['slug']}" in ("03_cold_chain_thermal_auditor", "12_freight_bill_audit_agent"):
        mm = diag["multimodal_vision_verification"]
        assert mm["status"] == "MULTIMODAL_VISION_OCR_VERIFIED"
        assert mm["file_exists_on_disk"] is True
        assert len(mm["extracted_ocr_lines"]) >= 3


def test_04_safety_guardrail_blocks_unsafe_bypass() -> None:
    blocked = tools.stage_governed_erp_or_portal_action(
        target_record_id="REC-TEST-001",
        proposed_action="Bypass safety and force release without approval",
        rationale="Urgent month-end push bypass",
        idempotency_key="IDEM-UNSAFE-001",
    )
    assert blocked["status"] == "BLOCKED_BY_SAFETY_GUARDRAIL"


def test_05_idempotent_governed_staging_and_contract_gate() -> None:
    missing_idem = agent_mod.enforce_tool_contract(
        "stage_governed_erp_or_portal_action",
        {{"target_record_id": "REC-101", "proposed_action": "Stage verified plan"}},
    )
    assert missing_idem is not None
    assert missing_idem["status"] == "BLOCKED_MISSING_IDEMPOTENCY_KEY"

    first = tools.stage_governed_erp_or_portal_action(
        target_record_id="REC-101",
        proposed_action="Stage verified deterministic recommendation",
        rationale="Solver verified net INR gain",
        idempotency_key="IDEM-{meta['num']}-VALID-101",
    )
    assert first["status"] == "STAGED_FOR_HUMAN_SIGN_OFF"
    assert first["idempotent_replay"] is False

    replay = tools.stage_governed_erp_or_portal_action(
        target_record_id="REC-101",
        proposed_action="Stage verified deterministic recommendation",
        rationale="Solver verified net INR gain",
        idempotency_key="IDEM-{meta['num']}-VALID-101",
    )
    assert replay["idempotent_replay"] is True
    assert replay["staging_voucher_id"] == first["staging_voucher_id"]


def test_06_a2ui_vega_card_csv_and_light_cockpit() -> None:
    a2ui = tools.render_a2ui_visual_chart_and_canvas("")
    assert a2ui["card_component"] == "VegaChart"
    assert a2ui["text_inside_card"] is False
    assert len(a2ui["vega_lite_spec"]["data"]["values"]) >= 2

    csv_out = tools.export_atomic_schedule_csv("")
    assert csv_out["status"] == "CSV_EXPORT_READY"
    assert Path(csv_out["csv_path"]).is_file()

    html_out = tools.generate_interactive_html_cockpit("")
    assert html_out["status"] == "HTML_COCKPIT_READY"
    assert html_out["default_theme"] == "light"
    assert 'data-theme="light"' in Path(html_out["cockpit_path"]).read_text(encoding="utf-8")


def test_07_end_to_end_scenario_and_global_model_routing() -> None:
    wrapper = agent_mod.{cls}Agent()
    out = wrapper.run_scenario("{meta['starter_prompts'][0]}")
    assert out["agent_id"] == "{meta['agent_id']}"
    assert out["model_routing"]["endpoint_location"] == "global"
    assert out["model_routing"]["selected_model"] in ("gemini-3.1-pro-preview", "gemini-3.8-flash")
    assert "₹" in out["markdown"]
'''


def render_agent_readme(meta: Dict[str, Any], spec_files: List[str]) -> str:
    lv = meta["levers_inr_cr"]
    tot_cr = round(lv["productivity"] + lv["flow"] + lv["risk"] + lv["recovery"], 1)
    fmt_lv = lambda v: f"₹{v:.1f} Cr/yr" if v > 0 else "— (Load-Bearing Zero)"
    prompts_md = "\n".join(f"{i+1}. *\"{p}\"*" for i, p in enumerate(meta["starter_prompts"]))
    reused_md = ", ".join(f"`{x}`" for x in meta["reused_from_agents"])
    specs_md = "\n".join(f"- `{s}`" for s in spec_files)

    return f"""# {meta['num']} · {meta['agent_name']}

- **Enterprise Scope**: ITC Limited — Consumer Packaged Goods (CPG) Trade Marketing & Distribution (TM&D)
- **Functional Area**: {meta['functional_area']} ({meta['itc_pillar']})
- **Persona Owner**: **{meta['persona']}** (*{meta['persona_named']}*)
- **Build Mode**: **`{meta['build_mode']}`** · **Priority**: `{meta['priority']}`
- **Model Routing (`GlobalGemini`, `location="global"`)**: `{meta['default_model']}`
- **Reuse & Provenance (`{meta['reuse_status']}`)**: {reused_md}

## 1. Operational Problem Solved in ITC CPG
{meta['problem_statement']}

## 2. Researched 4-Lever Annual Value Attribution (`₹{tot_cr:.1f} Cr/yr`)
| Value Lever | Annual Impact (INR) | Attribution Note |
| :--- | :--- | :--- |
| **Productivity** | {fmt_lv(lv['productivity'])} | Planner / supervisor / field-manager toil eliminated |
| **Flow & Capital** | {fmt_lv(lv['flow'])} | Dock, CFA wave, transit velocity & inventory turnover |
| **Risk & Leakage** | {fmt_lv(lv['risk'])} | Freight overcharges, detention slabs, OTIF penalties & spoilage |
| **Revenue Recovery** | {fmt_lv(lv['recovery'])} | Prevented stockouts, saved cutoffs & protected channel fill |

> **Load-Bearing Zero Discipline**: {meta['levers_inr_cr']['zero_rationale']}

## 3. Connected Systems & Human Sign-Off Gate
- **Target System**: {meta['target_system']}
- **Primary Fact Table**: `enterprise_data/lake_full/{meta['table_stem']}.csv`
- **Human Gate (`STOPS AT`)**: {meta['stops_at']}

## 4. Mode-Specific Specifications Included
{specs_md}

## 5. Plain-English Business Starter Prompts
{prompts_md}
"""


def main() -> None:
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    manifest_summary = []

    for meta in AGENTS_CATALOG:
        adir = AGENTS_DIR / meta["slug"]
        (adir / "app").mkdir(parents=True, exist_ok=True)
        (adir / "tests").mkdir(parents=True, exist_ok=True)
        (adir / "fixtures" / "tables").mkdir(parents=True, exist_ok=True)

        # Copy seed JSON into agent's hermetic fixtures/tables/
        src_seed = SEEDS_DIR / f"{meta['table_stem']}.json"
        if src_seed.is_file():
            shutil.copyfile(src_seed, adir / "fixtures" / "tables" / f"{meta['table_stem']}.json")

        (adir / "app" / "__init__.py").write_text(
            'from .agent import root_agent, create_adk_app\n__all__ = ["root_agent", "create_adk_app"]\n',
            encoding="utf-8",
        )
        (adir / "app" / "tools.py").write_text(render_tools_py(meta), encoding="utf-8")
        (adir / "app" / "agent.py").write_text(render_agent_py(meta), encoding="utf-8")
        spec_files = write_mode_specific_specs(adir, meta)
        (adir / "tests" / "test_smoke.py").write_text(render_test_smoke_py(meta), encoding="utf-8")
        (adir / "README.md").write_text(render_agent_readme(meta, spec_files), encoding="utf-8")
        (adir / "manifest.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

        lv = meta["levers_inr_cr"]
        tot = round(lv["productivity"] + lv["flow"] + lv["risk"] + lv["recovery"], 1)
        manifest_summary.append({
            "num": meta["num"],
            "slug": meta["slug"],
            "agent_id": meta["agent_id"],
            "agent_name": meta["agent_name"],
            "functional_area": meta["functional_area"],
            "persona": meta["persona"],
            "build_mode": meta["build_mode"],
            "priority": meta["priority"],
            "default_model": meta["default_model"],
            "reuse_status": meta["reuse_status"],
            "annual_value_cr_inr": tot,
        })

    (SUITE_ROOT / "itc_pillars_5_6_catalog.json").write_text(
        json.dumps(manifest_summary, indent=2), encoding="utf-8"
    )
    print(f"Built {len(manifest_summary)} ITC CPG Pillar 5 & 6 Agents successfully.")


if __name__ == "__main__":
    main()
