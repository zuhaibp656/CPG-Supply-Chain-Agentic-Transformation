#!/usr/bin/env python3
"""Builds the CPG Supply Chain Portal Data & Researched 4-Lever Value Model:
  - Preserves ALL 60 original Personas (P01..P60) & ALL 60 original Agents untouched by ID/name,
    plus 18 researched CPG Supply Chain Agents = 78 Agents Total.
  - Enforces strict, well-researched 4-Lever Attribution (`Productivity`, `Flow & Capital`,
    `Risk & Leakage`, `Revenue Recovery`) with LOAD-BEARING ZEROS:
      * 56 of 78 Agents (72%) move ONLY 2 Levers (Productivity + 1 operational/financial lever)
      * 22 of 78 Agents (28%) move 3 Levers (Productivity + 2 coupled levers)
      * 0 of 78 Agents claim all 4 Levers!
  - Generates 12 authentic, non-generic CPG operational workflows per Persona (60 × 12 = 720 cells)
    for the Amandeep-style Workforce & Workflow Chessboard (`personas/index.html`).
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


def fmt_inr(cr: float) -> str:
    """Formats a value denominated in Indian Crores (1 Cr = 100 Lakhs) as ₹X,XXX.X Cr or ₹XX L."""
    n = float(cr or 0.0)
    if n <= 0:
        return "—"
    if n >= 1000:
        return f"₹{n:,.1f} Cr"
    if n >= 1.0:
        return f"₹{n:.1f} Cr"
    lakhs = max(1, round(n * 100))
    return f"₹{lakhs} L"


def to_inr_prose(text: str) -> str:
    """Converts any legacy USD / million / billion prose references from base_60_catalog into Indian Rupees (₹ Cr / ₹ L / ₹)."""
    if not text:
        return ""
    s = str(text)
    s = re.sub(r"multi-million-dollar", "multi-crore", s, flags=re.I)
    s = re.sub(r"\$1\.77\s*Trillion|\$1\.77T", "₹148 Lakh Cr", s, flags=re.I)
    s = re.sub(r"\$1\.2T", "₹100 Lakh Cr", s, flags=re.I)
    s = re.sub(r"\$570B", "₹48 Lakh Cr", s, flags=re.I)

    def _repl_money(m: re.Match) -> str:
        num = float(m.group(1).replace(",", ""))
        unit = (m.group(2) or "").strip().lower()
        if unit in ("t", "trillion"):
            return f"₹{round(num * 83.5):,} Lakh Cr"
        if unit in ("b", "bn", "billion"):
            cr = num * 8350.0
            if cr >= 100000:
                return f"₹{cr / 100000.0:.2f} Lakh Cr"
            return f"₹{round(cr):,} Cr"
        if unit in ("m", "mn", "million"):
            cr = num * 8.35
            return f"₹{cr:.1f} Cr" if cr < 100 else f"₹{round(cr):,} Cr"
        if unit in ("k", "thousand"):
            lakhs = (num * 83.5) / 100.0
            return f"₹{lakhs:.1f} L" if lakhs >= 1.0 else f"₹{round(num * 83.5) * 1000:,}"
        inr_val = num * 45.0 if num >= 20 else num * 35.0
        if inr_val >= 100000:
            return f"₹{inr_val / 100000.0:.1f} L"
        if inr_val >= 100:
            return f"₹{int(round(inr_val, -1)):,}"
        return f"₹{int(round(inr_val))}"

    s = re.sub(
        r"\$([0-9][0-9,]*(?:\.[0-9]+)?)\s*(Trillion|Billion|Million|Thousand|bn|mn|T|B|M|K)?\b",
        _repl_money,
        s,
        flags=re.I,
    )
    s = re.sub(r"\bUSD\b", "INR", s)
    s = re.sub(r"\bdollar(s)?\b", r"rupee\1", s, flags=re.I)
    return s


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
        "savedHoursWk": 11,
        "linkedPersonas": ["demand_planner_forecaster", "commercial_planning_lead", "store_operations_omni_lead"],
        "oneLine": "Monitors 15-minute Blinkit, Zepto & Instacart dark-store sell-out spikes and local weather to trigger micro-replenishments before 10-minute delivery tiles go out of stock.",
        "reads": "15-min Q-Commerce partner dark-store inventory feeds, hyper-local PIN-code search trends, WeatherNext 3 rain/heat bursts, and urban Mother-Hub stock (`01_daily_pos_dms_qcomm_velocity.csv`).",
        "does": "Imputes censored dark-store stockout velocity using BigQuery ML TimesFM 2.5 and ranks urgent milk-run top-up totes across 420 urban dark stores.",
        "returns": "PIN-code-ranked micro-replenishment wave table + A2UI velocity surge card ready for 1-click urban dispatch.",
        "stopsAt": "Overriding contractual Quick-Commerce margin terms or committing emergency 3PL rider surge fees without Commercial Lead sign-off.",
        "safetyEnvelope": "Falls back to 7-day rolling dark-store baseline if partner API latency exceeds 30 minutes.",
        "subWorkflows": [
            ("Impute censored 15-min Blinkit & Zepto dark-store stockout velocity", "Partner APIs drop to zero scans once a dark-store bin empties, hiding true evening demand.", "Unimputed zero-scans starve the next morning's milk-run replenishment and forfeit 10-minute impulse orders."),
            ("Fuse PIN-code WeatherNext 3 rain/heat bursts into urban tote queues", "Planners check city-wide weekly weather manually rather than hyper-local 2-km PIN-code bursts.", "Beverage, ice-cream, and snack SKUs stock out across 420 dark stores within 90 minutes of a heat spike."),
        ],
    },
    {
        "id": "festival_monsoon_surge_planner",
        "deptId": "demand_sop",
        "subPillarId": "sop_ibp",
        "subPillarName": "S&OP / IBP",
        "name": "Festival & Monsoon Surge Planner",
        "tier": "P1",
        "paybackDays": 85,
        "savedHoursWk": 8,
        "linkedPersonas": ["sop_supply_planning_dir", "brand_innovation_mgr", "ibp_lead_chief_planning_off"],
        "oneLine": "Aligns movable regional festival calendars (Diwali, Eid, Onam, Lunar New Year) and monsoon onset shifts with gift-pack pre-builds 10 weeks ahead.",
        "reads": "Historical lunar-adjusted festival sell-through, IMD/WeatherNext monsoon onset ensembles, gift-box co-packing capacity, and CFA storage limits.",
        "does": "Runs date-shifted causal lift decomposition and finite pre-build optimization in OR-Tools so seasonal SKUs peak without post-festival markdowns.",
        "returns": "State-by-state pre-build & allocation schedule comparing P50 vs P90 monsoon/festival demand scenarios.",
        "stopsAt": "Locking third-party seasonal warehouse leases or authorizing overtime factory shifts.",
        "safetyEnvelope": "Caps pre-build exposure on single-season gift packs at 85% of prior-year sell-through unless signed off.",
        "subWorkflows": [
            ("Shift Gregorian ERP baselines to movable Diwali, Eid & Onam lunar dates", "Standard ERP year-over-year baselines compare October to October even when Diwali shifts by 19 days.", "Factories pre-build festive gift packs 3 weeks late or dump unsold seasonal cartons at 40% markdown."),
            ("Reconcile monsoon-onset regional demand shifts with CFA pre-positioning", "Regional planners adjust monsoon tea, soup, and personal-care allocations only after rainfall hits.", "Delayed CFA stock positioning misses the first 14 days of peak seasonal category uplift."),
        ],
    },
    {
        "id": "rgm_pack_price_architecture_agent",
        "deptId": "demand_sop",
        "subPillarId": "trade_promotion",
        "subPillarName": "Trade Promotion",
        "name": "RGM Price-Pack Architecture Agent",
        "tier": "P1",
        "paybackDays": 90,
        "savedHoursWk": 7,
        "linkedPersonas": ["trade_marketing_manager", "category_manager_portfolio", "commercial_finance_director"],
        "oneLine": "Simulates magic-price-point grammage shifts (₹5/₹10 sachets vs Modern Trade family packs) to protect gross margin under commodity inflation.",
        "reads": "SKU grammage/MRP master (`00_master_skus.jsonl`), cross-pack elasticity matrices, competitor pack trackers, and raw-material COGS drift.",
        "does": "Computes cross-SKU cannibalization and net Revenue Growth Management (RGM) margin contribution across General Trade and Modern Trade.",
        "returns": "Pack-price elasticity waterfall and recommended grammage/slab adjustments by channel.",
        "stopsAt": "Changing printed Maximum Retail Price (MRP) master records or statutory Legal Metrology declarations.",
        "safetyEnvelope": "Blocks any grammage recommendation that violates statutory standard pack-weight rules.",
        "subWorkflows": [
            ("Simulate ₹5/₹10 magic-price-point grammage vs. family-pack cannibalization", "Category teams model pack-weight changes in static spreadsheets without cross-channel elasticity.", "Discounting 1-kg Modern Trade pouches cannibalizes higher-margin General Trade ₹10 sachets in adjacent PIN codes."),
            ("Screen proposed pack-weight shifts against Legal Metrology rules", "Manual compliance checks happen late in artwork design after commercial sign-off.", "Late pack-weight rejections force emergency re-specification and miss seasonal trade-in windows."),
        ],
    },
    {
        "id": "farmgate_agri_commodity_hedger",
        "deptId": "sourcing_procurement",
        "subPillarId": "material_packaging",
        "subPillarName": "Material & Packaging",
        "name": "Farm-Gate Agri & Mandi Procurement Agent",
        "tier": "P0",
        "paybackDays": 45,
        "savedHoursWk": 10,
        "linkedPersonas": ["category_sourcing_mgr_direct", "strategic_sourcing_lead", "procurement_dir_risk_mgr"],
        "oneLine": "Synthesizes daily mandi crop arrivals, satellite soil-moisture yield indices, and CBOT/NCDEX futures to time wheat, edible oil, coffee, and spice forward buys.",
        "reads": "e-Choupal / mandi arrival volumes, moisture & gluten lab grades, Earth Engine crop NDVI, and supplier forward quotes (`02_po_grn_three_way_match_sourcing.csv`).",
        "does": "Scores physical buy-vs-wait windows and optimizes multi-mandi procurement splits factoring inward freight to ICML mills.",
        "returns": "Daily commodity buy window brief + landed mill cost comparison across mandis and Tier-1 processors.",
        "stopsAt": "Executing commodity futures derivatives or committing physical forward contracts above buyer authority.",
        "safetyEnvelope": "Enforces strict food-grade moisture and aflatoxin quality cutoffs before ranking low-price mandi lots.",
        "subWorkflows": [
            ("Correlate daily mandi arrivals & Earth Engine NDVI with NCDEX forward curves", "Agri buyers track regional mandi WhatsApp quotes manually across 60+ procurement centers.", "Buying 10 days after mandi arrival peaks locks in 4–7% higher landed wheat, palm oil, and spice COGS."),
            ("Optimize landed mill cost across mandi moisture grades & inward freight", "Buyers compare raw mandi spot prices without normalizing moisture shrinkage and freight to ICML mills.", "Cheaper high-moisture lots incur drying loss and lab rejections at factory intake."),
        ],
    },
    {
        "id": "artwork_allergen_packaging_gate",
        "deptId": "sourcing_procurement",
        "subPillarId": "material_packaging",
        "subPillarName": "Material & Packaging",
        "name": "Packaging Artwork & Allergen Gate",
        "tier": "P1",
        "paybackDays": 80,
        "savedHoursWk": 9,
        "linkedPersonas": ["packaging_rd_engineer", "regulatory_compliance_lead", "lifecycle_materials_mgr"],
        "oneLine": "Inspects pre-press packaging proofs via Gemini multimodal vision against BOM allergen tables and FSSAI/FDA/EU labeling laws before cylinder engraving.",
        "reads": "PDF/vector laminate proofs, active recipe BOM allergen lists, Legal Metrology font-height rules, and barcode GS1 specs.",
        "does": "Cross-verifies ingredient order, bold allergen callouts, nutritional math, and statutory license numbers pixel-by-pixel.",
        "returns": "Annotated pre-press compliance checklist flagging exact label discrepancies prior to print run.",
        "stopsAt": "Granting final regulatory artwork release or signing print-cylinder purchase orders.",
        "safetyEnvelope": "Routes any multi-language translation or novel health claim directly to Regulatory Affairs.",
        "subWorkflows": [
            ("Verify pre-press laminate artwork proofs against live recipe BOM allergens", "Packaging & QA teams eyeball 6-point ingredient text across 12 regional SKUs before cylinder engraving.", "A single missed soy/nut allergen bolding or wrong FSSAI license triggers printed film scrap and market recall."),
            ("Validate Legal Metrology MRP font height & GS1 barcode contrast", "Manual ruler and PDF layer checks miss subtle print-bleed encroachments on statutory declarations.", "Non-compliant laminate rolls get impounded during state Legal Metrology retail inspections."),
        ],
    },
    {
        "id": "supplier_dynamic_discounting_agent",
        "deptId": "sourcing_procurement",
        "subPillarId": "contract_po_mgmt",
        "subPillarName": "Contract & PO Mgmt",
        "name": "Supplier Dynamic Discounting Optimizer",
        "tier": "P1",
        "paybackDays": 70,
        "savedHoursWk": 6,
        "linkedPersonas": ["accounts_payable_lead", "commercial_sourcing_legal", "buyer_procurement_coord"],
        "oneLine": "Matches verified 3-way-matched vendor invoices against treasury surplus cash and vendor early-pay APR bids to capture risk-free margin.",
        "reads": "Approved AP invoice ledger, vendor cash-need APR offers (`00_multitier_suppliers.jsonl`), and daily treasury hurdle rates.",
        "does": "Solves knapsack allocation of surplus working capital across early-payment discount offers exceeding corporate hurdle APR.",
        "returns": "Ranked early-pay settlement proposal showing exact annualized yield and net cash discount captured.",
        "stopsAt": "Releasing bank wire transfers or altering contracted net payment terms.",
        "safetyEnvelope": "Excludes any invoice with an open GRN quantity variance or quality hold.",
        "subWorkflows": [
            ("Rank 3-way-matched vendor invoices for early-pay dynamic APR discounts", "Static 2%/10 Net 45 terms go uncaptured because AP clears invoices after the 10-day discount window.", "Surplus corporate cash earns overnight money-market rates instead of 14–18% risk-free annualized supplier discounts."),
            ("Screen early-pay candidates against open QA holds & GRN variances", "Manual early-pay runs occasionally settle vendors who have unresolved short-shipments on subsequent lots.", "Pre-paying disputed suppliers weakens commercial leverage on open quality claims."),
        ],
    },
    {
        "id": "plant_energy_utility_peak_shaver",
        "deptId": "manufacturing_prod",
        "subPillarId": "capacity_planning",
        "subPillarName": "Capacity Planning",
        "name": "Plant Boiler & Tariff Peak-Shaver",
        "tier": "P1",
        "paybackDays": 95,
        "savedHoursWk": 6,
        "linkedPersonas": ["plant_operations_manager", "vp_manufacturing_engineering", "supply_chain_ops_director"],
        "oneLine": "Synchronizes heavy Clean-in-Place (CIP) thermal cycles, cold-room pull-downs, and grinding mills with off-peak grid tariffs and rooftop solar windows.",
        "reads": "15-min smart-meter kWh telemetry, state Time-of-Day electricity tariffs, solar output forecasts, and finite line schedule (`03_plant_mes_oee_copacker_genealogy.csv`).",
        "does": "Shifts non-critical thermal/chiller pull-downs out of peak-tariff blocks via CP-SAT without delaying scheduled case output.",
        "returns": "Shift utility schedule cutting peak demand charges and Scope 2 carbon intensity per ton.",
        "stopsAt": "Changing pasteurization kill-step temperatures or overriding cold-room food-safety bounds.",
        "safetyEnvelope": "Hard-locks HACCP thermal safety minimums above all energy-saving objectives.",
        "subWorkflows": [
            ("Shift CIP boiler & cold-room pull-downs out of peak Time-of-Day tariff windows", "Shift supervisors trigger high-draw Clean-in-Place (CIP) steam cycles during 18:00–22:00 peak grid tariff hours.", "Simultaneous boiler and chiller draw breaches contracted kVA demand ceilings and spikes plant utility cost."),
            ("Align batch milling & compressor loads with onsite solar generation curve", "Utility rooms run fixed compressor setpoints regardless of cloud cover or rooftop solar output.", "Curtailed midday solar kWh and avoidable evening grid draw inflate conversion cost per ton."),
        ],
    },
    {
        "id": "copacker_material_yield_reconciler",
        "deptId": "manufacturing_prod",
        "subPillarId": "capacity_planning",
        "subPillarName": "Capacity Planning",
        "name": "Co-Packer BOM & Laminate Scrap Auditor",
        "tier": "P0",
        "paybackDays": 40,
        "savedHoursWk": 9,
        "linkedPersonas": ["external_sourcing_cmo_lead", "continuous_improvement_lead", "master_production_scheduler"],
        "oneLine": "Reconciles raw edible oil, sugar, and printed laminate film rolls issued to third-party co-packers against finished cases received and tolling scrap allowances.",
        "reads": "SAP subcontracting challans (541/543), co-packer batch consumption reports, BOM scrap tolerances, and finished GRNs.",
        "does": "Flags excess film/ingredient usage beyond contractual 1.2% tolerance and computes exact debit-note clawbacks.",
        "returns": "Co-packer mass-balance variance ledger + draft debit-note substantiation packet.",
        "stopsAt": "Posting financial debit memos or terminating CMO tolling allocations.",
        "safetyEnvelope": "Accounts for startup web-threading waste on short promotional runs before flagging anomalies.",
        "subWorkflows": [
            ("Reconcile SAP 541/543 subcontracting challans vs. co-packer finished case GRNs", "External manufacturing teams reconcile third-party co-packer material balances quarterly in Excel.", "Unflagged 2.5–4.0% laminate film and edible-oil usage above contractual 1.2% scrap norms leaks crores annually."),
            ("Normalize co-packer film scrap for short promo run web-threading allowances", "Flat scrap thresholds trigger disputes with honest co-packers running frequent small-batch promo SKUs.", "Automated run-length normalization isolates genuine material shrinkage for clean debit-note recovery."),
        ],
    },
    {
        "id": "lot_genealogy_recall_tracer",
        "deptId": "manufacturing_prod",
        "subPillarId": "quality_compliance",
        "subPillarName": "Quality & Compliance",
        "name": "2-Hour Lot Genealogy & Recall Tracer",
        "tier": "P0",
        "paybackDays": 50,
        "savedHoursWk": 8,
        "linkedPersonas": ["qa_manager_line_inspector", "regulatory_compliance_lead", "shop_floor_shift_lead"],
        "oneLine": "Traverses multi-hop supplier ingredient lots through ICML mixer batches to exact CFA depots and stockist invoices in under 90 seconds—shrinking recall blast radius by 80%.",
        "reads": "Raw-material COA lot logs, MES batch genealogy (`03_plant_mes_oee_copacker_genealogy.csv`), WMS pallet SSCC scans, and DMS stockist dispatch invoices.",
        "does": "Builds bidirectional lot containment graphs isolating only affected sub-batches instead of blanket multi-week plant recalls.",
        "returns": "Surgical lot hold list (exact pallets, CFAs, and distributors) + pre-filled FSSAI/FDA mock-recall trace report.",
        "stopsAt": "Issuing public consumer recall notices or releasing quarantined QA stock.",
        "safetyEnvelope": "Includes adjacent washdown transition batches whenever exact CIP cutover timestamps are missing.",
        "subWorkflows": [
            ("Trace suspect supplier ingredient lot across ICML silos to exact DMS stockists", "Mock recalls require 18–36 hours stitching LIMS certificates, MES batch logs, WMS SSCCs, and DMS invoices.", "Slow traceability forces precautionary multi-week plant holds 5× wider than the contaminated mixer sub-batch."),
            ("Bound recall blast radius across adjacent CIP washdown transition windows", "Manual lot queries miss partial silo heel mixing between consecutive production shifts.", "Graph genealogy isolates exact affected pallet SSCCs in 90 seconds with full FSSAI/FDA audit lineage."),
        ],
    },
    {
        "id": "fefo_shelf_life_allocator",
        "deptId": "inventory_warehouse",
        "subPillarId": "positioning_optimization",
        "subPillarName": "Positioning & Optimization",
        "name": "Dynamic FEFO & Shelf-Life Allocator",
        "tier": "P0",
        "paybackDays": 35,
        "savedHoursWk": 10,
        "linkedPersonas": ["inventory_controller_buyer", "replenishment_planner", "inventory_optimization_lead"],
        "oneLine": "Matches batch-level remaining shelf-life days against channel-specific Minimum Remaining Shelf-Life (MRSL) rules (e.g., 75% Modern Trade vs 55% General Trade) to prevent dock rejections and expiry.",
        "reads": "Batch expiry ledger (`04_fefo_inventory_dms_wms_ledger.csv`), customer MRSL contract rules, and transit days by lane.",
        "does": "Overrides naive FIFO picking with channel-aware First-Expired-First-Out (FEFO) optimization so mid-life lots flow immediately to high-turn General Trade beats.",
        "returns": "Batch-to-order allocation table eliminating Modern Trade MRSL rejections and DC expiry write-offs.",
        "stopsAt": "Shipping any lot past statutory expiry or waiving customer MRSL contract clauses.",
        "safetyEnvelope": "Hard-blocks allocation if transit lead-time + buffer exceeds remaining MRSL threshold.",
        "subWorkflows": [
            ("Match batch remaining shelf-life days to Modern Trade 75% MRSL vs. GT 55% rules", "Default WMS FIFO rules ship freshest lots to local kirana distributors while older batches age past 75% MRSL.", "Modern Trade chains reject full truckloads at receiving docks for missing MRSL by 3 days, incurring reverse freight and write-offs."),
            ("Re-route 60–72% remaining-life CFA batches into fast-turn General Trade beats", "Aging batch reports are reviewed monthly after lots have already crossed liquidation thresholds.", "Channel-aware FEFO clears mid-life stock at 100% wholesale realization weeks before markdown."),
        ],
    },
    {
        "id": "dms_distributor_stock_balancer",
        "deptId": "inventory_warehouse",
        "subPillarId": "omnichannel_visibility",
        "subPillarName": "Omnichannel Visibility",
        "name": "DMS Secondary Stock & Credit Balancer",
        "tier": "P0",
        "paybackDays": 45,
        "savedHoursWk": 11,
        "linkedPersonas": ["key_account_manager", "omnichannel_fulfillment_dir", "store_replenishment_lead"],
        "oneLine": "Monitors Distributor Management System (DMS) secondary stockists to spot where one distributor sits on 45 days of slow stock while an adjacent town stocks out—staging smart replenishment & credit-safe orders.",
        "reads": "DMS daily stockist closing inventory, tertiary kirana beat billings, distributor credit-limit aging, and CFA stock (`04_fefo_inventory_dms_wms_ledger.csv`).",
        "does": "Computes stockist-level Days-of-Inventory (DOI) norms and auto-drafts credit-compliant primary replenishment orders.",
        "returns": "Territory stock-imbalance map + auto-drafted DMS primary order queue.",
        "stopsAt": "Releasing orders to credit-blocked distributors or forcing stockist inter-transfers without consent.",
        "safetyEnvelope": "Respects state tax boundaries and distributor margin structures on every rebalance.",
        "subWorkflows": [
            ("Balance secondary stockist Days-of-Inventory (DOI) across adjacent territory towns", "Month-end primary billing targets push slow SKUs into compliant stockists while high-turn stockists run dry.", "Simultaneous 45-day distributor glut in Town A and kirana stockouts in Town B erode secondary off-take."),
            ("Stage credit-safe primary replenishment orders within distributor exposure limits", "Primary orders drafted by sales officers get blocked late at SAP dispatch due to unmonitored credit aging.", "Pre-checked DMS replenishment orders flow straight through credit gates without stockout lag."),
        ],
    },
    {
        "id": "qcommerce_assortment_micro_slotter",
        "deptId": "inventory_warehouse",
        "subPillarId": "warehouse_operations",
        "subPillarName": "Warehouse Operations",
        "name": "Urban Hub & Dark-Store Micro-Slotter",
        "tier": "P1",
        "paybackDays": 90,
        "savedHoursWk": 8,
        "linkedPersonas": ["dc_operations_mgr", "dc_shift_floor_lead", "inbound_receiving_supervisor"],
        "oneLine": "Re-slots high-velocity consumer packs into golden pick-faces every night based on hourly eCommerce basket co-occurrence so pickers hit <90-second pack times.",
        "reads": "WMS pick-path logs, basket co-affinity pairs, case dimensions, and next-day promo calendar.",
        "does": "Solves ergonomic golden-zone bin assignment minimizing picker walk meters and aisle congestion.",
        "returns": "20-move nightly putaway/re-slot task list for morning shift handoff.",
        "stopsAt": "Co-locating chemical home-care SKUs beside odor-sensitive food items.",
        "safetyEnvelope": "Enforces strict food vs non-food FEFO/hazard segregation in every bin move.",
        "subWorkflows": [
            ("Re-slot urban hub golden pick-faces nightly using basket co-occurrence pairs", "Pick-face bin maps are updated quarterly even though promo & weather velocity shifts every week.", "Pickers walk 35% extra meters across congested aisles, missing rapid dispatch cutoffs."),
            ("Enforce food vs. home-care odor/chemical segregation during dynamic re-slotting", "Ad-hoc floor putaway places scented detergent cartons adjacent to tea and biscuit totes.", "Constraint-checked slotting cuts pick walk distance while guaranteeing zero cross-taint."),
        ],
    },
    {
        "id": "eway_bill_gst_transit_auditor",
        "deptId": "logistics_fleet",
        "subPillarId": "route_carrier",
        "subPillarName": "Route & Carrier",
        "name": "E-Way Bill & Transit Tax Compliance Shield",
        "tier": "P0",
        "paybackDays": 30,
        "savedHoursWk": 9,
        "linkedPersonas": ["freight_controller_claims", "fleet_dispatcher_central_ops", "transport_planner_inbound_mgr"],
        "oneLine": "Cross-checks live truck GPS ETA against statutory E-Way Bill expiry clocks, HSN tax codes, and vehicle transshipment updates so linehaul trucks never suffer highway detention penalties.",
        "reads": "NIC E-Way Bill API validity timestamps, Samsara/GPS truck telemetry, SAP GST invoice HSN codes (`05_tms_shipments_eway_freight_audit.csv`).",
        "does": "Flags trucks within 4 hours of E-Way Bill expiry due to highway congestion or breakdown and prepares Part-B extension drafts.",
        "returns": "Live expiring-waybill alert queue + pre-validated Part-B vehicle/extension payload.",
        "stopsAt": "Submitting statutory tax declarations with unverified vehicle numbers.",
        "safetyEnvelope": "Alerts central dispatch 4 hours prior to midnight expiry window.",
        "subWorkflows": [
            ("Monitor truck GPS ETA against midnight NIC E-Way Bill statutory expiry clocks", "Dispatchers generate E-Way Bills at factory gate out and never track validity when trucks stall at ghats or borders.", "Expired waybills on highway inspection trigger Section 129 cargo seizure and 200% GST penalty."),
            ("Validate Part-B vehicle transshipment & HSN invoice match before state border entry", "Transporters swap breakdown trailers mid-route without updating Part-B vehicle numbers on the portal.", "Pre-validated Part-B extension payloads keep linehaul cargo compliant before midnight cutoffs."),
        ],
    },
    {
        "id": "modern_trade_dock_slot_booker",
        "deptId": "logistics_fleet",
        "subPillarId": "store_replenishment",
        "subPillarName": "Store Replenishment",
        "name": "Modern Trade Appointment & Fill-Rate Agent",
        "tier": "P1",
        "paybackDays": 75,
        "savedHoursWk": 8,
        "linkedPersonas": ["retail_logistics_dispatcher", "outbound_lead_industrial_eng", "customer_support_ops_lead"],
        "oneLine": "Synchronizes CFA wave completion and truck ETA with Reliance, DMart, Walmart, and Amazon vendor portal dock appointments to prevent PO expiry and OTIF chargebacks.",
        "reads": "Retailer ASN appointment calendars, WMS wave completion %, and live route traffic ETA.",
        "does": "Matches ready-to-ship loads against open retailer receiving slots and flags threatened PO cancellation cutoffs.",
        "returns": "Prioritized dock-load sequence + retailer portal slot-reschedule recommendation.",
        "stopsAt": "Canceling committed Modern Trade purchase orders.",
        "safetyEnvelope": "Prioritizes A-class festival/promo POs carrying >3% OTIF chargeback clauses.",
        "subWorkflows": [
            ("Synchronize CFA wave completion & truck ETA with Reliance/DMart dock slots", "Dispatchers book retailer vendor-portal receiving slots manually before knowing WMS pick-wave readiness.", "Missed 30-minute Modern Trade dock windows result in turned-away trucks, detention, and 3–5% OTIF fines."),
            ("Re-sequence outbound CFA dock loading by PO cancellation cutoff & penalty exposure", "CFA docks load trucks first-come-first-served rather than by retailer PO expiry clock.", "Penalty-weighted dock sequencing protects high-value Modern Trade and eCommerce fulfillment windows."),
        ],
    },
    {
        "id": "rural_van_beat_load_optimizer",
        "deptId": "logistics_fleet",
        "subPillarId": "last_mile_delivery",
        "subPillarName": "Last-Mile Delivery",
        "name": "General Trade Beat & Van-Load Optimizer",
        "tier": "P1",
        "paybackDays": 85,
        "savedHoursWk": 8,
        "linkedPersonas": ["last_mile_operations_lead", "ecommerce_logistics_dir", "transport_procurement_lead"],
        "oneLine": "Builds the daily SKU load-out sheet for rural & urban General Trade sales vans based on outlet-level reorder probability and van weight/cube limits.",
        "reads": "DMS kirana beat schedules, historical outlet SKU order probability, active trade schemes, and 1.5-ton van capacity.",
        "does": "Maximizes expected daily beat billings per kilometer while eliminating evening unsold van returns.",
        "returns": "Beat-wise morning van load manifest + top-3 cross-sell SKU prompts per outlet.",
        "stopsAt": "Extending unapproved cash credit to overdue general-trade outlets.",
        "safetyEnvelope": "Reserves 85% van cube for confirmed pre-booked orders before adding predictive top-up cases.",
        "subWorkflows": [
            ("Optimize morning 1.5-ton General Trade van SKU load-out by kirana reorder probability", "Van drivers load static habitual SKU mixes every morning regardless of which beat outlets are due to reorder.", "Vans run out of fast-moving ₹10 packs by noon while bringing back 22% unsold slow cartons every evening."),
            ("Generate outlet-specific top-3 cross-sell prompts aligned to active trade slabs", "Ready-stock van salesmen pitch only top-of-mind SKUs across 40 daily kirana stops.", "Data-backed van manifests lift lines-per-productive-call without exceeding 1.5-ton payload."),
        ],
    },
    {
        "id": "cold_chain_salvage_repack_advisor",
        "deptId": "circular_enable",
        "subPillarId": "expiry_markdowns",
        "subPillarName": "Expiry & Markdowns",
        "name": "Cold-Chain Excursion MKT Salvage Advisor",
        "tier": "P1",
        "paybackDays": 80,
        "savedHoursWk": 7,
        "linkedPersonas": ["cold_chain_qa_logistics_dir", "inventory_disposition_lead", "packaging_qa_food_safety"],
        "oneLine": "Computes Mean Kinetic Temperature (MKT) degradation curves when dairy, chocolate, or probiotic reefers suffer brief door-open excursions—saving safe stock from blanket destruction.",
        "reads": "Minute-by-minute IoT reefer logger traces (`05_tms_shipments_eway_freight_audit.csv`), SKU Arrhenius shelf-life stability curves, and QA micro specs.",
        "does": "Separates cosmetic/safe minor thermal blips (eligible for fast local clearance) from true stability breaches requiring quarantine.",
        "returns": "Pallet-level QA disposition brief + carrier thermal-claim evidence log.",
        "stopsAt": "Releasing temperature-abused infant, dairy, or pharma-nutrition lots without QA Lab sign-off.",
        "safetyEnvelope": "Zero-tolerance quarantine whenever cumulative excursion exceeds validated stability envelope.",
        "subWorkflows": [
            ("Compute Arrhenius Mean Kinetic Temperature (MKT) stability on reefer door excursions", "Any reefer crossing 8°C for 25 minutes at a toll or dock triggers blanket pallet quarantine and destruction.", "Safe chocolate, beverage, and dairy pallets within validated MKT stability envelopes get destroyed unnecessarily."),
            ("Isolate true thermal-breach pallets by reefer zone for QA hold & carrier claim", "Single-point return-air loggers fail to separate rear-door pallets from core-zone cargo.", "Zone-level MKT disposition rescues safe stock while documenting irreversible breaches for carrier recovery."),
        ],
    },
    {
        "id": "grey_market_diversion_sentinel",
        "deptId": "circular_enable",
        "subPillarId": "returns_claims_mgmt",
        "subPillarName": "Returns & Claims Mgmt",
        "name": "Channel Price-Erosion & Grey-Market Sentinel",
        "tier": "P1",
        "paybackDays": 90,
        "savedHoursWk": 7,
        "linkedPersonas": ["reverse_logistics_fraud_lead", "revenue_trade_finance_lead", "claims_specialist_controller"],
        "oneLine": "Detects deeply discounted institutional or regional promo stock leaking onto unauthorized B2B/online marketplaces by correlating batch lot scans and price anomalies.",
        "reads": "Marketplace price monitors, RMA lot-code scans (`06_returns_markdowns_rti_circular.csv`), and regional wholesale trade-scheme allocations.",
        "does": "Traces diverted lot prefixes back to originating bulk wholesale/institutional accounts eroding retail price integrity.",
        "returns": "Diversion trace dossier linking unauthorized listings to originating trade-scheme lots.",
        "stopsAt": "Terminating distributor agreements or withholding earned trade rebates unilaterally.",
        "safetyEnvelope": "Requires physical batch-code or test-buy verification before flagging a distributor account.",
        "subWorkflows": [
            ("Correlate unauthorized online price undercutting with institutional/canteen lot allocations", "Deeply discounted institutional or regional promo cases leak onto B2B portals, undercutting Modern Trade.", "Channel conflict triggers retailer margin-matching demands and erodes brand price architecture."),
            ("Trace diverted batch lot prefixes from RMA & test-buy scans to source wholesale accounts", "Manual channel audits cannot link marketplace seller listings back to originating CFA batch dispatches.", "Lot-prefix graph correlation pinpoints diversion leakage for commercial review."),
        ],
    },
    {
        "id": "epr_plastic_credit_ledger_agent",
        "deptId": "circular_enable",
        "subPillarId": "pallet_tote_reclamation",
        "subPillarName": "Pallet & Tote Reclamation",
        "name": "EPR Multi-Layer Plastic Credit Ledger",
        "tier": "P2",
        "paybackDays": 145,
        "savedHoursWk": 8,
        "linkedPersonas": ["cso_circular_lead", "chief_sustainability_officer", "asset_recovery_rti_manager", "customer_experience_cx_lead", "merchandising_store_ops_mgr", "reverse_logistics_lead_wh", "reverse_transport_planner"],
        "oneLine": "Reconciles state-wise rigid PET & Multi-Layered Plastic (MLP) laminate tonnage dispatched in CPG packs against verified recycler EPR certificates.",
        "reads": "SKU packaging polymer weights (`00_master_skus.jsonl`), state-wise CFA sales tonnage, and CPCB/EU registered recycler credit ledgers.",
        "does": "Calculates exact quarterly Category I/II/III plastic obligations by state and flags certificate shortfalls ahead of filing.",
        "returns": "Audit-ready EPR plastic mass-balance ledger and recycler credit purchase plan.",
        "stopsAt": "Filing statutory CPCB/EU portal declarations or purchasing unverified offset credits.",
        "safetyEnvelope": "Accepts only GST-verified, geo-tagged Waste Processing Organization (PWP) certificates.",
        "subWorkflows": [
            ("Compute state-wise Category I/II/III plastic & MLP tonnage from CFA dispatches", "Sustainability teams manually multiply SKU laminate weights by state sales invoices at quarter-end.", "Late plastic mass-balance math forces last-minute spot purchases of EPR recycler credits at 30% premiums."),
            ("Verify Plastic Waste Processor (PWP) GST & geo-tag certificates before CPCB filing", "Duplicate or unverified recycler certificates expose the enterprise to CPCB environmental compensation fines.", "Automated certificate lineage audit ensures 100% compliant statutory EPR filings."),
        ],
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# RESEARCHED 4-LEVER CPG VALUE ATTRIBUTION (78 AGENTS · ZERO 4-LEVER INFLATION!)
#   Each entry: (tier, paybackDays, seats, hrsYrPerSeat, flowCr, shieldCr, recovCr,
#                flowBasis, shieldBasis, recovBasis)
#   - Productivity Cr = round(seats * hrsYrPerSeat * 2500 / 1e7, 2)  (₹2,500/hr loaded CPG rate)
#   - 56 of 78 Agents (72%) move ONLY 2 Levers (Productivity + 1 operational/financial lever)
#   - 22 of 78 Agents (28%) move 3 Levers (Productivity + 2 coupled levers)
#   - 0 of 78 Agents claim all 4 Levers!
# ══════════════════════════════════════════════════════════════════════════════
ZERO_REASONS = {
    "flow": "No physical factory line, dock bay, or working-capital buffer waits on this workflow.",
    "shield": "Optimizes throughput, buffer sizing, or commercial capture rather than pricing an avoided compliance/audit loss.",
    "recov": "Protects cost, uptime, or compliance on existing volume — claims zero incremental unit sales.",
}

RES_AGENT_LEVERS = {
    # ── PILLAR 01 · PLANNING & STRATEGY (15 Agents) ──────────────────────────
    "demand_sensing_agent": (
        "P0", 45, 44, 310, 21.4, 0.0, 34.8,
        "Trims 4.2 days of excess safety-stock buffer across 48 CFAs (@ 22% carry cost)",
        "",
        "Prevents censored POS stockouts on A-class SKUs (@ 32% gross contribution margin)",
    ),
    "qcommerce_darkstore_sensing_agent": (
        "P0", 35, 28, 280, 0.0, 0.0, 26.4,
        "", "",
        "Captures 10-min Blinkit & Zepto impulse orders across 420 urban dark stores before tile stockout",
    ),
    "cpfr_sync_agent": (
        "P1", 90, 32, 260, 0.0, 0.0, 19.8,
        "", "",
        "Eliminates phantom Modern Trade shelf stockouts via POS-to-shipment reconciliation",
    ),
    "npi_demand_profiler": (
        "P1", 120, 18, 250, 0.0, 0.0, 18.4,
        "", "",
        "Matches regional launch velocity to lookalike SKUs, preventing early NPI stockouts",
    ),
    "promo_lift_simulator": (
        "P0", 60, 30, 270, 0.0, 38.4, 16.8,
        "",
        "Eliminates negative-ROI forward-buy & cannibalized promos across ₹6,100 Cr trade spend (BCG)",
        "Reallocates trade funding into high-elasticity packs & festival windows",
    ),
    "field_beat_distributor_sync_agent": (
        "P1", 110, 48, 240, 0.0, 0.0, 19.2,
        "", "",
        "Synchronizes General Trade distributor beat sell-in with local consumer promo lift",
    ),
    "trade_scheme_claims_reconciler": (
        "P0", 30, 36, 290, 0.0, 31.0, 0.0,
        "",
        "Blocks duplicate & invalid proof-of-performance retailer trade deductions via OCR audit",
        "",
    ),
    "rgm_pack_price_architecture_agent": (
        "P1", 90, 22, 250, 0.0, 13.8, 10.8,
        "",
        "Stops cross-channel margin dilution between ₹10 sachets and Modern Trade family pouches",
        "Unlocks positive Price-Pack Architecture (PPA) net revenue realization",
    ),
    "sop_scenario_weaver": (
        "P1", 105, 34, 270, 18.2, 0.0, 12.6,
        "Aligns constrained ICML line capacity & working capital across monthly S&OP cycles",
        "",
        "Protects high-margin channel fulfillment when raw material or line bottlenecks hit",
    ),
    "festival_monsoon_surge_planner": (
        "P1", 85, 24, 240, 0.0, 0.0, 19.6,
        "", "",
        "Captures movable Diwali, Eid & monsoon regional demand surges 10 weeks ahead",
    ),
    "disruption_war_room_orchestrator": (
        "P1", 95, 20, 260, 9.4, 26.8, 0.0,
        "Reroutes co-packer & depot allocations 62% faster during regional disruptions (WEF)",
        "Contains unmitigated supply-shock EBITDA loss across plant & port corridors (McKinsey)",
        "",
    ),
    "csco_control_tower_copilot": (
        "P2", 160, 38, 280, 0.0, 5.4, 0.0,
        "",
        "Prevents missed cross-pillar S&OP SLA escalations through automated pre-read synthesis",
        "",
    ),
    "working_capital_cash_bridge": (
        "P1", 120, 24, 270, 19.8, 0.0, 6.4,
        "Rationalizes slow-tail SKUs trapping working capital & changeover hours (@ 22% carry cost)",
        "",
        "Reassigns freed shelf facings to top-decile velocity hero SKUs",
    ),
    "eco_cutover_orchestrator": (
        "P1", 130, 22, 250, 0.0, 14.6, 0.0,
        "",
        "Eliminates obsolete printed laminate & recipe write-offs during BOM formulation transitions",
        "",
    ),
    "network_twin_architect": (
        "P2", 180, 20, 270, 13.2, 0.0, 0.0,
        "Optimizes CFA depot echelon footprint & pack cost-to-serve across Grocery, Club & Q-Comm",
        "", "",
    ),

    # ── PILLAR 02 · SOURCING & PROCUREMENT (12 Agents) ───────────────────────
    "tier_n_risk_sentinel": (
        "P0", 60, 30, 270, 9.6, 42.8, 0.0,
        "Pre-positions alternate resin & agri buffer lots so ICML lines avoid starvation halts",
        "Prevents multi-week plant shutdowns from Tier-2/3 feedstock & port disruptions",
        "",
    ),
    "farmgate_agri_commodity_hedger": (
        "P0", 45, 28, 265, 0.0, 26.4, 0.0,
        "",
        "Protects wheat, edible oil & spice COGS by timing mandi arrivals & NCDEX forward windows",
        "",
    ),
    "supplier_quality_sentinel": (
        "P1", 110, 26, 260, 0.0, 16.4, 0.0,
        "",
        "Catches expired BRC/FSSAI food-safety certs & CoA drifts before contaminated intake",
        "",
    ),
    "carbon_scope3_ledger": (
        "P2", 170, 24, 260, 0.0, 7.9, 0.0,
        "",
        "Avoids EU Deforestation Regulation (EUDR) & CBAM export compliance penalties",
        "",
    ),
    "commodity_index_advisor": (
        "P1", 95, 20, 270, 0.0, 21.2, 0.0,
        "",
        "Avoids peak-spot HDPE resin, kraft paper & palm-olein price spikes via index-linked triggers",
        "",
    ),
    "rfq_should_cost_agent": (
        "P1", 90, 28, 260, 0.0, 24.5, 0.0,
        "",
        "Eliminates 3–6% vendor margin padding on laminate, carton & conversion RFQs via clean-sheet math",
        "",
    ),
    "artwork_allergen_packaging_gate": (
        "P1", 80, 26, 260, 0.0, 15.8, 0.0,
        "",
        "Prevents undeclared-allergen recalls & cylinder re-engraving via multimodal proof inspection",
        "",
    ),
    "sustainable_packaging_agent": (
        "P2", 155, 18, 260, 0.0, 10.2, 0.0,
        "",
        "Avoids plastic-packaging tax penalties & high-speed wrapper film-break scrap on PCR blends",
        "",
    ),
    "tariff_esg_agent": (
        "P0", 45, 26, 260, 0.0, 33.8, 0.0,
        "",
        "Recovers uncollected vendor volume-rebate tiers & duty drawback entitlements across live spend",
        "",
    ),
    "master_data_leadtime_steward": (
        "P1", 100, 46, 265, 13.4, 0.0, 0.0,
        "Recalibrates padded SAP vendor lead-times that silently inflate safety-stock capital",
        "", "",
    ),
    "three_way_match_dispute": (
        "P0", 30, 52, 275, 0.0, 28.1, 0.0,
        "",
        "Blocks duplicatebillings, PO rate drift & GRN short-delivery overpayments prior to wire release",
        "",
    ),
    "supplier_dynamic_discounting_agent": (
        "P1", 70, 18, 245, 16.8, 0.0, 0.0,
        "Captures 14–18% risk-free annualized treasury yield on verified early-pay vendor invoices",
        "", "",
    ),

    # ── PILLAR 03 · MANUFACTURING & PRODUCTION (12 Agents) ───────────────────
    "finite_production_scheduler": (
        "P0", 60, 36, 265, 29.4, 0.0, 11.2,
        "Cuts allergen, flavor & pack-format changeover washdowns across 20 ICML plants (@ ₹3.8 L/line-hr)",
        "",
        "Frees constrained bottling & biscuit line hours for peak-demand hero SKUs",
    ),
    "line_schedule_optimizer": (
        "P1", 90, 40, 260, 16.4, 0.0, 6.8,
        "Dynamically reroutes perishable work-in-progress (WIP) around unplanned wrapper/filler halts",
        "",
        "Prevents regional dispatch shorts when primary packaging lines trip mid-shift",
    ),
    "labor_line_balancing_agent": (
        "P1", 105, 36, 255, 14.4, 0.0, 0.0,
        "Eliminates shift changeover micro-stoppages & overtime via certified-skill line balancing",
        "", "",
    ),
    "predictive_oee_sentinel": (
        "P1", 115, 24, 245, 24.8, 0.0, 0.0,
        "Prevents unplanned high-speed filler, sealer & boiler outages via vibration/thermal sensing",
        "", "",
    ),
    "plant_energy_utility_peak_shaver": (
        "P1", 95, 18, 235, 14.8, 0.0, 0.0,
        "Shifts CIP steam & cold-room pull-downs out of peak Time-of-Day electricity tariff windows",
        "", "",
    ),
    "copacker_allocation_agent": (
        "P1", 120, 22, 245, 15.6, 0.0, 0.0,
        "Optimizes internal ICML conversion utilization vs. external co-packer tolling slabs",
        "", "",
    ),
    "copacker_material_yield_reconciler": (
        "P0", 40, 26, 260, 0.0, 22.4, 0.0,
        "",
        "Claws back excess laminate film & edible-oil usage above 1.2% co-packer scrap norms",
        "",
    ),
    "capex_simulator_agent": (
        "P2", 180, 18, 250, 0.0, 11.2, 0.0,
        "",
        "Prevents stranded or mis-located multi-crore packaging line CapEx via multi-year twin stress tests",
        "",
    ),
    "inline_yield_guardian": (
        "P0", 75, 30, 260, 7.6, 23.4, 0.0,
        "Eliminates net-weight overfill giveaway on 600-pack/min filling lines",
        "Ejects micro-leaking seals & mis-printed MRP/lot packs inline before case-packing",
        "",
    ),
    "batch_record_auditor": (
        "P1", 110, 32, 255, 0.0, 14.8, 0.0,
        "",
        "Flags pasteurization & HACCP Critical Control Point (CCP) deviations before batch QA release",
        "",
    ),
    "lot_genealogy_recall_tracer": (
        "P0", 50, 25, 255, 0.0, 26.6, 0.0,
        "",
        "Shrinks recall blast radius by 80% in 90 seconds across ICML → CFA → DMS lot graphs",
        "",
    ),
    "scrap_defect_root_cause_agent": (
        "P1", 125, 25, 255, 16.2, 0.0, 0.0,
        "Isolates film-jaw temperature & viscosity drift to recover first-pass packaging yield",
        "", "",
    ),

    # ── PILLAR 04 · INVENTORY & WAREHOUSING (12 Agents) ──────────────────────
    "meio_safety_stock_agent": (
        "P0", 55, 26, 260, 48.6, 0.0, 14.4,
        "Releases 14–22% trapped multi-echelon buffer stock across Mother Hubs & 48 CFAs (@ 22% carry cost)",
        "",
        "Rebalances safety stock into volatile high-margin SKUs, lifting case fill rate +2.4%",
    ),
    "fefo_shelf_life_allocator": (
        "P0", 35, 26, 260, 17.8, 16.4, 0.0,
        "Accelerates mid-life inventory turns across General Trade beats, cutting expiry carry",
        "Eliminates Modern Trade 75%-MRSL dock rejections & depot shelf-life write-offs",
        "",
    ),
    "slob_disposition_agent": (
        "P0", 45, 26, 255, 18.4, 0.0, 16.2,
        "Frees congested CFA pallet bays & carrying capital tied up in Slow & Obsolete (SLOB) lots",
        "",
        "Recovers net margin via early promotional combo-packs before deep liquidation",
    ),
    "crossdock_transfer_orchestrator": (
        "P1", 95, 30, 260, 19.4, 0.0, 9.6,
        "Bypasses storage putaway via flow-through cross-docking & lateral inter-depot balancing",
        "",
        "Fills regional surge orders from adjacent depot surplus instead of losing sales",
    ),
    "warehouse_slotting_agent": (
        "P1", 105, 38, 255, 18.4, 0.0, 0.0,
        "Cuts picker travel distance 24% & boosts case-pick throughput via affinity golden-zone slotting",
        "", "",
    ),
    "qcommerce_assortment_micro_slotter": (
        "P1", 90, 28, 255, 12.6, 0.0, 0.0,
        "Compresses urban dark-store pick-and-pack cycle under 90 seconds via nightly micro-slotting",
        "", "",
    ),
    "dock_to_stock_agent": (
        "P1", 95, 44, 255, 13.8, 0.0, 0.0,
        "Compresses inbound receiving-to-putaway cycle from 18h to 3h, unlocking dock door capacity",
        "", "",
    ),
    "wave_fulfillment_copilot": (
        "P1", 100, 40, 255, 13.2, 0.0, 6.4,
        "Balances pick-pack zone labor dynamically so carrier linehaul cutoffs depart on time",
        "",
        "Prevents missed-wave short-shipments on peak promotional dispatch days",
    ),
    "planogram_merchandising_vision_auditor": (
        "P0", 60, 42, 265, 0.0, 0.0, 33.6,
        "", "",
        "Detects phantom backroom inventory & missing shelf facings via POS zero-scan + shelf vision",
    ),
    "dms_distributor_stock_balancer": (
        "P0", 45, 32, 255, 13.4, 0.0, 19.6,
        "Smooths 45-day secondary stockist gluts & working-capital lockup across 3,800 distributors",
        "",
        "Auto-stages credit-safe DMS primary orders before high-turn kirana beats stock out",
    ),
    "atp_order_promising_agent": (
        "P1", 110, 26, 260, 0.0, 0.0, 21.6,
        "", "",
        "Captures omnichannel & B2B orders via real-time multi-node Available-to-Promise (ATP) sourcing",
    ),
    "returns_triage_agent": (
        "P1", 115, 32, 255, 0.0, 0.0, 18.6,
        "", "",
        "Fast-tracks unopened A-grade returns straight back to sellable stock before seasonal value decays",
    ),

    # ── PILLAR 05 · DISTRIBUTION & LOGISTICS (15 Agents) ─────────────────────
    "load_consolidation_agent": (
        "P0", 45, 36, 260, 36.8, 0.0, 0.0,
        "Converts fragmented LTL dispatches into 93%-cube multi-stop 32-ft FTL linehauls (OR-Tools 3D)",
        "", "",
    ),
    "yard_dock_sequencer": (
        "P1", 95, 32, 260, 16.6, 0.0, 0.0,
        "Eliminates gate congestion & carrier detention hours via live GPS dock-door slotting",
        "", "",
    ),
    "cold_chain_auditor": (
        "P1", 100, 22, 245, 0.0, 23.4, 0.0,
        "",
        "Prevents spoiled dairy/chocolate cargo write-offs & recovers valid carrier reefer claims",
        "",
    ),
    "aisle_aligned_pallet_agent": (
        "P1", 115, 26, 255, 15.4, 0.0, 0.0,
        "Sequences mixed-SKU pallets by retail aisle layout, cutting store backroom sort & dock dwell",
        "", "",
    ),
    "modern_trade_dock_slot_booker": (
        "P1", 75, 28, 245, 8.4, 15.6, 0.0,
        "Eliminates rejected-truck waiting & redelivery trips at Reliance, DMart & Amazon FC docks",
        "Prevents 3–5% Modern Trade OTIF late-delivery penalties & PO auto-cancellations",
        "",
    ),
    "store_capacity_agent": (
        "P1", 120, 25, 255, 0.0, 0.0, 14.8,
        "", "",
        "Prevents weekend A-SKU shelf stockouts caused by backroom congestion throttling",
    ),
    "port_drayage_orchestrator": (
        "P1", 110, 25, 255, 18.2, 0.0, 0.0,
        "Eliminates JNPT/Mundra container demurrage, detention & nocturnal city-curfew idle hours",
        "", "",
    ),
    "geocoding_intelligence_agent": (
        "P1", 105, 25, 255, 0.0, 0.0, 13.6,
        "", "",
        "Cuts failed first-attempt drop-offs that otherwise convert into cancelled COD/kirana orders",
    ),
    "rural_van_beat_load_optimizer": (
        "P1", 85, 28, 245, 0.0, 0.0, 16.8,
        "", "",
        "Lifts daily van beat billings & lines-per-call via outlet reorder-probability load manifests",
    ),
    "multimodal_mode_shift_agent": (
        "P1", 100, 25, 255, 19.4, 0.0, 0.0,
        "Shifts predictable inter-state replenishment from spot road trucks onto CONCOR rail & coastal",
        "", "",
    ),
    "otif_penalty_shield": (
        "P0", 40, 36, 255, 0.0, 28.4, 8.2,
        "",
        "Shields 3–5% Modern Trade & Quick-Commerce OTIF chargebacks via proactive rerouting",
        "Protects preferred-vendor shelf allocation & promotional slot eligibility",
    ),
    "fleetflow_dispatch": (
        "P0", 45, 46, 265, 26.8, 0.0, 10.4,
        "Cuts fleet fuel & stem-kilometers 12% via live Google Maps & WeatherNext 3 dynamic routing",
        "",
        "Protects same-day retail & dark-store replenishment fill during monsoon/highway disruptions",
    ),
    "eway_bill_gst_transit_auditor": (
        "P0", 30, 28, 255, 0.0, 24.2, 0.0,
        "",
        "Eliminates Section 129 GST highway truck seizures (200% tax fine) on expiring E-Way Bills",
        "",
    ),
    "freight_control_tower": (
        "P1", 95, 26, 260, 19.8, 0.0, 0.0,
        "Avoids 18–25% spot-market broker premiums by predicting primary carrier tender rejections early",
        "", "",
    ),
    "freight_bill_audit_agent": (
        "P0", 30, 38, 250, 0.0, 38.2, 0.0,
        "",
        "Recovers 5–15% carrier detention, fuel-index & weight-slab overcharges across ₹3,400 Cr freight (Capgemini)",
        "",
    ),

    # ── PILLAR 06 · RETURNS & REVERSE LOGISTICS (12 Agents) ──────────────────
    "reverse_rma_optimizer": (
        "P0", 45, 32, 255, 0.0, 29.5, 10.8,
        "",
        "Blocks counterfeit, tampered & out-of-policy B2B/eCommerce return fraud via vision triage",
        "Routes verified unopened cases straight to rapid resale instead of scrap",
    ),
    "grey_market_diversion_sentinel": (
        "P1", 90, 22, 245, 0.0, 17.8, 6.2,
        "",
        "Stops institutional/regional trade-scheme leakage onto unauthorized B2B marketplaces",
        "Restores full-margin authorized distributor & Modern Trade sell-through",
    ),
    "keep_it_routing_advisor": (
        "P1", 90, 25, 255, 0.0, 0.0, 16.4,
        "", "",
        "Preserves net contribution margin by comparing reverse haulage cost against local salvage value",
    ),
    "osd_freight_claims_agent": (
        "P1", 95, 30, 260, 0.0, 19.4, 0.0,
        "",
        "Automates ePOD & transit-damage evidence packets to recover carrier OS&D claims before time-bar",
        "",
    ),
    "dynamic_markdown_agent": (
        "P0", 50, 26, 255, 0.0, 0.0, 32.4,
        "", "",
        "Converts near-expiry dairy, bakery & beverage lots into revenue via DTE elasticity markdowns",
    ),
    "cold_chain_salvage_repack_advisor": (
        "P1", 80, 22, 245, 0.0, 13.6, 10.4,
        "",
        "Quarantines true Arrhenius MKT thermal breaches before unsafe cold-chain release",
        "Saves safe pallets from blanket destruction after brief dock-door temperature blips",
    ),
    "short_dated_redistributor": (
        "P1", 115, 22, 245, 0.0, 0.0, 16.8,
        "", "",
        "Matches 60%-life depot lots to high-velocity value channels & institutional kitchens before expiry",
    ),
    "food_waste_esg_copilot": (
        "P2", 165, 25, 255, 0.0, 6.8, 0.0,
        "",
        "Prevents statutory organic-waste & Scope 3 disclosure penalties with audited diversion ledgers",
        "",
    ),
    "rti_balance_reconciler": (
        "P0", 60, 26, 260, 21.6, 0.0, 0.0,
        "Accelerates RFID CHEP pallet & foldable crate turns, cutting pool rental & replacement CapEx",
        "", "",
    ),
    "intermodal_rail_linehaul_agent": (
        "P1", 110, 22, 240, 15.8, 0.0, 0.0,
        "Eliminates paid empty backhauls by pairing outbound trucks with retail crate/cage recovery",
        "", "",
    ),
    "sanitation_health_agent": (
        "P1", 120, 22, 240, 0.0, 14.8, 0.0,
        "",
        "Prevents cross-batch microbial contamination & damaged-crate product crush via wash/ATP audits",
        "",
    ),
    "epr_plastic_credit_ledger_agent": (
        "P2", 145, 25, 250, 0.0, 10.4, 0.0,
        "",
        "Prevents CPCB Extended Producer Responsibility (EPR) plastic-shortfall fines & spot premiums",
        "",
    ),
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
    "demand_sop": "SAP IBP · Distributor Management System (DMS) · Retail POS",
    "sourcing_procurement": "SAP Ariba · SAP S/4HANA MM · Mandi & Commodity Feeds",
    "manufacturing_prod": "SAP S/4HANA PP · Siemens Opcenter MES · LIMS QA",
    "inventory_warehouse": "Manhattan Active WMS · SAP EWM · DMS Stock Ledger",
    "logistics_fleet": "Oracle OTM · SAP TM · NIC E-Way Bill API",
    "circular_enable": "SAP S/4HANA Returns · RFID Pool Ledger · CPCB EPR Portal",
}

MONOLITH_TASKS_BY_DEPT = {
    "demand_sop": [
        ("Execute nightly SAP IBP time-series disaggregation & MRP net-requirements explosion", "SAP IBP & S/4HANA MRP", "Deterministic BOM explosion across 20 plants and 48 CFAs already runs reliably inside SAP IBP; replacing core MRP is not an agent use case.", "Nightly batch", "SKU × Plant"),
        ("Enforce SKU Master, GST HSN tax codes & statutory Maximum Retail Price (MRP) slabs", "SAP S/4HANA Material Master (MARA)", "Authoritative pricing, tax, and unit-of-measure master records require strict ERP transactional locking.", "Continuous", "Enterprise master"),
    ],
    "sourcing_procurement": [
        ("Post 3-way-matched Goods Receipt Notes (MIGO) & financial vendor ledger entries (MIRO)", "SAP S/4HANA Materials Management & FI", "Double-entry sub-ledger accounting and statutory GST input-tax-credit postings belong strictly inside core ERP.", "Transactional", "PO / Invoice"),
        ("Execute encrypted host-to-host bank NEFT/RTGS payment runs", "SAP Treasury & Bank Payment Hub", " Treasury settlement rails are deterministic, cryptographic, and governed by dual-custody banking controls.", "Daily pay-run", "Approved batch"),
    ],
    "manufacturing_prod": [
        ("Run millisecond PLC interlocks, pasteurizer PID loops & high-speed checkweigher diverters", "Siemens Opcenter MES & Plant SCADA/PLC", "Hard real-time (<10 ms) closed-loop machine control and safety interlocks run deterministically at the PLC layer.", "Millisecond loop", "Packaging line"),
        ("Record immutable Batch Production Record (BPR) sensor historians & SAP PP confirmations", "SAP S/4HANA PP & Plant Historian", "System-of-record production confirmations and lot serial numbers must write atomically to the transactional ledger.", "Per batch", "ICML plant"),
    ],
    "inventory_warehouse": [
        ("Execute real-time RF barcode bin scans, AS/RS crane PLC moves & inventory reservations", "Manhattan Active WMS / SAP EWM", "Sub-second warehouse bin locking and automated crane control are handled natively by the core WMS.", "Real-time scan", "Storage bin"),
        ("Post statutory stock-transfer invoices (STO) & inter-state GST ledger entries", "SAP S/4HANA EWM & Billing", "Fiscal stock ownership transfers across state borders require authoritative ERP invoice generation.", "Transactional", "CFA depot"),
    ],
    "logistics_fleet": [
        ("Transmit statutory EDI 204/214 carrier messages & generate official IRN/QR E-Way Bills", "Oracle OTM & NIC GST Portal API", "Transactional carrier EDI state machines and government cryptographic invoice registration run in core TMS.", "Transactional", "Shipment ID"),
        ("Settle approved carrier freight vouchers into General Ledger cost centers", "SAP S/4HANA TM & Accounts Payable", "Final financial disbursement and freight cost-center accrual run deterministically post-approval.", "Weekly run", "Carrier ledger"),
    ],
    "circular_enable": [
        ("Post credit memos, GST sales-return reversals & inventory write-off journal entries", "SAP S/4HANA SD/FI Returns Ledger", "Statutory revenue-reversal accounting and tax credit notes must execute inside the audited financial monolith.", "Transactional", "Credit memo"),
        ("Maintain serialized RFID pool asset balances & customer deposit ledgers", "SAP Returnable Packaging & RFID Core", "Core asset custody accounting is already tracked reliably once exceptions are reconciled.", "Daily sync", "RTI pool"),
    ],
}

NOT_OWNED_BY_DEPT = {
    "demand_sop": [
        {"task": "Sign off monthly consensus S&OP demand lock & factory overtime commitments", "owner": "{person} ({role})", "because": "Commits cross-functional working capital and commercial revenue targets — requires named executive accountability."},
        {"task": "Approve printed Maximum Retail Price (MRP) changes & annual Modern Trade JBP terms", "owner": "VP Commercial Sales & Legal Metrology Sign-Off", "because": "Binding counterparty margin contracts and statutory pack-price declarations cannot be delegated to an agent."},
    ],
    "sourcing_procurement": [
        {"task": "Authorize physical commodity forward contracts & multi-crore vendor awards", "owner": "{person} ({role}) & Procurement Committee", "because": "Fiduciary supplier selection and balance-sheet commodity commitments require human commercial sign-off."},
        {"task": "Release raw-material lots after a food-safety microbiological or allergen hold", "owner": "Head of Quality Assurance & Regulatory", "because": "Consumer food-safety disposition carries statutory FSSAI/FDA liability and stays 100% human."},
    ],
    "manufacturing_prod": [
        {"task": "Execute physical Lockout/Tagout (LOTO) & confined-space maintenance permits", "owner": "Certified Shift Maintenance Engineer", "because": "Life-safety physical isolation at high-speed machinery requires hands-on human verification on the shop floor."},
        {"task": "Sign statutory Qualified Person (QP) / FSSAI food-safety batch release", "owner": "{person} ({role})", "because": "Legal product release into human consumption requires a licensed human officer's signature."},
    ],
    "inventory_warehouse": [
        {"task": "Approve commercial Minimum Remaining Shelf-Life (MRSL) concessions with retail chains", "owner": "{person} ({role}) & Key Account Lead", "because": "Negotiating shelf-life waivers is a relationship and brand-equity judgment call between humans."},
        {"task": "Authorize financial inventory destruction & statutory write-off certificates", "owner": "Regional Finance Controller & QA", "because": "Physical stock destruction and P&L write-offs require dual human audit witnessing."},
    ],
    "logistics_fleet": [
        {"task": "Command driver Hours-of-Service safety halts & severe-weather highway stand-downs", "owner": "{person} ({role}) & Fleet Safety Officer", "because": "Human life safety on highways overrides every OTIF delivery clock and stays strictly under human authority."},
        {"task": "Sign multi-year 3PL dedicated-fleet rate cards & fuel-escalation clauses", "owner": "VP Logistics & Procurement Legal", "because": "Long-term capital lease and carrier contract commitments require human negotiation and legal execution."},
    ],
    "circular_enable": [
        {"task": "Sign statutory CPCB / EU Extended Producer Responsibility (EPR) board filings", "owner": "{person} ({role}) & Company Secretary", "because": "Statutory environmental declarations carry director-level legal attestation and cannot be auto-submitted."},
        {"task": "Approve distributor termination or legal recovery for grey-market diversion", "owner": "National Sales Director & Legal Counsel", "because": "Channel enforcement requires verified physical evidence and human commercial judgment."},
    ],
}

SOURCE_BY_DEPT = {
    "demand_sop": "[BCG RGM '25 · Unilever '26]",
    "sourcing_procurement": "[Gartner SCM '26 · ASCM SCOR]",
    "manufacturing_prod": "[GE Appliances '26 · HACCP]",
    "inventory_warehouse": "[Home Depot '26 · ASCM SCOR]",
    "logistics_fleet": "[Capgemini '25 · GST Sec 129]",
    "circular_enable": "[WEF '26 · CPCB EPR Rules]",
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


def build_lever_meta(aid: str):
    tier, payback, seats, hrs_yr, flow_cr, shield_cr, recov_cr, flow_b, shield_b, recov_b = RES_AGENT_LEVERS[aid]
    prod_cr = round((seats * hrs_yr * 2500.0) / 1e7, 2)
    flow_cr = round(float(flow_cr), 2)
    shield_cr = round(float(shield_cr), 2)
    recov_cr = round(float(recov_cr), 2)
    tot_cr = round(prod_cr + flow_cr + shield_cr + recov_cr, 2)

    active = [k for k, val in (("prod", prod_cr), ("flow", flow_cr), ("shield", shield_cr), ("recov", recov_cr)) if val > 0]
    assert 1 <= len(active) <= 3, f"Agent {aid} must move 1..3 levers, got {len(active)}"

    prod_b = f"{seats} CPG specialists × {hrs_yr} hrs/yr redeployed @ ₹2,500/hr"
    basis = {
        "prod": prod_b,
        "flow": flow_b if flow_cr > 0 else ZERO_REASONS["flow"],
        "shield": shield_b if shield_cr > 0 else ZERO_REASONS["shield"],
        "recov": recov_b if recov_cr > 0 else ZERO_REASONS["recov"],
    }
    return tier, payback, seats, hrs_yr, prod_cr, flow_cr, shield_cr, recov_cr, tot_cr, active, basis


# Build unified 78-Agent Registry
all_agents_map = {}

# 1. Load all 60 original agents first (zero overwrites!)
for aid, a in cat["agents"].items():
    st = PILLAR_STYLE[a["deptId"]]
    dep_info = deployed_map.get(aid)
    tier, payback, seats, hrs_yr, prod, flow, shield, recov, tot_val, active_levers, lever_basis = build_lever_meta(aid)
    subs = a.get("subAgents", [])
    reads = to_inr_prose(subs[0]["role"]) if len(subs) > 0 else f"Ingests {SYSTEM_BY_DEPT[a['deptId']]} and BigQuery Cortex v7 tables."
    does = to_inr_prose(subs[1]["role"]) if len(subs) > 1 else to_inr_prose(a.get("solverStack") or "Runs Vertex AI TimesFM & OR-Tools deterministic optimization.")
    returns = to_inr_prose(subs[2]["role"]) if len(subs) > 2 else to_inr_prose(a.get("outcome") or "Produces ranked exception action table and A2UI visual brief.")
    ge_full = dep_info.get("gemini_enterprise_agent", "") if dep_info else ""
    ge_short = ge_full.split("/")[-1] if ge_full else ""
    ge_url = (
        f"https://vertexaisearch.cloud.google.com/home/cid/{GE_CID}/r/agent/{ge_short}/session/-?mods=&authuser={GE_AUTH}"
        if ge_short else GE_WORKSPACE_URL
    )
    vfile = VIDEO_BY_AGENT.get(aid) or VIDEO_BY_DEPT.get(a["deptId"], "demand_sensing_demo.mp4")

    # Extract rich sub-workflows for chessboard generation
    sub_wfs = []
    prob_sentence = to_inr_prose((a.get("problem") or "").split(". ")[0].strip())
    if prob_sentence and not prob_sentence.endswith("."):
        prob_sentence += "."
    for s_i, sub in enumerate(subs[:3]):
        role_clean = to_inr_prose(sub.get("role", "").strip().rstrip("."))
        sname = to_inr_prose(sub.get("name", "").strip())
        wf_title = f"{sname}: {role_clean[0].lower() + role_clean[1:]}" if sname and role_clean else (role_clean or a["name"])
        if len(wf_title) > 96:
            wf_title = role_clean[:94].rstrip()
        sub_wfs.append((
            wf_title,
            f"Specialists manually pull CSV exports from {SYSTEM_BY_DEPT[a['deptId']]} to handle {sname.lower() if sname else 'this step'} on spreadsheets.",
            prob_sentence or "Delayed manual reconciliation misses fast-moving CPG shelf-life, OTIF, and margin exceptions.",
            f"{role_clean}. Stages policy-checked output via {to_inr_prose(a.get('apiWriteback', 'Apigee MCP'))} for human sign-off.",
        ))

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
        "priorityTier": tier,
        "prioBoard": "first" if tier == "P0" else ("next" if tier == "P1" else "routine"),
        "paybackDays": payback,
        "seats": seats,
        "hrsPerSeatYr": hrs_yr,
        "prod": prod, "flow": flow, "shield": shield, "recov": recov,
        "activeLevers": active_levers,
        "leverCount": len(active_levers),
        "leverBasis": lever_basis,
        "annualValueCr": tot_val,
        "annualValueDisplay": fmt_inr(tot_val),
        "oneLine": to_inr_prose(a.get("shortDesc") or a.get("outcome") or ""),
        "outcome": to_inr_prose(a.get("outcome") or a.get("shortDesc") or ""),
        "problem": to_inr_prose(a.get("problem") or ""),
        "reads": f"{reads} Connected CPG systems: {SYSTEM_BY_DEPT[a['deptId']]}.",
        "does": f"{does} ({to_inr_prose(a.get('solverStack', 'BigQuery ML + Google OR-Tools'))}).",
        "returns": f"{returns} Stages policy-checked action via {to_inr_prose(a.get('apiWriteback', 'Apigee MCP'))}.",
        "stopsAt": f"Never commits unapproved {SYSTEM_BY_DEPT[a['deptId']].split('·')[0].strip()} ledger mutations or overrides safety/contract policy without human sign-off.",
        "safetyEnvelope": "Flags missing sensor/ERP records for human review rather than extrapolating unverified values.",
        "samplePrompt": f"Show me our highest-priority {a.get('subPillarName', 'supply chain').lower()} exceptions across our CPG plants and CFA hubs this week, quantify ₹ Lakhs/Crores margin at risk, and recommend corrective actions.",
        "liveInGE": dep_info is not None,
        "geUrl": ge_url,
        "videoSrc": f"assets/media/video/{vfile}",
        "model": "gemini-3.1-pro-preview",
        "primaryPersonaId": a.get("primaryPersonaId", ""),
        "_subWfs": sub_wfs,
    }

# 2. Add the 18 new CPG agents cleanly
for na in NEW_CPG_AGENTS:
    aid = na["id"]
    st = PILLAR_STYLE[na["deptId"]]
    tier, payback, seats, hrs_yr, prod, flow, shield, recov, tot_val, active_levers, lever_basis = build_lever_meta(aid)
    vfile = VIDEO_BY_DEPT.get(na["deptId"], "demand_sensing_demo.mp4")
    sub_wfs = []
    for wf_t, wf_today, wf_vuln in na.get("subWorkflows", []):
        sub_wfs.append((
            wf_t,
            wf_today,
            wf_vuln,
            f"{to_inr_prose(na['does'])} Stops at: {to_inr_prose(na['stopsAt'])}",
        ))
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
        "priorityTier": tier,
        "prioBoard": "first" if tier == "P0" else ("next" if tier == "P1" else "routine"),
        "paybackDays": payback,
        "seats": seats,
        "hrsPerSeatYr": hrs_yr,
        "prod": prod, "flow": flow, "shield": shield, "recov": recov,
        "activeLevers": active_levers,
        "leverCount": len(active_levers),
        "leverBasis": lever_basis,
        "annualValueCr": tot_val,
        "annualValueDisplay": fmt_inr(tot_val),
        "oneLine": to_inr_prose(na["oneLine"]),
        "outcome": to_inr_prose(na["returns"]),
        "problem": to_inr_prose(na["oneLine"]),
        "reads": to_inr_prose(na["reads"]),
        "does": to_inr_prose(na["does"]),
        "returns": to_inr_prose(na["returns"]),
        "stopsAt": to_inr_prose(na["stopsAt"]),
        "safetyEnvelope": to_inr_prose(na["safetyEnvelope"]),
        "samplePrompt": f"Run {na['name']} across our active CPG SKUs and CFA depots today—highlight urgent exceptions, ₹ Lakhs/Crores impact, and what needs sign-off.",
        "liveInGE": False,
        "geUrl": GE_WORKSPACE_URL,
        "videoSrc": f"assets/media/video/{vfile}",
        "model": "gemini-3.1-pro-preview",
        "primaryPersonaId": na["linkedPersonas"][0],
        "linkedPersonas": na["linkedPersonas"],
        "_subWfs": sub_wfs,
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

CADENCES = ["15-min cycle", "Continuous", "Daily 05:30", "Per shift", "Daily", "Event-driven", "Weekly S&OP", "On approval"]
FRICTIONS = ["judgment", "traceability", "integrity", "computation", "synthesis", "consistency", "calculation", "assembly"]

personas = []
for idx, (pid, p) in enumerate(cat["personas"].items(), start=1):
    st = PILLAR_STYLE[p["deptId"]]
    pcode = f"P{idx:02d}"
    human_name, human_setting = PERSONA_HUMANS[idx - 1]
    primary_aid = p.get("primaryAgentId", "")
    primary_ag = all_agents_map[primary_aid]

    # Assemble this persona's 2-to-4 Agent Suite
    suite_ids = [primary_aid]
    for xid in extra_links_by_persona.get(pid, []):
        if xid not in suite_ids:
            suite_ids.append(xid)
    for peer_id in subpillar_agents.get((p["deptId"], p.get("subPillarName", "")), []):
        if peer_id not in suite_ids and len(suite_ids) < 3:
            suite_ids.append(peer_id)
    suite_ids = suite_ids[:4]

    raw_before = str(p.get("toilHoursBefore", "26"))
    raw_after = str(p.get("toilHoursAfter", "6"))
    if "$" in raw_before or "/inv" in raw_before or "/hr" in raw_before or "%" in raw_before:
        b_num, a_num = 28.0, 12.0
    else:
        b_num = float(re.findall(r"[\d.]+", raw_before)[0]) if re.findall(r"[\d.]+", raw_before) else 26.0
        a_num = float(re.findall(r"[\d.]+", raw_after)[0]) if re.findall(r"[\d.]+", raw_after) else 8.0
        if b_num > 45:
            b_num, a_num = 28.0, 9.0
    saved_hrs = max(5, round(b_num - a_num))

    # Build rich Agent Suite objects WITH exact 4-lever attribution on each suite member!
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
            "prod": ag_obj["prod"],
            "flow": ag_obj["flow"],
            "shield": ag_obj["shield"],
            "recov": ag_obj["recov"],
            "activeLevers": ag_obj["activeLevers"],
            "leverCount": ag_obj["leverCount"],
            "leverBasis": ag_obj["leverBasis"],
            "annualValueCr": ag_obj["annualValueCr"],
            "annualValueDisplay": ag_obj["annualValueDisplay"],
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

    # Non-double-counted Persona Value (in ₹ Crores): Primary Agent + any New CPG Agent owned primarily by this persona
    owned_agent_ids = [primary_aid] + [
        na["id"] for na in NEW_CPG_AGENTS if na["linkedPersonas"][0] == pid
    ]
    p_prod = round(sum(all_agents_map[x]["prod"] for x in owned_agent_ids), 2)
    p_flow = round(sum(all_agents_map[x]["flow"] for x in owned_agent_ids), 2)
    p_shield = round(sum(all_agents_map[x]["shield"] for x in owned_agent_ids), 2)
    p_recov = round(sum(all_agents_map[x]["recov"] for x in owned_agent_ids), 2)
    p_total = round(p_prod + p_flow + p_shield + p_recov, 2)

    p_basis = {}
    for lk in ("prod", "flow", "shield", "recov"):
        non_zero_notes = [all_agents_map[x]["leverBasis"][lk] for x in owned_agent_ids if all_agents_map[x][lk] > 0]
        p_basis[lk] = non_zero_notes[0] if non_zero_notes else ZERO_REASONS[lk]
    p_active_levers = [k for k, val in (("prod", p_prod), ("flow", p_flow), ("shield", p_shield), ("recov", p_recov)) if val > 0]

    p_tier = "P0" if any(all_agents_map[x]["priorityTier"] == "P0" for x in owned_agent_ids) else primary_ag["priorityTier"]
    b_prio = "first" if p_tier == "P0" else ("next" if p_tier == "P1" else "routine")

    # Build 12 authentic operational workflows for this persona (8 Agentic + 2 System + 2 Human)
    raw_agentic_pool = []
    for s_idx, sid in enumerate(suite_ids):
        ag_o = all_agents_map[sid]
        for wf_i, (wf_title, wf_today, wf_vuln, wf_plug) in enumerate(ag_o["_subWfs"]):
            raw_agentic_pool.append((s_idx, wf_i, ag_o, wf_title, wf_today, wf_vuln, wf_plug))

    # Add tailored synthesis / staged write-back / audit workflows if needed to reach 8 distinct agentic cells
    sys_short = SYSTEM_BY_DEPT[p["deptId"]].split("·")[0].strip()
    fallback_extras = [
        (0, 9, primary_ag,
         f"Stage policy-checked {p.get('subPillarName', 'operational')} action packet via Apigee MCP",
         f"{human_name.split()[0]} manually keys approved adjustments screen-by-screen into {sys_short}.",
         "Manual re-keying introduces SKU/quantity typos and delays execution by 6–18 hours after consensus.",
         f"{primary_ag['name']} pre-validates master-data & authority bounds and stages a 1-click {sys_short} write-back."),
        (min(1, len(suite_ids)-1), 10, all_agents_map[suite_ids[min(1, len(suite_ids)-1)]],
         f"Assemble cited {p.get('subPillarName', 'weekly')} variance & root-cause dossier in BigQuery Cortex",
         f"Analysts spend Friday afternoons stitching {SYSTEM_BY_DEPT[p['deptId']]} exports into review slides.",
         "Backward-looking variance decks arrive after the window to recover margin or shelf fill has closed.",
         f"{all_agents_map[suite_ids[min(1, len(suite_ids)-1)]]['name']} auto-compiles row-level rupee attribution with exact source lineage."),
    ]
    for fb in fallback_extras:
        if len(raw_agentic_pool) < 8:
            raw_agentic_pool.append(fb)
    raw_agentic_pool = raw_agentic_pool[:8]

    # Assign realistic build-queue priority (`first` / `next` / `routine`) per cell gated on agent tier
    if b_prio == "first":
        prio_pattern = ["first", "first", "next", "next", "next", "routine", "routine", "routine"]
    elif b_prio == "next":
        prio_pattern = ["next", "next", "next", "next", "routine", "routine", "routine", "routine"]
    else:
        prio_pattern = ["next", "routine", "routine", "routine", "routine", "routine", "routine", "routine"]

    status_map = {"first": "critical", "next": "friction", "routine": "baseline"}
    wt_map = {"first": 3.0, "next": 2.0, "routine": 1.0}
    wt_sum = sum(wt_map[pr] for pr in prio_pattern)

    actions = []
    for c_idx, (_, _, ag_o, wf_title, wf_today, wf_vuln, wf_plug) in enumerate(raw_agentic_pool):
        pr = prio_pattern[c_idx]
        st_tag = status_map[pr]
        cell_cr = round(p_total * (wt_map[pr] / wt_sum), 2)
        actions.append({
            "code": f"W{c_idx + 1:02d}",
            "fullCode": f"{pcode}W{c_idx + 1:02d}",
            "title": wf_title,
            "name": wf_title,
            "own": "agentic",
            "prio": pr,
            "status": st_tag,
            "friction": FRICTIONS[c_idx % len(FRICTIONS)],
            "scope": p.get("subPillarName", st["title"]),
            "cadence": CADENCES[c_idx % len(CADENCES)],
            "valueCr": cell_cr,
            "valueDisplay": fmt_inr(cell_cr),
            "today": wf_today,
            "vuln": wf_vuln,
            "withAgent": wf_plug,
            "plug": wf_plug,
            "agentId": ag_o["id"],
            "agentCode": ag_o["code"],
            "agentName": ag_o["name"],
            "agentPrio": ag_o["priorityTier"],
            "agentPaybackDays": ag_o["paybackDays"],
            "agentVal": {
                "prod": ag_o["prod"],
                "flow": ag_o["flow"],
                "shield": ag_o["shield"],
                "recov": ag_o["recov"],
                "total": ag_o["annualValueCr"],
                "leverCount": ag_o["leverCount"],
                "activeLevers": ag_o["activeLevers"],
            },
            "agentBasis": ag_o["leverBasis"],
            "liveInGE": ag_o["liveInGE"],
            "geUrl": ag_o["geUrl"],
            "source": SOURCE_BY_DEPT[p["deptId"]],
        })

    # Append 2 Incumbent System of Record (`own: "system"`) workflows — NEVER carry a priority rail!
    for m_idx, (m_title, m_holder, m_because, m_freq, m_scope) in enumerate(MONOLITH_TASKS_BY_DEPT[p["deptId"]]):
        wnum = len(actions) + 1
        actions.append({
            "code": f"W{wnum:02d}",
            "fullCode": f"{pcode}W{wnum:02d}",
            "title": m_title,
            "name": m_title,
            "own": "system",
            "prio": "",
            "status": "baseline",
            "friction": "execution",
            "scope": m_scope,
            "cadence": m_freq,
            "valueCr": 0.0,
            "valueDisplay": "—",
            "holder": m_holder,
            "reason": m_because,
            "because": m_because,
            "source": "[ERP / WMS Core]",
        })

    # Append 2 Human-Only Authority & Safety Gate (`own: "human"`) workflows — NEVER carry a priority rail!
    for h_idx, h_spec in enumerate(NOT_OWNED_BY_DEPT[p["deptId"]]):
        wnum = len(actions) + 1
        h_owner = h_spec["owner"].format(person=human_name, role=p["name"])
        actions.append({
            "code": f"W{wnum:02d}",
            "fullCode": f"{pcode}W{wnum:02d}",
            "title": h_spec["task"],
            "name": h_spec["task"],
            "own": "human",
            "prio": "",
            "status": "critical" if h_idx == 0 else "baseline",
            "friction": "judgment",
            "scope": "Enterprise policy gate",
            "cadence": "Before execution",
            "valueCr": 0.0,
            "valueDisplay": "—",
            "holder": h_owner,
            "reason": h_spec["because"],
            "because": h_spec["because"],
            "source": "[Governance Gate]",
        })

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
        "name": p["name"],
        "whatTheyDo": to_inr_prose(p.get("summary") or p.get("mandate") or ""),
        "whyItMatters": f"In high-velocity CPG operations across {human_setting}, delayed visibility directly triggers Modern Trade OTIF penalties, FEFO shelf-life write-offs, or unrecovered trade/freight leakage measured in ₹ Lakhs and Crores.",
        "systemsTouched": SYSTEM_BY_DEPT[p["deptId"]],
        "notOwned": [{"task": x["task"], "owner": x["owner"].format(person=human_name, role=p["name"])} for x in NOT_OWNED_BY_DEPT[p["deptId"]]],
        "honestLimit": f"Agents prepare deterministic scenarios and stage ERP/WMS actions, but {human_name} retains final commercial, safety, and counterparty accountability.",
        "headlineStat": to_inr_prose(p.get("headlineStat", "")),
        "toilHoursBefore": int(b_num),
        "toilHoursAfter": int(a_num),
        "savedHrs": saved_hrs,
        "primaryAgentId": primary_aid,
        "primaryAgentName": primary_ag["name"],
        "liveInGE": any(s["liveInGE"] for s in agent_suite),
        "priorityTier": p_tier,
        "prioBoard": b_prio,
        "paybackDays": primary_ag["paybackDays"],
        "val": {
            "prod": p_prod,
            "flow": p_flow,
            "shield": p_shield,
            "recov": p_recov,
            "total": p_total,
            "activeLevers": p_active_levers,
            "leverCount": len(p_active_levers),
            "basis": p_basis,
        },
        "annualValueCr": p_total,
        "annualValueDisplay": fmt_inr(p_total),
        "agentSuite": agent_suite,
        "actions": actions,
    })

# Clean internal helper field before serializing agents
for ag_v in all_agents_map.values():
    ag_v.pop("_subWfs", None)

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
                "annualValueCr": p_obj["annualValueCr"],
                "annualValueDisplay": p_obj["annualValueDisplay"],
                "activeLevers": p_obj["val"]["activeLevers"],
                "leverCount": p_obj["val"]["leverCount"],
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
        "coreQuestion": to_inr_prose(d.get("coreQuestion", "").strip()),
        "systems": SYSTEM_BY_DEPT[dept_id],
        "subPillars": sub_pillars,
        "personaCount": len(d.get("personaIds", [])),
        "agentCount": len(dept_agents),
        "newAgentCount": sum(1 for x in dept_agents if x["isNewCpgAgent"]),
        "p0Count": sum(1 for x in dept_agents if x["priorityTier"] == "P0"),
        "liveCount": sum(1 for x in dept_agents if x["liveInGE"]),
    })

CITATIONS = [
    {
        "org": "World Economic Forum",
        "year": "2026",
        "stat": "-62% Disruption Response Time",
        "sub": "Autonomous multi-agent supply chain networks cut disruption detection-to-recovery latency by 62% across plant & logistics corridors.",
        "url": "https://www.weforum.org/agenda/2026/09/how-agentic-ai-is-reshaping-supply-chain-resilience/",
    },
    {
        "org": "McKinsey Global Institute",
        "year": "2025",
        "stat": "45% of 1-Year EBITDA at Risk",
        "sub": "Supply chain shocks lasting 1+ month strike every 3.7 years, putting nearly half a year's operating profit (~₹3,400 Cr on a ₹68,000 Cr CPG business) at stake.",
        "url": "https://www.mckinsey.com/capabilities/operations/our-insights/risk-resilience-and-rebalancing-in-global-value-chains",
    },
    {
        "org": "Gartner Supply Chain",
        "year": "2026",
        "stat": "₹4.45 Lakh Cr Agentic SCM Spend",
        "sub": "Supply chain management software embedded with autonomous agentic AI projected to reach ₹4.45 Lakh Crore globally by 2030.",
        "url": "https://www.gartner.com/en/newsroom/press-releases/2026-04-07-gartner-forecasts-supply-chain-management-software-with-agentic-ai-will-grow-to-53-billion-in-spend-by-2030",
    },
    {
        "org": "Capgemini Research Institute",
        "year": "2025",
        "stat": "41% → 53% Last-Mile Cost Share",
        "sub": "Fulfillment and last-mile dispatch now exceed half of total logistics spend while 5–15% of carrier freight invoices carry billing errors.",
        "url": "https://www.capgemini.com/insights/research-library/the-last-mile-delivery-challenge/",
    },
    {
        "org": "BCG Consumer Goods Practice",
        "year": "2025",
        "stat": "25%–50% Trade Promos Destroy Margin",
        "sub": "Up to half of CPG trade promotions fail to break even due to unmodeled pack cannibalization, forward-buying, and unverified retailer deductions.",
        "url": "https://www.bcg.com/publications/2025/ai-powered-revenue-growth-management-in-consumer-goods",
    },
    {
        "org": "Unilever & Google Cloud",
        "year": "2026",
        "stat": "104-Week Rolling ML Forecast",
        "sub": "Production CPG deployment forecasting 5M+ SKU-customer combinations weekly alongside 40+ smart factory digital twins.",
        "url": "https://www.unilever.com/news/press-and-media/press-releases/2026/google-cloud-partnership-pioneers-next-generation-of-consumer-goods-technologies",
    },
]

payload = {
    "meta": {
        "domain": "CPG Multi-Echelon Supply Chain",
        "currency": "INR",
        "currencyUnits": "Crores (₹ Cr) & Lakhs (₹ L)",
        "pillars": len(departments),
        "subPillars": sum(len(d["subPillars"]) for d in departments),
        "personas": len(personas),
        "workflows": sum(len(p["actions"]) for p in personas),
        "baseAgents": 60,
        "newCpgAgents": len(NEW_CPG_AGENTS),
        "agents": len(all_agents_map),
        "twoLeverAgents": sum(1 for a in all_agents_map.values() if a["leverCount"] == 2),
        "threeLeverAgents": sum(1 for a in all_agents_map.values() if a["leverCount"] == 3),
        "p0Agents": sum(1 for a in all_agents_map.values() if a["priorityTier"] == "P0"),
        "liveInGE": sum(1 for a in all_agents_map.values() if a["liveInGE"]),
    },
    "departments": departments,
    "personas": personas,
    "agents": list(all_agents_map.values()),
    "citations": CITATIONS,
}

with open(OUT_DATA, "w", encoding="utf-8") as f:
    f.write("window.SC_DATA = ")
    json.dump(payload, f, separators=(",", ":"))
    f.write(";\n")

by_agent_js = {
    aid: {
        "tier": "first" if ag["priorityTier"] == "P0" else ("next" if ag["priorityTier"] == "P1" else "routine"),
        "priorityCode": ag["priorityTier"],
        "isNewCpg": ag["isNewCpgAgent"],
        "paybackDays": ag["paybackDays"],
        "seats": ag["seats"],
        "hrsPerSeatYr": ag["hrsPerSeatYr"],
        "prod": ag["prod"], "flow": ag["flow"], "shield": ag["shield"], "recov": ag["recov"],
        "total": ag["annualValueCr"],
        "leverCount": ag["leverCount"],
        "activeLevers": ag["activeLevers"],
        "basis": ag["leverBasis"],
        "why": ag["oneLine"],
    }
    for aid, ag in all_agents_map.items()
}

val_js_code = """/* CPG Supply Chain 4-Lever Researched Indian Rupee Value Model (₹ Crores & ₹ Lakhs · 60 Personas · 78 Agents · Load-Bearing Zeros) */
window.SC_VALUES = (function () {
  var ESTATE_BASELINE = {
    label: "₹42,000 Cr COGS / ₹68,000 Cr Gross Revenue Multi-Site CPG Enterprise Benchmark (20 ICML Plants · 48 CFA Depots · 3,800 DMS Stockists · 420 Dark Stores)",
    currency: "INR"
  };
  var LEVERS = [
    { id: "prod", short: "Productivity", name: "Productivity", color: "#3186FF", metric: "SG&A opex · planner, buyer & QA hours redeployed (@ ₹2,500/hr)", def: "Expert hours reclaimed from manual ERP/DMS spreadsheet assembly and redeployed onto commercial & supplier decisions (never stated as headcount reduction)." },
    { id: "flow", short: "Flow & Capital", name: "Flow & Capital", color: "#00AF57", metric: "Plant OEE %, 22% inventory carry cost & 32-ft FTL cube utilization", def: "Counted ONLY when an agent sits on a physical asset critical path (ICML changeover/uptime, warehouse wave, trailer cube) or releases multi-echelon safety stock." },
    { id: "shield", short: "Risk & Leakage", name: "Risk & Leakage", color: "#4B31E3", metric: "Audit clawbacks, OTIF/GST fines & recall/supplier barrier protection", def: "Expected financial leakage and compliance loss prevented across 3-way match, freight bills (5–15% error), trade deductions, E-Way bills & lot recalls." },
    { id: "recov", short: "Revenue Recovery", name: "Revenue Recovery", color: "#12B5CB", metric: "Incremental shelf/dark-store off-take, RGM pack margin & FEFO salvage", def: "The ONLY lever that counts upward — lost shelf/Quick-Commerce sales captured and near-expiry/returned stock converted into net contribution margin." }
  ];
  var BY_AGENT = """ + json.dumps(by_agent_js, separators=(",", ":")) + """;
  function r2(n) { return Math.round((n || 0) * 100) / 100; }
  function fmtINR(cr, suffix) {
    var sfx = suffix || "";
    var n = Number(cr) || 0;
    if (n <= 0) return "—";
    if (n >= 1000) return "₹" + n.toLocaleString("en-IN", { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + " Cr" + sfx;
    if (n >= 1) return "₹" + n.toFixed(1) + " Cr" + sfx;
    return "₹" + Math.max(1, Math.round(n * 100)) + " L" + sfx;
  }
  function computeForPersonas(personas) {
    var byPersonaId = {}, byDeptId = {};
    var estateTotals = { prod: 0, flow: 0, shield: 0, recov: 0, total: 0, savedHrsWk: 0, personas: 0, firstCount: 0, nextCount: 0, routineCount: 0 };
    (personas || []).forEach(function (p) {
      var v = p.val || { prod: 0.7, flow: 0, shield: 14.0, recov: 0, total: 14.7 };
      var tier = p.prioBoard || "next";
      var rec = {
        personaId: p.id, agentId: p.primaryAgentId, deptId: p.deptId,
        tier: tier, priorityCode: p.priorityTier || "P1", paybackDays: p.paybackDays || 90,
        prod: v.prod, flow: v.flow, shield: v.shield, recov: v.recov, total: v.total,
        leverCount: v.leverCount || 2, activeLevers: v.activeLevers || ["prod", "shield"],
        basis: v.basis || {},
        why: (BY_AGENT[p.primaryAgentId] && BY_AGENT[p.primaryAgentId].why) || p.whatTheyDo
      };
      byPersonaId[p.id] = rec;
      if (!byDeptId[p.deptId]) byDeptId[p.deptId] = { prod: 0, flow: 0, shield: 0, recov: 0, total: 0, savedHrsWk: 0, personas: 0, firstCount: 0, nextCount: 0, routineCount: 0 };
      var d = byDeptId[p.deptId];
      d.prod = r2(d.prod + v.prod); d.flow = r2(d.flow + v.flow); d.shield = r2(d.shield + v.shield); d.recov = r2(d.recov + v.recov); d.total = r2(d.total + v.total);
      d.savedHrsWk += (p.savedHrs || 0); d.personas += 1;
      if (tier === "first") d.firstCount += 1; else if (tier === "next") d.nextCount += 1; else d.routineCount += 1;

      estateTotals.prod = r2(estateTotals.prod + v.prod); estateTotals.flow = r2(estateTotals.flow + v.flow);
      estateTotals.shield = r2(estateTotals.shield + v.shield); estateTotals.recov = r2(estateTotals.recov + v.recov);
      estateTotals.total = r2(estateTotals.total + v.total); estateTotals.savedHrsWk += (p.savedHrs || 0); estateTotals.personas += 1;
      if (tier === "first") estateTotals.firstCount += 1; else if (tier === "next") estateTotals.nextCount += 1; else estateTotals.routineCount += 1;
    });
    return { byPersonaId: byPersonaId, byDeptId: byDeptId, estateTotals: estateTotals };
  }
  return { ESTATE_BASELINE: ESTATE_BASELINE, LEVERS: LEVERS, BY_AGENT: BY_AGENT, fmtINR: fmtINR, computeForPersonas: computeForPersonas };
})();
"""

with open(OUT_VAL, "w", encoding="utf-8") as f:
    f.write(val_js_code)

est_tot = round(sum(p["val"]["total"] for p in personas), 1)
est_prod = round(sum(p["val"]["prod"] for p in personas), 1)
est_flow = round(sum(p["val"]["flow"] for p in personas), 1)
est_shield = round(sum(p["val"]["shield"] for p in personas), 1)
est_recov = round(sum(p["val"]["recov"] for p in personas), 1)
print(
    f"Built CPG Portal Data: {len(personas)} personas × 12 workflows = {payload['meta']['workflows']} cells | "
    f"78 agents ({payload['meta']['twoLeverAgents']} move 2 levers, {payload['meta']['threeLeverAgents']} move 3 levers, 0 move 4 levers!) | "
    f"Estate Total: ₹{est_tot:,.1f} Cr/yr (Prod ₹{est_prod} Cr · Flow ₹{est_flow} Cr · Shield ₹{est_shield} Cr · Recov ₹{est_recov} Cr)"
)
