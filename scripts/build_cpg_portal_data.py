#!/usr/bin/env python3
"""Builds the CPG Supply Chain Portal Data & 4-Lever Value Model:
  - Preserves ALL 60 original Personas (P01..P60) & ALL 60 original Agents untouched by ID/name.
  - Enriches every Persona with a realistic human leader profile (~60% Indian & ~40% global names),
    CPG operational setting, crisp role definition, decision boundaries, and NO old journey timeline.
  - Adds 18 deeply researched CPG Supply Chain Agents (78 Agents Total: 60 Original + 18 New CPG Gaps).
  - Equips every Persona with a cohesive 2-to-4 Agent Suite (Reads / Does / Returns / Stops At / Safety Envelope),
    explicitly marking Priority 0 (P0 · Deploy First to GE), Priority 1 (P1 · Build Next), and Priority 2 (P2 · Enabler).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_CAT = ROOT / "data" / "base_60_catalog.json"
GE_META = ROOT / "data" / "existing_ge_deployments.json"
OUT_DATA = ROOT / "data" / "sc_story_data.js"
OUT_VAL = ROOT / "data" / "sc_value_model.js"

with open(BASE_CAT, encoding="utf-8") as f:
    cat = json.load(f)
with open(GE_META, encoding="utf-8") as f:
    dep = json.load(f)

deployed_map = {item["agent_id"]: item for item in dep.get("agents_deployed", [])}
GE_CID = "47d2d150-f788-4afc-af12-df8dd05ed34a"
GE_AUTH = "admin@zuhaibp.altostrat.com"
GE_WORKSPACE_URL = f"https://vertexaisearch.cloud.google.com/home/cid/{GE_CID}?authuser={GE_AUTH}"

# 60 realistic human names (~60% Indian & ~40% International CPG Supply Chain leaders)
PERSONA_HUMANS = [
    ("Vikram Deshmukh", "Mumbai Corporate S&OP Tower · Western Hub"),
    ("Elena Rostova", "Geneva / Bengaluru Commercial Sync Desk"),
    ("Arjun Nair", "Gurugram Foods Innovation & Launch Center"),
    ("Claire Beaumont", "Chicago / Mumbai Modern Trade RGM Hub"),
    ("Rajesh Iyer", "Bhiwandi CFA & General Trade Key Accounts"),
    ("Marcus Vance", "Hyderabad Shared Commercial Finance Center"),
    ("Ananya Chatterjee", "Kolkata / Mumbai Integrated S&OP Hub"),
    ("Kenji Takahashi", "Singapore / Mumbai Global CSCO War-Room"),
    ("Siddharth Menon", "Bengaluru Executive IBP Control Tower"),
    ("Sofia Lindqvist", "Rotterdam / Mumbai Portfolio Margin Desk"),
    ("Rohan Kulkarni", "Pune Packaging Cutover & BOM Studio"),
    ("Hannah Brooks", "London / Mumbai Cost-to-Serve Analytics"),
    ("Karthik Subramanian", "Chennai Multi-Tier Sourcing Nerve Center"),
    ("Mateo Silva", "Sao Paulo / Kochi Agri Vendor Qualification"),
    ("Meera Krishnan", "Bengaluru Scope 3 & Deforestation Desk"),
    ("Lukas Weber", "Frankfurt / Sanand Resin & Feedstock Desk"),
    ("Pranav Joshi", "Mumbai Direct Materials Should-Cost Desk"),
    ("Nadia Al-Mansoor", "Dubai / Haridwar Sustainable Packaging Lab"),
    ("Deepika Rao", "Mumbai Commercial Procurement Legal"),
    ("Liam O'Connor", "Dublin / Pune Inbound MRP Expediting Desk"),
    ("Sanjay Gupta", "Noida Shared Accounts Payable Recovery Hub"),
    ("Camille Laurent", "Haridwar ICML High-Speed Bottling Campus"),
    ("Nikhil Verma", "Ranjangaon Pune ICML Packaging Floor"),
    ("Rachel Goldstein", "Malur Bengaluru Multi-Line Plant Ops"),
    ("Divya Shetty", "Mumbai Multi-Plant OEE Engineering Desk"),
    ("Henrik Larsen", "Sri City / Rotterdam Co-Packer Network"),
    ("Karan Malhotra", "Corporate Industrial CapEx Twin Studio"),
    ("Isabella Rossi", "Medak Food Park High-Speed Vision QA"),
    ("Abhishek Sen", "Haridwar GMP & FSSAI/FDA Release Lab"),
    ("Daniel Park", "Sanand Lean Six Sigma & CAPA Center"),
    ("Pooja Nambiar", "Bengaluru Multi-Echelon Inventory Hub"),
    ("Thomas Becker", "Bhiwandi SLOB & Freshness Control Desk"),
    ("Gaurav Tiwari", "Nagpur MIHAN National Cross-Dock Hub"),
    ("Chloe Martin", "Dankuni Automated AS/RS Fulfillment Center"),
    ("Varun Bhatia", "Bilaspur Gurugram Inbound Receiving Dock"),
    ("Yuki Sato", "Hosur High-Velocity Wave Fulfillment Floor"),
    ("Shruti Deshpande", "Mumbai Modern Trade & Q-Commerce Ops"),
    ("Gabriel Morales", "Dallas / Bengaluru Omnichannel ATP Hub"),
    ("Aditya Pillai", "Bhiwandi Reverse Grading & Refurb Hub"),
    ("Emma Lindholm", "Pune Primary Linehaul Consolidation Desk"),
    ("Manish Agarwal", "Haridwar ICML Smart Yard & Gate Tower"),
    ("Oliver Wright", "Kochi / Nhava Sheva Reefer Cold-Chain Desk"),
    ("Neha Saxena", "Hosur Store-Ready Pallet Engineering"),
    ("Carlos Mendoza", "Ahmedabad Regional Store Replenishment"),
    ("Suresh Reddy", "JNPT Mumbai Port Drayage & Curfew Desk"),
    ("Freja Nielsen", "Bengaluru Hyper-Local Q-Commerce Dispatch"),
    ("Tarun Kapoor", "Delhi NCR D2C & 3PL Mode-Shift Tower"),
    ("Sarah Jenkins", "Mumbai OTIF Penalty & Customer Ops Shield"),
    ("Kavita Hegde", "Central FleetFlow Corridor Control Room"),
    ("Julian Vance", "National Carrier Waterfall Procurement"),
    ("Harshvardhan Roy", "Chennai Freight Bill & Accessorial Audit"),
    ("Maya Lin", "Bengaluru Multimodal RMA Fraud Lab"),
    ("Ashwin Sundaram", "Mumbai Consumer Refund & Keep-It Desk"),
    ("Lucas Meyer", "Nagpur Carrier OS&D Claims Control"),
    ("Ritika Bose", "Hyderabad Fresh ESL & Markdown Studio"),
    ("Noah Abrams", "Delhi NCR Short-Dated Secondary Clearing"),
    ("Vivek Choudhary", "Corporate Zero-Waste & Food-Bank Ledger"),
    ("Eva Novak", "Bhiwandi CHEP/PECO RFID Pool Control"),
    ("Swati Gokhale", "Pune Milk-Run Empty Crate Backhaul Desk"),
    ("Benjamin Hart", "Haridwar Reusable Tote Wash & QA Gate"),
]

# 18 New Deeply-Researched CPG Supply Chain Agents (added alongside the 60 original agents = 78 total)
NEW_CPG_AGENTS = [
    {
        "id": "qcommerce_darkstore_sensing_agent",
        "deptId": "demand_sop",
        "subPillarId": "demand_forecasting",
        "subPillarName": "Demand Forecasting",
        "name": "Q-Commerce Dark-Store Velocity Agent",
        "tier": "P0",
        "paybackDays": 35,
        "prod": 0.5, "flow": 2.4, "shield": 0.8, "recov": 5.6,
        "savedHoursWk": 11,
        "linkedPersonas": ["demand_planner_forecaster", "commercial_planning_lead", "store_operations_omni_lead"],
        "oneLine": "Monitors 15-minute Blinkit, Zepto & Instacart dark-store sell-out spikes and local weather to trigger micro-replenishments before 10-minute delivery tiles go out of stock.",
        "reads": "15-min Q-Commerce partner dark-store inventory feeds, hyper-local PIN-code search trends, WeatherNext 3 rain/heat bursts, and urban Mother-Hub stock (`01_daily_pos_dms_qcomm_velocity.csv`).",
        "does": "Imputes censored dark-store stockout velocity using BigQuery ML TimesFM 2.5 and ranks urgent milk-run top-up totes across 420 urban dark stores.",
        "returns": "PIN-code-ranked micro-replenishment wave table + A2UI velocity surge card ready for 1-click urban dispatch.",
        "stopsAt": "Overriding contractual Quick-Commerce margin terms or committing emergency 3PL rider surge fees without Commercial Lead sign-off.",
        "safetyEnvelope": "Falls back to 7-day rolling dark-store baseline if partner API latency exceeds 30 minutes.",
    },
    {
        "id": "festival_monsoon_surge_planner",
        "deptId": "demand_sop",
        "subPillarId": "sop_ibp",
        "subPillarName": "S&OP / IBP",
        "name": "Festival & Monsoon Surge Planner",
        "tier": "P1",
        "paybackDays": 85,
        "prod": 0.4, "flow": 2.1, "shield": 1.4, "recov": 3.2,
        "savedHoursWk": 8,
        "linkedPersonas": ["sop_supply_planning_dir", "brand_innovation_mgr", "ibp_lead_chief_planning_off"],
        "oneLine": "Aligns movable regional festival calendars (Diwali, Eid, Onam, Lunar New Year) and monsoon onset shifts with gift-pack pre-builds 10 weeks ahead.",
        "reads": "Historical lunar-adjusted festival sell-through, IMD/WeatherNext monsoon onset ensembles, gift-box co-packing capacity, and CFA storage limits.",
        "does": "Runs date-shifted causal lift decomposition and finite pre-build optimization in OR-Tools so seasonal SKUs peak without post-festival markdowns.",
        "returns": "State-by-state pre-build & allocation schedule comparing P50 vs P90 monsoon/festival demand scenarios.",
        "stopsAt": "Locking third-party seasonal warehouse leases or authorizing overtime factory shifts.",
        "safetyEnvelope": "Caps pre-build exposure on single-season gift packs at 85% of prior-year sell-through unless signed off.",
    },
    {
        "id": "rgm_pack_price_architecture_agent",
        "deptId": "demand_sop",
        "subPillarId": "trade_promotion",
        "subPillarName": "Trade Promotion",
        "name": "RGM Price-Pack Architecture Agent",
        "tier": "P1",
        "paybackDays": 90,
        "prod": 0.4, "flow": 0.0, "shield": 3.8, "recov": 2.9,
        "savedHoursWk": 7,
        "linkedPersonas": ["trade_marketing_manager", "category_manager_portfolio", "commercial_finance_director"],
        "oneLine": "Simulates magic-price-point grammage shifts (₹5/₹10 sachets vs Modern Trade family packs) to protect gross margin under commodity inflation.",
        "reads": "SKU grammage/MRP master (`00_master_skus.jsonl`), cross-pack elasticity matrices, competitor pack trackers, and raw-material COGS drift.",
        "does": "Computes cross-SKU cannibalization and net Revenue Growth Management (RGM) margin contribution across General Trade and Modern Trade.",
        "returns": "Pack-price elasticity waterfall and recommended grammage/slab adjustments by channel.",
        "stopsAt": "Changing printed Maximum Retail Price (MRP) master records or statutory Legal Metrology declarations.",
        "safetyEnvelope": "Blocks any grammage recommendation that violates statutory standard pack-weight rules.",
    },
    {
        "id": "farmgate_agri_commodity_hedger",
        "deptId": "sourcing_procurement",
        "subPillarId": "material_packaging",
        "subPillarName": "Material & Packaging",
        "name": "Farm-Gate Agri & Mandi Procurement Agent",
        "tier": "P0",
        "paybackDays": 45,
        "prod": 0.5, "flow": 1.6, "shield": 6.8, "recov": 0.0,
        "savedHoursWk": 10,
        "linkedPersonas": ["category_sourcing_mgr_direct", "strategic_sourcing_lead", "procurement_dir_risk_mgr"],
        "oneLine": "Synthesizes daily mandi crop arrivals, satellite soil-moisture yield indices, and CBOT/NCDEX futures to time wheat, edible oil, coffee, and spice forward buys.",
        "reads": "e-Choupal / mandi arrival volumes, moisture & gluten lab grades, Earth Engine crop NDVI, and supplier forward quotes (`02_po_grn_three_way_match_sourcing.csv`).",
        "does": "Scores physical buy-vs-wait windows and optimizes multi-mandi procurement splits factoring inward freight to ICML mills.",
        "returns": "Daily commodity buy window brief + landed mill cost comparison across mandis and Tier-1 processors.",
        "stopsAt": "Executing commodity futures derivatives or committing physical forward contracts above buyer authority.",
        "safetyEnvelope": "Enforces strict food-grade moisture and aflatoxin quality cutoffs before ranking low-price mandi lots.",
    },
    {
        "id": "artwork_allergen_packaging_gate",
        "deptId": "sourcing_procurement",
        "subPillarId": "material_packaging",
        "subPillarName": "Material & Packaging",
        "name": "Packaging Artwork & Allergen Gate",
        "tier": "P1",
        "paybackDays": 80,
        "prod": 0.5, "flow": 0.0, "shield": 4.4, "recov": 0.0,
        "savedHoursWk": 9,
        "linkedPersonas": ["packaging_rd_engineer", "regulatory_compliance_lead", "lifecycle_materials_mgr"],
        "oneLine": "Inspects pre-press packaging proofs via Gemini multimodal vision against BOM allergen tables and FSSAI/FDA/EU labeling laws before cylinder engraving.",
        "reads": "PDF/vector laminate proofs, active recipe BOM allergen lists, Legal Metrology font-height rules, and barcode GS1 specs.",
        "does": "Cross-verifies ingredient order, bold allergen callouts, nutritional math, and statutory license numbers pixel-by-pixel.",
        "returns": "Annotated pre-press compliance checklist flagging exact label discrepancies prior to print run.",
        "stopsAt": "Granting final regulatory artwork release or signing print-cylinder purchase orders.",
        "safetyEnvelope": "Routes any multi-language translation or novel health claim directly to Regulatory Affairs.",
    },
    {
        "id": "supplier_dynamic_discounting_agent",
        "deptId": "sourcing_procurement",
        "subPillarId": "contract_po_mgmt",
        "subPillarName": "Contract & PO Mgmt",
        "name": "Supplier Dynamic Discounting Optimizer",
        "tier": "P1",
        "paybackDays": 70,
        "prod": 0.3, "flow": 3.4, "shield": 2.1, "recov": 0.0,
        "savedHoursWk": 6,
        "linkedPersonas": ["accounts_payable_lead", "commercial_sourcing_legal", "buyer_procurement_coord"],
        "oneLine": "Matches verified 3-way-matched vendor invoices against treasury surplus cash and vendor early-pay APR bids to capture risk-free margin.",
        "reads": "Approved AP invoice ledger, vendor cash-need APR offers (`00_multitier_suppliers.jsonl`), and daily treasury hurdle rates.",
        "does": "Solves knapsack allocation of surplus working capital across early-payment discount offers exceeding corporate hurdle APR.",
        "returns": "Ranked early-pay settlement proposal showing exact annualized yield and net cash discount captured.",
        "stopsAt": "Releasing bank wire transfers or altering contracted net payment terms.",
        "safetyEnvelope": "Excludes any invoice with an open GRN quantity variance or quality hold.",
    },
    {
        "id": "plant_energy_utility_peak_shaver",
        "deptId": "manufacturing_prod",
        "subPillarId": "capacity_planning",
        "subPillarName": "Capacity Planning",
        "name": "Plant Boiler & Tariff Peak-Shaver",
        "tier": "P1",
        "paybackDays": 95,
        "prod": 0.3, "flow": 2.9, "shield": 1.8, "recov": 0.0,
        "savedHoursWk": 6,
        "linkedPersonas": ["plant_operations_manager", "vp_manufacturing_engineering", "supply_chain_ops_director"],
        "oneLine": "Synchronizes heavy Clean-in-Place (CIP) thermal cycles, cold-room pull-downs, and grinding mills with off-peak grid tariffs and rooftop solar windows.",
        "reads": "15-min smart-meter kWh telemetry, state Time-of-Day electricity tariffs, solar output forecasts, and finite line schedule (`03_plant_mes_oee_copacker_genealogy.csv`).",
        "does": "Shifts non-critical thermal/chiller pull-downs out of peak-tariff blocks via CP-SAT without delaying scheduled case output.",
        "returns": "Shift utility schedule cutting peak demand charges and Scope 2 carbon intensity per ton.",
        "stopsAt": "Changing pasteurization kill-step temperatures or overriding cold-room food-safety bounds.",
        "safetyEnvelope": "Hard-locks HACCP thermal safety minimums above all energy-saving objectives.",
    },
    {
        "id": "copacker_material_yield_reconciler",
        "deptId": "manufacturing_prod",
        "subPillarId": "capacity_planning",
        "subPillarName": "Capacity Planning",
        "name": "Co-Packer BOM & Laminate Scrap Auditor",
        "tier": "P0",
        "paybackDays": 40,
        "prod": 0.5, "flow": 1.4, "shield": 5.8, "recov": 0.0,
        "savedHoursWk": 9,
        "linkedPersonas": ["external_sourcing_cmo_lead", "continuous_improvement_lead", "master_production_scheduler"],
        "oneLine": "Reconciles raw edible oil, sugar, and printed laminate film rolls issued to third-party co-packers against finished cases received and tolling scrap allowances.",
        "reads": "SAP subcontracting challans (541/543), co-packer batch consumption reports, BOM scrap tolerances, and finished GRNs.",
        "does": "Flags excess film/ingredient usage beyond contractual 1.2% tolerance and computes exact debit-note clawbacks.",
        "returns": "Co-packer mass-balance variance ledger + draft debit-note substantiation packet.",
        "stopsAt": "Posting financial debit memos or terminating CMO tolling allocations.",
        "safetyEnvelope": "Accounts for startup web-threading waste on short promotional runs before flagging anomalies.",
    },
    {
        "id": "lot_genealogy_recall_tracer",
        "deptId": "manufacturing_prod",
        "subPillarId": "quality_compliance",
        "subPillarName": "Quality & Compliance",
        "name": "2-Hour Lot Genealogy & Recall Tracer",
        "tier": "P0",
        "paybackDays": 50,
        "prod": 0.5, "flow": 0.0, "shield": 7.4, "recov": 0.0,
        "savedHoursWk": 8,
        "linkedPersonas": ["qa_manager_line_inspector", "regulatory_compliance_lead", "shop_floor_shift_lead"],
        "oneLine": "Traverses multi-hop supplier ingredient lots through ICML mixer batches to exact CFA depots and stockist invoices in under 90 seconds—shrinking recall blast radius by 80%.",
        "reads": "Raw-material COA lot logs, MES batch genealogy (`03_plant_mes_oee_copacker_genealogy.csv`), WMS pallet SSCC scans, and DMS stockist dispatch invoices.",
        "does": "Builds bidirectional lot containment graphs isolating only affected sub-batches instead of blanket multi-week plant recalls.",
        "returns": "Surgical lot hold list (exact pallets, CFAs, and distributors) + pre-filled FSSAI/FDA mock-recall trace report.",
        "stopsAt": "Issuing public consumer recall notices or releasing quarantined QA stock.",
        "safetyEnvelope": "Includes adjacent washdown transition batches whenever exact CIP cutover timestamps are missing.",
    },
    {
        "id": "fefo_shelf_life_allocator",
        "deptId": "inventory_warehouse",
        "subPillarId": "positioning_optimization",
        "subPillarName": "Positioning & Optimization",
        "name": "Dynamic FEFO & Shelf-Life Allocator",
        "tier": "P0",
        "paybackDays": 35,
        "prod": 0.5, "flow": 4.8, "shield": 3.9, "recov": 3.4,
        "savedHoursWk": 10,
        "linkedPersonas": ["inventory_controller_buyer", "replenishment_planner", "inventory_optimization_lead"],
        "oneLine": "Matches batch-level remaining shelf-life days against channel-specific Minimum Remaining Shelf-Life (MRSL) rules (e.g., 75% Modern Trade vs 55% General Trade) to prevent dock rejections and expiry.",
        "reads": "Batch expiry ledger (`04_fefo_inventory_dms_wms_ledger.csv`), customer MRSL contract rules, and transit days by lane.",
        "does": "Overrides naive FIFO picking with channel-aware First-Expired-First-Out (FEFO) optimization so mid-life lots flow immediately to high-turn General Trade beats.",
        "returns": "Batch-to-order allocation table eliminating Modern Trade MRSL rejections and DC expiry write-offs.",
        "stopsAt": "Shipping any lot past statutory expiry or waiving customer MRSL contract clauses.",
        "safetyEnvelope": "Hard-blocks allocation if transit lead-time + buffer exceeds remaining MRSL threshold.",
    },
    {
        "id": "dms_distributor_stock_balancer",
        "deptId": "inventory_warehouse",
        "subPillarId": "omnichannel_visibility",
        "subPillarName": "Omnichannel Visibility",
        "name": "DMS Secondary Stock & Credit Balancer",
        "tier": "P0",
        "paybackDays": 45,
        "prod": 0.6, "flow": 3.6, "shield": 1.2, "recov": 5.1,
        "savedHoursWk": 11,
        "linkedPersonas": ["key_account_manager", "omnichannel_fulfillment_dir", "store_replenishment_lead"],
        "oneLine": "Monitors Distributor Management System (DMS) secondary stockists to spot where one distributor sits on 45 days of slow stock while an adjacent town stocks out—staging smart replenishment & credit-safe orders.",
        "reads": "DMS daily stockist closing inventory, tertiary kirana beat billings, distributor credit-limit aging, and CFA stock (`04_fefo_inventory_dms_wms_ledger.csv`).",
        "does": "Computes stockist-level Days-of-Inventory (DOI) norms and auto-drafts credit-compliant primary replenishment orders.",
        "returns": "Territory stock-imbalance map + auto-drafted DMS primary order queue.",
        "stopsAt": "Releasing orders to credit-blocked distributors or forcing stockist inter-transfers without consent.",
        "safetyEnvelope": "Respects state tax boundaries and distributor margin structures on every rebalance.",
    },
    {
        "id": "qcommerce_assortment_micro_slotter",
        "deptId": "inventory_warehouse",
        "subPillarId": "warehouse_operations",
        "subPillarName": "Warehouse Operations",
        "name": "Urban Hub & Dark-Store Micro-Slotter",
        "tier": "P1",
        "paybackDays": 90,
        "prod": 0.5, "flow": 2.7, "shield": 0.0, "recov": 1.8,
        "savedHoursWk": 8,
        "linkedPersonas": ["dc_operations_mgr", "dc_shift_floor_lead", "inbound_receiving_supervisor"],
        "oneLine": "Re-slots high-velocity consumer packs into golden pick-faces every night based on hourly eCommerce basket co-occurrence so pickers hit <90-second pack times.",
        "reads": "WMS pick-path logs, basket co-affinity pairs, case dimensions, and next-day promo calendar.",
        "does": "Solves ergonomic golden-zone bin assignment minimizing picker walk meters and aisle congestion.",
        "returns": "20-move nightly putaway/re-slot task list for morning shift handoff.",
        "stopsAt": "Co-locating chemical home-care SKUs beside Odor-sensitive food items.",
        "safetyEnvelope": "Enforces strict food vs non-food FEFO/hazard segregation in every bin move.",
    },
    {
        "id": "eway_bill_gst_transit_auditor",
        "deptId": "logistics_fleet",
        "subPillarId": "route_carrier",
        "subPillarName": "Route & Carrier",
        "name": "E-Way Bill & Transit Tax Compliance Shield",
        "tier": "P0",
        "paybackDays": 30,
        "prod": 0.5, "flow": 1.2, "shield": 6.4, "recov": 0.0,
        "savedHoursWk": 9,
        "linkedPersonas": ["freight_controller_claims", "fleet_dispatcher_central_ops", "transport_planner_inbound_mgr"],
        "oneLine": "Cross-checks live truck GPS ETA against statutory E-Way Bill expiry clocks, HSN tax codes, and vehicle transshipment updates so linehaul trucks never suffer highway detention penalties.",
        "reads": "NIC E-Way Bill API validity timestamps, Samsara/GPS truck telemetry, SAP GST invoice HSN codes (`05_tms_shipments_eway_freight_audit.csv`).",
        "does": "Flags trucks within 4 hours of E-Way Bill expiry due to highway congestion or breakdown and prepares Part-B extension drafts.",
        "returns": "Live expiring-waybill alert queue + pre-validated Part-B vehicle/extension payload.",
        "stopsAt": "Submitting statutory tax declarations with unverified vehicle numbers.",
        "safetyEnvelope": "Alerts central dispatch 4 hours prior to midnight expiry window.",
    },
    {
        "id": "modern_trade_dock_slot_booker",
        "deptId": "logistics_fleet",
        "subPillarId": "store_replenishment",
        "subPillarName": "Store Replenishment",
        "name": "Modern Trade Appointment & Fill-Rate Agent",
        "tier": "P1",
        "paybackDays": 75,
        "prod": 0.5, "flow": 1.9, "shield": 3.9, "recov": 1.6,
        "savedHoursWk": 8,
        "linkedPersonas": ["retail_logistics_dispatcher", "outbound_lead_industrial_eng", "customer_support_ops_lead"],
        "oneLine": "Synchronizes CFA wave completion and truck ETA with Reliance, DMart, Walmart, and Amazon vendor portal dock appointments to prevent PO expiry and OTIF chargebacks.",
        "reads": "Retailer ASN appointment calendars, WMS wave completion %, and live route traffic ETA.",
        "does": "Matches ready-to-ship loads against open retailer receiving slots and flags threatened PO cancellation cutoffs.",
        "returns": "Prioritized dock-load sequence + retailer portal slot-reschedule recommendation.",
        "stopsAt": "Canceling committed Modern Trade purchase orders.",
        "safetyEnvelope": "Prioritizes A-class festival/promo POs carrying >3% OTIF chargeback clauses.",
    },
    {
        "id": "rural_van_beat_load_optimizer",
        "deptId": "logistics_fleet",
        "subPillarId": "last_mile_delivery",
        "subPillarName": "Last-Mile Delivery",
        "name": "General Trade Beat & Van-Load Optimizer",
        "tier": "P1",
        "paybackDays": 85,
        "prod": 0.5, "flow": 2.4, "shield": 0.0, "recov": 3.3,
        "savedHoursWk": 8,
        "linkedPersonas": ["last_mile_operations_lead", "ecommerce_logistics_dir", "transport_procurement_lead"],
        "oneLine": "Builds the daily SKU load-out sheet for rural & urban General Trade sales vans based on outlet-level reorder probability and van weight/cube limits.",
        "reads": "DMS kirana beat schedules, historical outlet SKU order probability, active trade schemes, and 1.5-ton van capacity.",
        "does": "Maximizes expected daily beat billings per kilometer while eliminating evening unsold van returns.",
        "returns": "Beat-wise morning van load manifest + top-3 cross-sell SKU prompts per outlet.",
        "stopsAt": "Extending unapproved cash credit to overdue general-trade outlets.",
        "safetyEnvelope": "Reserves 85% van cube for confirmed pre-booked orders before adding predictive top-up cases.",
    },
    {
        "id": "cold_chain_salvage_repack_advisor",
        "deptId": "circular_enable",
        "subPillarId": "expiry_markdowns",
        "subPillarName": "Expiry & Markdowns",
        "name": "Cold-Chain Excursion MKT Salvage Advisor",
        "tier": "P1",
        "paybackDays": 80,
        "prod": 0.4, "flow": 0.9, "shield": 3.7, "recov": 2.8,
        "savedHoursWk": 7,
        "linkedPersonas": ["cold_chain_qa_logistics_dir", "inventory_disposition_lead", "packaging_qa_food_safety"],
        "oneLine": "Computes Mean Kinetic Temperature (MKT) degradation curves when dairy, chocolate, or probiotic reefers suffer brief door-open excursions—saving safe stock from blanket destruction.",
        "reads": "Minute-by-minute IoT reefer logger traces (`05_tms_shipments_eway_freight_audit.csv`), SKU Arrhenius shelf-life stability curves, and QA micro specs.",
        "does": "Separates cosmetic/safe minor thermal blips (eligible for fast local clearance) from true stability breaches requiring quarantine.",
        "returns": "Pallet-level QA disposition brief + carrier thermal-claim evidence log.",
        "stopsAt": "Releasing temperature-abused infant, dairy, or pharma-nutrition lots without QA Lab sign-off.",
        "safetyEnvelope": "Zero-tolerance quarantine whenever cumulative excursion exceeds validated stability envelope.",
    },
    {
        "id": "grey_market_diversion_sentinel",
        "deptId": "circular_enable",
        "subPillarId": "returns_claims_mgmt",
        "subPillarName": "Returns & Claims Mgmt",
        "name": "Channel Price-Erosion & Grey-Market Sentinel",
        "tier": "P1",
        "paybackDays": 90,
        "prod": 0.4, "flow": 0.0, "shield": 4.9, "recov": 1.7,
        "savedHoursWk": 7,
        "linkedPersonas": ["reverse_logistics_fraud_lead", "revenue_trade_finance_lead", "claims_specialist_controller"],
        "oneLine": "Detects deeply discounted institutional or regional promo stock leaking onto unauthorized B2B/online marketplaces by correlating batch lot scans and price anomalies.",
        "reads": "Marketplace price monitors, RMA lot-code scans (`06_returns_markdowns_rti_circular.csv`), and regional wholesale trade-scheme allocations.",
        "does": "Traces diverted lot prefixes back to originating bulk wholesale/institutional accounts eroding retail price integrity.",
        "returns": "Diversion trace dossier linking unauthorized listings to originating trade-scheme lots.",
        "stopsAt": "Terminating distributor agreements or withholding earned trade rebates unilaterally.",
        "safetyEnvelope": "Requires physical batch-code or test-buy verification before flagging a distributor account.",
    },
    {
        "id": "epr_plastic_credit_ledger_agent",
        "deptId": "circular_enable",
        "subPillarId": "pallet_tote_reclamation",
        "subPillarName": "Pallet & Tote Reclamation",
        "name": "EPR Multi-Layer Plastic Credit Ledger",
        "tier": "P2",
        "paybackDays": 145,
        "prod": 0.5, "flow": 0.0, "shield": 2.9, "recov": 0.0,
        "savedHoursWk": 8,
        "linkedPersonas": ["cso_circular_lead", "chief_sustainability_officer", "asset_recovery_rti_manager", "customer_experience_cx_lead", "merchandising_store_ops_mgr", "reverse_logistics_lead_wh", "reverse_transport_planner"],
        "oneLine": "Reconciles state-wise rigid PET & Multi-Layered Plastic (MLP) laminate tonnage dispatched in CPG packs against verified recycler EPR certificates.",
        "reads": "SKU packaging polymer weights (`00_master_skus.jsonl`), state-wise CFA sales tonnage, and CPCB/EU registered recycler credit ledgers.",
        "does": "Calculates exact quarterly Category I/II/III plastic obligations by state and flags certificate shortfalls ahead of filing.",
        "returns": "Audit-ready EPR plastic mass-balance ledger and recycler credit purchase plan.",
        "stopsAt": "Filing statutory CPCB/EU portal declarations or purchasing unverified offset credits.",
        "safetyEnvelope": "Accepts only GST-verified, geo-tagged Waste Processing Organization (PWP) certificates.",
    },
]

# Base 60 Agent Value & Priority Table (upgrading our 18 top Build-First agents + 6 new P0s = 24 P0 agents total!)
BASE_60_META = {
    "demand_sensing_agent": ("P0", 45, 0.9, 6.4, 1.8, 9.2),
    "promo_lift_simulator": ("P0", 60, 0.6, 0.0, 11.4, 4.8),
    "trade_scheme_claims_reconciler": ("P0", 30, 0.5, 0.0, 8.6, 0.0),
    "cpfr_sync_agent": ("P1", 90, 0.6, 2.8, 0.9, 3.6),
    "npi_demand_profiler": ("P1", 120, 0.3, 1.9, 2.4, 2.9),
    "field_beat_distributor_sync_agent": ("P1", 110, 0.8, 0.0, 2.1, 4.4),
    "sop_scenario_weaver": ("P1", 105, 0.7, 4.1, 3.2, 2.8),
    "disruption_war_room_orchestrator": ("P1", 95, 0.4, 2.2, 6.5, 3.1),
    "working_capital_cash_bridge": ("P1", 120, 0.5, 4.6, 2.1, 1.4),
    "eco_cutover_orchestrator": ("P1", 130, 0.4, 1.8, 3.4, 0.0),
    "csco_control_tower_copilot": ("P2", 160, 0.6, 0.0, 1.5, 0.0),
    "network_twin_architect": ("P2", 180, 0.5, 2.9, 1.1, 0.0),

    "tier_n_risk_sentinel": ("P0", 60, 0.6, 2.4, 11.8, 4.1),
    "tariff_esg_agent": ("P0", 45, 0.4, 0.0, 9.4, 0.0),
    "three_way_match_dispute": ("P0", 30, 0.9, 0.0, 7.8, 0.0),
    "supplier_quality_sentinel": ("P1", 110, 0.5, 1.2, 4.2, 0.0),
    "commodity_index_advisor": ("P1", 95, 0.4, 0.0, 5.9, 0.0),
    "rfq_should_cost_agent": ("P1", 90, 0.5, 0.0, 6.8, 0.0),
    "master_data_leadtime_steward": ("P1", 100, 0.8, 2.7, 1.9, 0.0),
    "carbon_scope3_ledger": ("P2", 170, 0.5, 0.0, 2.2, 0.0),
    "sustainable_packaging_agent": ("P2", 155, 0.4, 0.8, 2.6, 0.0),

    "finite_production_scheduler": ("P0", 60, 0.7, 8.6, 2.1, 3.4),
    "inline_yield_guardian": ("P0", 75, 0.6, 1.9, 6.4, 1.5),
    "line_schedule_optimizer": ("P1", 90, 0.8, 4.2, 1.7, 1.9),
    "labor_line_balancing_agent": ("P1", 105, 0.7, 2.8, 2.4, 0.0),
    "predictive_oee_sentinel": ("P1", 115, 0.4, 5.1, 2.9, 0.0),
    "copacker_allocation_agent": ("P1", 120, 0.4, 2.5, 3.1, 1.8),
    "batch_record_auditor": ("P1", 110, 0.6, 1.1, 3.8, 0.0),
    "scrap_defect_root_cause_agent": ("P1", 125, 0.5, 2.3, 3.3, 0.0),
    "capex_simulator_agent": ("P2", 180, 0.4, 1.8, 2.4, 0.0),

    "meio_safety_stock_agent": ("P0", 55, 0.5, 14.8, 0.0, 4.5),
    "slob_disposition_agent": ("P0", 45, 0.5, 4.9, 3.6, 4.2),
    "planogram_merchandising_vision_auditor": ("P0", 60, 0.8, 1.5, 0.0, 8.9),
    "crossdock_transfer_orchestrator": ("P1", 95, 0.6, 5.4, 1.4, 2.8),
    "warehouse_slotting_agent": ("P1", 105, 0.7, 4.8, 0.8, 0.0),
    "dock_to_stock_agent": ("P1", 95, 0.7, 2.9, 2.3, 0.0),
    "wave_fulfillment_copilot": ("P1", 100, 0.8, 3.2, 1.9, 1.6),
    "atp_order_promising_agent": ("P1", 110, 0.5, 2.1, 0.0, 5.2),
    "returns_triage_agent": ("P1", 115, 0.6, 1.8, 1.2, 3.9),

    "load_consolidation_agent": ("P0", 45, 0.7, 9.8, 1.4, 0.0),
    "fleetflow_dispatch": ("P0", 45, 0.9, 7.4, 2.8, 3.1),
    "otif_penalty_shield": ("P0", 40, 0.7, 0.0, 7.9, 2.2),
    "freight_bill_audit_agent": ("P0", 30, 0.6, 0.0, 10.6, 0.0),
    "yard_dock_sequencer": ("P1", 95, 0.6, 3.4, 2.2, 0.0),
    "cold_chain_auditor": ("P1", 100, 0.4, 0.0, 6.2, 1.4),
    "aisle_aligned_pallet_agent": ("P1", 115, 0.5, 3.6, 0.0, 1.5),
    "store_capacity_agent": ("P1", 120, 0.5, 2.9, 0.0, 2.4),
    "port_drayage_orchestrator": ("P1", 110, 0.5, 2.8, 3.7, 0.0),
    "geocoding_intelligence_agent": ("P1", 105, 0.5, 2.4, 1.1, 1.8),
    "multimodal_mode_shift_agent": ("P1", 100, 0.5, 4.5, 1.6, 0.0),
    "freight_control_tower": ("P1", 95, 0.5, 3.1, 4.3, 0.0),

    "reverse_rma_optimizer": ("P0", 45, 0.6, 0.0, 8.2, 3.1),
    "dynamic_markdown_agent": ("P0", 50, 0.5, 1.6, 0.0, 8.7),
    "rti_balance_reconciler": ("P0", 60, 0.5, 4.2, 2.9, 2.1),
    "keep_it_routing_advisor": ("P1", 90, 0.5, 1.8, 1.4, 3.6),
    "osd_freight_claims_agent": ("P1", 95, 0.6, 0.0, 5.4, 0.0),
    "short_dated_redistributor": ("P1", 115, 0.4, 1.7, 1.1, 3.4),
    "intermodal_rail_linehaul_agent": ("P1", 110, 0.4, 3.9, 0.0, 1.1),
    "sanitation_health_agent": ("P1", 120, 0.4, 0.0, 4.1, 0.0),
    "food_waste_esg_copilot": ("P2", 165, 0.5, 0.0, 1.9, 0.9),
}

PILLAR_STYLE = {
    "demand_sop": {"num": "01", "scor": "Planning & Strategy", "color": "#3186FF", "ink": "#286DD1", "photo": "sc_plan_source.png", "title": "Planning & Strategy", "shortFor": "POS, Q-Commerce & S&OP consensus", "svgType": "demand_wave", "flagship": "demand_sensing_agent", "proofLabel": "Unilever · 104-Wk ML Forecast", "proofUrl": "https://www.unilever.com/news/press-and-media/press-releases/2026/google-cloud-partnership-pioneers-next-generation-of-consumer-goods-technologies"},
    "sourcing_procurement": {"num": "02", "scor": "Sourcing & Procurement", "color": "#FC413D", "ink": "#C62A27", "photo": "sc_source.png", "title": "Sourcing & Procurement", "shortFor": "Agri/Mandi, Tier-N risk & 3-Way Match", "svgType": "supplier_graph", "flagship": "tier_n_risk_sentinel", "proofLabel": "Gartner · Tier-2+ Visibility Gap", "proofUrl": "https://www.gartner.com/en/newsroom/press-releases/2026-04-07-gartner-forecasts-supply-chain-management-software-with-agentic-ai-will-grow-to-53-billion-in-spend-by-2030"},
    "manufacturing_prod": {"num": "03", "scor": "Manufacturing & Production", "color": "#D97706", "ink": "#8A6200", "photo": "sc_make_fulfill.png", "title": "Manufacturing & Production", "shortFor": "ICML finite scheduling, Co-Packers & QA", "svgType": "plant_oee", "flagship": "finite_production_scheduler", "proofLabel": "GE Appliances · 800+ Factory Agents", "proofUrl": "https://cloud.google.com/blog/topics/google-cloud-next/welcome-to-google-cloud-next26"},
    "inventory_warehouse": {"num": "04", "scor": "Inventory & Warehousing", "color": "#4B31E3", "ink": "#4B31E3", "photo": "sc_fulfill.png", "title": "Inventory & Warehousing", "shortFor": "FEFO shelf-life, MEIO & DMS balancing", "svgType": "meio_buffer", "flagship": "meio_safety_stock_agent", "proofLabel": "Home Depot · 2,300+ Stores Grounded", "proofUrl": "https://cloud.google.com/customers/the-home-depot"},
    "logistics_fleet": {"num": "05", "scor": "Distribution & Logistics", "color": "#0A7684", "ink": "#0A7684", "photo": "sc_deliver_return.png", "title": "Distribution & Logistics", "shortFor": "Linehaul, E-Way bills & Freight audit", "svgType": "freight_corridor", "flagship": "fleetflow_dispatch", "proofLabel": "Capgemini · 41%→53% Last-Mile Cost", "proofUrl": "https://www.capgemini.com/insights/research-library/the-last-mile-delivery-challenge/"},
    "circular_enable": {"num": "06", "scor": "Returns & Reverse Logistics", "color": "#00AF57", "ink": "#007F3F", "photo": "sc_return.png", "title": "Returns & Reverse Logistics", "shortFor": "RMA triage, Fresh markdowns & EPR/RTI", "svgType": "circular_loop", "flagship": "reverse_rma_optimizer", "proofLabel": "WEF · -62% Disruption Response", "proofUrl": "https://www.weforum.org/agenda/2026/09/how-agentic-ai-is-reshaping-supply-chain-resilience/"},
}

SYSTEM_BY_DEPT = {
    "demand_sop": "SAP IBP · DMS · Retail POS",
    "sourcing_procurement": "SAP Ariba · S/4HANA MM · Mandi Feeds",
    "manufacturing_prod": "SAP PP · Siemens Opcenter MES · LIMS",
    "inventory_warehouse": "Manhattan WMS · SAP EWM · DMS Stock",
    "logistics_fleet": "Oracle OTM · SAP TM · NIC E-Way API",
    "circular_enable": "SAP CRM · Returns Ledger · CPCB EPR",
}

NOT_OWNED_BY_DEPT = {
    "demand_sop": [
        {"task": "Changing printed Maximum Retail Price (MRP) on packaging", "owner": "Commercial Pricing & Legal"},
        {"task": "Executing physical plant overtime or co-packer shifts", "owner": "Plant Operations Manager"},
        {"task": "Signing binding annual Modern Trade JBP contracts", "owner": "VP Sales & Finance"},
    ],
    "sourcing_procurement": [
        {"task": "Executing speculative commodity futures derivatives", "owner": "Corporate Treasury Committee"},
        {"task": "Releasing raw material lots failing food-safety micro specs", "owner": "Head of Quality Assurance"},
        {"task": "Authorizing bank wire disbursements to vendors", "owner": "Treasury & Financial Controller"},
    ],
    "manufacturing_prod": [
        {"task": "Bypassing HACCP pasteurization or allergen washdown holds", "owner": "Plant Quality & Food Safety Lead"},
        {"task": "Physical lockout/tagout (LOTO) maintenance execution", "owner": "Certified Shift Maintenance Engineer"},
        {"task": "Approving multi-million-dollar new line CapEx", "owner": "Board Investment Committee"},
    ],
    "inventory_warehouse": [
        {"task": "Waiving retailer Minimum Remaining Shelf-Life (MRSL) terms", "owner": "Key Account Commercial Lead"},
        {"task": "Writing off expired inventory lots on financial books", "owner": "Plant / Regional Finance Controller"},
        {"task": "Overriding credit blocks on overdue distributors", "owner": "Commercial Credit Control"},
    ],
    "logistics_fleet": [
        {"task": "Driving hours-of-service safety overrides", "owner": "Fleet Safety Officer & Carrier"},
        {"task": "Filing statutory tax litigation on seized E-Way cargo", "owner": "Indirect Tax & Legal Counsel"},
        {"task": "Releasing cold-chain loads after severe thermal excursion", "owner": "Cold-Chain QA Director"},
    ],
    "circular_enable": [
        {"task": "Terminating wholesale stockist contracts for diversion", "owner": "National Sales Director & Legal"},
        {"task": "Filing statutory CPCB / EU sustainability disclosures", "owner": "Chief Sustainability Officer & Board"},
        {"task": "Releasing returned food/personal-care stock into food chain", "owner": "QA & Regulatory Compliance"},
    ],
}

VIDEO_BY_DEPT = {
    "demand_sop": "demand_sensing_demo.mp4",
    "sourcing_procurement": "o2d_suite_demo.mp4",
    "manufacturing_prod": "o2d_suite_demo.mp4",
    "inventory_warehouse": "smart_warehouse_demo.mp4",
    "logistics_fleet": "fleetflow_dispatch_demo.mp4",
    "circular_enable": "f2f_fleet_demo.mp4",
}
VIDEO_BY_AGENT = {
    "demand_sensing_agent": "demand_sensing_demo.mp4",
    "promo_lift_simulator": "promo_lift_simulator_demo.mp4",
}

# Build unified 78-Agent Registry
all_agents_map = {}

# 1. Load all 60 original agents first (zero overwrites!)
for aid, a in cat["agents"].items():
    st = PILLAR_STYLE[a["deptId"]]
    dep_info = deployed_map.get(aid)
    tier, payback, prod, flow, shield, recov = BASE_60_META.get(aid, ("P1", 100, 0.5, 2.0, 2.0, 1.0))
    tot_val = round(prod + flow + shield + recov, 1)
    subs = a.get("subAgents", [])
    reads = subs[0]["role"] if len(subs) > 0 else f"Ingests {SYSTEM_BY_DEPT[a['deptId']]} and BigQuery Cortex v7 tables."
    does = subs[1]["role"] if len(subs) > 1 else (a.get("solverStack") or "Runs Vertex AI TimesFM & OR-Tools deterministic optimization.")
    returns = subs[2]["role"] if len(subs) > 2 else (a.get("outcome") or "Produces ranked exception action table and A2UI visual brief.")
    ge_full = dep_info.get("gemini_enterprise_agent", "") if dep_info else ""
    ge_short = ge_full.split("/")[-1] if ge_full else ""
    ge_url = (
        f"https://vertexaisearch.cloud.google.com/home/cid/{GE_CID}/r/agent/{ge_short}/session/-?mods=&authuser={GE_AUTH}"
        if ge_short else GE_WORKSPACE_URL
    )
    vfile = VIDEO_BY_AGENT.get(aid) or VIDEO_BY_DEPT.get(a["deptId"], "demand_sensing_demo.mp4")

    all_agents_map[aid] = {
        "id": aid,
        "code": f"CPG-{st['num']}-{len([x for x in all_agents_map.values() if x['deptId']==a['deptId']])+1:02d}",
        "isNewCpgAgent": False,
        "deptId": a["deptId"],
        "deptTitle": st["title"],
        "deptColor": st["color"],
        "deptInk": st["ink"],
        "subPillarName": a.get("subPillarName", ""),
        "name": a["name"],
        "priorityTier": tier,  # P0 | P1 | P2
        "prioBoard": "first" if tier == "P0" else ("next" if tier == "P1" else "routine"),
        "paybackDays": payback,
        "prod": prod, "flow": flow, "shield": shield, "recov": recov,
        "annualValueM": tot_val,
        "oneLine": a.get("shortDesc") or a.get("outcome") or "",
        "outcome": a.get("outcome") or a.get("shortDesc") or "",
        "problem": a.get("problem") or "",
        "reads": f"{reads} Connected CPG systems: {SYSTEM_BY_DEPT[a['deptId']]}.",
        "does": f"{does} ({a.get('solverStack', 'BigQuery ML + Google OR-Tools')}).",
        "returns": f"{returns} Stages policy-checked action via {a.get('apiWriteback', 'Apigee MCP')}.",
        "stopsAt": f"Never commits unapproved {SYSTEM_BY_DEPT[a['deptId']].split('·')[0].strip()} ledger mutations or overrides safety/contract policy without human sign-off.",
        "safetyEnvelope": "Flags missing sensor/ERP records for human review rather than extrapolating unverified values.",
        "samplePrompt": f"Show me our highest-priority {a.get('subPillarName', 'supply chain').lower()} exceptions across our CPG plants and CFA hubs this week, quantify margin at risk, and recommend corrective actions.",
        "liveInGE": dep_info is not None,
        "geUrl": ge_url,
        "videoSrc": f"assets/media/video/{vfile}",
        "model": "gemini-3.1-pro-preview",
        "primaryPersonaId": a.get("primaryPersonaId", ""),
    }

# 2. Add the 18 new CPG agents cleanly
for na in NEW_CPG_AGENTS:
    aid = na["id"]
    st = PILLAR_STYLE[na["deptId"]]
    tot_val = round(na["prod"] + na["flow"] + na["shield"] + na["recov"], 1)
    vfile = VIDEO_BY_DEPT.get(na["deptId"], "demand_sensing_demo.mp4")
    all_agents_map[aid] = {
        "id": aid,
        "code": f"CPG-{st['num']}-N{len([x for x in all_agents_map.values() if x['deptId']==na['deptId'] and x['isNewCpgAgent']])+1:02d}",
        "isNewCpgAgent": True,
        "deptId": na["deptId"],
        "deptTitle": st["title"],
        "deptColor": st["color"],
        "deptInk": st["ink"],
        "subPillarName": na["subPillarName"],
        "name": na["name"],
        "priorityTier": na["tier"],
        "prioBoard": "first" if na["tier"] == "P0" else ("next" if na["tier"] == "P1" else "routine"),
        "paybackDays": na["paybackDays"],
        "prod": na["prod"], "flow": na["flow"], "shield": na["shield"], "recov": na["recov"],
        "annualValueM": tot_val,
        "oneLine": na["oneLine"],
        "outcome": na["returns"],
        "problem": na["oneLine"],
        "reads": na["reads"],
        "does": na["does"],
        "returns": na["returns"],
        "stopsAt": na["stopsAt"],
        "safetyEnvelope": na["safetyEnvelope"],
        "samplePrompt": f"Run {na['name']} across our active CPG SKUs and CFA depots today—highlight urgent exceptions, margin impact, and what needs sign-off.",
        "liveInGE": False,
        "geUrl": GE_WORKSPACE_URL,
        "videoSrc": f"assets/media/video/{vfile}",
        "model": "gemini-3.1-pro-preview",
        "primaryPersonaId": na["linkedPersonas"][0],
        "linkedPersonas": na["linkedPersonas"],
    }

# Group sub-pillar peers so every single Persona gets a genuine 2-to-4 Agent Suite!
subpillar_agents = {}
for aid, ag in all_agents_map.items():
    key = (ag["deptId"], ag["subPillarName"])
    subpillar_agents.setdefault(key, []).append(aid)

extra_links_by_persona = {}
for na in NEW_CPG_AGENTS:
    for pid in na["linkedPersonas"]:
        extra_links_by_persona.setdefault(pid, []).append(na["id"])

personas = []
for idx, (pid, p) in enumerate(cat["personas"].items(), start=1):
    st = PILLAR_STYLE[p["deptId"]]
    pcode = f"P{idx:02d}"
    human_name, human_setting = PERSONA_HUMANS[idx - 1]
    primary_aid = p.get("primaryAgentId", "")
    primary_ag = all_agents_map[primary_aid]

    # Assemble this persona's 2-to-4 Agent Suite (Primary Agent + New CPG Agent(s) + Sub-pillar Collaborator)
    suite_ids = [primary_aid]
    for xid in extra_links_by_persona.get(pid, []):
        if xid not in suite_ids:
            suite_ids.append(xid)
    for peer_id in subpillar_agents.get((p["deptId"], p.get("subPillarName", "")), []):
        if peer_id not in suite_ids and len(suite_ids) < 3:
            suite_ids.append(peer_id)
    suite_ids = suite_ids[:4]

    raw_before = p.get("toilHoursBefore", 26)
    raw_after = p.get("toilHoursAfter", 6)
    b_num = float(re.findall(r"[\d.]+", str(raw_before))[0]) if re.findall(r"[\d.]+", str(raw_before)) else 26.0
    a_num = float(re.findall(r"[\d.]+", str(raw_after))[0]) if re.findall(r"[\d.]+", str(raw_after)) else 6.0
    saved_hrs = max(2, round(b_num - a_num))

    # Build rich Agent Suite objects for this persona
    agent_suite = []
    weights = [0.55, 0.28, 0.17] if len(suite_ids) == 3 else ([0.65, 0.35] if len(suite_ids) == 2 else [0.48, 0.24, 0.16, 0.12])
    for s_idx, sid in enumerate(suite_ids):
        ag_obj = all_agents_map[sid]
        w = weights[s_idx] if s_idx < len(weights) else 0.15
        agent_suite.append({
            "n": s_idx + 1,
            "id": sid,
            "code": ag_obj["code"],
            "name": ag_obj["name"],
            "isPrimary": (s_idx == 0),
            "isNewCpgAgent": ag_obj["isNewCpgAgent"],
            "priorityTier": ag_obj["priorityTier"],
            "paybackDays": ag_obj["paybackDays"],
            "annualValueM": ag_obj["annualValueM"],
            "roleShareHrs": round(saved_hrs * w, 1),
            "oneLine": ag_obj["oneLine"],
            "reads": ag_obj["reads"],
            "does": ag_obj["does"],
            "returns": ag_obj["returns"],
            "stopsAt": ag_obj["stopsAt"],
            "safetyEnvelope": ag_obj["safetyEnvelope"],
            "liveInGE": ag_obj["liveInGE"],
            "geUrl": ag_obj["geUrl"],
            "videoSrc": ag_obj["videoSrc"],
        })

    # Non-double-counted Persona Value: Primary Agent + any New CPG Agent owned primarily by this persona
    owned_agent_ids = [primary_aid] + [
        na["id"] for na in NEW_CPG_AGENTS if na["linkedPersonas"][0] == pid
    ]
    p_prod = round(sum(all_agents_map[x]["prod"] for x in owned_agent_ids), 1)
    p_flow = round(sum(all_agents_map[x]["flow"] for x in owned_agent_ids), 1)
    p_shield = round(sum(all_agents_map[x]["shield"] for x in owned_agent_ids), 1)
    p_recov = round(sum(all_agents_map[x]["recov"] for x in owned_agent_ids), 1)
    p_total = round(p_prod + p_flow + p_shield + p_recov, 1)

    p_tier = "P0" if any(all_agents_map[x]["priorityTier"] == "P0" for x in owned_agent_ids) else primary_ag["priorityTier"]
    b_prio = "first" if p_tier == "P0" else ("next" if p_tier == "P1" else "routine")

    if b_prio == "first":
        p1, p2, p3, p4, p5 = "first", "first", "next", "next", "routine"
        w1, w2, w3, w4, w5 = 0.36, 0.28, 0.18, 0.12, 0.06
    elif b_prio == "next":
        p1, p2, p3, p4, p5 = "next", "next", "next", "routine", "routine"
        w1, w2, w3, w4, w5 = 0.32, 0.26, 0.20, 0.14, 0.08
    else:
        p1, p2, p3, p4, p5 = "routine", "routine", "routine", "routine", "routine"
        w1, w2, w3, w4, w5 = 0.28, 0.24, 0.20, 0.16, 0.12

    focus = p.get("focusAreas", [])
    sys_name = SYSTEM_BY_DEPT[p["deptId"]]
    s2_ag = agent_suite[1] if len(agent_suite) > 1 else agent_suite[0]

    actions = [
        {"code": f"{pcode}W01", "title": focus[0] if len(focus) > 0 else f"Live {p.get('subPillarName')} Sensing", "own": "agentic", "prio": p1, "valueM": round(p_total * w1, 2),
         "today": f"Manual CSV & portal checks across {sys_name} ({int(b_num)}h/wk toil).",
         "withAgent": f"{primary_ag['name']} continuously grounds telemetry and flags exceptions early.",
         "agentName": primary_ag["name"], "agentId": primary_aid, "liveInGE": primary_ag["liveInGE"], "cadence": "Continuous"},
        {"code": f"{pcode}W02", "title": focus[1] if len(focus) > 1 else f"{s2_ag['name']} Optimization", "own": "agentic", "prio": p2, "valueM": round(p_total * w2, 2),
         "today": "Static ERP rules miss shelf-life, Q-Commerce velocity, or tariff constraints.",
         "withAgent": f"{s2_ag['name']} runs deterministic math to rank margin-optimal options.",
         "agentName": s2_ag["name"], "agentId": s2_ag["id"], "liveInGE": s2_ag["liveInGE"], "cadence": "Event-driven"},
        {"code": f"{pcode}W03", "title": focus[2] if len(focus) > 2 else "Cross-Echelon Trade-Off Sync", "own": "agentic", "prio": p3, "valueM": round(p_total * w3, 2),
         "today": "Phone & email escalations across ICML plants, CFA depots, and buyers.",
         "withAgent": "Agent suite reconciles working capital, FEFO shelf-life, and OTIF service.",
         "agentName": primary_ag["name"], "agentId": primary_aid, "liveInGE": primary_ag["liveInGE"], "cadence": "Daily"},
        {"code": f"{pcode}W04", "title": "Staged MCP Write-Back Proposal", "own": "agentic", "prio": p4, "valueM": round(p_total * w4, 2),
         "today": "Manual screen-by-screen transaction entry inside core ERP/WMS.",
         "withAgent": "Stages policy-checked transaction via Apigee MCP awaiting 1-click sign-off.",
         "agentName": primary_ag["name"], "agentId": primary_aid, "liveInGE": primary_ag["liveInGE"], "cadence": "On approval"},
        {"code": f"{pcode}W05", "title": "Exception & Audit Substantiation", "own": "agentic", "prio": p5, "valueM": round(p_total * w5, 2),
         "today": "Hours compiling variance decks and deduction claim proofs.",
         "withAgent": "Auto-generates cited BigQuery Cortex v7 ledger packet.",
         "agentName": s2_ag["name"], "agentId": s2_ag["id"], "liveInGE": s2_ag["liveInGE"], "cadence": "Weekly"},
        {"code": f"{pcode}W06", "title": f"{sys_name.split('·')[0].strip()} Ledger Commit", "own": "system", "prio": "", "valueM": 0,
         "holder": sys_name.split("·")[0].strip(), "reason": "Core financial & inventory postings remain in system of record; zero rip-and-replace.", "cadence": "Transactional"},
        {"code": f"{pcode}W07", "title": "Master Data & Statutory Controls", "own": "system", "prio": "", "valueM": 0,
         "holder": sys_name.split("·")[0].strip(), "reason": "SKU MRP master, tax codes, and role permissions remain locked in core ERP.", "cadence": "Continuous"},
        {"code": f"{pcode}W08", "title": f"{human_name.split()[0]}'s Final Sign-Off", "own": "human", "prio": "", "valueM": 0,
         "holder": f"{human_name} ({p['name']})", "reason": "Commercial trade-offs, vendor awards, and safety/QA releases stay strictly human.", "cadence": "Policy gate"},
    ]

    personas.append({
        "id": pid,
        "code": pcode,
        "personName": human_name,
        "setting": human_setting,
        "deptId": p["deptId"],
        "deptTitle": st["title"],
        "scor": st["scor"],
        "deptColor": st["color"],
        "deptInk": st["ink"],
        "subPillarId": p.get("subPillarId", ""),
        "subPillarName": p.get("subPillarName", ""),
        "name": p["name"],  # Role title preserved
        "whatTheyDo": p.get("summary") or p.get("mandate") or "",
        "whyItMatters": f"In high-velocity CPG operations across {human_setting}, delayed visibility directly triggers Modern Trade OTIF penalties, FEFO shelf-life write-offs, or unrecovered trade/freight leakage.",
        "systemsTouched": sys_name,
        "notOwned": NOT_OWNED_BY_DEPT[p["deptId"]],
        "honestLimit": f"Agents prepare deterministic scenarios and stage ERP/WMS actions, but {human_name} retains final commercial, safety, and counterparty accountability.",
        "headlineStat": p.get("headlineStat", ""),
        "toilHoursBefore": int(b_num),
        "toilHoursAfter": int(a_num),
        "savedHrs": saved_hrs,
        "primaryAgentId": primary_aid,
        "primaryAgentName": primary_ag["name"],
        "liveInGE": any(s["liveInGE"] for s in agent_suite),
        "priorityTier": p_tier,
        "prioBoard": b_prio,
        "paybackDays": primary_ag["paybackDays"],
        "val": {"prod": p_prod, "flow": p_flow, "shield": p_shield, "recov": p_recov, "total": p_total},
        "annualValueM": p_total,
        "agentSuite": agent_suite,
        "actions": actions,
    })

departments = []
for dept_id, d in cat["departments"].items():
    st = PILLAR_STYLE[dept_id]
    dept_agents = [a for a in all_agents_map.values() if a["deptId"] == dept_id]
    p_by_id = {x["id"]: x for x in personas}
    sub_pillars = []
    for sp in d.get("subPillars", []):
        items = []
        for it in sp.get("items", []):
            p_obj = p_by_id[it["personaId"]]
            items.append({
                "personaId": p_obj["id"],
                "personaCode": p_obj["code"],
                "personName": p_obj["personName"],
                "personaName": p_obj["name"],
                "setting": p_obj["setting"],
                "suiteCount": len(p_obj["agentSuite"]),
                "suiteNames": [s["name"] for s in p_obj["agentSuite"]],
                "agentId": p_obj["primaryAgentId"],
                "agentName": p_obj["primaryAgentName"],
                "priorityTier": p_obj["priorityTier"],
                "annualValueM": p_obj["annualValueM"],
                "desc": p_obj["whatTheyDo"],
                "outcome": all_agents_map[p_obj["primaryAgentId"]]["oneLine"],
                "liveInGE": p_obj["liveInGE"],
            })
        sub_pillars.append({
            "id": sp["id"],
            "name": sp["name"],
            "story": f"CPG {sp['name']} across ICML plants, CFA state depots, General Trade DMS, Modern Trade & Quick-Commerce.",
            "items": items,
        })

    departments.append({
        "id": dept_id,
        "num": st["num"],
        "scor": st["scor"],
        "title": st["title"],
        "shortFor": st["shortFor"],
        "photo": st["photo"],
        "color": st["color"],
        "ink": st["ink"],
        "svgType": st["svgType"],
        "proofLabel": st["proofLabel"],
        "proofUrl": st["proofUrl"],
        "flagshipAgentId": st["flagship"],
        "coreQuestion": d.get("coreQuestion", "").strip(),
        "systems": SYSTEM_BY_DEPT[dept_id],
        "subPillars": sub_pillars,
        "personaCount": len(d.get("personaIds", [])),
        "agentCount": len(dept_agents),
        "newAgentCount": sum(1 for x in dept_agents if x["isNewCpgAgent"]),
        "p0Count": sum(1 for x in dept_agents if x["priorityTier"] == "P0"),
        "liveCount": sum(1 for x in dept_agents if x["liveInGE"]),
    })

payload = {
    "meta": {
        "domain": "CPG Multi-Echelon Supply Chain",
        "pillars": len(departments),
        "subPillars": sum(len(d["subPillars"]) for d in departments),
        "personas": len(personas),
        "baseAgents": 60,
        "newCpgAgents": len(NEW_CPG_AGENTS),
        "agents": len(all_agents_map),
        "p0Agents": sum(1 for a in all_agents_map.values() if a["priorityTier"] == "P0"),
        "liveInGE": sum(1 for a in all_agents_map.values() if a["liveInGE"]),
    },
    "departments": departments,
    "personas": personas,
    "agents": list(all_agents_map.values()),
}

with open(OUT_DATA, "w", encoding="utf-8") as f:
    f.write("window.SC_DATA = ")
    json.dump(payload, f, separators=(",", ":"))
    f.write(";\n")

# Emit matching sc_value_model.js reading seamlessly from p.val + BY_AGENT
by_agent_js = {
    aid: {
        "tier": "first" if ag["priorityTier"] == "P0" else ("next" if ag["priorityTier"] == "P1" else "routine"),
        "priorityCode": ag["priorityTier"],
        "isNewCpg": ag["isNewCpgAgent"],
        "paybackDays": ag["paybackDays"],
        "prod": ag["prod"], "flow": ag["flow"], "shield": ag["shield"], "recov": ag["recov"],
        "why": ag["oneLine"],
    }
    for aid, ag in all_agents_map.items()
}

val_js_code = """/* CPG Supply Chain 4-Lever Value & Priority Model (60 Personas · 78 Agents: 60 Core + 18 New CPG Use Cases) */
window.SC_VALUES = (function () {
  var ESTATE_BASELINE = {
    label: "$5.0B COGS / $8.0B Revenue Multi-Site CPG Enterprise Benchmark (ICML Plants · CFA Depots · DMS · Modern Trade · Q-Commerce)",
    loadedRateHr: 105
  };
  var LEVERS = [
    { id: "prod", name: "Productivity & Redeployment", color: "#3186FF", unit: "$M/yr", def: "Planner, buyer, QA & dispatcher hours reclaimed from ERP/DMS spreadsheets and redeployed to commercial & supplier negotiations." },
    { id: "flow", name: "Flow & Working Capital", color: "#00AF57", unit: "$M/yr", def: "22% annual carrying cost saved via Multi-Echelon Inventory Optimization (MEIO) & FEFO, ICML changeover OEE hours, and 3D trailer consolidation." },
    { id: "shield", name: "Leakage & Risk Shield", color: "#4B31E3", unit: "$M/yr", def: "Hard cash protected across 3-way match, freight & trade-deduction audits, Co-Packer scrap, E-Way bill fines, and Tier-2+/recall containment." },
    { id: "recov", name: "Revenue & Salvage Recovery", color: "#12B5CB", unit: "$M/yr", def: "Incremental gross margin saved from Quick-Commerce & shelf stockout prevention, DMS secondary balancing, dynamic markdowns & RMA triage." }
  ];
  var BY_AGENT = """ + json.dumps(by_agent_js, separators=(",", ":")) + """;
  function r1(n) { return Math.round((n || 0) * 10) / 10; }
  function computeForPersonas(personas) {
    var byPersonaId = {}, byDeptId = {};
    var estateTotals = { prod: 0, flow: 0, shield: 0, recov: 0, total: 0, savedHrsWk: 0, personas: 0, firstCount: 0, nextCount: 0, routineCount: 0 };
    (personas || []).forEach(function (p) {
      var v = p.val || { prod: 0.5, flow: 1.5, shield: 1.5, recov: 1.0, total: 4.5 };
      var tier = p.prioBoard || "next";
      var rec = {
        personaId: p.id, agentId: p.primaryAgentId, deptId: p.deptId,
        tier: tier, priorityCode: p.priorityTier || "P1", paybackDays: p.paybackDays || 90,
        prod: v.prod, flow: v.flow, shield: v.shield, recov: v.recov, total: v.total,
        why: (BY_AGENT[p.primaryAgentId] && BY_AGENT[p.primaryAgentId].why) || p.whatTheyDo
      };
      byPersonaId[p.id] = rec;
      if (!byDeptId[p.deptId]) byDeptId[p.deptId] = { prod: 0, flow: 0, shield: 0, recov: 0, total: 0, savedHrsWk: 0, personas: 0, firstCount: 0, nextCount: 0, routineCount: 0 };
      var d = byDeptId[p.deptId];
      d.prod = r1(d.prod + v.prod); d.flow = r1(d.flow + v.flow); d.shield = r1(d.shield + v.shield); d.recov = r1(d.recov + v.recov); d.total = r1(d.total + v.total);
      d.savedHrsWk += (p.savedHrs || 0); d.personas += 1;
      if (tier === "first") d.firstCount += 1; else if (tier === "next") d.nextCount += 1; else d.routineCount += 1;

      estateTotals.prod = r1(estateTotals.prod + v.prod); estateTotals.flow = r1(estateTotals.flow + v.flow);
      estateTotals.shield = r1(estateTotals.shield + v.shield); estateTotals.recov = r1(estateTotals.recov + v.recov);
      estateTotals.total = r1(estateTotals.total + v.total); estateTotals.savedHrsWk += (p.savedHrs || 0); estateTotals.personas += 1;
      if (tier === "first") estateTotals.firstCount += 1; else if (tier === "next") estateTotals.nextCount += 1; else estateTotals.routineCount += 1;
    });
    return { byPersonaId: byPersonaId, byDeptId: byDeptId, estateTotals: estateTotals };
  }
  return { ESTATE_BASELINE: ESTATE_BASELINE, LEVERS: LEVERS, BY_AGENT: BY_AGENT, computeForPersonas: computeForPersonas };
})();
"""

with open(OUT_VAL, "w", encoding="utf-8") as f:
    f.write(val_js_code)

print(f"Built CPG Portal Data: {len(personas)} named personas, {len(all_agents_map)} agents (60 base + {len(NEW_CPG_AGENTS)} new CPG), {payload['meta']['p0Agents']} P0 agents.")
