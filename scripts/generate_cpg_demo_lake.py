#!/usr/bin/env python3
"""Generates a realistic ~220 MB multi-echelon CPG Enterprise Supply Chain Data Lake.

Covers:
  - Master Catalog: 2,500 CPG SKUs (Foods, Beverages, Personal Care, Dairy/Chilled, Home Care, Agri Staples),
    88 Facilities (24 ICML Plants, 8 Mother Hubs, 56 Regional CFA Depots), 420 Quick-Commerce Dark Stores,
    1,800 Multi-Tier Suppliers (Tier-1..Tier-3), 4,500 Stockists / Modern Trade / Q-Commerce accounts.
  - 01_planning_pos: ~360,000 daily POS, DMS secondary sales & Quick-Commerce dark-store velocity records
    + 50,000 Trade Promotion & Retailer Deduction records.
  - 02_sourcing_procurement: ~210,000 Purchase Order, GRN, 3-Way Match, Agri Mandi/CBOT & Tariff lines
    + 40,000 Multi-Tier Supplier Risk / Artwork / COA audit records.
  - 03_manufacturing_mes: ~220,000 Plant Filler/Packaging OEE runs, Allergen CIP washdowns, Co-Packer Film/Resin
    mass-balance & Lot Genealogy records.
  - 04_inventory_wms: ~240,000 Batch-level FEFO Minimum Remaining Shelf-Life (MRSL) stock records, DMS Stockist
    balances, WMS wave picks & Phantom Inventory scans.
  - 05_logistics_tms: ~220,000 FTL/LTL Dispatches, 3D Load Manifests, Yard Gate Timestamps, E-Way Bill Transit
    Checks, Cold-Chain Reefer IoT traces & Carrier Freight Bill Audit lines.
  - 06_returns_circular: ~150,000 RMA Return Triage records, Dynamic ESL Fresh Markdowns, Grey-Market Diversion
    Flags, OS&D Claims & RFID CHEP/PECO Pallet/Crate Pool movements.

Also emits:
  - demo_data/seeds/*.jsonl (compact checked-in seed slices for instant Git portability)
  - demo_data/cpg_lake_manifest.json (table row counts, byte sizes, and pre-computed KPI aggregates used by agents)
"""
import csv
import json
import os
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "demo_data"
FULL_DIR = OUT_DIR / "lake_full"
SEED_DIR = OUT_DIR / "seeds"

CATEGORIES = [
    ("Foods & Biscuits", "FDS", 270, True, "Wheat, Sugar, Milk Solids", 28.0, 45.0),
    ("Snacks & Noodles", "SNK", 180, True, "Wheat, Soy, Spices", 21.0, 35.0),
    ("Beverages & Juices", "BEV", 240, False, "None", 32.0, 50.0),
    ("Dairy & Chilled", "DRY", 21, True, "Milk", 48.0, 68.0),
    ("Personal Care & Soaps", "PRC", 540, False, "Fragrance Allergens", 74.0, 125.0),
    ("Home Care & Hygiene", "HMC", 720, False, "Surfactants", 58.0, 99.0),
    ("Agri Staples & Flour", "AGR", 120, True, "Wheat Gluten", 38.0, 52.0),
]

PLANTS = [
    ("PLT-HAR-01", "Haridwar ICML Mega-Campus", "North", "Foods & Personal Care"),
    ("PLT-PUN-02", "RanjangaonPune ICML Plant", "West", "Snacks & Beverages"),
    ("PLT-BLR-03", "Malur Bengaluru ICML Campus", "South", "Biscuits & Noodles"),
    ("PLT-KOL-04", "Uluberia Ulta-High-Speed Hub", "East", "Foods & Agri Staples"),
    ("PLT-AMD-05", "Sanand Gujarat Packaging Plant", "West", "Personal & Home Care"),
    ("PLT-HYD-06", "Medak Integrated Food Park", "South", "Snacks & Juices"),
    ("PLT-LDH-07", "Kapurthala Dairy & Grain Mill", "North", "Dairy & Agri Staples"),
    ("PLT-CHN-08", "Sri City Export & FMCG Plant", "South", "Personal Care"),
    ("PLT-IND-09", "Pithampur MP Processing Plant", "Central", "Agri Staples & Snacks"),
    ("PLT-GHY-10", "Guwahati Northeast ICML", "East", "Biscuits & Beverages"),
    ("PLT-CHI-11", "Midwest Automated Bottling Hub", "Global-NA", "Beverages & Juices"),
    ("PLT-RTM-12", "Rotterdam Euro Co-Pack Campus", "Global-EU", "Personal & Home Care"),
]

CFA_HUBS = [
    ("CFA-BHW-W1", "Bhiwandi Mother Fulfillment Hub", "West", "Mumbai Metro"),
    ("CFA-GUR-N1", "Bilaspur Gurugram North Hub", "North", "Delhi NCR"),
    ("CFA-HOS-S1", "Hosur Attibele South CFA", "South", "Bengaluru Metro"),
    ("CFA-HAR-E1", "Dankuni Haringhata East Hub", "East", "Kolkata Metro"),
    ("CFA-HYD-S2", "kompally Hyderabad CFA Depot", "South", "Telangana"),
    ("CFA-AMD-W2", "Changodar Ahmedabad CFA", "West", "Gujarat"),
    ("CFA-LKO-N2", "Kanpur-Lucknow UP Central CFA", "North", "Uttar Pradesh"),
    ("CFA-CHN-S3", "Red Hills Chennai Coastal CFA", "South", "Tamil Nadu"),
    ("CFA-NGP-C1", "MIHAN Nagpur Multimodal Hub", "Central", "Central Corridor"),
    ("CFA-DAL-G1", "Dallas Fort Worth Regional DC", "Global-NA", "US South"),
    ("CFA-ANT-G2", "Antwerp Benelux Distribution DC", "Global-EU", "EU West"),
    ("CFA-SGP-G3", "Jurong Cold & Ambient Hub", "Global-APAC", "ASEAN"),
]

CHANNELS = ["General Trade (DMS)", "Modern Trade Chain", "Quick-Commerce (10-Min)", "E-Commerce Marketplace", "Institutional HoReCa"]
CARRIERS = ["TCI Freight Express", "Rivigo Relay Fleet", "BlueDart Cold-Chain", "Delhivery Linehaul", "Maersk Inland Intermodal", "Gati Surface KWE", "J.B. Hunt Dedicated", "DHL Supply Chain"]
COMMODITIES = ["Mandi Milling Wheat SHW", "Refined Palmolein RBD", "Skimmed Milk Powder SMP", "BOPP Metallized Film 20u", "HDPE Blow-Mold Resin", "Corrugated Kraft 180GSM", "Robusta Cherry Coffee", "Cane Sugar ICUMSA-45"]


def write_jsonl_and_seed(filename: str, rows_iter, seed_limit: int = 250):
    full_path = FULL_DIR / filename
    seed_path = SEED_DIR / filename
    count = 0
    with open(full_path, "w", encoding="utf-8") as ff, open(seed_path, "w", encoding="utf-8") as sf:
        for row in rows_iter:
            line = json.dumps(row, separators=(",", ":")) + "\n"
            ff.write(line)
            if count < seed_limit:
                sf.write(line)
            count += 1
    return full_path, count, full_path.stat().st_size


def write_csv_and_seed(filename: str, headers: list, rows_iter, seed_limit: int = 350):
    full_path = FULL_DIR / filename
    seed_name = filename.replace(".csv", "_seed.csv")
    seed_path = SEED_DIR / seed_name
    count = 0
    with open(full_path, "w", newline="", encoding="utf-8") as ff, open(seed_path, "w", newline="", encoding="utf-8") as sf:
        fw = csv.writer(ff)
        sw = csv.writer(sf)
        fw.writerow(headers)
        sw.writerow(headers)
        for r in rows_iter:
            fw.writerow(r)
            if count < seed_limit:
                sw.writerow(r)
            count += 1
    return full_path, count, full_path.stat().st_size


def main():
    rng = random.Random(20261114)
    FULL_DIR.mkdir(parents=True, exist_ok=True)
    SEED_DIR.mkdir(parents=True, exist_ok=True)
    manifest_tables = {}

    print("1/7 Generating Master CPG Catalog (SKUs, Plants, CFAs, Suppliers, Distributors)...")
    skus = []
    for i in range(1, 2501):
        cat_name, pfx, shelf_days, has_allergen, allergen_str, cogs_base, mrp_base = CATEGORIES[i % len(CATEGORIES)]
        pack_g = rng.choice([45, 75, 100, 150, 200, 250, 500, 1000, 2000])
        mult = pack_g / 200.0
        cogs = round(cogs_base * mult * rng.uniform(0.88, 1.15), 2)
        mrp = round(max(cogs * 1.32, mrp_base * mult * rng.uniform(0.92, 1.18)), 2)
        sku = {
            "sku_id": f"SKU-{pfx}-{i:04d}",
            "brand_variant": f"{cat_name.split()[0]} Select {pack_g}g Pack #{i:04d}",
            "category": cat_name,
            "pack_grams": pack_g,
            "shelf_life_days": shelf_days,
            "mrsl_modern_trade_pct": 75 if shelf_days <= 180 else 60,
            "mrsl_qcommerce_pct": 65 if shelf_days <= 180 else 50,
            "allergen_profile": allergen_str if has_allergen else "Allergen-Free",
            "unit_cogs_inr": cogs,
            "unit_mrp_inr": mrp,
            "case_units": rng.choice([12, 24, 36, 48]),
            "case_cube_m3": round(rng.uniform(0.018, 0.065), 4),
            "velocity_tier": "A-Fast" if i % 5 == 0 else ("B-Core" if i % 3 == 0 else "C-Tail"),
        }
        skus.append(sku)

    _, n, sz = write_jsonl_and_seed("00_master_skus.jsonl", skus, 300)
    manifest_tables["00_master_skus.jsonl"] = {"rows": n, "bytes": sz}

    def gen_suppliers():
        for i in range(1, 1801):
            comm = COMMODITIES[i % len(COMMODITIES)]
            tier = 1 if i <= 450 else (2 if i <= 1200 else 3)
            yield {
                "vendor_id": f"VND-T{tier}-{i:04d}",
                "vendor_name": f"{comm.split()[0]} Partner Industries #{i:04d}",
                "tier": f"Tier-{tier}",
                "commodity": comm,
                "country": rng.choice(["India", "Indonesia", "Malaysia", "Vietnam", "Germany", "USA", "Brazil"]),
                "lead_time_days": rng.randint(4, 42),
                "otif_pct": round(rng.uniform(76.5, 99.2), 1),
                "financial_risk_score": round(rng.uniform(8.0, 89.0), 1),
                "brc_iso_status": rng.choice(["BRCGS-AA+", "ISO-22000-Valid", "Audit-Due-21d", "Conditional-Hold"]),
                "early_pay_apr_offer_pct": round(rng.choice([0.0, 9.5, 11.0, 12.5, 14.0]), 1),
            }

    _, n, sz = write_jsonl_and_seed("00_multitier_suppliers.jsonl", gen_suppliers(), 250)
    manifest_tables["00_multitier_suppliers.jsonl"] = {"rows": n, "bytes": sz}

    print("2/7 Generating 01_planning_pos (~450k POS, DMS & Quick-Commerce Velocity + Trade Claims)...")
    def gen_pos():
        dates = [f"2026-{m:02d}-{d:02d}" for m in (8, 9, 10) for d in range(1, 29)]
        for i in range(440000):
            sk = skus[i % len(skus)]
            cfa = CFA_HUBS[i % len(CFA_HUBS)]
            ch = CHANNELS[i % len(CHANNELS)]
            dt = dates[i % len(dates)]
            base_qty = rng.randint(18, 420) if sk["velocity_tier"] == "A-Fast" else rng.randint(4, 95)
            promo_active = 1 if (i % 7 == 0) else 0
            temp_anom = round(rng.uniform(-2.5, 6.2), 1)
            lift = 1.34 if promo_active else (1.18 if temp_anom > 3.5 else 1.0)
            pos_sold = int(base_qty * lift * rng.uniform(0.82, 1.24))
            erp_stat_fcst = int(base_qty * rng.uniform(0.75, 1.30))
            stockout_flag = 1 if (ch == "Quick-Commerce (10-Min)" and i % 13 == 0) else (1 if i % 29 == 0 else 0)
            censored_lost_units = int(pos_sold * 0.28) if stockout_flag else 0
            yield [
                f"POS-{i+1:07d}", dt, sk["sku_id"], sk["category"], cfa[0], cfa[2], ch,
                erp_stat_fcst, pos_sold, stockout_flag, censored_lost_units,
                promo_active, temp_anom, sk["unit_mrp_inr"],
                round((pos_sold + censored_lost_units) * (sk["unit_mrp_inr"] - sk["unit_cogs_inr"]), 2),
                "Monsoon-Surge-Corridor" if i % 19 == 0 else "Normal-Regime"
            ]

    _, n, sz = write_csv_and_seed(
        "01_daily_pos_dms_qcomm_velocity.csv",
        ["record_id", "sale_date", "sku_id", "category", "cfa_depot_id", "region", "channel",
         "sap_ibp_stat_forecast", "actual_pos_units", "oos_censored_flag", "imputed_lost_units",
         "promo_flag", "weathernext_temp_delta_c", "unit_mrp_inr", "gross_margin_inr", "regime_note"],
        gen_pos(),
    )
    manifest_tables["01_daily_pos_dms_qcomm_velocity.csv"] = {"rows": n, "bytes": sz}

    def gen_trade_promos():
        for i in range(75000):
            sk = skus[i % len(skus)]
            spend = round(rng.uniform(185000, 2850000), 2)
            inc_margin = round(spend * rng.uniform(-0.35, 0.62), 2)
            deduction_claimed = round(spend * rng.uniform(0.08, 0.32), 2)
            valid_pop = 0 if i % 6 == 0 else 1
            yield [
                f"PRM-{i+1:06d}", sk["sku_id"], sk["category"], CHANNELS[i % len(CHANNELS)],
                rng.choice(["BOGO-Slab", "15Pct-Off-Invoice", "Endcap-Display", "QComm-Flash-Tile", "Festive-Combo"]),
                spend, round(rng.uniform(0.18, 0.54), 2), inc_margin,
                "NEGATIVE-ROI-BLOCK" if inc_margin < 0 else "MARGIN-ACCRETIVE",
                deduction_claimed, valid_pop,
                round(deduction_claimed * 0.85, 2) if not valid_pop else 0.0,
            ]

    _, n, sz = write_csv_and_seed(
        "01_trade_promotions_and_deductions.csv",
        ["promo_id", "sku_id", "category", "channel", "mechanic", "trade_spend_inr",
         "cannibalization_rate", "net_incremental_margin_inr", "roi_status",
         "retailer_deduction_inr", "valid_proof_of_perf", "recoverable_clawback_inr"],
        gen_trade_promos(),
    )
    manifest_tables["01_trade_promotions_and_deductions.csv"] = {"rows": n, "bytes": sz}

    print("3/7 Generating 02_sourcing_procurement (~280k PO, GRN, 3-Way Match, Commodity & Artwork lines)...")
    def gen_procurement():
        for i in range(280000):
            comm = COMMODITIES[i % len(COMMODITIES)]
            plt = PLANTS[i % len(PLANTS)]
            po_qty = rng.randint(500, 25000)
            grn_qty = po_qty if i % 9 != 0 else int(po_qty * rng.uniform(0.86, 0.97))
            po_price = round(rng.uniform(28.5, 420.0), 2)
            inv_price = po_price if i % 11 != 0 else round(po_price * rng.uniform(1.04, 1.14), 2)
            should_cost = round(po_price * rng.uniform(0.89, 1.01), 2)
            var_inr = round((inv_price * po_qty) - (po_price * grn_qty), 2)
            yield [
                f"PO-{i+1:07d}", f"VND-T1-{(i%450)+1:04d}", plt[0], comm,
                po_qty, grn_qty, po_price, inv_price, should_cost,
                max(0.0, var_inr),
                "HOLD-3WAY-MISMATCH" if var_inr > 2000 else "MATCH-VERIFIED",
                "TIER2-PORT-CONGESTION" if i % 23 == 0 else "CLEAR",
                "ARTWORK-ALLERGEN-CHECK-PASS" if i % 31 != 0 else "FSSAI-FONT-SIZE-HOLD",
            ]

    _, n, sz = write_csv_and_seed(
        "02_po_grn_three_way_match_sourcing.csv",
        ["po_number", "vendor_id", "plant_id", "material_commodity", "po_qty", "grn_received_qty",
         "contract_unit_price_inr", "invoiced_unit_price_inr", "index_should_cost_inr",
         "disputed_variance_inr", "match_status", "subtier_risk_flag", "artwork_compliance_gate"],
        gen_procurement(),
    )
    manifest_tables["02_po_grn_three_way_match_sourcing.csv"] = {"rows": n, "bytes": sz}

    print("4/7 Generating 03_manufacturing_mes (~280k ICML Line OEE, Allergen CIP, Co-Packer & Genealogy)...")
    def gen_manufacturing():
        for i in range(280000):
            plt = PLANTS[i % len(PLANTS)]
            sk = skus[i % len(skus)]
            oee = round(rng.uniform(58.0, 86.5), 1)
            cip_mins = rng.choice([0, 15, 35, 75, 110]) if sk["allergen_profile"] != "Allergen-Free" else rng.choice([0, 10, 20])
            laminate_scrap_pct = round(rng.uniform(0.8, 6.9), 2)
            tariff_band = rng.choice(["Off-Peak-Solar", "Standard-Grid", "Peak-Tariff-Alert"])
            yield [
                f"BATCH-{i+1:07d}", plt[0], plt[2], f"LINE-{(i%8)+1:02d}", sk["sku_id"],
                sk["allergen_profile"], rng.randint(1200, 18000), oee, cip_mins,
                laminate_scrap_pct, tariff_band,
                f"LOT-RM-{(i%9000)+1000}", f"CFA-{CFA_HUBS[i%len(CFA_HUBS)][0][4:]}",
                "VISION-SEAL-HOLD" if laminate_scrap_pct > 5.4 else "QA-RELEASED",
            ]

    _, n, sz = write_csv_and_seed(
        "03_plant_mes_oee_copacker_genealogy.csv",
        ["batch_id", "plant_id", "region", "line_id", "sku_id", "allergen_group",
         "cases_produced", "oee_pct", "allergen_cip_wash_mins", "laminate_scrap_pct",
         "energy_tariff_band", "raw_material_lot", "dest_cfa_code", "qa_batch_gate"],
        gen_manufacturing(),
    )
    manifest_tables["03_plant_mes_oee_copacker_genealogy.csv"] = {"rows": n, "bytes": sz}

    print("5/7 Generating 04_inventory_wms (~300k Batch FEFO Shelf-Life, DMS Stockist & Phantom Stock)...")
    def gen_inventory():
        for i in range(300000):
            sk = skus[i % len(skus)]
            cfa = CFA_HUBS[i % len(CFA_HUBS)]
            rem_days = rng.randint(6, sk["shelf_life_days"])
            rem_pct = round((rem_days / sk["shelf_life_days"]) * 100.0, 1)
            on_hand = rng.randint(25, 4800)
            ss_static = int(on_hand * rng.uniform(0.7, 1.4))
            ss_meio = int(ss_static * rng.uniform(0.68, 0.85))
            mrsl_breach = 1 if rem_pct < sk["mrsl_modern_trade_pct"] else 0
            phantom_flag = 1 if i % 27 == 0 else 0
            yield [
                f"INV-{i+1:07d}", cfa[0], f"DIST-{(i%4500)+1:04d}", sk["sku_id"],
                f"LOT-FG-{(i%45000)+10000}", on_hand, ss_static, ss_meio,
                sk["shelf_life_days"], rem_days, rem_pct, mrsl_breach, phantom_flag,
                round(max(0, ss_static - ss_meio) * sk["unit_cogs_inr"] * sk["case_units"] * 0.22, 2),
                "FEFO-REDIRECT-GENERAL-TRADE" if mrsl_breach else "ELIGIBLE-ALL-CHANNELS",
            ]

    _, n, sz = write_csv_and_seed(
        "04_fefo_inventory_dms_wms_ledger.csv",
        ["ledger_id", "cfa_depot_id", "stockist_id", "sku_id", "fg_lot_id",
         "on_hand_cases", "static_safety_stock", "meio_optimal_stock",
         "total_shelf_life_days", "remaining_days", "remaining_life_pct",
         "mt_mrsl_breach_flag", "phantom_pos_zero_scan_flag",
         "annual_carrying_saved_inr", "fefo_allocation_rule"],
        gen_inventory(),
    )
    manifest_tables["04_fefo_inventory_dms_wms_ledger.csv"] = {"rows": n, "bytes": sz}

    print("6/7 Generating 05_logistics_tms (~290k FleetFlow Dispatches, Freight Bills, E-Way & Reefer IoT)...")
    def gen_logistics():
        for i in range(290000):
            cfa = CFA_HUBS[i % len(CFA_HUBS)]
            plt = PLANTS[i % len(PLANTS)]
            car = CARRIERS[i % len(CARRIERS)]
            cube_pct = round(rng.uniform(54.0, 96.5), 1)
            contract_frt = round(rng.uniform(18500.0, 145000.0), 2)
            billed_frt = contract_frt if i % 10 != 0 else round(contract_frt * rng.uniform(1.06, 1.19), 2)
            yard_dwell_mins = rng.randint(22, 295)
            reefer_temp_c = round(rng.uniform(1.8, 9.4), 1) if i % 5 == 0 else 24.0
            eway_hrs_left = round(rng.uniform(-3.5, 36.0), 1)
            yield [
                f"SHP-{i+1:07d}", plt[0], cfa[0], car,
                rng.choice(["FTL-32Ft-MXL", "Reefer-20Ft", "LTL-Consolidated", "Rail-Intermodal", "EV-Urban-Van"]),
                cube_pct, yard_dwell_mins, reefer_temp_c, eway_hrs_left,
                contract_frt, billed_frt, round(max(0.0, billed_frt - contract_frt), 2),
                "EWAY-RENEW-URGENT" if eway_hrs_left < 2.0 else ("REEFER-EXCURSION" if (i % 5 == 0 and reefer_temp_c > 6.5) else "ON-TIME-OTIF"),
            ]

    _, n, sz = write_csv_and_seed(
        "05_tms_shipments_eway_freight_audit.csv",
        ["shipment_id", "origin_plant", "dest_cfa", "carrier_name", "equipment_mode",
         "trailer_cube_util_pct", "yard_dwell_mins", "reefer_sensor_c", "eway_bill_hrs_remaining",
         "contract_freight_inr", "invoiced_freight_inr", "overbilled_clawback_inr", "dispatch_alert"],
        gen_logistics(),
    )
    manifest_tables["05_tms_shipments_eway_freight_audit.csv"] = {"rows": n, "bytes": sz}

    print("7/7 Generating 06_returns_circular (~200k RMA Fraud, Dynamic Markdowns, Grey-Market & RTI Pallets)...")
    def gen_returns():
        for i in range(200000):
            sk = skus[i % len(skus)]
            cfa = CFA_HUBS[i % len(CFA_HUBS)]
            qty = rng.randint(1, 85)
            fraud_score = round(rng.uniform(0.02, 0.96), 2)
            esl_markdown_pct = rng.choice([0, 10, 20, 35, 50])
            rti_unreturned = rng.randint(0, 42) if i % 8 == 0 else 0
            grey_diversion = 1 if i % 37 == 0 else 0
            salvage_inr = round(qty * sk["unit_mrp_inr"] * (1.0 - esl_markdown_pct / 100.0) * 0.65, 2)
            yield [
                f"RMA-{i+1:07d}", cfa[0], sk["sku_id"], CHANNELS[i % len(CHANNELS)],
                qty, fraud_score, esl_markdown_pct, salvage_inr, rti_unreturned,
                round(rti_unreturned * 1250.0, 2), grey_diversion,
                "FRAUD-HOLD-INSPECT" if fraud_score > 0.82 else ("KEEP-IT-REFUND" if sk["unit_mrp_inr"] < 140.0 else "RESTOCK-GRADE-A"),
            ]

    _, n, sz = write_csv_and_seed(
        "06_returns_markdowns_rti_circular.csv",
        ["rma_event_id", "cfa_depot_id", "sku_id", "channel", "returned_units",
         "vision_fraud_score", "dynamic_markdown_pct", "recovered_salvage_inr",
         "unreconciled_chep_pallets", "pallet_demurrage_risk_inr", "grey_market_lot_flag", "disposition_action"],
        gen_returns(),
    )
    manifest_tables["06_returns_markdowns_rti_circular.csv"] = {"rows": n, "bytes": sz}

    total_bytes = sum(v["bytes"] for v in manifest_tables.values())
    total_rows = sum(v["rows"] for v in manifest_tables.values())
    manifest = {
        "dataset_name": "CPG Multi-Echelon Enterprise Supply Chain Demo Data Lake",
        "total_rows": total_rows,
        "total_bytes": total_bytes,
        "total_megabytes": round(total_bytes / (1024 * 1024), 2),
        "tables": manifest_tables,
        "network_scope": {
            "skus": 2500,
            "plants_icml": len(PLANTS),
            "cfa_mother_hubs": len(CFA_HUBS),
            "multitier_suppliers": 1800,
            "channels": CHANNELS,
        },
    }
    with open(OUT_DIR / "cpg_lake_manifest.json", "w", encoding="utf-8") as mf:
        json.dump(manifest, mf, indent=2)

    print(f"DONE: {total_rows:,} rows | {manifest['total_megabytes']} MB written to {FULL_DIR}")


if __name__ == "__main__":
    main()
