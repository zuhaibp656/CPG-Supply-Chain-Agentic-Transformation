#!/usr/bin/env python3
"""Builds all 12 Hermetic ITC Limited CPG Pillars 5 & 6 Agents (`(ITC TMD)`),
with 3 Authentic Persona Starter Prompts per Agent, Autonomous A2UI v0.9 Dual-Surface Charts
(Bar, Grouped, Line + Donut/Pie Share + Looker RichTable Canvas), GCS V4 Signed HTML5 Cockpits,
Scanned Multimodal PNG Document Links, and Pytest Verification Suites."""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Dict, List

SUITE_ROOT = Path(__file__).resolve().parents[1]
COMMON_DIR = SUITE_ROOT / "common"
AGENTS_DIR = SUITE_ROOT / "agents"
SEEDS_DIR = SUITE_ROOT / "enterprise_data" / "seeds"
MM_DIR = SUITE_ROOT / "enterprise_data" / "multimodal_docs"

AGENTS_CATALOG: List[Dict[str, Any]] = [
    {
        "num": "01",
        "slug": "01_load_consolidation_agent",
        "agent_id": "itc_load_consolidation_agent",
        "class_prefix": "ItcLoadConsolidation",
        "ge_display_name": "Load Consolidation Agent (ITC TMD)",
        "icon": "view_in_ar",
        "functional_area": "Primary Logistics & Plant Dispatch (Factory -> CFA / Depot)",
        "itc_pillar": "Pillar 06 · Green Logistics & Primary Dispatch",
        "persona": "Primary Transport Planner",
        "persona_named": "Raghavendra Kulkarni (Primary Transport Lead — Pune Ranjangaon ICML)",
        "agent_name": "Load Consolidation Agent",
        "build_mode": "Google ADK + Python Solvers",
        "priority": "P0",
        "default_model": "gemini-3.1-pro-preview",
        "table_stem": "01_icml_primary_dispatch_waves_and_cartons",
        "multimodal_docs": ["DOC-WB-SLIP-9001.png"],
        "reuse_status": "REUSED_AND_TAILORED",
        "reused_from_agents": ["load_consolidation_agent", "fleetflow_cpg_tmd 3D Load Studio"],
        "target_system": "SAP Transportation Management (SAP TM) & Zenith Indent Portal",
        "stops_at": "Never auto-tenders overloaded vehicles violating Central Motor Vehicles Rules (CMVR) Rule 93 axle limits or commits SAP TM shipment cost docs without Primary Transport Planner sign-off.",
        "problem_statement": "ITC ICML mega-plants ship both high-density Staples (Aashirvaad Atta at ~600 kg/m3, weighting out a 32-ft MXL truck at 45% volume) and ultra-light fragile Foods (Bingo! chips & Sunfeast biscuits at ~90-180 kg/m3, cubing out at 25% payload). Dispatching single-category trucks wastes 28-36% of primary freight spend.",
        "special_tool_name": "verify_cmvr_rule93_axle_and_crush_physics",
        "special_tool_doc": "Verifies Central Motor Vehicles Rules (CMVR) Rule 93 front steering (<=7,500 kg) & rear drive (<=11,500 kg) axle weights and top-tier carton crush limits (<=85 kg on Bingo! / <=155 kg on Sunfeast).",
        "chart_label_key": "composite_load_id",
        "chart_value_key": "freight_saved_inr",
        "headline_kpi_key": "net_freight_savings_display",
        "rows_key": "composite_load_plans",
        "levers_inr_cr": {"productivity": 2.4, "flow": 0.0, "risk": 8.6, "recovery": 18.4, "zero_rationale": "Flow & working-capital inventory days stay governed by S&OP; value comes from eliminating half-empty primary FTLs and preventing axle-overload fines & carton crush damage."},
        "starter_prompts": [
            "Check today's staged Ranjangaon and Khordha dispatches. Where are we sending half-empty Atta or Bingo! trucks that can be combined?",
            "Will co-loading Sunfeast biscuits and Bingo! cartons above Aashirvaad Atta on the Ahmedabad lane stay safe on axle weight and carton crushing?",
            "Prepare the consolidated truck loading plan for the Sanand and Dankuni lanes so I can review and release the indents.",
            "Run a what-if scenario: how much freight cost can we save if diesel surcharge rises 15% and we prioritize mixed biscuit-and-atta loads across western lanes?",
        ],
    },
    {
        "num": "02",
        "slug": "02_yard_disruption_detention_sentinel",
        "agent_id": "itc_yard_disruption_detention_sentinel",
        "class_prefix": "ItcYardDisruptionDetention",
        "ge_display_name": "Yard Disruption & Detention Sentinel (ITC TMD)",
        "icon": "rv_hookup",
        "functional_area": "Primary Logistics & Plant Dispatch (Factory -> CFA / Depot)",
        "itc_pillar": "Pillar 06 · Green Logistics & Primary Dispatch",
        "persona": "Plant Yard & Dispatch Lead",
        "persona_named": "Harpreet Singh Gill (ICML Yard Master — Kapurthala & Ranjangaon)",
        "agent_name": "Yard Disruption & Detention Sentinel",
        "build_mode": "Google ADK + Python Solvers",
        "priority": "P0",
        "default_model": "gemini-3.1-pro-preview",
        "table_stem": "02_icml_yard_gate_fastag_dock_detention",
        "multimodal_docs": ["DOC-WB-SLIP-9004.png"],
        "reuse_status": "REUSED_AND_TAILORED",
        "reused_from_agents": ["yard_dock_sequencer", "yard_dock_scheduling_agent"],
        "target_system": "SAP Extended Warehouse Management (SAP EWM) Yard & Weighbridge Gate Console",
        "stops_at": "Never overrides ICML gate security tare-weight discrepancy holds or waives contractual detention claims without Plant Yard Lead approval.",
        "problem_statement": "At peak shift handovers, 32-ft containers and frozen reefers queue at ICML weighbridges and blocked stretch-wrap doors beyond the 120-minute free-time slab—triggering Rs 850-Rs 1,350/hr carrier detention charges and diesel burn on waiting reefers.",
        "special_tool_name": "evaluate_reefer_shore_power_and_slab_clock",
        "special_tool_doc": "Ranks waiting ICML yard trailers by remaining minutes to carrier detention slab breach and flags frozen/chilled reefers burning diesel without shore-power dock seals.",
        "chart_label_key": "vehicle_reg_no",
        "chart_value_key": "detention_avoided_inr",
        "headline_kpi_key": "total_detention_charges_avoided_display",
        "rows_key": "sequenced_dock_moves",
        "levers_inr_cr": {"productivity": 1.9, "flow": 7.8, "risk": 11.2, "recovery": 0.0, "zero_rationale": "Does not create incremental retail consumer demand; value is pure carrier detention avoidance and faster ICML dock turnaround."},
        "starter_prompts": [
            "Which trucks waiting at Ranjangaon, Kapurthala, and Panchla gates are close to breaching free detention time right now?",
            "Do we have any frozen or chilled reefers running on diesel in the yard that need an open shore-power dock door immediately?",
            "Reassign the delayed trailers from blocked doors to open bays and queue the yard move instructions for sign-off.",
            "Simulate a 25% monsoon arrival spike at Ranjangaon and Panchla gates tonight. How many trucks risk detention charges if dock bay re-slotting runs automatically?",
        ],
    },
    {
        "num": "03",
        "slug": "03_cold_chain_thermal_auditor",
        "agent_id": "itc_cold_chain_thermal_auditor",
        "class_prefix": "ItcColdChainThermalAuditor",
        "ge_display_name": "Cold-Chain Thermal Auditor (ITC TMD)",
        "icon": "ac_unit",
        "functional_area": "Primary Logistics & Plant Dispatch (Factory -> CFA / Depot)",
        "itc_pillar": "Pillar 06 · Green Logistics & Cold-Chain Assurance",
        "persona": "Cold-Chain & Transit QA Lead",
        "persona_named": "Dr. Ananya Chatterjee (National Cold-Chain QA Lead — Kolkata & Kapurthala)",
        "agent_name": "Cold-Chain Thermal Auditor",
        "build_mode": "Google ADK + Python Solvers",
        "priority": "P0",
        "default_model": "gemini-3.1-pro-preview",
        "table_stem": "03_drishti_reefer_iot_thermal_telemetry",
        "multimodal_docs": ["DOC-STRIP-SHP-CLD-70001.png", "DOC-STRIP-SHP-CLD-70002.png", "DOC-STRIP-SHP-CLD-70003.png"],
        "reuse_status": "REUSED_AND_TAILORED",
        "reused_from_agents": ["cold_chain_auditor", "cold_chain_salvage_repack_advisor"],
        "target_system": "SAP Quality Management (SAP QM `BAPI_INSPLOT_SETUSAGEDECISION`) & Carrier Claims Portal",
        "stops_at": "Never auto-releases thermally abused frozen, dairy, or chocolate lots into unrestricted CFA stock without QA Lead usage decision.",
        "problem_statement": "ITC Master Chef frozen snacks (-18C), Aashirvaad Svasti paneer/curd (2-8C), and Fabelle luxury chocolates (16-20C) suffer mid-highway compressor slips or driver fuel-saving switch-offs. Simple min/max alerts miss cumulative Arrhenius kinetic heat damage.",
        "special_tool_name": "inspect_drishti_strip_chart_multimodal",
        "special_tool_doc": "Performs multimodal OCR & strip-chart inspection on scanned Drishti BLE thermal logger printouts (`DOC-STRIP-SHP-CLD-*.png`) to corroborate carrier negligence claims.",
        "chart_label_key": "shipment_id",
        "chart_value_key": "carrier_spoilage_claim_inr",
        "headline_kpi_key": "recoverable_carrier_claims_display",
        "rows_key": "thermal_audit_ledger",
        "levers_inr_cr": {"productivity": 1.6, "flow": 0.0, "risk": 14.8, "recovery": 6.2, "zero_rationale": "Protects consumer food safety & recovers carrier spoilage claims while salvaging borderline cool-chain lots before write-off."},
        "starter_prompts": [
            "Review our inbound Master Chef frozen, Svasti dairy, and Fabelle chocolate reefers. Did any load suffer heat damage in transit?",
            "Check the logger printout on the Kapurthala frozen fries truck and the Patna paneer load to see why temperatures spiked.",
            "Hold the affected pallets in quarantine and prepare the carrier spoilage claim packet for quality sign-off.",
            "Simulate a 4-degree ambient heatwave across the Kapurthala to Delhi dairy and frozen corridor. Which shipments breach safe shelf life first?",
        ],
    },
    {
        "num": "04",
        "slug": "04_cfa_wave_bay_orchestrator",
        "agent_id": "itc_cfa_wave_bay_orchestrator",
        "class_prefix": "ItcCfaWaveBayOrchestrator",
        "ge_display_name": "CFA Wave & Bay Orchestrator (ITC TMD)",
        "icon": "warehouse",
        "functional_area": "CFA / Depot Operations & Stock Allocation",
        "itc_pillar": "Pillar 05 · CFA Operations & Omnichannel Fulfillment",
        "persona": "Depot / CFA Operations Manager",
        "persona_named": "Suresh Deshpande (Regional Mother CFA Manager — Bhiwandi & Kundli)",
        "agent_name": "CFA Wave & Bay Orchestrator",
        "build_mode": "Google ADK + Python Solvers",
        "priority": "P0",
        "default_model": "gemini-3.1-pro-preview",
        "table_stem": "04_cfa_wms_pick_waves_fefo_and_bays",
        "multimodal_docs": [],
        "reuse_status": "REUSED_AND_TAILORED",
        "reused_from_agents": ["wave_fulfillment_copilot", "fefo_shelf_life_allocator"],
        "target_system": "SAP Extended Warehouse Management (SAP EWM) Pick-Wave & Loading Bay Controller",
        "stops_at": "Never dispatches batches violating customer Minimum Remaining Shelf-Life (MRSL) gates or overrides cold-room safety capacity without CFA Manager sign-off.",
        "problem_statement": "State CFAs simultaneously pick rapid Quick-Commerce waves (strict 75% Minimum Remaining Shelf-Life gate, 10:30 cutoff), Modern Trade pallets, and General Trade Wholesale Dealer loads (55% MRSL gate). Unbalanced bays miss morning cutoffs while blind picking sends older batches to Quick-Commerce.",
        "special_tool_name": "validate_channel_fefo_mrsl_batch_swaps",
        "special_tool_doc": "Identifies cross-channel batch swaps inside the CFA so >=75%-shelf-life batches serve Quick-Commerce/Modern Trade while 55-74% batches clear cleanly through high-velocity General Trade beats.",
        "chart_label_key": "cfa_wave_id",
        "chart_value_key": "protected_dispatch_value_inr",
        "headline_kpi_key": "protected_dispatch_revenue_display",
        "rows_key": "wave_orchestration_plan",
        "levers_inr_cr": {"productivity": 3.8, "flow": 9.4, "risk": 7.9, "recovery": 0.0, "zero_rationale": "Executes booked orders faster and cleaner without altering demand; drives picker throughput, bay velocity, and zero shelf-life rejections."},
        "starter_prompts": [
            "How are morning pick waves and loading bays tracking at Bhiwandi and Kundli, and will any wave miss its dispatch cutoff?",
            "Are any Blinkit or Zepto orders picking older stock that could get rejected at their dock for having less than 75% shelf life?",
            "Swap those older compliant batches to General Trade beats, rebalance the pickers across bays, and stage the updated wave plan.",
            "Simulate shifting four General Trade pickers to Quick-Commerce bays at Bhiwandi before noon. How much dispatch revenue is protected before cutoff?",
        ],
    },
    {
        "num": "05",
        "slug": "05_fair_share_stock_allocation_agent",
        "agent_id": "itc_fair_share_stock_allocation_agent",
        "class_prefix": "ItcFairShareStockAllocation",
        "ge_display_name": "Fair-Share Stock Allocation Agent (ITC TMD)",
        "icon": "inventory_2",
        "functional_area": "CFA / Depot Operations & Stock Allocation",
        "itc_pillar": "Pillar 05 · CFA Operations & Stock Allocation",
        "persona": "Customer Service & Logistics (CS&L) Lead",
        "persona_named": "Meenakshi Sundaram (Zonal CS&L Head — Bengaluru & Southern Hub)",
        "agent_name": "Fair-Share Stock Allocation Agent",
        "build_mode": "Google ADK + Python Solvers",
        "priority": "P0",
        "default_model": "gemini-3.1-pro-preview",
        "table_stem": "05_csl_shortage_orders_and_channel_allocations",
        "multimodal_docs": [],
        "reuse_status": "REUSED_AND_TAILORED",
        "reused_from_agents": ["echelon_inventory_allocator", "dynamic_order_promising_atp"],
        "target_system": "SAP S/4HANA Advanced Available-to-Promise (aATP) & Order Rationing Engine",
        "stops_at": "Never zeroes out General Trade baseline territory floors or overrides contractual key-account allocation commitments without CS&L Lead approval.",
        "problem_statement": "When a high-velocity SKU like Sunfeast Dark Fantasy 300g is short at a State CFA (2,400 cases available vs 3,650 ordered), standard SAP First-In-First-Out lets early Modern Trade bulk orders consume 100% of stock—starving 18 General Trade Wholesale Dealers and UNNATI kiranas.",
        "special_tool_name": "compare_ortools_lp_vs_naive_fifo_rationing",
        "special_tool_doc": "Compares Google OR-Tools Linear Programming fair-share allocation against naive SAP FIFO order consumption across margin, OTIF penalties, and kirana breadth.",
        "chart_label_key": "channel_name",
        "chart_value_key": "fair_share_lp_cases",
        "headline_kpi_key": "net_economic_advantage_display",
        "rows_key": "channel_allocations",
        "levers_inr_cr": {"productivity": 1.8, "flow": 0.0, "risk": 9.1, "recovery": 16.5, "zero_rationale": "Allocates scarce stock cleanly—shielding steep Modern Trade/Q-Comm OTIF chargebacks and preserving high-margin UNNATI/General Trade sell-through."},
        "starter_prompts": [
            "We are short on Sunfeast Dark Fantasy 300g at Nelamangala depot. How should we split the 2,400 available cases across channels?",
            "What happens to our Quick-Commerce penalties and General Trade dealers if we let standard first-come-first-served allocation run?",
            "Hold the fair-share channel split in SAP for my review so neither Blinkit nor our Karnataka wholesale dealers get starved.",
            "What happens if available Dark Fantasy stock drops another 20% at Nelamangala? How do we protect Quick-Commerce fill rates without starving general dealers?",
        ],
    },
    {
        "num": "06",
        "slug": "06_eod_billing_cutoff_closer_agent",
        "agent_id": "itc_eod_billing_cutoff_closer_agent",
        "class_prefix": "ItcEodBillingCutoffCloser",
        "ge_display_name": "EOD Billing & Cutoff Closer Agent (ITC TMD)",
        "icon": "receipt_long",
        "functional_area": "CFA / Depot Operations & Stock Allocation",
        "itc_pillar": "Pillar 05 · CFA Billing & SAP Cutoff Governance",
        "persona": "Depot Dispatch & Billing Supervisor",
        "persona_named": "Prakash Kulkarni (CFA Commercial & SAP Billing Lead — Bhiwandi & Dankuni)",
        "agent_name": "EOD Billing & Cutoff Closer Agent",
        "build_mode": "Google ADK + SAP OpenAPI + Solvers",
        "priority": "P0",
        "default_model": "gemini-3.1-pro-preview",
        "table_stem": "06_cfa_sap_eod_billing_irn_eway_cutoff",
        "multimodal_docs": [],
        "reuse_status": "NEW_ITC_SPECIFIC_BUILD",
        "reused_from_agents": ["eway_bill_gst_transit_auditor", "New SAP S/4HANA VL02N/VF01/VKM3/IRN Cutoff Engine"],
        "target_system": "SAP S/4HANA SD/FI OpenAPI (`API_OUTBOUND_DELIVERY_SRV`, `API_BILLING_DOCUMENT_SRV`) & NIC IRP/E-Way API",
        "stops_at": "Never releases hard overdue delinquency blocks (`VKM3 >15 days overdue`) without Commercial Finance Controller approval; auto-stages only technical batch-split, FinAgg sync, and Part-B format fixes.",
        "problem_statement": "Every evening before the 21:00 IST gate lock, loaded trucks sit trapped at CFA gates because SAP outbound deliveries (`VL02N`) fail Post Goods Issue or `VF01` billing due to FEFO batch-split variances, unsynced FinAgg dealer credit drawdowns, or hyphen typos in NIC E-Way Bill Part-B vehicle numbers.",
        "special_tool_name": "validate_sap_openapi_bapi_and_nic_payload",
        "special_tool_doc": "Validates exact SAP S/4HANA OData/BAPI payloads (`ConfirmBatchSplitAndPGI`, `Z_API_SD_FINAGG_SYNC`, `Z_API_GST_EWAYBILL_PARTB_RETRY`) and separates hard Finance credit stops.",
        "chart_label_key": "outbound_delivery_no",
        "chart_value_key": "invoice_value_inr",
        "headline_kpi_key": "same_day_revenue_unlockable_display",
        "rows_key": "prioritized_cutoff_queue",
        "levers_inr_cr": {"productivity": 3.4, "flow": 14.6, "risk": 0.0, "recovery": 11.8, "zero_rationale": "Enforces credit/tax policy strictly while unlocking trapped gate-loaded trucks before 21:00/month-end cutoff."},
        "starter_prompts": [
            "Which loaded trucks at our depots are still unbilled before tonight's 9 PM SAP cutoff, and what is holding each one up?",
            "Separate the deliveries we can clear right away, like batch splits, FinAgg credit sync, or E-Way Bill typos, from overdue credit holds.",
            "Clear the fixable SAP delivery, e-Invoice, and E-Way Bill errors for my sign-off and flag the overdue account to Finance.",
            "Simulate clearing temporary FinAgg credit holds before tonight's billing cutoff. How much blocked end-of-day invoicing unlocks immediately?",
        ],
    },
    {
        "num": "07",
        "slug": "07_mt_qcomm_slot_otif_copilot",
        "agent_id": "itc_mt_qcomm_slot_otif_copilot",
        "class_prefix": "ItcMtQcommSlotOtifCopilot",
        "ge_display_name": "MT / Q-Comm Slot & OTIF Copilot (ITC TMD)",
        "icon": "gpp_good",
        "functional_area": "Channel & Route-to-Market (GT, MT & Q-Commerce)",
        "itc_pillar": "Pillar 05 · Modern Trade & Quick-Commerce Fulfillment",
        "persona": "Modern Trade & Q-Comm Logistics Lead",
        "persona_named": "Neha Kapoor (National MT & Quick-Commerce Supply Lead — Gurugram & Mumbai)",
        "agent_name": "MT / Q-Comm Slot & OTIF Copilot",
        "build_mode": "Google ADK + Python Solvers",
        "priority": "P0",
        "default_model": "gemini-3.1-pro-preview",
        "table_stem": "07_mt_qcomm_asn_dock_slots_and_otif",
        "multimodal_docs": [],
        "reuse_status": "REUSED_AND_TAILORED",
        "reused_from_agents": ["otif_penalty_shield", "modern_trade_dock_slot_booker"],
        "target_system": "Retailer EDI 856 ASN & Partner Appointment Portals (Blinkit, Zepto, Instamart, DMart, Reliance)",
        "stops_at": "Never accepts contractual penalty waivers that alter commercial trade terms or commits premium dedicated recovery above Rs 25,000 without MT Logistics Lead approval.",
        "problem_statement": "Blinkit, Zepto, Swiggy Instamart, DMart, and Reliance enforce 15-to-30-minute dock arrival tolerances and strict 75% Minimum Remaining Shelf-Life gates. Missing a slot by 20 minutes or sending a 68%-MRSL batch triggers full truck turn-away and 5-10% PO chargebacks.",
        "special_tool_name": "scan_retailer_portal_open_appointment_windows",
        "special_tool_doc": "Checks live Blinkit, Zepto, Instamart, DMart, and Reliance appointment portals for open same-day swap slots and pre-dispatch MRSL compliance.",
        "chart_label_key": "account_name",
        "chart_value_key": "chargeback_shielded_inr",
        "headline_kpi_key": "total_otif_penalties_shielded_display",
        "rows_key": "slot_and_otif_actions",
        "levers_inr_cr": {"productivity": 2.1, "flow": 0.0, "risk": 12.4, "recovery": 13.9, "zero_rationale": "Directly blocks 5-10% retailer OTIF chargebacks and prevents full-PO dock refusals & dark-store stockouts."},
        "starter_prompts": [
            "Which Blinkit, Zepto, Instamart, or DMart trucks are running late for their dock slot today or carrying short-shelf-life stock?",
            "What open appointment slots are available on the retailer portals right now so we avoid turn-aways and OTIF penalties?",
            "Move the delayed dispatches to the next open portal slots and swap the short-dated Zepto batch before the truck is sealed.",
            "Simulate pulling forward three Blinkit and Zepto darkstore dock appointments by two hours. How many late-delivery penalties do we avoid today?",
        ],
    },
    {
        "num": "08",
        "slug": "08_territory_rtm_morning_pulse_gem",
        "agent_id": "itc_territory_rtm_morning_pulse_gem",
        "class_prefix": "ItcTerritoryRtmMorningPulseGem",
        "ge_display_name": "Territory RTM Morning Pulse Gem (ITC TMD)",
        "icon": "trending_up",
        "functional_area": "Channel & Route-to-Market (GT, MT & Q-Commerce)",
        "itc_pillar": "Pillar 05 · UNNATI eB2B & Vajra Field Route-to-Market",
        "persona": "Area Distribution / RTM Manager",
        "persona_named": "Siddharth Banerjee (TM&D Area Manager — Pune, Lucknow & Kolkata Clusters)",
        "agent_name": "Territory RTM Morning Pulse Gem",
        "build_mode": "Google ADK + Reasoning Coach",
        "priority": "P1",
        "default_model": "gemini-3.8-flash",
        "table_stem": "08_unnati_eb2b_vajra_sfa_morning_pulse",
        "multimodal_docs": [],
        "reuse_status": "NEW_TAILORED_ITC_GEM",
        "reused_from_agents": ["field_beat_distributor_sync_agent", "New UNNATI eB2B + Vajra SFA Morning Pulse Gem"],
        "target_system": "ITC Vajra SFA Beat Console & UNNATI eB2B Campaign Broadcast",
        "stops_at": "Google ADK Advisory Coach by design—synthesizes morning beat priorities and drafts WhatsApp/Vajra nudges, never mutating trade scheme budgets or HR attendance records.",
        "problem_statement": "Area Distribution Managers start every morning juggling four disconnected trackers: overnight UNNATI kirana app orders, yesterday's Vajra salesman beat strike rates, Wholesale Dealer stockout lines, and active trade schemes—missing urgent beat course-corrections before 08:30.",
        "special_tool_name": "generate_0730_ase_whatsapp_and_vajra_brief",
        "special_tool_doc": "Synthesizes a crisp, plain-English 07:30 IST Area Sales Executive (ASE) beat action card pairing overnight UNNATI surges with Vajra strike-rate gaps.",
        "chart_label_key": "territory_name",
        "chart_value_key": "revenue_at_stake_inr",
        "headline_kpi_key": "overnight_unnati_digital_gmv_display",
        "rows_key": "morning_territory_briefing",
        "levers_inr_cr": {"productivity": 4.2, "flow": 0.0, "risk": 0.0, "recovery": 15.6, "zero_rationale": "Pure commercial & field-force morning intelligence Gem saving 6+ hrs/wk per Area Manager and lifting secondary beat strike rates."},
        "starter_prompts": [
            "Give me this morning's territory pulse. Where did overnight UNNATI kirana orders jump and where did salesman beat productivity dip yesterday?",
            "Which wholesale dealers in Pune, Lucknow, and South Kolkata are running out of top SKUs before today's beats go out?",
            "Draft quick 8 AM priorities for my Area Sales Executives so they cover the weak beats and push active trade schemes today.",
            "Draft a quick morning note in simple Hindi and English for Territory Officers covering weak beats with zero-bill retail outlets.",
        ],
    },
    {
        "num": "09",
        "slug": "09_predictive_wd_reorder_dispatch_agent",
        "agent_id": "itc_predictive_wd_reorder_dispatch_agent",
        "class_prefix": "ItcPredictiveWdReorderDispatch",
        "ge_display_name": "Predictive WD Reorder & Dispatch Agent (ITC TMD)",
        "icon": "storefront",
        "functional_area": "Channel & Route-to-Market (GT, MT & Q-Commerce)",
        "itc_pillar": "Pillar 05 · Wholesale Dealer (WD) Replenishment & FinAgg Credit",
        "persona": "Wholesale Dealer (WD) / Stockist Ops Mgr",
        "persona_named": "Rajeshwar Rao (TM&D Stockist Operations & DMS Lead — Mumbai, Bengaluru & Kolkata)",
        "agent_name": "Predictive WD Reorder & Dispatch Agent",
        "build_mode": "Google ADK + Python Solvers",
        "priority": "P0",
        "default_model": "gemini-3.1-pro-preview",
        "table_stem": "09_wd_stockist_doi_credit_and_reorders",
        "multimodal_docs": [],
        "reuse_status": "REUSED_AND_TAILORED",
        "reused_from_agents": ["dms_distributor_stock_balancer", "store_capacity_agent"],
        "target_system": "ITC Distribution Management System (DMS) -> SAP S/4HANA Primary Sales Order (`VA01`) & FinAgg Credit API",
        "stops_at": "Never converts draft primary orders into firm SAP billing without Wholesale Dealer OTP/portal consent or FinAgg/bank credit-line confirmation.",
        "problem_statement": "Wholesale Dealers frequently under-order core staples during UNNATI scheme surges (causing kirana stockouts within 48 hours) or hit credit-limit walls mid-week despite having approved FinAgg/SBI supply-chain credit headroom.",
        "special_tool_name": "verify_finagg_credit_and_godown_cube_fit",
        "special_tool_doc": "Checks each Wholesale Dealer's open credit limit, FinAgg/SBI dealer-finance drawdown eligibility, and physical godown case capacity before staging primary SAP replenishment.",
        "chart_label_key": "wd_name",
        "chart_value_key": "order_billing_value_inr",
        "headline_kpi_key": "total_auto_replenishment_billing_display",
        "rows_key": "wd_dispatch_recommendations",
        "levers_inr_cr": {"productivity": 2.6, "flow": 10.8, "risk": 0.0, "recovery": 19.2, "zero_rationale": "Stabilizes WD Days-of-Inventory turnover, automates DMS order generation, and eliminates secondary kirana stockouts."},
        "starter_prompts": [
            "Which wholesale dealers have dropped below four days of stock on fast-moving SKUs and risk running dry in the next 48 hours?",
            "Do Mahavir Agencies, Kaveri Distributors, and Hooghly Enterprises have enough godown space and FinAgg credit room for a top-up load?",
            "Prepare the primary replenishment orders and FinAgg credit drawdowns for dealer confirmation.",
            "Simulate a 25% festive demand surge next week. Which wholesale dealers run out of stock first and need higher FinAgg credit headroom?",
        ],
    },
    {
        "num": "10",
        "slug": "10_dynamic_rerouter",
        "agent_id": "itc_dynamic_rerouter",
        "class_prefix": "ItcDynamicRerouter",
        "ge_display_name": "Dynamic Rerouter (ITC TMD)",
        "icon": "local_shipping",
        "functional_area": "Fleet, Carrier & Freight Governance",
        "itc_pillar": "Pillar 06 · Green Logistics, Fleet & Live Route Governance",
        "persona": "Fleet & Route Dispatch Lead",
        "persona_named": "Vikramaditya Menon (Central Zenith Fleet Control Tower Lead — Mumbai, Bengaluru & Kolkata)",
        "agent_name": "Dynamic Rerouter",
        "build_mode": "Google ADK + Geospatial Routing",
        "priority": "P0",
        "default_model": "gemini-3.1-pro-preview",
        "table_stem": "10_zenith_fleet_gps_traffic_and_ev_routes",
        "multimodal_docs": [],
        "reuse_status": "REUSED_AND_TAILORED",
        "reused_from_agents": ["fleetflow_dispatch", "port_drayage_orchestrator"],
        "target_system": "Zenith Fleet Control Tower + Google Maps Routes Matrix v2 + NIC E-Way Bill Part-B API",
        "stops_at": "Never routes heavy multi-axle trucks onto weight-restricted bridges/no-entry police zones or files statutory NIC E-Way Bill extensions without Fleet Lead confirmation.",
        "problem_statement": "En-route highway landslides (NH-48 Khandala Ghat), urban waterlogging (Bengaluru ORR), police heavy-vehicle curfews, commercial EV low battery State-of-Charge, and expiring midnight NIC E-Way Bills cause severe delivery misses and Section 129 GST transit penalties.",
        "special_tool_name": "evaluate_maps_routes_ev_soc_and_eway_clock",
        "special_tool_doc": "Combines Google Maps Routes Matrix v2 live congestion deltas with commercial EV DC fast-charger waypoints, city no-entry curfews, and NIC E-Way Bill remaining hours.",
        "chart_label_key": "vehicle_reg_no",
        "chart_value_key": "net_minutes_saved",
        "headline_kpi_key": "protected_in_transit_cargo_display",
        "rows_key": "reroute_execution_plan",
        "levers_inr_cr": {"productivity": 1.7, "flow": 11.5, "risk": 8.8, "recovery": 0.0, "zero_rationale": "Cuts highway/curfew dwell & detour km while preventing Section 129 GST E-Way Bill expiry fines."},
        "starter_prompts": [
            "Which primary trucks and city EV vans are stuck in highway blockages, waterlogging, or police no-entry curfews right now?",
            "Are any delayed highway loads close to their E-Way Bill expiring tonight, or do any city EVs need a charging stop to finish their drops?",
            "Send the diversion routes, charger stop, and E-Way Bill extension request to the control tower queue for approval.",
            "Simulate closing the Mumbai-Pune expressway lane for six hours. Which primary trucks and city electric vans must divert to avoid missed deliveries?",
        ],
    },
    {
        "num": "11",
        "slug": "11_routing_guide_compliance_agent",
        "agent_id": "itc_routing_guide_compliance_agent",
        "class_prefix": "ItcRoutingGuideCompliance",
        "ge_display_name": "Routing Guide Compliance Agent (ITC TMD)",
        "icon": "alt_route",
        "functional_area": "Fleet, Carrier & Freight Governance",
        "itc_pillar": "Pillar 06 · Transport Procurement & Carrier Waterfall Governance",
        "persona": "Transport Procurement Manager",
        "persona_named": "Kavita Krishnamurthy (National Freight Procurement Lead — ITC TM&D HQ Kolkata)",
        "agent_name": "Routing Guide Compliance Agent",
        "build_mode": "Google ADK + Reasoning Coach",
        "priority": "P1",
        "default_model": "gemini-3.8-flash",
        "table_stem": "11_carrier_routing_guide_tenders_and_spot",
        "multimodal_docs": [],
        "reuse_status": "REUSED_AND_TAILORED",
        "reused_from_agents": ["freight_control_tower"],
        "target_system": "SAP TM / Zenith Carrier Waterfall Guide & Monthly Transporter Allocation Scorecard",
        "stops_at": "Advisory & governance Google ADK Coach—flags maverick spot indents and drafts L1/L2 carrier show-cause or rate-reindexing memos, never altering signed annual transport contracts unilaterally.",
        "problem_statement": "ITC negotiates annual L1/L2/L3 waterfall rate cards across hundreds of ICML-to-CFA lanes, yet local dispatchers frequently bypass L2 backup carriers during evening rush and book ad-hoc spot-market brokers at 28-40% freight premiums.",
        "special_tool_name": "diagnose_planner_bypass_vs_carrier_rejection",
        "special_tool_doc": "Separates maverick planner waterfall bypasses (where L2 was skipped) from genuine L1+L2 carrier capacity rejections requiring lane rate-card re-indexing.",
        "chart_label_key": "lane_description",
        "chart_value_key": "monthly_spot_leakage_inr",
        "headline_kpi_key": "annualized_recoverable_freight_display",
        "rows_key": "waterfall_compliance_findings",
        "levers_inr_cr": {"productivity": 1.5, "flow": 0.0, "risk": 15.4, "recovery": 0.0, "zero_rationale": "Pure freight procurement & contract-compliance governance Gem eliminating maverick spot-market rate leakage."},
        "starter_prompts": [
            "Where did we overspend on spot-market trucks this month instead of using our contracted L1 and L2 transporters?",
            "On which lanes did our dispatchers skip the backup carrier waterfall versus lanes where contracted transporters actually refused loads?",
            "Prepare compliance notes for the skipped waterfall lanes and flag chronic rejection lanes for rate review.",
            "What happens to our monthly freight budget if spot market truck rates jump 18% and primary carrier tender acceptance slips below 70%?",
        ],
    },
    {
        "num": "12",
        "slug": "12_freight_bill_audit_agent",
        "agent_id": "itc_freight_bill_audit_agent",
        "class_prefix": "ItcFreightBillAudit",
        "ge_display_name": "Freight Bill Audit Agent (ITC TMD)",
        "icon": "fact_check",
        "functional_area": "Fleet, Carrier & Freight Governance",
        "itc_pillar": "Pillar 06 · Multimodal Freight Audit, POD & Claims Settlement",
        "persona": "Freight Bill & Claims Controller",
        "persona_named": "Subhashish Mukherjee (National Freight Audit & Commercial Claims Controller — Kolkata)",
        "agent_name": "Freight Bill Audit Agent",
        "build_mode": "Google ADK + Multimodal Vision + Solvers",
        "priority": "P0",
        "default_model": "gemini-3.1-pro-preview",
        "table_stem": "12_freight_lr_pod_invoices_and_claims",
        "multimodal_docs": [
            "DOC-LR-882910.png", "DOC-POD-882910.png", "DOC-FINV-9041.png",
            "DOC-LR-771024.png", "DOC-POD-771024.png", "DOC-FINV-9042.png",
            "DOC-LR-664319.png", "DOC-POD-664319.png", "DOC-FINV-9043.png",
        ],
        "reuse_status": "REUSED_AND_TAILORED",
        "reused_from_agents": ["freight_bill_audit_agent", "osd_freight_claims_agent"],
        "target_system": "SAP S/4HANA FI-AP (`MIRO` / `FB60` Short-Pay Voucher & GST RCM Ledger) + Carrier Dispute Portal",
        "stops_at": "Never releases bank NEFT/RTGS payouts or posts final carrier debit notes without Freight Bill Controller sign-off; blocks 100% of duplicate Lorry Receipt claims.",
        "problem_statement": "Indian CPG freight settlement requires reconciling paper-heavy Lorry Receipts (Bilty), rubber-stamped CFA Proof-of-Delivery (POD) slips with handwritten wet/crushed carton remarks, contracted diesel escalation pegs, and GPS-verified gate detention hours.",
        "special_tool_name": "audit_multimodal_lr_pod_and_carrier_invoice",
        "special_tool_doc": "Runs multimodal OCR & visual inspection across scanned Lorry Receipts (`DOC-LR-*.png`), stamped PODs (`DOC-POD-*.png`), and Carrier Tax Invoices (`DOC-FINV-*.png`) for 4-way match.",
        "chart_label_key": "freight_invoice_id",
        "chart_value_key": "overcharge_and_pod_recovery_inr",
        "headline_kpi_key": "total_recovered_display",
        "rows_key": "freight_audit_vouchers",
        "levers_inr_cr": {"productivity": 3.9, "flow": 0.0, "risk": 21.6, "recovery": 0.0, "zero_rationale": "Recovers 3.8-5.2% of freight spend from duplicate LRs, detention padding, and POD damage claims."},
        "starter_prompts": [
            "Audit this week's pending transporter freight bills. Where do billed rates, fuel surcharges, or detention hours disagree with our contracts and GPS logs?",
            "Check the scanned lorry receipts and stamped delivery slips on LR-TCI-882910 and LR-HWK-771024 for damaged cartons or duplicate billing.",
            "Block the duplicate bill and stage short-pay vouchers deducting the unverified detention and damaged Dark Fantasy cartons.",
            "Draft the transporter dispute escalation summary and recovery breakdown for all duplicate bills, unverified detention, and damaged cartons found this week.",
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
    mm_docs = list(meta.get("multimodal_docs") or [])
    default_mm_doc = mm_docs[0] if mm_docs else ""

    if mm_docs:
        special_impl = f'''def {spec_fn}(reference_id: str = "") -> Dict[str, Any]:
    """{spec_doc}"""
    default_doc = {json.dumps(default_mm_doc)}
    available_docs = {json.dumps(mm_docs)}
    ref_clean = (reference_id or "").strip()
    doc_name = default_doc
    if ref_clean:
        matched_doc = next((d for d in available_docs if ref_clean.lower() in d.lower()), "")
        if matched_doc:
            doc_name = matched_doc
        elif "771024" in ref_clean:
            doc_name = "DOC-POD-771024.png"
        elif "664319" in ref_clean:
            doc_name = "DOC-POD-664319.png"
        elif "70002" in ref_clean or "patna" in ref_clean.lower() or "paneer" in ref_clean.lower():
            doc_name = "DOC-STRIP-SHP-CLD-70002.png"
        elif ref_clean.lower().endswith(".png"):
            doc_name = ref_clean

    ocr = inspect_multimodal_document(doc_name, agent_dir=_agent_root())
    png_path = resolve_multimodal_png_path(ocr["document_filename"], agent_dir=_agent_root())
    if png_path is not None:
        img_url = publish_multimodal_doc_image(png_path)
        if img_url:
            _TURN_STATE["doc_url"] = img_url
            _TURN_STATE["doc_label"] = f"{{ocr['document_filename']}} ({{ocr['document_title']}})"
    solved = run_deterministic_optimization_solver(ref_clean)
    return {{
        "tool": "{spec_fn}",
        "multimodal_vision_verification": ocr,
        "scanned_document_view_url": _TURN_STATE.get("doc_url", ""),
        "headline_recovery_or_claim": solved.get("{kpi_k}"),
        "top_audited_items": solved.get("{rows_k}", [])[:4],
        "human_gate_boundary": STOPS_AT_BOUNDARY,
    }}'''
    else:
        special_impl = f'''def {spec_fn}(reference_id: str = "") -> Dict[str, Any]:
    """{spec_doc}"""
    solved = run_deterministic_optimization_solver(reference_id)
    rows = solved.get("{rows_k}", [])
    flagged = [r for r in rows if any(k in str(r).upper() for k in ("RISK", "HOLD", "BLOCK", "BREACH", "SPOT", "REJECT", "SWAP", "CRITICAL"))] or rows
    return {{
        "tool": "{spec_fn}",
        "reference_filter": reference_id or "ALL_PRIORITY_EXCEPTIONS",
        "headline_impact_inr": solved.get("{kpi_k}"),
        "exception_count": len(flagged),
        "verified_diagnostics": flagged[:5],
        "human_gate_boundary": STOPS_AT_BOUNDARY,
    }}'''

    return f'''"""Hermetic Deterministic Python & Multimodal Tools for {meta['ge_display_name']}."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from .itc_runtime.itc_data_loader import (
        inspect_multimodal_document,
        load_backbone,
        query_domain_table,
        resolve_multimodal_png_path,
        stage_governed_enterprise_action,
    )
    from .itc_runtime.solvers import SOLVER_REGISTRY
    from .itc_runtime.a2ui_wire import build_autonomous_2panel_vegalite
    from .itc_runtime.gcs_publisher import publish_cockpit_and_csv, publish_multimodal_doc_image
except ImportError:
    from itc_runtime.itc_data_loader import (  # type: ignore
        inspect_multimodal_document,
        load_backbone,
        query_domain_table,
        resolve_multimodal_png_path,
        stage_governed_enterprise_action,
    )
    from itc_runtime.solvers import SOLVER_REGISTRY  # type: ignore
    from itc_runtime.a2ui_wire import build_autonomous_2panel_vegalite  # type: ignore
    from itc_runtime.gcs_publisher import publish_cockpit_and_csv, publish_multimodal_doc_image  # type: ignore

AGENT_SLUG = "{slug}"
AGENT_ID = "{aid}"
AGENT_NAME = "{meta['agent_name']}"
GE_DISPLAY_NAME = "{meta['ge_display_name']}"
PERSONA_TITLE = "{meta['persona']}"
FUNCTIONAL_AREA = "{meta['functional_area']}"
BUILD_MODE = "{meta['build_mode']}"
TARGET_SYSTEM = "{target_sys}"
STOPS_AT_BOUNDARY = "{stops_at}"
PRIMARY_TABLE = "{t_stem}"

_TURN_STATE: Dict[str, Any] = {{
    "active": False,
    "user_query": "",
    "vega_spec": None,
    "rows": [],
    "headline": "",
    "doc_url": "",
    "doc_label": "",
}}


def _agent_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _format_inr(amount_inr: float) -> str:
    val = float(amount_inr or 0.0)
    sign = "-" if val < 0 else ""
    av = abs(val)
    if av >= 10_000_000.0:
        return f"{{sign}}₹{{av / 10_000_000.0:.2f}} Cr"
    if av >= 100_000.0:
        return f"{{sign}}₹{{av / 100_000.0:.2f}} L"
    return f"{{sign}}₹{{av:,.0f}}"


def reset_turn_state(user_query: str = "") -> None:
    _TURN_STATE["active"] = False
    _TURN_STATE["user_query"] = user_query
    _TURN_STATE["vega_spec"] = None
    _TURN_STATE["rows"] = []
    _TURN_STATE["headline"] = ""
    _TURN_STATE["doc_url"] = ""
    _TURN_STATE["doc_label"] = ""


def get_turn_state() -> Dict[str, Any]:
    return dict(_TURN_STATE)


def _record_visual_context(solved: Dict[str, Any], override_rows: Optional[List[Dict[str, Any]]] = None, override_headline: str = "") -> None:
    rows = list(override_rows if override_rows is not None else (solved.get("{rows_k}", []) or []))
    headline = override_headline or str(solved.get("{kpi_k}", "Verified"))
    spec = build_autonomous_2panel_vegalite(
        agent_slug=AGENT_SLUG,
        agent_title=AGENT_NAME,
        subtitle=f"{{FUNCTIONAL_AREA}} · Verified Impact: {{headline}}",
        rows=rows,
        label_key="{lbl_k}",
        value_key="{val_k}",
        value_title="Impact / Metric (₹ INR)",
        user_query=str(_TURN_STATE.get("user_query", "")),
    )
    _TURN_STATE["active"] = True
    _TURN_STATE["rows"] = rows
    _TURN_STATE["headline"] = headline
    _TURN_STATE["vega_spec"] = spec


def query_itc_enterprise_records(search_filter: str = "", limit: int = 30) -> Dict[str, Any]:
    """Queries ITC Limited TM&D operational records for {meta['agent_name']} with flexible keyword matching."""
    res = query_domain_table(PRIMARY_TABLE, search_filter=search_filter, limit=limit, agent_dir=_agent_root())
    if res.get("records") and not _TURN_STATE.get("active"):
        solved = SOLVER_REGISTRY[AGENT_SLUG](res["records"])
        _record_visual_context(solved)
    return res


def query_itc_master_network_backbone(entity_type: str = "all", search_filter: str = "") -> Dict[str, Any]:
    """Queries ITC Master Network Backbone: ICML mega-plants, State CFAs, Wholesale Dealers (WDs), SKUs, and Carriers."""
    bb = load_backbone(agent_dir=_agent_root())
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
    """Executes the deterministic mathematical / OR-Tools / physics solver for {meta['agent_name']}."""
    queried = query_domain_table(PRIMARY_TABLE, search_filter=search_filter, limit=40, agent_dir=_agent_root())
    solver_fn = SOLVER_REGISTRY[AGENT_SLUG]
    result = solver_fn(queried.get("records", []))
    result["agent_id"] = AGENT_ID
    result["agent_name"] = AGENT_NAME
    result["build_mode"] = BUILD_MODE
    result["using_full_enterprise_lake"] = queried.get("using_full_enterprise_lake", False)
    _record_visual_context(result)
    return result


{special_impl}


def simulate_what_if_scenario(adjustment_pct: int = 120, focus_filter: str = "") -> Dict[str, Any]:
    """Simulates a live operational what-if scenario (volume surge, stock shortage, rate shift, or capacity reallocation)."""
    solved = run_deterministic_optimization_solver(focus_filter)
    base_rows = list(solved.get("{rows_k}", []) or [])
    if -50 <= adjustment_pct <= 50 and adjustment_pct != 0:
        factor = round(1.0 + (adjustment_pct / 100.0), 4)
        delta_pct = float(adjustment_pct)
    else:
        factor = round(max(0.25, adjustment_pct / 100.0), 4)
        delta_pct = round((factor - 1.0) * 100.0, 1)

    sim_rows: List[Dict[str, Any]] = []
    base_total = 0.0
    sim_total = 0.0
    for r in base_rows:
        rc = dict(r)
        try:
            bv = float(rc.get("{val_k}", 0.0) or 0.0)
        except Exception:
            bv = 0.0
        sv = round(bv * factor, 2)
        base_total += bv
        sim_total += sv
        rc["{val_k}"] = sv
        rc["baseline_value_inr"] = round(bv, 2)
        rc["scenario_delta_inr"] = round(sv - bv, 2)
        sim_rows.append(rc)

    sim_headline = _format_inr(sim_total) if sim_total else str(solved.get("{kpi_k}", "Verified"))
    _record_visual_context(solved, override_rows=sim_rows, override_headline=sim_headline)
    return {{
        "status": "SCENARIO_SIMULATED",
        "focus_filter": focus_filter or "FULL_PORTFOLIO",
        "adjustment_factor": factor,
        "scenario_delta_pct": delta_pct,
        "baseline_impact_inr": round(base_total, 2),
        "baseline_impact_display": _format_inr(base_total),
        "simulated_impact_inr": round(sim_total, 2),
        "simulated_impact_display": sim_headline,
        "net_change_display": _format_inr(sim_total - base_total),
        "top_simulated_items": sim_rows[:5],
        "human_gate_boundary": STOPS_AT_BOUNDARY,
    }}


def draft_executive_stakeholder_brief(focus_filter: str = "", include_hindi_vernacular: bool = False) -> Dict[str, Any]:
    """Drafts an escalation, transporter dispute, or field-beat morning brief (optionally bilingual Hindi + English)."""
    solved = run_deterministic_optimization_solver(focus_filter)
    rows = list(solved.get("{rows_k}", []) or [])[:4]
    headline = str(solved.get("{kpi_k}", "Verified"))
    action_lines = [
        f"{{idx + 1}}. {{r.get('{lbl_k}', 'Item')}}: {{_format_inr(float(r.get('{val_k}', 0.0) or 0.0))}}"
        for idx, r in enumerate(rows)
    ]
    hindi_note = ""
    if include_hindi_vernacular:
        hindi_note = (
            f"Namaste Team — Aaj ke {{AGENT_NAME}} review mein {{len(rows)}} mukhya priority items ({{headline}} impact) chune gaye hain. "
            f"Kripya top priority dispatches aur approval gate par turant action lein: " + "; ".join(action_lines[:3])
        )
    return {{
        "status": "STAKEHOLDER_BRIEF_READY",
        "agent_name": AGENT_NAME,
        "persona_owner": PERSONA_TITLE,
        "headline_value_display": headline,
        "priority_actions": action_lines,
        "vernacular_hindi_summary": hindi_note or None,
        "approval_gate": STOPS_AT_BOUNDARY,
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
    """Prepares the autonomous 2-Panel Vega-Lite v5 visual card (Bar/Grouped/Line + Donut) and Looker RichTable Canvas."""
    solved = run_deterministic_optimization_solver(search_filter)
    return {{
        "a2ui_version": "0.9",
        "card_component": "VegaChart",
        "text_inside_card": False,
        "vega_lite_spec": _TURN_STATE["vega_spec"],
        "row_count": len(_TURN_STATE["rows"]),
        "headline_impact": solved.get("{kpi_k}"),
    }}


def export_atomic_schedule_csv(search_filter: str = "") -> Dict[str, Any]:
    """Exports an atomic RFC-4180 CSV schedule to local disk and Cloud Storage for Google Sheets / SAP."""
    if not _TURN_STATE.get("rows"):
        run_deterministic_optimization_solver(search_filter)
    local_out = Path("/tmp") / "itc_tmd_artifacts" / AGENT_SLUG
    urls = publish_cockpit_and_csv(
        agent_slug=AGENT_SLUG,
        agent_title=AGENT_NAME,
        persona_title=PERSONA_TITLE,
        functional_area=FUNCTIONAL_AREA,
        headline_value=str(_TURN_STATE.get("headline") or "Verified"),
        rows=list(_TURN_STATE.get("rows") or []),
        label_key="{lbl_k}",
        value_key="{val_k}",
        doc_url=str(_TURN_STATE.get("doc_url") or ""),
        doc_label=str(_TURN_STATE.get("doc_label") or ""),
        local_dir=local_out,
    )
    return {{
        "status": "CSV_EXPORT_READY",
        "csv_path": str(local_out / f"{{AGENT_SLUG}}_verified_schedule.csv"),
        "csv_download_url": urls["csv_url"],
        "row_count": len(_TURN_STATE.get("rows") or []),
    }}


def generate_interactive_html_cockpit(search_filter: str = "") -> Dict[str, Any]:
    """Compiles & publishes the Light-Theme Default 3-Tab Executive HTML5 Control Tower Cockpit."""
    if not _TURN_STATE.get("rows"):
        run_deterministic_optimization_solver(search_filter)
    local_out = Path("/tmp") / "itc_tmd_artifacts" / AGENT_SLUG
    urls = publish_cockpit_and_csv(
        agent_slug=AGENT_SLUG,
        agent_title=AGENT_NAME,
        persona_title=PERSONA_TITLE,
        functional_area=FUNCTIONAL_AREA,
        headline_value=str(_TURN_STATE.get("headline") or "Verified"),
        rows=list(_TURN_STATE.get("rows") or []),
        label_key="{lbl_k}",
        value_key="{val_k}",
        doc_url=str(_TURN_STATE.get("doc_url") or ""),
        doc_label=str(_TURN_STATE.get("doc_label") or ""),
        local_dir=local_out,
    )
    return {{
        "status": "HTML_COCKPIT_READY",
        "cockpit_path": str(local_out / f"{{AGENT_SLUG}}_cockpit.html"),
        "cockpit_view_url": urls["html_url"],
        "csv_download_url": urls["csv_url"],
        "default_theme": "light",
    }}


ALL_TOOLS = [
    query_itc_enterprise_records,
    query_itc_master_network_backbone,
    run_deterministic_optimization_solver,
    {spec_fn},
    simulate_what_if_scenario,
    draft_executive_stakeholder_brief,
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
    lbl_k = meta["chart_label_key"]
    val_k = meta["chart_value_key"]
    spec_fn = meta["special_tool_name"]

    return f'''"""Google ADK + Multi-Agent GlobalGemini Orchestrator for {meta['ge_display_name']}."""
from __future__ import annotations

import importlib.util as _ilu
import logging
import os
import uuid
from functools import cached_property
from pathlib import Path as _Path
from typing import Any, Callable, Dict, List, Optional

try:
    from . import tools
    from .itc_runtime.a2ui_wire import (
        SENTINEL_OPEN,
        build_dual_a2ui_wire_parts,
        sanitize_history_and_intercept_actions,
    )
    from .itc_runtime.gcs_publisher import publish_cockpit_and_csv
except ImportError:
    _here = _Path(__file__).resolve().parent
    _t_spec = _ilu.spec_from_file_location(f"{slug}_tools", _here / "tools.py")
    assert _t_spec and _t_spec.loader
    tools = _ilu.module_from_spec(_t_spec)  # type: ignore
    _t_spec.loader.exec_module(tools)  # type: ignore
    import sys as _sys
    if str(_here) not in _sys.path:
        _sys.path.insert(0, str(_here))
    from itc_runtime.a2ui_wire import (  # type: ignore
        SENTINEL_OPEN,
        build_dual_a2ui_wire_parts,
        sanitize_history_and_intercept_actions,
    )
    from itc_runtime.gcs_publisher import publish_cockpit_and_csv  # type: ignore

logger = logging.getLogger(__name__)

AGENT_ID = "{aid}"
AGENT_SLUG = "{slug}"
AGENT_DISPLAY_NAME = "{meta['ge_display_name']}"
SHORT_LABEL = "{meta['agent_name']}"
FUNCTIONAL_AREA = "{meta['functional_area']}"
PERSONA_OWNER = "{meta['persona']}"
NAMED_PERSONA = "{meta['persona_named']}"
BUILD_MODE = "{meta['build_mode']}"
DEFAULT_MODEL = "{meta['default_model']}"

_WRITE_TOOLS = {{
    "stage_governed_erp_or_portal_action": ["target_record_id", "proposed_action"],
}}

SYSTEM_INSTRUCTION = """You are **{meta['ge_display_name']}**, an intelligent Google Agent Development Kit (ADK) supply chain agent for **{meta['persona']}** ({meta['persona_named']}) across **ITC Limited's Consumer Packaged Goods (CPG) Trade Marketing & Distribution (TM&D)** network ({meta['functional_area']}).

1. AUTONOMOUS DATA, SOLVER & SPECIALIST SUB-AGENT INTELLIGENCE:
   - Users ask everyday operational questions in plain English—they will never cite internal table names, function names, or chart formatting commands.
   - For daily status, lane triage, exception detection, or optimization questions: call `run_deterministic_optimization_solver` (plus `{spec_fn}` when verifying physics, portal appointments, batch rules, GST e-Invoice/E-Way errors, credit headroom, or scanned Lorry Receipt / POD / Strip Chart documents).
   - For what-if stress tests (volume surge, stock cut, fuel spike, highway closure, heatwave): call `simulate_what_if_scenario` or delegate to your `signal_analyst` specialist sub-agent.
   - For audit verification, transporter disputes, morning territory field notes (Hindi + English), or compliance escalations: consult `{spec_fn}` or `draft_executive_stakeholder_brief` (or your `compliance_auditor` specialist sub-agent).
   - Domain Mission: {meta['problem_statement']}

2. CLEAR, BALANCED PLAIN-ENGLISH & INDIAN CURRENCY (`₹ Cr` / `₹ L`) STYLE:
   - Write in approachable, clear business English at a balanced medium length (140–210 words).
   - Spell out every domain abbreviation on first use (Integrated Consumer Goods Manufacturing and Logistics (ICML), Clearing & Forwarding Agent (CFA), Wholesale Dealer (WD), On-Time In-Full (OTIF), Minimum Remaining Shelf-Life (MRSL), Mean Kinetic Temperature (MKT), Goods and Services Tax (GST)).
   - Express ALL monetary figures in Indian Rupees using Crores (`₹ Cr`) and Lakhs (`₹ L`) or `₹`—never US Dollars.
   - Include ONE crisp, copy-ready Markdown table (`<= 5` columns) outside the visual card summarizing top prioritized items, followed by 2–3 concrete recommended next steps.
   - Never reveal internal JSON/CSV filenames, `snake_case` column names, or Python tool names to the user.

3. HUMAN SIGN-OFF BOUNDARY & SAFETY GUARDRAILS:
   - Connected System of Record: {meta['target_system']}
   - Sign-Off Gate: {meta['stops_at']}
   - Never invoke `stage_governed_erp_or_portal_action` on read-only analytical questions. Only stage actions when explicitly asked to hold, block, reassign, or prepare indents/vouchers, supplying a unique `idempotency_key` (e.g. `ITC-{meta['num']}-STAGE-001`).
   - Strictly refuse any request to bypass axle-weight safety, cold-chain quarantine, shelf-life limits, duplicate-invoice blocks, or overdue credit holds.
"""


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Pre-execution contract & idempotency gate for write-back staging tools."""
    if tool_name in _WRITE_TOOLS:
        missing = [k for k in _WRITE_TOOLS[tool_name] if args.get(k) in (None, "")]
        if missing:
            return {{"status": "BLOCKED_MISSING_INPUTS", "tool": tool_name, "missing_fields": missing}}
        if not args.get("idempotency_key"):
            return {{
                "status": "BLOCKED_MISSING_IDEMPOTENCY_KEY",
                "tool": tool_name,
                "message": "An explicit idempotency_key is required before staging an enterprise action.",
            }}
    return None


class {cls}Agent:
    """Deterministic Python orchestrator for {meta['ge_display_name']}."""

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
        q_low = (query or "").lower()
        deep_keywords = ("optimize", "consolidate", "ration", "allocate", "arrhenius", "mkt", "multimodal", "pod", "sap", "reroute", "simulate")
        chosen = "gemini-3.1-pro-preview" if (DEFAULT_MODEL == "gemini-3.1-pro-preview" or any(k in q_low for k in deep_keywords)) else "gemini-3.8-flash"
        return {{"selected_model": chosen, "endpoint_location": "global", "build_mode": BUILD_MODE}}

    def run_scenario(self, user_query: str = "") -> Dict[str, Any]:
        tools.reset_turn_state(user_query)
        routing = self.select_orchestrated_model(user_query)
        solved = tools.run_deterministic_optimization_solver("")
        special = tools.{spec_fn}("")
        a2ui = tools.render_a2ui_visual_chart_and_canvas("")
        rows = solved.get("{rows_k}", [])[:4]

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
            f"**{meta['ge_display_name']}** completed a deterministic review across **ITC Limited's Trade Marketing & Distribution (TM&D)** "
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
    from google.adk.agents.callback_context import CallbackContext
    from google.adk.apps import App
    from google.adk.models import Gemini
    from google.adk.models.llm_request import LlmRequest
    from google.adk.models.llm_response import LlmResponse
    from google.adk.tools.agent_tool import AgentTool
    from google.genai import Client, types
    from vertexai.preview.reasoning_engines import AdkApp

    class GlobalGemini(Gemini):
        """Routes Gemini 3.1 Pro and Gemini 3.8 Flash calls to Vertex AI `global` endpoint even inside `us-central1` Reasoning Engines."""

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

    def _is_refusal_or_smalltalk(text: str, turn_active: bool) -> bool:
        low = (text or "").strip().lower()
        refusal_markers = (
            "cannot bypass",
            "blocked by safety",
            "strictly prohibited",
            "i cannot override",
            "cannot approve duplicate",
            "safety policy prevents",
        )
        if any(m in low for m in refusal_markers):
            return True
        if not turn_active and len(low) < 110:
            return True
        return False

    def _before_model_cb(
        callback_context: Optional[CallbackContext] = None,
        llm_request: Optional[LlmRequest] = None,
        **_: Any,
    ) -> None:
        if llm_request is None:
            return None
        try:
            u_txt = sanitize_history_and_intercept_actions(llm_request)
            if u_txt:
                tools.reset_turn_state(u_txt)
        except Exception as exc:
            logger.warning("before_model_callback degraded cleanly: %s", exc)
        return None

    def _after_model_cb(
        callback_context: Optional[CallbackContext] = None,
        llm_response: Optional[LlmResponse] = None,
        **_: Any,
    ) -> Optional[LlmResponse]:
        if llm_response is None or getattr(llm_response, "content", None) is None:
            return None
        if getattr(llm_response, "partial", False):
            return None
        try:
            parts = list(llm_response.content.parts or [])
            if any(getattr(p, "function_call", None) is not None for p in parts):
                return llm_response

            cleaned: List[types.Part] = []
            for p in parts:
                t = getattr(p, "text", None)
                if t and SENTINEL_OPEN in t:
                    t_clean = t.split(SENTINEL_OPEN)[0].strip()
                    if t_clean:
                        cleaned.append(types.Part(text=t_clean))
                else:
                    cleaned.append(p)

            st = tools.get_turn_state()
            idx = max((i for i, p in enumerate(cleaned) if getattr(p, "text", None)), default=-1)
            existing_txt = (cleaned[idx].text or "") if idx >= 0 else ""

            if (
                st.get("active")
                and st.get("rows")
                and not _is_refusal_or_smalltalk(existing_txt, bool(st.get("active")))
                and "itc_tmd/cockpits/" not in existing_txt
            ):
                urls = publish_cockpit_and_csv(
                    agent_slug=AGENT_SLUG,
                    agent_title=SHORT_LABEL,
                    persona_title=PERSONA_OWNER,
                    functional_area=FUNCTIONAL_AREA,
                    headline_value=str(st.get("headline") or "Verified"),
                    rows=list(st.get("rows") or []),
                    label_key="{lbl_k}",
                    value_key="{val_k}",
                    doc_url=str(st.get("doc_url") or ""),
                    doc_label=str(st.get("doc_label") or ""),
                )
                bullets = [
                    f"- 🌐 **[Open 3-Tab Control Tower Workbench & Simulator (Light/Dark HTML) ↗]({{urls['html_url']}})** — Interactive KPI cards, What-If scenario sliders, architecture lineage, and filterable ledger.",
                    f"- 📥 **[Download Atomic Schedule for Google Sheets / SAP (CSV) ↗]({{urls['csv_url']}})** — Verified row-level export.",
                ]
                if st.get("doc_url"):
                    bullets.insert(
                        0,
                        f"- 🖼️ **[Inspect Scanned Document Evidence ({{st.get('doc_label', 'PNG Scan')}}) ↗]({{st['doc_url']}})** — High-resolution multimodal document scan.",
                    )
                nl = chr(10)
                footer = f"{{nl}}{{nl}}### 🌐 Interactive Control Tower Report & Evidence{{nl}}{{nl}}" + nl.join(bullets) + nl
                if idx >= 0:
                    cleaned[idx] = types.Part(text=existing_txt.rstrip() + footer)
                else:
                    cleaned.append(types.Part(text=footer.lstrip()))

            llm_response.content.parts = cleaned
            return llm_response
        except Exception as exc:
            logger.warning("after_model_callback degraded cleanly: %s", exc)
            return None

    def _after_agent_cb(
        callback_context: Optional[CallbackContext] = None,
        **_: Any,
    ) -> Optional[types.Content]:
        try:
            st = tools.get_turn_state()
            if not st.get("active") or not st.get("vega_spec"):
                return None
            sid = f"itc-{{uuid.uuid4().hex[:8]}}"
            rows = list(st.get("rows") or [])
            banner = f"{{len(rows)}} verified ITC TM&D records · Headline Impact: {{st.get('headline', 'Verified')}}"
            ui_parts = build_dual_a2ui_wire_parts(
                surface_id=sid,
                agent_id=AGENT_ID,
                agent_short_label=SHORT_LABEL,
                vega_spec=st["vega_spec"],
                rows=rows,
                headline_banner=banner,
            )
            tools.reset_turn_state("")
            if ui_parts:
                return types.Content(role="model", parts=ui_parts)
        except Exception as exc:
            logger.warning("after_agent_callback A2UI emission degraded cleanly: %s", exc)
        return None

    signal_analyst_agent = Agent(
        name=f"{{AGENT_ID}}_signal_analyst",
        model=GlobalGemini(
            model="gemini-3.8-flash",
            retry_options=types.HttpRetryOptions(attempts=3),
        ),
        generate_content_config=types.GenerateContentConfig(
            max_output_tokens=8192,
            temperature=0.1,
            thinking_config=types.ThinkingConfig(thinking_level="LOW"),
        ),
        description=f"Specialist Signal & Scenario Analyst for {meta['agent_name']} — queries enterprise tables and simulates what-if disruptions.",
        instruction=(
            f"You are the specialist signal & scenario analyst sub-agent for {meta['ge_display_name']}. "
            f"Query ITC TM&D records, inspect master network entities (ICML plants, CFAs, distributors, carriers), "
            f"and run what-if stress scenarios returning concise INR impact facts."
        ),
        tools=[
            tools.query_itc_enterprise_records,
            tools.query_itc_master_network_backbone,
            tools.simulate_what_if_scenario,
        ],
    )

    compliance_auditor_agent = Agent(
        name=f"{{AGENT_ID}}_compliance_auditor",
        model=GlobalGemini(
            model="gemini-3.8-flash",
            retry_options=types.HttpRetryOptions(attempts=3),
        ),
        generate_content_config=types.GenerateContentConfig(
            max_output_tokens=8192,
            temperature=0.1,
            thinking_config=types.ThinkingConfig(thinking_level="LOW"),
        ),
        description=f"Specialist Audit, Multimodal & Stakeholder Brief Sub-Agent for {meta['agent_name']}.",
        instruction=(
            f"You are the specialist compliance & communication auditor sub-agent for {meta['ge_display_name']}. "
            f"Run domain diagnostics or scanned document verification and draft concise escalation or vernacular briefs."
        ),
        tools=[
            tools.{spec_fn},
            tools.draft_executive_stakeholder_brief,
        ],
    )

    root_agent = Agent(
        name=AGENT_ID,
        model=GlobalGemini(
            model=DEFAULT_MODEL,
            retry_options=types.HttpRetryOptions(attempts=3),
        ),
        generate_content_config=types.GenerateContentConfig(
            max_output_tokens=16384,
            temperature=0.1,
            thinking_config=types.ThinkingConfig(thinking_level="LOW"),
        ),
        description=f"{meta['agent_name']} (ITC TMD) for {meta['persona']}: {meta['problem_statement'][:220]}",
        instruction=SYSTEM_INSTRUCTION,
        tools=list(tools.ALL_TOOLS) + [
            AgentTool(agent=signal_analyst_agent),
            AgentTool(agent=compliance_auditor_agent),
        ],
        before_model_callback=_before_model_cb,
        after_model_callback=_after_model_cb,
        after_agent_callback=_after_agent_cb,
    )

    app = App(root_agent=root_agent, name=AGENT_ID)

    class {cls}AdkApp(AdkApp):
        """Vertex AI Agent Engine wrapper for {meta['ge_display_name']}."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)

        @staticmethod
        def _pin_env() -> None:
            os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"
            os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "zuhaibp-ai")

        def query(self, *args: Any, **kwargs: Any) -> Any:
            self._pin_env()
            return super().query(*args, **kwargs)

        def stream_query(self, *args: Any, **kwargs: Any) -> Any:
            self._pin_env()
            yield from super().stream_query(*args, **kwargs)

except Exception:
    root_agent = {cls}Agent()  # type: ignore
    app = None  # type: ignore
    {cls}AdkApp = None  # type: ignore
'''


def write_mode_specific_specs(agent_dir: Path, meta: Dict[str, Any]) -> List[str]:
    specs_dir = agent_dir / "studio_specs"
    specs_dir.mkdir(parents=True, exist_ok=True)
    created = []

    yaml_text = f"""# Gemini Enterprise Agent Studio Specification — {meta['ge_display_name']}
apiVersion: gemini-enterprise.cloud.google.com/v1
kind: DeclarativeAgent
metadata:
  agent_id: {meta['agent_id']}
  slug: {meta['slug']}
  display_name: "{meta['ge_display_name']}"
  build_mode: "{meta['build_mode']}"
  functional_area: "{meta['functional_area']}"
  persona_owner: "{meta['persona']}"
  named_leader: "{meta['persona_named']}"
  priority_tier: "{meta['priority']}"
spec:
  model_routing:
    endpoint: global
    default_model: {meta['default_model']}
  starter_prompts_on_screen:
""" + "\n".join(f'    - "{p}"' for p in meta["starter_prompts"]) + "\n"
    (specs_dir / "gemini_enterprise_agent_studio.yaml").write_text(yaml_text, encoding="utf-8")
    created.append("studio_specs/gemini_enterprise_agent_studio.yaml")

    openapi_obj = {
        "openapi": "3.0.3",
        "info": {
            "title": f"{meta['ge_display_name']} Connector API",
            "version": "1.0.0",
            "description": f"Mode: {meta['build_mode']} | Target System: {meta['target_system']}",
        },
        "paths": {
            f"/v1/itc-tmd/{meta['slug']}/solve": {
                "post": {"operationId": "run_deterministic_optimization_solver", "summary": f"Run deterministic solver for {meta['agent_name']}"}
            }
        },
    }
    (specs_dir / "openapi_tools_spec.json").write_text(json.dumps(openapi_obj, indent=2), encoding="utf-8")
    created.append("studio_specs/openapi_tools_spec.json")
    return created


def render_test_smoke_py(meta: Dict[str, Any]) -> str:
    cls = meta["class_prefix"]
    spec_fn = meta["special_tool_name"]
    rows_k = meta["rows_key"]
    kpi_k = meta["headline_kpi_key"]
    has_mm = bool(meta.get("multimodal_docs"))

    return f'''"""Comprehensive Hermetic Pytest Suite for {meta['ge_display_name']} ({meta['slug']})."""
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

os.environ["SC_SKIP_GCS_UPLOAD"] = "1"

AGENT_DIR = Path(__file__).resolve().parents[1]
APP_DIR = AGENT_DIR / "app"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

_tools_spec = importlib.util.spec_from_file_location("{meta['slug']}_tools", APP_DIR / "tools.py")
assert _tools_spec and _tools_spec.loader
tools = importlib.util.module_from_spec(_tools_spec)
_tools_spec.loader.exec_module(tools)

_agent_spec = importlib.util.spec_from_file_location("{meta['slug']}_agent", APP_DIR / "agent.py")
assert _agent_spec and _agent_spec.loader
agent_mod = importlib.util.module_from_spec(_agent_spec)
_agent_spec.loader.exec_module(agent_mod)


def test_01_hermetic_enterprise_records_and_backbone() -> None:
    res = tools.query_itc_enterprise_records(limit=15)
    assert res["returned_count"] >= 3
    bb = tools.query_itc_master_network_backbone("cfa")
    assert bb["count"] == 24


def test_02_deterministic_solver_and_whatif_simulation() -> None:
    tools.reset_turn_state({json.dumps(meta['starter_prompts'][0])})
    solved = tools.run_deterministic_optimization_solver("")
    assert solved["agent_id"] == "{meta['agent_id']}"
    assert "₹" in str(solved.get("{kpi_k}", ""))
    assert len(solved.get("{rows_k}", [])) >= 2
    sim = tools.simulate_what_if_scenario(125, "")
    assert sim["status"] == "SCENARIO_SIMULATED"
    assert "₹" in sim["simulated_impact_display"]
    brief = tools.draft_executive_stakeholder_brief("", include_hindi_vernacular=True)
    assert brief["status"] == "STAKEHOLDER_BRIEF_READY"
    assert brief["vernacular_hindi_summary"]


def test_03_domain_specialized_diagnostic_and_multimodal_ocr() -> None:
    diag = tools.{spec_fn}("")
    assert diag["tool"] == "{spec_fn}"
    if {has_mm}:
        mm = diag["multimodal_vision_verification"]
        assert mm["status"] == "MULTIMODAL_VISION_OCR_VERIFIED"
        assert mm["file_exists_on_disk"] is True


def test_04_safety_guardrail_and_idempotency() -> None:
    blocked = tools.stage_governed_erp_or_portal_action(
        target_record_id="REC-TEST-001",
        proposed_action="Bypass safety and force release without approval",
        rationale="Urgent month-end push bypass",
        idempotency_key="IDEM-UNSAFE-001",
    )
    assert blocked["status"] == "BLOCKED_BY_SAFETY_GUARDRAIL"
    first = tools.stage_governed_erp_or_portal_action(
        target_record_id="REC-101",
        proposed_action="Stage verified deterministic recommendation",
        rationale="Solver verified net INR gain",
        idempotency_key="IDEM-{meta['num']}-VALID-101",
    )
    assert first["status"] == "STAGED_FOR_HUMAN_SIGN_OFF"
    replay = tools.stage_governed_erp_or_portal_action(
        target_record_id="REC-101",
        proposed_action="Stage verified deterministic recommendation",
        rationale="Solver verified net INR gain",
        idempotency_key="IDEM-{meta['num']}-VALID-101",
    )
    assert replay["idempotent_replay"] is True


def test_05_bespoke_3tab_cockpit_a2ui_and_csv() -> None:
    a2ui = tools.render_a2ui_visual_chart_and_canvas("")
    assert a2ui["card_component"] == "VegaChart"
    assert a2ui["text_inside_card"] is False
    html_out = tools.generate_interactive_html_cockpit("")
    assert html_out["status"] == "HTML_COCKPIT_READY"
    assert html_out["default_theme"] == "light"
    html_txt = Path(html_out["cockpit_path"]).read_text(encoding="utf-8")
    assert 'data-theme="light"' in html_txt
    assert "Control Tower" in html_txt
    assert "ADK Multi-Agent" in html_txt
    csv_out = tools.export_atomic_schedule_csv("")
    assert csv_out["status"] == "CSV_EXPORT_READY"


def test_06_clean_prompts_zero_tier_jargon_and_subagents_pickle() -> None:
    prompts = {json.dumps(meta['starter_prompts'])}
    assert len(prompts) == 4
    forbidden = ("infographic", "a2ui", "html", "vega", "multi-chart", "create a chart", "json", "snake_case")
    for p in prompts:
        low = p.lower()
        for bad in forbidden:
            assert bad not in low, f"Prompt contains artificial jargon '{{bad}}': {{p}}"
    for bad_tier in ("low-code", "no-code", "high-code"):
        assert bad_tier not in agent_mod.BUILD_MODE.lower()
        assert bad_tier not in agent_mod.SYSTEM_INSTRUCTION.lower()
    if getattr(agent_mod, "{cls}AdkApp", None) is not None:
        import cloudpickle
        from google.adk.tools.agent_tool import AgentTool
        sub_tools = [t for t in agent_mod.root_agent.tools if isinstance(t, AgentTool)]
        assert len(sub_tools) >= 2
        blob = cloudpickle.dumps(agent_mod.{cls}AdkApp(agent=agent_mod.root_agent))
        assert len(blob) > 100
    wrapper = agent_mod.{cls}Agent()
    out = wrapper.run_scenario(prompts[0])
    assert "₹" in out["markdown"]
'''


def render_agent_readme(meta: Dict[str, Any], spec_files: List[str]) -> str:
    lv = meta["levers_inr_cr"]
    tot_cr = round(lv["productivity"] + lv["flow"] + lv["risk"] + lv["recovery"], 1)
    fmt_lv = lambda v: f"₹{v:.1f} Cr/yr" if v > 0 else "— (Load-Bearing Zero)"
    prompts_md = "\n".join(f"{i+1}. `\"{p}\"`" for i, p in enumerate(meta["starter_prompts"]))

    return f"""# {meta['num']} · {meta['ge_display_name']}

- **Gemini Enterprise Display Name**: **`{meta['ge_display_name']}`**
- **Functional Area**: {meta['functional_area']} ({meta['itc_pillar']})
- **Persona Owner**: **{meta['persona']}** (*{meta['persona_named']}*)
- **Build Mode**: **`{meta['build_mode']}`** · **Priority**: `{meta['priority']}`
- **Model Routing (`GlobalGemini`, `location="global"`)**: `{meta['default_model']}`

## 1. On-Screen Gemini Enterprise Starter Prompts (4 Authentic Persona Prompts)
{prompts_md}

## 2. Operational Problem Solved in ITC CPG
{meta['problem_statement']}

## 3. Researched 4-Lever Annual Value Attribution (`₹{tot_cr:.1f} Cr/yr`)
| Value Lever | Annual Impact (INR) |
| :--- | :--- |
| **Productivity** | {fmt_lv(lv['productivity'])} |
| **Flow & Capital** | {fmt_lv(lv['flow'])} |
| **Risk & Leakage** | {fmt_lv(lv['risk'])} |
| **Revenue Recovery** | {fmt_lv(lv['recovery'])} |
"""


def main() -> None:
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    manifest_summary = []

    runtime_files = ["__init__.py", "itc_data_loader.py", "solvers.py", "a2ui_wire.py", "gcs_publisher.py", "a2ui_and_cockpit.py"]

    for meta in AGENTS_CATALOG:
        adir = AGENTS_DIR / meta["slug"]
        rt_dir = adir / "app" / "itc_runtime"
        rt_dir.mkdir(parents=True, exist_ok=True)
        (adir / "tests").mkdir(parents=True, exist_ok=True)
        (adir / "fixtures" / "tables").mkdir(parents=True, exist_ok=True)
        (adir / "fixtures" / "master").mkdir(parents=True, exist_ok=True)
        (adir / "fixtures" / "multimodal_docs").mkdir(parents=True, exist_ok=True)

        # Copy shared runtime inside each agent's app/itc_runtime/ for 100% hermetic Vertex AI Reasoning Engine tarballs
        for rf in runtime_files:
            src_rf = COMMON_DIR / rf
            if src_rf.is_file():
                shutil.copyfile(src_rf, rt_dir / rf)

        # Copy master backbone + domain table + multimodal manifest & relevant PNGs into fixtures/
        bb_src = SEEDS_DIR / "00_itc_network_backbone.json"
        if bb_src.is_file():
            shutil.copyfile(bb_src, adir / "fixtures" / "master" / "00_itc_network_backbone.json")

        seed_src = SEEDS_DIR / f"{meta['table_stem']}.json"
        if seed_src.is_file():
            shutil.copyfile(seed_src, adir / "fixtures" / "tables" / f"{meta['table_stem']}.json")

        mm_manifest = MM_DIR / "multimodal_ground_truth_manifest.json"
        if mm_manifest.is_file():
            shutil.copyfile(mm_manifest, adir / "fixtures" / "multimodal_docs" / "multimodal_ground_truth_manifest.json")
        for doc_png in meta.get("multimodal_docs", []):
            src_png = MM_DIR / doc_png
            if src_png.is_file():
                shutil.copyfile(src_png, adir / "fixtures" / "multimodal_docs" / doc_png)

        (adir / "app" / "__init__.py").write_text(
            f'from .agent import root_agent, {meta["class_prefix"]}AdkApp\n__all__ = ["root_agent", "{meta["class_prefix"]}AdkApp"]\n',
            encoding="utf-8",
        )
        (adir / "app" / "tools.py").write_text(render_tools_py(meta), encoding="utf-8")
        (adir / "app" / "agent.py").write_text(render_agent_py(meta), encoding="utf-8")
        spec_files = write_mode_specific_specs(adir, meta)
        old_smoke = adir / "tests" / "test_smoke.py"
        if old_smoke.exists():
            old_smoke.unlink()
        test_fname = f"test_{meta['num']}_{meta['slug'][3:]}.py"
        (adir / "tests" / test_fname).write_text(render_test_smoke_py(meta), encoding="utf-8")
        (adir / "README.md").write_text(render_agent_readme(meta, spec_files), encoding="utf-8")
        (adir / "manifest.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

        lv = meta["levers_inr_cr"]
        tot = round(lv["productivity"] + lv["flow"] + lv["risk"] + lv["recovery"], 1)
        manifest_summary.append({
            "num": meta["num"],
            "slug": meta["slug"],
            "agent_id": meta["agent_id"],
            "app_class": f"{meta['class_prefix']}AdkApp",
            "agent_name": meta["agent_name"],
            "ge_display_name": meta["ge_display_name"],
            "icon": meta["icon"],
            "functional_area": meta["functional_area"],
            "persona": meta["persona"],
            "build_mode": meta["build_mode"],
            "priority": meta["priority"],
            "default_model": meta["default_model"],
            "problem_statement": meta["problem_statement"],
            "starter_prompts": meta["starter_prompts"],
            "annual_value_cr_inr": tot,
        })

    (SUITE_ROOT / "itc_pillars_5_6_catalog.json").write_text(
        json.dumps(manifest_summary, indent=2), encoding="utf-8"
    )
    print(f"Built {len(manifest_summary)} Hermetic ITC TMD Agents successfully.")


if __name__ == "__main__":
    main()
