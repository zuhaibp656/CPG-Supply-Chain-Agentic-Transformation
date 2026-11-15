#!/usr/bin/env python3
"""Generates the ITC Limited CPG Trade Marketing & Distribution (TM&D) Enterprise Data Lake
for Pillars 5 & 6 (12 Distribution, CFA, Route-to-Market & Freight Governance Agents).

Outputs:
1. `enterprise_data/seeds/00_itc_network_backbone.json`:
   - 8 Integrated Consumer Goods Manufacturing and Logistics (ICML) Mega-Plants
   - 24 State Clearing & Forwarding Agent (CFA) Depots across 5 TM&D Zones
   - 360 Wholesale Dealers (WDs) / Exclusive Stockists with FinAgg/SBI credit limits
   - 120 Authentic ITC CPG SKUs (Aashirvaad, Sunfeast, Bingo!, Yippee!, Master Chef Frozen,
     Svasti Dairy, Fabelle Chocolates, Fiama, Savlon, Engage, Classmate) with exact physical
     carton LxWxH, gross kg, crush limit kg, shelf-life days, Arrhenius Ea, MRP (INR), HSN/GST
   - 48 Contracted Transporters (L1/L2/L3 Waterfall + Green Logistics EV Fleet + Spot Brokers)
2. `enterprise_data/lake_full/*.csv`:
   - 12 cross-linked enterprise transactional tables (~200+ MB, ~1.62M rows)
3. `enterprise_data/seeds/*.json`:
   - 12 container-portable 80-row deterministic seed tables (preserving every hero anomaly & golden thread)
4. `enterprise_data/multimodal_docs/*.png` + `multimodal_ground_truth_manifest.json`:
   - 24 realistic scanned Lorry Receipts (LRs), Stamped PODs with handwritten shortage/detention remarks,
     Carrier GST Freight Invoices, ICML Weighbridge Tickets, and Drishti Reefer Strip Charts.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
import random
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "enterprise_data"
LAKE_DIR = DATA_DIR / "lake_full"
SEEDS_DIR = DATA_DIR / "seeds"
MM_DIR = DATA_DIR / "multimodal_docs"

RNG = random.Random(20261115)


def build_icml_plants() -> List[Dict[str, Any]]:
    return [
        {
            "icml_id": "ICML-MH-RANJ01",
            "plant_name": "Ranjangaon ICML Mega-Campus",
            "city": "Pune (Ranjangaon MIDC)",
            "state": "Maharashtra",
            "gst_state_code": "27",
            "zone": "West",
            "lat": 18.7954,
            "lon": 74.2891,
            "dock_doors": 28,
            "reefer_plugs": 8,
            "asrs_pallets": 42000,
            "primary_categories": ["Staples & Atta", "Biscuits & Cakes", "Snacks & Chips", "Personal Care"],
            "free_detention_mins": 120,
        },
        {
            "icml_id": "ICML-OR-KHOR02",
            "plant_name": "Khordha ICML Integrated Complex",
            "city": "Bhubaneswar (Khordha)",
            "state": "Odisha",
            "gst_state_code": "21",
            "zone": "East",
            "lat": 20.1864,
            "lon": 85.6223,
            "dock_doors": 20,
            "reefer_plugs": 4,
            "asrs_pallets": 28000,
            "primary_categories": ["Biscuits & Cakes", "Instant Noodles", "Snacks & Chips"],
            "free_detention_mins": 120,
        },
        {
            "icml_id": "ICML-WB-PANC03",
            "plant_name": "Panchla & Uluberia ICML Hub",
            "city": "Howrah (Panchla)",
            "state": "West Bengal",
            "gst_state_code": "19",
            "zone": "East",
            "lat": 22.5411,
            "lon": 88.1419,
            "dock_doors": 26,
            "reefer_plugs": 10,
            "asrs_pallets": 38000,
            "primary_categories": ["Staples & Atta", "Dairy & Chilled", "Luxury Chocolates", "Snacks & Chips"],
            "free_detention_mins": 120,
        },
        {
            "icml_id": "ICML-UK-HARI04",
            "plant_name": "Haridwar SIDCUL ICML Campus",
            "city": "Haridwar",
            "state": "Uttarakhand",
            "gst_state_code": "05",
            "zone": "North",
            "lat": 29.9562,
            "lon": 78.0715,
            "dock_doors": 24,
            "reefer_plugs": 4,
            "asrs_pallets": 34000,
            "primary_categories": ["Personal Care", "Instant Noodles", "Stationery", "Biscuits & Cakes"],
            "free_detention_mins": 120,
        },
        {
            "icml_id": "ICML-PB-KAPU05",
            "plant_name": "Kapurthala Agro & Cold-Chain ICML",
            "city": "Kapurthala",
            "state": "Punjab",
            "gst_state_code": "03",
            "zone": "North",
            "lat": 31.3801,
            "lon": 75.3812,
            "dock_doors": 22,
            "reefer_plugs": 12,
            "asrs_pallets": 36000,
            "primary_categories": ["Staples & Atta", "Frozen Foods", "Dairy & Chilled", "Snacks & Chips"],
            "free_detention_mins": 120,
        },
        {
            "icml_id": "ICML-TN-PUDU06",
            "plant_name": "Pudukkottai Southern ICML",
            "city": "Pudukkottai",
            "state": "Tamil Nadu",
            "gst_state_code": "33",
            "zone": "South",
            "lat": 10.3833,
            "lon": 78.8001,
            "dock_doors": 20,
            "reefer_plugs": 6,
            "asrs_pallets": 30000,
            "primary_categories": ["Snacks & Chips", "Biscuits & Cakes", "Staples & Spices"],
            "free_detention_mins": 120,
        },
        {
            "icml_id": "ICML-KA-MALU07",
            "plant_name": "Malur Bengaluru ICML & Fabelle Craft",
            "city": "Malur (Kolar)",
            "state": "Karnataka",
            "gst_state_code": "29",
            "zone": "South",
            "lat": 13.0037,
            "lon": 77.9383,
            "dock_doors": 26,
            "reefer_plugs": 10,
            "asrs_pallets": 40000,
            "primary_categories": ["Staples & Atta", "Luxury Chocolates", "Instant Noodles", "Biscuits & Cakes"],
            "free_detention_mins": 120,
        },
        {
            "icml_id": "ICML-TG-MEDA08",
            "plant_name": "Medak Telangana ICML Campus",
            "city": "Medak (Sangareddy)",
            "state": "Telangana",
            "gst_state_code": "36",
            "zone": "South-Central",
            "lat": 17.8716,
            "lon": 78.4112,
            "dock_doors": 22,
            "reefer_plugs": 6,
            "asrs_pallets": 32000,
            "primary_categories": ["Biscuits & Cakes", "Snacks & Chips", "Beverages & Juices"],
            "free_detention_mins": 120,
        },
    ]


def build_cfa_depots() -> List[Dict[str, Any]]:
    raw = [
        ("CFA-MH-BHIW", "Bhiwandi Mega Mother CFA", "Mumbai MMR", "Maharashtra", "27", "West", "ICML-MH-RANJ01", 19.2813, 73.0483, 18, 16500),
        ("CFA-MH-NAGP", "Butibori Central Transit CFA", "Nagpur", "Maharashtra", "27", "Central", "ICML-MH-RANJ01", 20.9272, 79.0045, 12, 9400),
        ("CFA-GJ-SANJ", "Sanand Gujarat State CFA", "Ahmedabad", "Gujarat", "24", "West", "ICML-MH-RANJ01", 22.9921, 72.3815, 14, 12800),
        ("CFA-GJ-SURT", "Palsana South Gujarat CFA", "Surat", "Gujarat", "24", "West", "ICML-MH-RANJ01", 21.0850, 72.9790, 10, 8200),
        ("CFA-MP-INDR", "Dewas Naka MP State CFA", "Indore", "Madhya Pradesh", "23", "Central", "ICML-MH-RANJ01", 22.7788, 75.8954, 12, 10100),
        ("CFA-DL-KUND", "Kundli NCR Mega CFA", "Delhi NCR (Sonipat)", "Haryana", "06", "North", "ICML-UK-HARI04", 28.8754, 77.1232, 20, 18200),
        ("CFA-UP-LKO1", "Amausi Central UP CFA", "Lucknow", "Uttar Pradesh", "09", "North", "ICML-UK-HARI04", 26.7654, 80.8832, 14, 13600),
        ("CFA-UP-GZBD", "Dasna Western UP CFA", "Ghaziabad", "Uttar Pradesh", "09", "North", "ICML-UK-HARI04", 28.6812, 77.5234, 12, 11400),
        ("CFA-UP-VNS1", "Ramnagar Eastern UP CFA", "Varanasi", "Uttar Pradesh", "09", "North", "ICML-WB-PANC03", 25.2678, 83.0298, 10, 8900),
        ("CFA-PB-LUDH", "Doraha Punjab State CFA", "Ludhiana", "Punjab", "03", "North", "ICML-PB-KAPU05", 30.8012, 76.0312, 12, 10900),
        ("CFA-RJ-JAIP", "VKIA Rajasthan State CFA", "Jaipur", "Rajasthan", "08", "North", "ICML-PB-KAPU05", 26.9921, 75.7745, 12, 11200),
        ("CFA-WB-DANK", "Dankuni Eastern Mother CFA", "Kolkata", "West Bengal", "19", "East", "ICML-WB-PANC03", 22.6789, 88.2912, 18, 16900),
        ("CFA-WB-SILG", "Siliguri North-East Gateway CFA", "Siliguri", "West Bengal", "19", "East", "ICML-WB-PANC03", 26.7123, 88.4289, 10, 7800),
        ("CFA-BR-PATN", "Fatuha Bihar State CFA", "Patna", "Bihar", "10", "East", "ICML-WB-PANC03", 25.5112, 85.3021, 14, 12600),
        ("CFA-JH-RANC", "Namkum Jharkhand CFA", "Ranchi", "Jharkhand", "20", "East", "ICML-OR-KHOR02", 23.3321, 85.3812, 10, 7400),
        ("CFA-AS-GUWA", "Changasari North-East Hub CFA", "Guwahati", "Assam", "18", "East", "ICML-WB-PANC03", 26.2412, 91.7012, 12, 9100),
        ("CFA-OR-CUTT", "Choudwar Odisha State CFA", "Cuttack", "Odisha", "21", "East", "ICML-OR-KHOR02", 20.5212, 85.9123, 12, 9600),
        ("CFA-KA-NELM", "Nelamangala Bengaluru Mega CFA", "Bengaluru", "Karnataka", "29", "South", "ICML-KA-MALU07", 13.0989, 77.3912, 18, 17400),
        ("CFA-KA-HUBB", "Hubballi North Karnataka CFA", "Hubballi", "Karnataka", "29", "South", "ICML-KA-MALU07", 15.3647, 75.1240, 10, 7900),
        ("CFA-TN-REDH", "Red Hills Chennai Mega CFA", "Chennai", "Tamil Nadu", "33", "South", "ICML-TN-PUDU06", 13.1912, 80.1834, 16, 15200),
        ("CFA-TN-COIM", "Sulur Kongu Nadu CFA", "Coimbatore", "Tamil Nadu", "33", "South", "ICML-TN-PUDU06", 11.0254, 77.1254, 12, 9800),
        ("CFA-TG-SHAM", "Shamshabad Hyderabad Mega CFA", "Hyderabad", "Telangana", "36", "South-Central", "ICML-TG-MEDA08", 17.2403, 78.4294, 16, 14900),
        ("CFA-AP-VIJA", "Gannavaram Coastal AP CFA", "Vijayawada", "Andhra Pradesh", "37", "South-Central", "ICML-TG-MEDA08", 16.5412, 80.8012, 12, 10600),
        ("CFA-KL-ALUV", "Aluva Cochin State CFA", "Kochi", "Kerala", "32", "South", "ICML-TN-PUDU06", 10.1076, 76.3516, 12, 9500),
    ]
    out = []
    for cid, name, city, state, gst, zone, primary_icml, lat, lon, bays, mt in raw:
        out.append({
            "cfa_id": cid,
            "cfa_name": name,
            "city": city,
            "state": state,
            "gst_state_code": gst,
            "zone": zone,
            "primary_icml_id": primary_icml,
            "sap_plant_code": f"I{gst}{cid[-2:]}",
            "lat": lat,
            "lon": lon,
            "loading_bays": bays,
            "monthly_throughput_mt": mt,
            "eod_billing_cutoff_ist": "21:00",
            "cold_room_chilled_pallets": 180 if zone in ("North", "West", "South", "East") else 90,
            "cold_room_frozen_pallets": 140,
        })
    return out


def build_sku_master() -> List[Dict[str, Any]]:
    families = [
        # (brand, family, temp_regime, min_c, max_c, ea_kj, l_cm, w_cm, h_cm, gross_kg, crush_kg, shelf_days, mrp_case_inr, hsn, gst_pct, variants)
        ("Aashirvaad", "Staples & Atta", "Ambient", 15.0, 38.0, 42.0, 52.0, 38.0, 26.0, 30.8, 420.0, 120, 1590.0, "11010000", 5.0, [
            "Shudh Chakki Atta 10kgx3", "Shudh Chakki Atta 5kgx6", "Select Sharbati Atta 5kgx6",
            "Superior MP Atta 10kgx3", "Multigrain Atta 5kgx6", "Multigrain Atta 1kgx20",
            "Organic Whole Wheat Atta 5kgx4", "Sugar Release Control Atta 5kgx4",
            "Iodized Crystal Salt 1kgx25", "Active Salt Proactive 1kgx25",
            "Turmeric Powder 200gx50", "Chilli Powder 200gx50", "Coriander Powder 200gx50",
            "Shahi Garam Masala 100gx60", "Rava Suji 1kgx20", "Besan Gram Flour 1kgx20",
            "Svasti Pure Cow Ghee 1Lx12", "Svasti Pure Cow Ghee 500mlx24"
        ]),
        ("Bingo!", "Snacks & Chips", "Ambient", 15.0, 35.0, 48.0, 60.0, 42.0, 38.0, 4.6, 85.0, 135, 960.0, "19059040", 12.0, [
            "Mad Angles Achaari Masti 72gx48", "Mad Angles Tomato Madness 72gx48", "Mad Angles Peri Peri 72gx48",
            "Tedhe Medhe Masala Tadka 90gx48", "Tedhe Medhe Chatpata Swing 45gx96",
            "Original Style Chili Sprinkled 100gx36", "Original Style Salt Sprinkled 100gx36",
            "Hashtags Cream & Onion 65gx48", "Hashtags Spicy Masala 65gx48",
            "Potato Chips Classic Salted Rs10x120", "No Rulz Masala Curlz 70gx48",
            "Nachos Sweet Chilli 80gx36", "Street Bites Dahi Puri 55gx60", "Millet Angles Masala 65gx48",
            "Mad Angles Cheese Nachos 130gx24", "Tedhe Medhe Navratan Mix 180gx30"
        ]),
        ("Sunfeast", "Biscuits & Cakes", "Ambient", 15.0, 34.0, 52.0, 48.0, 36.0, 30.0, 9.4, 155.0, 180, 1440.0, "19053100", 18.0, [
            "Dark Fantasy Choco Fills 300gx24", "Dark Fantasy Choco Fills 75gx72",
            "Dark Fantasy Bourbon Bliss 150gx48", "Dark Fantasy Vanilla Fills 300gx24",
            "Moms Magic Cashew & Almond 200gx48", "Moms Magic Rich Butter 200gx48",
            "Marie Light Active Oats 250gx36", "Marie Light Orange 200gx48",
            "Bounce Tangy Orange Cream 80gx96", "Bounce Elaichi Cream 80gx96",
            "Farmlite Digestive High Fibre 250gx36", "Farmlite 5-Seed Digestive 200gx36",
            "All Rounder Thin Potato Biscuit 75gx64", "Glucose Plus Energy Biscuit 100gx96",
            "Caker Trinity Choco Layer Cake 120gx36", "Supermilk Fortified Biscuit 150gx48",
            "Nice Sugar Sprinkled Coconut 150gx48", "Dream Cream Strawberry 100gx72"
        ]),
        ("Sunfeast Yippee!", "Instant Noodles & Pasta", "Ambient", 15.0, 36.0, 46.0, 50.0, 38.0, 28.0, 8.8, 140.0, 240, 1380.0, "19023010", 12.0, [
            "Magic Masala Noodles 4-Pack 280gx32", "Magic Masala Family Pack 420gx24",
            "Mood Masala Noodles 70gx96", "Power Up Atta Noodles 280gx32",
            "Tricolor Pasta Masala 65gx72", "Pasta Treat Sour Cream Onion 70gx72",
            "Korean Fiery Ramyun Veg 105gx48", "Quik Mealz Chicken Cup 70gx36",
            "Quik Mealz Veggie Delight Cup 70gx36", "Saucy Masala Noodles 280gx32",
            "Magic Masala Single Rs14x120", "Millets Super Noodles 240gx32"
        ]),
        ("ITC Master Chef", "Frozen Foods", "Frozen (-18C)", -22.0, -16.0, 86.5, 42.0, 32.0, 26.0, 10.5, 210.0, 270, 3240.0, "20041000", 12.0, [
            "Crispy French Fries 1kgx10", "Peri Peri French Fries 420gx20",
            "Aloo Tikki Burger Patty 1.2kgx8", "Veggie Pizza Pocket 340gx24",
            "Mumbai Vada Pops 400gx20", "Cheesy Corn Triangles 320gx24",
            "hara Bhara Kebab Frozen 400gx20", "Paneer Pakoda IQF 400gx20",
            "Classic Chicken Nuggets 500gx18", "Chicken Seekh Kebab IQF 500gx18",
            "IQF Super Safe Prawns Large 500gx16", "Green Peas IQF 1kgx10",
            "Lachha Paratha Frozen 400gx24", "Malabar Paratha Frozen 400gx24"
        ]),
        ("Aashirvaad Svasti", "Dairy & Chilled", "Chilled (2-8C)", 2.0, 8.0, 91.2, 40.0, 30.0, 24.0, 12.4, 195.0, 21, 2180.0, "04061000", 5.0, [
            "Fresh Malai Paneer Block 200gx40", "Fresh Malai Paneer 500gx20",
            "Rich Thick Pouch Curd 400gx30", "Mishti Doi Bengal Classic 400gx24",
            "Mango Lassi Tetra/Cup 200mlx48", "Sweetened Rose Lassi 200mlx48",
            "Select Pasteurized Table Butter 500gx20", "Probiotic Spiced Buttermilk 200mlx48",
            "UHT Slim Toned Milk 1Lx12", "Paneer Cubes Chilled 1kgx10"
        ]),
        ("Fabelle & Candyman", "Luxury Chocolates & Confectionery", "Cool-Chain (16-20C)", 15.0, 20.0, 84.0, 38.0, 28.0, 22.0, 6.8, 130.0, 210, 4860.0, "18069010", 18.0, [
            "Fabelle Choco Deck Milk & Nut 110gx36", "Fabelle Soft Centres Almond 130gx24",
            "Fabelle Tiramisu Luxury Bar 125gx24", "Fabelle Hazelnut Mousse Bar 110gx36",
            "Fabelle Dark Ganache Boutique Box 200gx16", "Fabelle Gianduja Trilogy 150gx20",
            "Candyman Fantastik Choco Roll XL 360gx24", "Candyman Tadka Lollipop Jar 600gx12",
            "Candyman Fruitee Fun Tub 750gx12", "Jelimals Fruit Gummies 100gx60"
        ]),
        ("Fiama, Savlon & Engage", "Personal Care & Hygiene", "Ambient", 12.0, 38.0, 38.0, 44.0, 32.0, 26.0, 14.2, 290.0, 730, 3680.0, "34011190", 18.0, [
            "Fiama Gel Bar Celebration Pack 125gx8x12", "Fiama Blackcurrant Bearberry Shower Gel 250mlx24",
            "Savlon Antiseptic Disinfectant Liquid 500mlx24", "Savlon Moisture Shield Handwash Refill 725mlx20",
            "Savlon Glycerin Germ Protection Soap 125gx4x24", "Savlon Surface Disinfectant Spray 230mlx24",
            "Engage W2 Perfume Spray Women 120mlx36", "Engage M1 Perfume Spray Men 120mlx36",
            "Engage Yang Eau De Parfum 100mlx24", "Vivel Aloe Vera Satin Soap 150gx4x24",
            "Nimyle Herbal Floor Cleaner Citrus 1Lx12", "Charmis Deep Radiance Face Wash 100mlx36"
        ]),
        ("Classmate & Paperkraft", "Stationery", "Ambient", 10.0, 40.0, 30.0, 46.0, 34.0, 28.0, 24.6, 460.0, 1095, 2940.0, "48202000", 12.0, [
            "Classmate Longbook Unruled 172pgx72", "Classmate Six-Subject Spiral 300pgx36",
            "Classmate King Size Ruled 180pgx72", "Classmate Octane Gel Pen Blue Packx120",
            "Classmate Hook Ball Pen Jarx48", "Classmate Archimedes Geometry Boxx48",
            "Paperkraft Signature Executive Green 160pgx36", "Paperkraft Chopin Matte Penx60",
            "Classmate Scrapbook & Drawing Combox60", "Classmate Pulse College Spiral 240pgx48"
        ]),
    ]
    skus: List[Dict[str, Any]] = []
    idx = 1
    for brand, cat, regime, min_c, max_c, ea_kj, l_cm, w_cm, h_cm, g_kg, crush_kg, shelf, mrp, hsn, gst, variants in families:
        for v in variants:
            if idx > 120:
                break
            vol_m3 = round((l_cm * w_cm * h_cm) / 1_000_000.0, 5)
            density = round(g_kg / max(vol_m3, 0.001), 1)
            skus.append({
                "sku_id": f"ITC-SKU-{idx:03d}",
                "brand": brand,
                "sku_name": f"{brand} {v}",
                "category": cat,
                "temp_regime": regime,
                "min_temp_c": min_c,
                "max_temp_c": max_c,
                "arrhenius_ea_kj_mol": ea_kj,
                "carton_l_cm": l_cm,
                "carton_w_cm": w_cm,
                "carton_h_cm": h_cm,
                "carton_vol_m3": vol_m3,
                "gross_weight_kg": round(g_kg * (0.94 + (idx % 7) * 0.02), 2),
                "bulk_density_kg_m3": density,
                "max_top_load_crush_kg": crush_kg,
                "total_shelf_life_days": shelf,
                "mrsl_mt_qcomm_pct": 75.0,
                "mrsl_gt_wd_pct": 55.0,
                "mrp_per_case_inr": round(mrp * (0.9 + (idx % 9) * 0.03), 2),
                "gross_margin_pct": round(24.0 + (idx % 15) * 1.4, 1),
                "hsn_code": hsn,
                "gst_rate_pct": gst,
            })
            idx += 1
    return skus


def build_wholesale_dealers(cfas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    prefixes = [
        "Shree Balaji", "Mahavir", "Annapurna", "Siddhivinayak", "Kaveri", "Ganga", "Narmada",
        "Rajputana", "Utkal", "Hooghly", "Deccan", "Sahyadri", "Doaba", "Awadh", "Coromandel",
    ]
    suffixes = ["Agencies", "Enterprises", "Distributors", "Marketing", "Traders", "Associates"]
    fin_partners = ["FinAgg Supply Chain Credit", "SBI e-DFS Dealer Finance", "Axis Bank Channel Credit", "ICICI Corp Channel Line"]
    wds: List[Dict[str, Any]] = []
    for i in range(1, 361):
        cfa = cfas[(i - 1) % len(cfas)]
        tier = "Platinum WD" if i % 6 == 0 else ("Gold WD" if i % 3 == 0 else "Silver WD")
        cred_limit_lakh = 85.0 if tier == "Platinum WD" else (48.0 if tier == "Gold WD" else 24.0)
        wds.append({
            "wd_code": f"WD-{cfa['state'][:2].upper()}-{i:04d}",
            "wd_name": f"{prefixes[i % len(prefixes)]} {suffixes[(i // 3) % len(suffixes)]} ({cfa['city']})",
            "parent_cfa_id": cfa["cfa_id"],
            "zone": cfa["zone"],
            "city": cfa["city"],
            "state": cfa["state"],
            "wd_tier": tier,
            "unnati_outlets_mapped": 280 + (i % 12) * 45,
            "vajra_sfa_beats": 12 + (i % 8),
            "target_doi_days": 12 if tier == "Platinum WD" else 14,
            "godown_capacity_cases": 6500 if tier == "Platinum WD" else (4200 if tier == "Gold WD" else 2500),
            "finagg_credit_limit_lakh_inr": cred_limit_lakh,
            "financing_partner": fin_partners[i % len(fin_partners)],
            "distance_from_cfa_km": 18 + (i * 7) % 165,
        })
    return wds


def build_carriers() -> List[Dict[str, Any]]:
    names = [
        ("TCI Freight Primary Logistics", "L1", "32ft MXL Container", 18000, 63.5, 4.10, 850),
        ("VRL Logistics Surface Linehaul", "L1", "32ft MXL Container", 18000, 63.5, 4.18, 850),
        ("Mahindra Logistics Contract Fleet", "L1", "32ft MXL Container", 18000, 63.5, 4.15, 800),
        ("CJ Darcl Primary FTL", "L2", "32ft MXL Container", 18000, 63.5, 4.42, 900),
        ("RIVIGO / Gati Express Linehaul", "L2", "32ft SXL Container", 15000, 56.0, 4.55, 950),
        ("Coldman / Snowman Reefer Express", "L1", "32ft Dual-Zone Reefer", 15000, 54.0, 6.85, 1350),
        ("Crystal Cold-Chain Logistics", "L2", "20ft Chilled Reefer", 9000, 31.0, 7.25, 1250),
        (" Delhivery Mid-Mile FTL", "L2", "20ft SXL Container", 9000, 33.0, 4.70, 750),
        ("Varuna Integrated Logistics", "L1", "32ft MXL Container", 18000, 63.5, 4.12, 850),
        (" Ritco Supply Chain Solutions", "L3", "32ft MXL Container", 18000, 63.5, 4.88, 950),
        ("ITC Green Fleet - Magenta EV Mobility", "L1", "Tata Ace EV 4W", 1000, 5.2, 8.90, 400),
        ("ITC Green Fleet - Zypp / MoEVing Urban", "L1", "Euler HiLoad EV 3W", 680, 4.1, 9.20, 350),
        ("SafeExpress MT/Q-Comm Dedicated", "L1", "14ft Closed LCV", 4000, 16.5, 6.10, 650),
        ("BLR Logistiks Western Corridor", "L2", "32ft MXL Container", 18000, 63.5, 4.48, 850),
        ("Spot Market Broker - Highway King Trans", "SPOT", "32ft MXL Container", 18000, 63.5, 5.95, 1400),
        ("Spot Market Broker - Jai Hind Roadlines", "SPOT", "20ft SXL Container", 9000, 33.0, 6.35, 1300),
    ]
    carriers: List[Dict[str, Any]] = []
    for i in range(48):
        base = names[i % len(names)]
        tier = base[1]
        carriers.append({
            "carrier_id": f"CAR-ITC-{i+1:03d}",
            "carrier_name": f"{base[0].strip()} #{(i // len(names)) + 1}",
            "waterfall_tier": tier,
            "vehicle_type": base[2],
            "max_payload_kg": base[3],
            "usable_volume_m3": base[4],
            "contract_rate_per_mt_km_inr": round(base[5] * (1.0 + (i % 5) * 0.015), 2),
            "detention_rate_per_hr_inr": base[6],
            "is_ev_green_fleet": "EV" in base[2],
            "gst_rcm_applicable": tier == "SPOT",
            "historical_tender_accept_pct": round(94.5 - (0 if tier == "L1" else (6.5 if tier == "L2" else (14.0 if tier == "L3" else 28.0))) - (i % 4) * 1.1, 1),
        })
    return carriers


def write_csv_and_seed(
    filename_stem: str,
    hero_rows: List[Dict[str, Any]],
    total_rows: int,
    row_builder_fn,
) -> Dict[str, Any]:
    csv_path = LAKE_DIR / f"{filename_stem}.csv"
    seed_path = SEEDS_DIR / f"{filename_stem}.json"

    seed_rows = list(hero_rows)
    while len(seed_rows) < min(85, total_rows):
        seed_rows.append(row_builder_fn(len(seed_rows)))

    seed_path.write_text(json.dumps(seed_rows, indent=2), encoding="utf-8")

    fieldnames = list(seed_rows[0].keys())
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for r in seed_rows:
            writer.writerow(r)
        for idx in range(len(seed_rows), total_rows):
            writer.writerow(row_builder_fn(idx))

    sz_mb = round(csv_path.stat().st_size / (1024 * 1024), 2)
    return {
        "table": filename_stem,
        "rows": total_rows,
        "seed_rows": len(seed_rows),
        "size_mb": sz_mb,
        "columns": fieldnames,
    }


def generate_all_12_tables(
    icmls: List[Dict[str, Any]],
    cfas: List[Dict[str, Any]],
    skus: List[Dict[str, Any]],
    wds: List[Dict[str, Any]],
    carriers: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    stats: List[Dict[str, Any]] = []
    atta_skus = [s for s in skus if s["category"] == "Staples & Atta"]
    snack_skus = [s for s in skus if s["category"] in ("Snacks & Chips", "Biscuits & Cakes")]
    cold_skus = [s for s in skus if "C)" in s["temp_regime"]]
    l1_mxl = [c for c in carriers if c["waterfall_tier"] == "L1" and "32ft MXL" in c["vehicle_type"]]
    spot_carriers = [c for c in carriers if c["waterfall_tier"] == "SPOT"]
    ev_carriers = [c for c in carriers if c["is_ev_green_fleet"]]

    # -------------------------------------------------------------------------
    # TABLE 01: Primary Logistics — Load Consolidation (ICML -> State CFA)
    # -------------------------------------------------------------------------
    hero_01 = [
        {
            "dispatch_wave_id": "WAVE-ICML-RANJ-20261115-A",
            "shipment_id": "SHP-PRI-90001",
            "icml_id": "ICML-MH-RANJ01",
            "dest_cfa_id": "CFA-GJ-SANJ",
            "lane_name": "Ranjangaon ICML -> Sanand Ahmedabad CFA (665 km)",
            "distance_km": 665,
            "stop_sequence": 1,
            "sku_id": atta_skus[0]["sku_id"],
            "sku_name": atta_skus[0]["sku_name"],
            "category": "Staples & Atta",
            "staged_cases": 560,
            "gross_weight_kg": 17248.0,
            "volume_m3": 28.75,
            "max_top_load_crush_kg": 420.0,
            "baseline_truck_plan": "TRK-UNOPT-01 (Atta-Only Weight-Out: 95.8% wt, 45.3% cube)",
            "baseline_trucks_used": 1,
            "baseline_freight_inr": 62500.0,
            "carrier_id": l1_mxl[0]["carrier_id"],
            "vehicle_type": "32ft MXL Container (18 MT / 63.5 m3)",
            "cmvr_rule93_front_axle_limit_kg": 7500,
            "cmvr_rule93_rear_axle_limit_kg": 11500,
            "consolidation_status": "CANDIDATE_HEAVY_BASE_CO_LOAD",
        },
        {
            "dispatch_wave_id": "WAVE-ICML-RANJ-20261115-A",
            "shipment_id": "SHP-PRI-90002",
            "icml_id": "ICML-MH-RANJ01",
            "dest_cfa_id": "CFA-GJ-SANJ",
            "lane_name": "Ranjangaon ICML -> Sanand Ahmedabad CFA (665 km)",
            "distance_km": 665,
            "stop_sequence": 1,
            "sku_id": snack_skus[0]["sku_id"],
            "sku_name": snack_skus[0]["sku_name"],
            "category": "Snacks & Chips",
            "staged_cases": 610,
            "gross_weight_kg": 2806.0,
            "volume_m3": 58.38,
            "max_top_load_crush_kg": 85.0,
            "baseline_truck_plan": "TRK-UNOPT-02 (Snacks-Only Cube-Out: 15.6% wt, 91.9% cube)",
            "baseline_trucks_used": 1,
            "baseline_freight_inr": 62500.0,
            "carrier_id": l1_mxl[0]["carrier_id"],
            "vehicle_type": "32ft MXL Container (18 MT / 63.5 m3)",
            "cmvr_rule93_front_axle_limit_kg": 7500,
            "cmvr_rule93_rear_axle_limit_kg": 11500,
            "consolidation_status": "CANDIDATE_LIGHT_TOP_CO_LOAD",
        },
        {
            "dispatch_wave_id": "WAVE-ICML-RANJ-20261115-A",
            "shipment_id": "SHP-PRI-90003",
            "icml_id": "ICML-MH-RANJ01",
            "dest_cfa_id": "CFA-GJ-SURT",
            "lane_name": "Ranjangaon ICML -> Surat Palsana CFA -> Sanand Multi-Stop (680 km)",
            "distance_km": 420,
            "stop_sequence": 1,
            "sku_id": atta_skus[2]["sku_id"],
            "sku_name": atta_skus[2]["sku_name"],
            "category": "Staples & Atta",
            "staged_cases": 340,
            "gross_weight_kg": 10472.0,
            "volume_m3": 17.46,
            "max_top_load_crush_kg": 420.0,
            "baseline_truck_plan": "TRK-UNOPT-03 (Partial LTL Dispatch: 58.2% wt, 27.5% cube)",
            "baseline_trucks_used": 1,
            "baseline_freight_inr": 48200.0,
            "carrier_id": l1_mxl[1]["carrier_id"],
            "vehicle_type": "32ft MXL Container (18 MT / 63.5 m3)",
            "cmvr_rule93_front_axle_limit_kg": 7500,
            "cmvr_rule93_rear_axle_limit_kg": 11500,
            "consolidation_status": "CANDIDATE_MULTI_STOP_LIFO_MERGE",
        },
        {
            "dispatch_wave_id": "WAVE-ICML-KHOR-20261115-B",
            "shipment_id": "SHP-PRI-90004",
            "icml_id": "ICML-OR-KHOR02",
            "dest_cfa_id": "CFA-WB-DANK",
            "lane_name": "Khordha ICML -> Dankuni Kolkata Mother CFA (455 km)",
            "distance_km": 455,
            "stop_sequence": 1,
            "sku_id": snack_skus[4]["sku_id"],
            "sku_name": snack_skus[4]["sku_name"],
            "category": "Biscuits & Cakes",
            "staged_cases": 490,
            "gross_weight_kg": 4606.0,
            "volume_m3": 25.40,
            "max_top_load_crush_kg": 155.0,
            "baseline_truck_plan": "TRK-UNOPT-04 (Half-Empty Urgent Biscuit FTL: 25.6% wt, 40.0% cube)",
            "baseline_trucks_used": 1,
            "baseline_freight_inr": 44800.0,
            "carrier_id": l1_mxl[2]["carrier_id"],
            "vehicle_type": "32ft MXL Container (18 MT / 63.5 m3)",
            "cmvr_rule93_front_axle_limit_kg": 7500,
            "cmvr_rule93_rear_axle_limit_kg": 11500,
            "consolidation_status": "CANDIDATE_LIGHT_TOP_CO_LOAD",
        },
    ]

    def row_01(i: int) -> Dict[str, Any]:
        icml = icmls[i % len(icmls)]
        cfa = cfas[(i * 3) % len(cfas)]
        sku = atta_skus[i % len(atta_skus)] if i % 2 == 0 else snack_skus[i % len(snack_skus)]
        cases = 180 + (i * 17) % 420
        wt = round(cases * sku["gross_weight_kg"], 1)
        vol = round(cases * sku["carton_vol_m3"], 2)
        dist = 240 + (i * 29) % 980
        return {
            "dispatch_wave_id": f"WAVE-{icml['icml_id'][-6:]}-202611{(i % 15)+1:02d}-{(i % 3)+1}",
            "shipment_id": f"SHP-PRI-{100000 + i}",
            "icml_id": icml["icml_id"],
            "dest_cfa_id": cfa["cfa_id"],
            "lane_name": f"{icml['city']} -> {cfa['city']} ({dist} km)",
            "distance_km": dist,
            "stop_sequence": 1 if i % 4 != 0 else 2,
            "sku_id": sku["sku_id"],
            "sku_name": sku["sku_name"],
            "category": sku["category"],
            "staged_cases": cases,
            "gross_weight_kg": min(wt, 17850.0),
            "volume_m3": min(vol, 61.5),
            "max_top_load_crush_kg": sku["max_top_load_crush_kg"],
            "baseline_truck_plan": "SINGLE_COMMODITY_FTL" if i % 3 != 0 else "OPTIMIZED_COMPOSITE_FTL",
            "baseline_trucks_used": 1,
            "baseline_freight_inr": round(24000 + dist * 58.5, 2),
            "carrier_id": l1_mxl[i % len(l1_mxl)]["carrier_id"],
            "vehicle_type": "32ft MXL Container (18 MT / 63.5 m3)",
            "cmvr_rule93_front_axle_limit_kg": 7500,
            "cmvr_rule93_rear_axle_limit_kg": 11500,
            "consolidation_status": "CANDIDATE_HEAVY_BASE_CO_LOAD" if sku["category"] == "Staples & Atta" else "CANDIDATE_LIGHT_TOP_CO_LOAD",
        }

    stats.append(write_csv_and_seed("01_icml_primary_dispatch_waves_and_cartons", hero_01, 145000, row_01))

    # -------------------------------------------------------------------------
    # TABLE 02: Plant Yard & Dispatch — Yard Disruption & Detention Sentinel
    # -------------------------------------------------------------------------
    hero_02 = [
        {
            "yard_event_id": "YRD-RANJ-8001",
            "icml_id": "ICML-MH-RANJ01",
            "shipment_id": "SHP-PRI-90001",
            "vehicle_reg_no": "MH12-QW-4821",
            "carrier_id": "CAR-ITC-001",
            "carrier_name": "TCI Freight Primary Logistics #1",
            "load_category": "Staples & Snacks Composite FTL",
            "is_reefer_load": False,
            "assigned_dock_door": "DOCK-R04 (Blocked - Stretch-Wrap Jam)",
            "alternate_fast_dock": "DOCK-R11 (Available - AS/RS Spur B)",
            "gate_checkin_ist": "2026-11-15T06:05:00+05:30",
            "current_yard_dwell_mins": 178,
            "free_time_allowance_mins": 120,
            "billable_detention_mins": 58,
            "detention_rate_per_hr_inr": 850.0,
            "projected_detention_penalty_inr": 2550.0,
            "fastag_geofence_status": "WAITING_IN_YARD_APRON",
            "weighbridge_tare_kg": 9820.0,
            "disruption_alert": "DOCK_CONGESTION_DETENTION_BREACH",
        },
        {
            "yard_event_id": "YRD-KAPU-8002",
            "icml_id": "ICML-PB-KAPU05",
            "shipment_id": "SHP-CLD-70001",
            "vehicle_reg_no": "PB08-CX-9104",
            "carrier_id": "CAR-ITC-006",
            "carrier_name": "Coldman / Snowman Reefer Express #1",
            "load_category": "ITC Master Chef Frozen (-18C)",
            "is_reefer_load": True,
            "assigned_dock_door": "DOCK-C02 (Occupied - Late Inbound)",
            "alternate_fast_dock": "DOCK-C05 (Reefer Seal + Shore Power Open)",
            "gate_checkin_ist": "2026-11-15T06:40:00+05:30",
            "current_yard_dwell_mins": 142,
            "free_time_allowance_mins": 90,
            "billable_detention_mins": 52,
            "detention_rate_per_hr_inr": 1350.0,
            "projected_detention_penalty_inr": 4050.0,
            "fastag_geofence_status": "REEFER_RUNNING_ON_DIESEL_AT_GATE",
            "weighbridge_tare_kg": 11240.0,
            "disruption_alert": "CRITICAL_REEFER_SHORE_POWER_AND_DETENTION_RISK",
        },
        {
            "yard_event_id": "YRD-PANC-8003",
            "icml_id": "ICML-WB-PANC03",
            "shipment_id": "SHP-PRI-90019",
            "vehicle_reg_no": "WB11-ek-3390",
            "carrier_id": "CAR-ITC-002",
            "carrier_name": "VRL Logistics Surface Linehaul #1",
            "load_category": "Aashirvaad Atta + Svasti Ghee",
            "is_reefer_load": False,
            "assigned_dock_door": "DOCK-P08 (Crew Shift Handover Delay)",
            "alternate_fast_dock": "DOCK-P14 (Available)",
            "gate_checkin_ist": "2026-11-15T07:10:00+05:30",
            "current_yard_dwell_mins": 114,
            "free_time_allowance_mins": 120,
            "billable_detention_mins": 0,
            "detention_rate_per_hr_inr": 850.0,
            "projected_detention_penalty_inr": 1700.0,
            "fastag_geofence_status": "APPROACHING_FREE_TIME_SLAB_IN_6_MINS",
            "weighbridge_tare_kg": 9640.0,
            "disruption_alert": "PREEMPTIVE_SLAB_BREACH_WARNING",
        },
    ]

    def row_02(i: int) -> Dict[str, Any]:
        icml = icmls[i % len(icmls)]
        car = carriers[i % len(carriers)]
        dwell = 45 + (i * 19) % 195
        free_m = 90 if "Reefer" in car["vehicle_type"] else 120
        bill_m = max(0, dwell - free_m)
        hrs_exposed = math.ceil((bill_m + 45) / 60.0) if dwell > (free_m - 15) else 0
        return {
            "yard_event_id": f"YRD-{icml['icml_id'][-6:]}-{10000 + i}",
            "icml_id": icml["icml_id"],
            "shipment_id": f"SHP-PRI-{100000 + i}",
            "vehicle_reg_no": f"{icml['state'][:2].upper()}{(i % 39)+10:02d}-TR-{(1000 + i) % 9999:04d}",
            "carrier_id": car["carrier_id"],
            "carrier_name": car["carrier_name"],
            "load_category": "Frozen & Chilled" if "Reefer" in car["vehicle_type"] else "Dry Foods & Personal Care",
            "is_reefer_load": "Reefer" in car["vehicle_type"],
            "assigned_dock_door": f"DOCK-{(i % icml['dock_doors'])+1:02d}",
            "alternate_fast_dock": f"DOCK-{((i + 5) % icml['dock_doors'])+1:02d}",
            "gate_checkin_ist": f"2026-11-{(i % 15)+1:02d}T{(i % 23):02d}:{(i * 7) % 60:02d}:00+05:30",
            "current_yard_dwell_mins": dwell,
            "free_time_allowance_mins": free_m,
            "billable_detention_mins": bill_m,
            "detention_rate_per_hr_inr": float(car["detention_rate_per_hr_inr"]),
            "projected_detention_penalty_inr": round(hrs_exposed * car["detention_rate_per_hr_inr"], 2),
            "fastag_geofence_status": "WAITING_IN_YARD_APRON" if bill_m > 0 else "DOCKED_ON_SCHEDULE",
            "weighbridge_tare_kg": round(9200.0 + (i % 14) * 180.0, 1),
            "disruption_alert": "DOCK_CONGESTION_DETENTION_BREACH" if bill_m > 0 else "NOMINAL_FLOW",
        }

    stats.append(write_csv_and_seed("02_icml_yard_gate_fastag_dock_detention", hero_02, 125000, row_02))

    # -------------------------------------------------------------------------
    # TABLE 03: Cold-Chain QA — Drishti Reefer IoT Telemetry & Arrhenius MKT
    # -------------------------------------------------------------------------
    hero_03 = [
        {
            "telemetry_event_id": "DRISHTI-70001-01",
            "shipment_id": "SHP-CLD-70001",
            "lr_number": "LR-SNOW-2026-88412",
            "icml_id": "ICML-PB-KAPU05",
            "dest_cfa_id": "CFA-DL-KUND",
            "carrier_id": "CAR-ITC-006",
            "carrier_name": "Coldman / Snowman Reefer Express #1",
            "sku_id": cold_skus[0]["sku_id"],
            "sku_name": cold_skus[0]["sku_name"],
            "temp_regime": "Frozen (-18C)",
            "setpoint_c": -18.0,
            "max_allowed_c": -15.0,
            "arrhenius_ea_kj_mol": 86.5,
            "temp_trace_15min_c": "-18.4|-18.1|-17.8|-14.2|-11.6|-9.8|-8.9|-9.4|-11.2|-15.6|-17.9|-18.2",
            "excursion_duration_mins": 105,
            "peak_temp_c": -8.9,
            "ambient_highway_c": 36.5,
            "door_open_events": 2,
            "compressor_fault_code": "COMP_EVAP_FAN_SLIP_NH44_KARNAL",
            "cargo_invoice_value_inr": 1485000.0,
            "scanned_strip_chart_doc": "DOC-STRIP-SHP-CLD-70001.png",
        },
        {
            "telemetry_event_id": "DRISHTI-70002-01",
            "shipment_id": "SHP-CLD-70002",
            "lr_number": "LR-CRYS-2026-44109",
            "icml_id": "ICML-WB-PANC03",
            "dest_cfa_id": "CFA-BR-PATN",
            "carrier_id": "CAR-ITC-007",
            "carrier_name": "Crystal Cold-Chain Logistics #1",
            "sku_id": [s for s in cold_skus if "Paneer" in s["sku_name"]][0]["sku_id"],
            "sku_name": [s for s in cold_skus if "Paneer" in s["sku_name"]][0]["sku_name"],
            "temp_regime": "Chilled (2-8C)",
            "setpoint_c": 4.0,
            "max_allowed_c": 8.0,
            "arrhenius_ea_kj_mol": 91.2,
            "temp_trace_15min_c": "4.2|4.5|5.1|9.4|12.8|14.1|14.6|13.9|11.8|8.4|5.9|4.6",
            "excursion_duration_mins": 120,
            "peak_temp_c": 14.6,
            "ambient_highway_c": 34.8,
            "door_open_events": 4,
            "compressor_fault_code": "DRIVER_SWITCHED_OFF_REEFER_AT_DHABA_HALT",
            "cargo_invoice_value_inr": 864000.0,
            "scanned_strip_chart_doc": "DOC-STRIP-SHP-CLD-70002.png",
        },
        {
            "telemetry_event_id": "DRISHTI-70003-01",
            "shipment_id": "SHP-CLD-70003",
            "lr_number": "LR-SNOW-2026-88499",
            "icml_id": "ICML-KA-MALU07",
            "dest_cfa_id": "CFA-MH-BHIW",
            "carrier_id": "CAR-ITC-006",
            "carrier_name": "Coldman / Snowman Reefer Express #1",
            "sku_id": [s for s in cold_skus if "Fabelle" in s["sku_name"]][0]["sku_id"],
            "sku_name": [s for s in cold_skus if "Fabelle" in s["sku_name"]][0]["sku_name"],
            "temp_regime": "Cool-Chain (16-20C)",
            "setpoint_c": 18.0,
            "max_allowed_c": 21.0,
            "arrhenius_ea_kj_mol": 84.0,
            "temp_trace_15min_c": "17.8|18.1|18.4|21.6|23.4|24.1|22.5|19.8|18.5|18.1|17.9|18.0",
            "excursion_duration_mins": 60,
            "peak_temp_c": 24.1,
            "ambient_highway_c": 37.2,
            "door_open_events": 1,
            "compressor_fault_code": "DEFROST_CYCLE_FAT_BLOOM_WATCH",
            "cargo_invoice_value_inr": 1920000.0,
            "scanned_strip_chart_doc": "DOC-STRIP-SHP-CLD-70003.png",
        },
    ]

    def row_03(i: int) -> Dict[str, Any]:
        sku = cold_skus[i % len(cold_skus)]
        icml = icmls[i % len(icmls)]
        cfa = cfas[(i * 5) % len(cfas)]
        setp = -18.0 if "Frozen" in sku["temp_regime"] else (4.0 if "Chilled" in sku["temp_regime"] else 18.0)
        max_c = -15.0 if "Frozen" in sku["temp_regime"] else (8.0 if "Chilled" in sku["temp_regime"] else 21.0)
        spike = (i % 9 == 0)
        pts = [round(setp + (6.8 if (spike and 3 <= k <= 7) else ((k % 3) * 0.4 - 0.3)), 1) for k in range(12)]
        return {
            "telemetry_event_id": f"DRISHTI-{80000 + i}",
            "shipment_id": f"SHP-CLD-{80000 + i}",
            "lr_number": f"LR-CLD-2026-{30000 + i}",
            "icml_id": icml["icml_id"],
            "dest_cfa_id": cfa["cfa_id"],
            "carrier_id": "CAR-ITC-006" if i % 2 == 0 else "CAR-ITC-007",
            "carrier_name": "Coldman / Snowman Reefer Express #1" if i % 2 == 0 else "Crystal Cold-Chain Logistics #1",
            "sku_id": sku["sku_id"],
            "sku_name": sku["sku_name"],
            "temp_regime": sku["temp_regime"],
            "setpoint_c": setp,
            "max_allowed_c": max_c,
            "arrhenius_ea_kj_mol": sku["arrhenius_ea_kj_mol"],
            "temp_trace_15min_c": "|".join(str(x) for x in pts),
            "excursion_duration_mins": 75 if spike else 0,
            "peak_temp_c": max(pts),
            "ambient_highway_c": round(31.0 + (i % 10) * 0.9, 1),
            "door_open_events": 3 if spike else (i % 2),
            "compressor_fault_code": "PROLONGED_UNSEALED_DOCK_TRANSFER" if spike else "NONE",
            "cargo_invoice_value_inr": round(420000.0 + (i % 20) * 65000.0, 2),
            "scanned_strip_chart_doc": "DOC-STRIP-SHP-CLD-70001.png",
        }

    stats.append(write_csv_and_seed("03_drishti_reefer_iot_thermal_telemetry", hero_03, 155000, row_03))

    # -------------------------------------------------------------------------
    # TABLE 04: CFA Operations — CFA Wave & Bay Orchestrator (FEFO + Bay Balancing)
    # -------------------------------------------------------------------------
    hero_04 = [
        {
            "cfa_wave_id": "CFAW-BHIW-AM01",
            "cfa_id": "CFA-MH-BHIW",
            "cfa_name": "Bhiwandi Mega Mother CFA",
            "channel": "Quick-Commerce (Blinkit/Zepto)",
            "assigned_bay": "BAY-B02 (Overloaded - 194% Capacity)",
            "recommended_bay": "BAY-B09 (38% Utilized - Fast-Track Conveyor)",
            "sku_id": snack_skus[0]["sku_id"],
            "sku_name": snack_skus[0]["sku_name"],
            "sap_batch_currently_picked": "B2607A (49% Shelf-Life Left - MRSL REJECTION RISK!)",
            "fefo_compliant_swap_batch": "B2610C (84% Shelf-Life Left - Q-Comm 75% MRSL Safe)",
            "remaining_shelf_life_pct": 49.0,
            "required_channel_mrsl_pct": 75.0,
            "order_cases": 420,
            "pick_lines": 68,
            "assigned_pickers": 3,
            "optimal_pickers": 6,
            "dispatch_cutoff_ist": "10:30",
            "estimated_finish_ist": "11:48",
            "order_value_inr": 403200.0,
            "wave_risk_flag": "DUAL_BAY_BOTTLENECK_AND_MRSL_BATCH_MISMATCH",
        },
        {
            "cfa_wave_id": "CFAW-BHIW-AM02",
            "cfa_id": "CFA-MH-BHIW",
            "cfa_name": "Bhiwandi Mega Mother CFA",
            "channel": "General Trade Wholesale Dealer (WD)",
            "assigned_bay": "BAY-B09 (Under-utilized)",
            "recommended_bay": "BAY-B02 (Swap Older Batch B2607A Here - 55% GT MRSL Eligible)",
            "sku_id": snack_skus[0]["sku_id"],
            "sku_name": snack_skus[0]["sku_name"],
            "sap_batch_currently_picked": "B2610C (84% Shelf-Life Left - Wasted Freshness on Fast GT)",
            "fefo_compliant_swap_batch": "B2607A (58% Effective GT Window via Immediate WD Beat)",
            "remaining_shelf_life_pct": 84.0,
            "required_channel_mrsl_pct": 55.0,
            "order_cases": 510,
            "pick_lines": 42,
            "assigned_pickers": 7,
            "optimal_pickers": 4,
            "dispatch_cutoff_ist": "13:30",
            "estimated_finish_ist": "11:10",
            "order_value_inr": 489600.0,
            "wave_risk_flag": "FRESH_STOCK_CANNIBALIZING_MT_QCOMM_POOL",
        },
        {
            "cfa_wave_id": "CFAW-KUND-AM03",
            "cfa_id": "CFA-DL-KUND",
            "cfa_name": "Kundli NCR Mega CFA",
            "channel": "Modern Trade (DMart / Reliance Smart)",
            "assigned_bay": "BAY-K04 (Congested - 168% Load)",
            "recommended_bay": "BAY-K12 (Open Dock Leveler)",
            "sku_id": atta_skus[0]["sku_id"],
            "sku_name": atta_skus[0]["sku_name"],
            "sap_batch_currently_picked": "A2610N (82% Shelf-Life Left)",
            "fefo_compliant_swap_batch": "A2610N (Retain Compliant Batch)",
            "remaining_shelf_life_pct": 82.0,
            "required_channel_mrsl_pct": 75.0,
            "order_cases": 780,
            "pick_lines": 54,
            "assigned_pickers": 3,
            "optimal_pickers": 6,
            "dispatch_cutoff_ist": "11:00",
            "estimated_finish_ist": "12:15",
            "order_value_inr": 1240200.0,
            "wave_risk_flag": "LABOR_UNDERSTAFFED_MT_SLOT_MISS_IMMINENT",
        },
    ]

    def row_04(i: int) -> Dict[str, Any]:
        cfa = cfas[i % len(cfas)]
        sku = skus[i % len(skus)]
        ch = ["General Trade Wholesale Dealer (WD)", "Modern Trade (DMart / Reliance)", "Quick-Commerce (Blinkit/Zepto)", "UNNATI eB2B Direct"][i % 4]
        req_mrsl = 75.0 if ("Modern" in ch or "Quick" in ch) else 55.0
        rem_sl = round(48.0 + (i % 45), 1)
        cases = 120 + (i * 13) % 580
        return {
            "cfa_wave_id": f"CFAW-{cfa['cfa_id'][-4:]}-{10000 + i}",
            "cfa_id": cfa["cfa_id"],
            "cfa_name": cfa["cfa_name"],
            "channel": ch,
            "assigned_bay": f"BAY-{(i % cfa['loading_bays'])+1:02d}",
            "recommended_bay": f"BAY-{((i + 3) % cfa['loading_bays'])+1:02d}",
            "sku_id": sku["sku_id"],
            "sku_name": sku["sku_name"],
            "sap_batch_currently_picked": f"B26{(i % 9)+1:02d}X",
            "fefo_compliant_swap_batch": f"B2610Z",
            "remaining_shelf_life_pct": rem_sl,
            "required_channel_mrsl_pct": req_mrsl,
            "order_cases": cases,
            "pick_lines": 18 + (i % 55),
            "assigned_pickers": 2 + (i % 6),
            "optimal_pickers": 4 + (i % 4),
            "dispatch_cutoff_ist": "11:00" if req_mrsl == 75.0 else "15:00",
            "estimated_finish_ist": "11:35" if rem_sl < req_mrsl else "10:25",
            "order_value_inr": round(cases * sku["mrp_per_case_inr"] * 0.82, 2),
            "wave_risk_flag": "MRSL_REJECTION_RISK" if rem_sl < req_mrsl else "OPTIMAL_WAVE",
        }

    stats.append(write_csv_and_seed("04_cfa_wms_pick_waves_fefo_and_bays", hero_04, 135000, row_04))

    # -------------------------------------------------------------------------
    # TABLE 05: CS&L — Fair-Share Stock Allocation Agent (Shortage Rationing)
    # -------------------------------------------------------------------------
    df_sku = [s for s in skus if "Dark Fantasy Choco Fills 300g" in s["sku_name"]][0]
    hero_05 = [
        {
            "allocation_pool_id": "SHORT-NELM-DF300",
            "cfa_id": "CFA-KA-NELM",
            "cfa_name": "Nelamangala Bengaluru Mega CFA",
            "sku_id": df_sku["sku_id"],
            "sku_name": df_sku["sku_name"],
            "available_cfa_pool_cases": 2400,
            "total_competing_demand_cases": 3650,
            "customer_segment_id": "QCOMM-BLINKIT-BLR",
            "channel_name": "Quick-Commerce (Blinkit / Zepto Mother Hub)",
            "requested_cases": 950,
            "fifo_naive_alloc_cases": 950,
            "min_strategic_floor_pct": 85.0,
            "otif_penalty_pct_on_shortfall": 8.0,
            "net_margin_per_case_inr": 395.0,
            "case_net_realization_inr": 1180.0,
            "priority_weight": 1.35,
        },
        {
            "allocation_pool_id": "SHORT-NELM-DF300",
            "cfa_id": "CFA-KA-NELM",
            "cfa_name": "Nelamangala Bengaluru Mega CFA",
            "sku_id": df_sku["sku_id"],
            "sku_name": df_sku["sku_name"],
            "available_cfa_pool_cases": 2400,
            "total_competing_demand_cases": 3650,
            "customer_segment_id": "MT-DMART-SOUTH",
            "channel_name": "Modern Trade (DMart & Reliance Smart)",
            "requested_cases": 1100,
            "fifo_naive_alloc_cases": 1100,
            "min_strategic_floor_pct": 80.0,
            "otif_penalty_pct_on_shortfall": 5.5,
            "net_margin_per_case_inr": 355.0,
            "case_net_realization_inr": 1140.0,
            "priority_weight": 1.20,
        },
        {
            "allocation_pool_id": "SHORT-NELM-DF300",
            "cfa_id": "CFA-KA-NELM",
            "cfa_name": "Nelamangala Bengaluru Mega CFA",
            "sku_id": df_sku["sku_id"],
            "sku_name": df_sku["sku_name"],
            "available_cfa_pool_cases": 2400,
            "total_competing_demand_cases": 3650,
            "customer_segment_id": "UNNATI-GOLD-BLR",
            "channel_name": "UNNATI eB2B Gold Kirana App Orders",
            "requested_cases": 750,
            "fifo_naive_alloc_cases": 350,
            "min_strategic_floor_pct": 65.0,
            "otif_penalty_pct_on_shortfall": 1.5,
            "net_margin_per_case_inr": 430.0,
            "case_net_realization_inr": 1245.0,
            "priority_weight": 1.15,
        },
        {
            "allocation_pool_id": "SHORT-NELM-DF300",
            "cfa_id": "CFA-KA-NELM",
            "cfa_name": "Nelamangala Bengaluru Mega CFA",
            "sku_id": df_sku["sku_id"],
            "sku_name": df_sku["sku_name"],
            "available_cfa_pool_cases": 2400,
            "total_competing_demand_cases": 3650,
            "customer_segment_id": "GT-WD-KARNATAKA",
            "channel_name": "General Trade Wholesale Dealers (18 WDs)",
            "requested_cases": 850,
            "fifo_naive_alloc_cases": 0,
            "min_strategic_floor_pct": 50.0,
            "otif_penalty_pct_on_shortfall": 0.5,
            "net_margin_per_case_inr": 415.0,
            "case_net_realization_inr": 1225.0,
            "priority_weight": 1.00,
        },
    ]

    def row_05(i: int) -> Dict[str, Any]:
        cfa = cfas[(i // 4) % len(cfas)]
        sku = skus[(i // 4) % len(skus)]
        seg_idx = i % 4
        chs = [
            ("QCOMM-HUB", "Quick-Commerce (Blinkit / Zepto)", 82.0, 8.0, 1.35),
            ("MT-CHAIN", "Modern Trade (DMart / Reliance)", 78.0, 5.5, 1.20),
            ("UNNATI-EB2B", "UNNATI eB2B Kirana Digital", 65.0, 1.5, 1.15),
            ("GT-WD-BASE", "General Trade Wholesale Dealers", 50.0, 0.5, 1.00),
        ][seg_idx]
        req = 300 + ((i * 23) % 600)
        return {
            "allocation_pool_id": f"SHORT-{cfa['cfa_id'][-4:]}-{1000 + (i // 4)}",
            "cfa_id": cfa["cfa_id"],
            "cfa_name": cfa["cfa_name"],
            "sku_id": sku["sku_id"],
            "sku_name": sku["sku_name"],
            "available_cfa_pool_cases": 1150,
            "total_competing_demand_cases": 1780,
            "customer_segment_id": f"{chs[0]}-{cfa['cfa_id'][-4:]}",
            "channel_name": chs[1],
            "requested_cases": req,
            "fifo_naive_alloc_cases": req if seg_idx < 2 else max(0, 1150 - 950),
            "min_strategic_floor_pct": chs[2],
            "otif_penalty_pct_on_shortfall": chs[3],
            "net_margin_per_case_inr": round(sku["mrp_per_case_inr"] * (sku["gross_margin_pct"] / 100.0), 2),
            "case_net_realization_inr": round(sku["mrp_per_case_inr"] * 0.81, 2),
            "priority_weight": chs[4],
        }

    stats.append(write_csv_and_seed("05_csl_shortage_orders_and_channel_allocations", hero_05, 120000, row_05))

    # -------------------------------------------------------------------------
    # TABLE 06: Depot Dispatch & Billing — EOD Billing & Cutoff Closer (SAP OpenAPI)
    # -------------------------------------------------------------------------
    hero_06 = [
        {
            "outbound_delivery_no": "809451021",
            "sap_sales_order_no": "4500918821",
            "cfa_id": "CFA-MH-BHIW",
            "cfa_name": "Bhiwandi Mega Mother CFA",
            "wd_or_customer_code": "WD-MA-0001",
            "customer_name": "Mahavir Agencies (Mumbai MMR)",
            "channel": "General Trade WD",
            "loading_status": "TRUCK_LOADED_WAITING_AT_GATE",
            "vehicle_reg_no": "MH04-kp-7712",
            "eod_cutoff_ist": "21:00",
            "minutes_to_cutoff": 68,
            "sap_vl02n_pgi_status": "BLOCKED_BATCH_SPLIT_MISMATCH",
            "sap_vf01_billing_block": "NONE",
            "nic_einvoice_irn_status": "PENDING_PGI",
            "nic_eway_bill_part_b_status": "PENDING_IRN",
            "blocker_code": "SAP_VL02N_FEFO_BATCH_SPLIT_VARIANCE",
            "auto_fixable_via_bapi": True,
            "sap_bapi_endpoint": "API_OUTBOUND_DELIVERY_SRV/ConfirmBatchSplitAndPGI",
            "invoice_value_inr": 1845000.0,
            "cases_loaded": 1120,
        },
        {
            "outbound_delivery_no": "809451028",
            "sap_sales_order_no": "4500918844",
            "cfa_id": "CFA-DL-KUND",
            "cfa_name": "Kundli NCR Mega CFA",
            "wd_or_customer_code": "WD-HA-0006",
            "customer_name": "Doaba Distributors (Delhi NCR)",
            "channel": "General Trade Platinum WD",
            "loading_status": "STAGED_AT_BAY_K03",
            "vehicle_reg_no": "HR55-AN-2901",
            "eod_cutoff_ist": "21:00",
            "minutes_to_cutoff": 54,
            "sap_vl02n_pgi_status": "PGI_POSTED",
            "sap_vf01_billing_block": "VKM3_CREDIT_EXPOSURE_EXCEEDED_BY_1_8L",
            "nic_einvoice_irn_status": "BLOCKED_BY_VKM3",
            "nic_eway_bill_part_b_status": "BLOCKED_BY_VKM3",
            "blocker_code": "FINAGG_AUTO_DRAWDOWN_PENDING_SYNC",
            "auto_fixable_via_bapi": True,
            "sap_bapi_endpoint": "Z_API_SD_FINAGG_SYNC_AND_VF01_BILLING",
            "invoice_value_inr": 2460000.0,
            "cases_loaded": 1490,
        },
        {
            "outbound_delivery_no": "809451034",
            "sap_sales_order_no": "4500918890",
            "cfa_id": "CFA-WB-DANK",
            "cfa_name": "Dankuni Eastern Mother CFA",
            "wd_or_customer_code": "MT-RELIANCE-KOL",
            "customer_name": "Reliance Smart Distribution Hub Dankuni",
            "channel": "Modern Trade",
            "loading_status": "TRUCK_SEALED_AT_GATE",
            "vehicle_reg_no": "WB23-F-8820",
            "eod_cutoff_ist": "21:00",
            "minutes_to_cutoff": 39,
            "sap_vl02n_pgi_status": "PGI_POSTED",
            "sap_vf01_billing_block": "VF01_POSTED_DOC_90441209",
            "nic_einvoice_irn_status": "IRN_GENERATED_8f4a21c9",
            "nic_eway_bill_part_b_status": "ERROR_PART_B_VEHICLE_FORMAT_HYPHEN",
            "blocker_code": "NIC_EWAY_PART_B_VEHICLE_REGEX_ERROR",
            "auto_fixable_via_bapi": True,
            "sap_bapi_endpoint": "Z_API_GST_EWAYBILL_PARTB_RETRY",
            "invoice_value_inr": 3120000.0,
            "cases_loaded": 1780,
        },
        {
            "outbound_delivery_no": "809451041",
            "sap_sales_order_no": "4500918912",
            "cfa_id": "CFA-TN-REDH",
            "cfa_name": "Red Hills Chennai Mega CFA",
            "wd_or_customer_code": "WD-TA-0020",
            "customer_name": "Coromandel Marketing (Chennai)",
            "channel": "General Trade WD",
            "loading_status": "STAGED_AT_BAY_R06",
            "vehicle_reg_no": "TN02-BM-6104",
            "eod_cutoff_ist": "21:00",
            "minutes_to_cutoff": 45,
            "sap_vl02n_pgi_status": "PGI_POSTED",
            "sap_vf01_billing_block": "VKM3_OVERDUE_19_DAYS_HARD_BLOCK",
            "nic_einvoice_irn_status": "BLOCKED_CREDIT_HARD_STOP",
            "nic_eway_bill_part_b_status": "BLOCKED_CREDIT_HARD_STOP",
            "blocker_code": "HARD_CREDIT_DELINQUENCY_REQUIRES_FINANCE_CONTROLLER",
            "auto_fixable_via_bapi": False,
            "sap_bapi_endpoint": "MANUAL_COMMERCIAL_FINANCE_SIGN_OFF_REQUIRED",
            "invoice_value_inr": 1390000.0,
            "cases_loaded": 840,
        },
    ]

    def row_06(i: int) -> Dict[str, Any]:
        cfa = cfas[i % len(cfas)]
        wd = wds[i % len(wds)]
        blocked = (i % 7 == 0)
        b_types = [
            ("SAP_VL02N_FEFO_BATCH_SPLIT_VARIANCE", True, "API_OUTBOUND_DELIVERY_SRV/ConfirmBatchSplitAndPGI"),
            ("FINAGG_AUTO_DRAWDOWN_PENDING_SYNC", True, "Z_API_SD_FINAGG_SYNC_AND_VF01_BILLING"),
            ("NIC_EWAY_PART_B_VEHICLE_REGEX_ERROR", True, "Z_API_GST_EWAYBILL_PARTB_RETRY"),
            ("HARD_CREDIT_DELINQUENCY_REQUIRES_FINANCE_CONTROLLER", False, "MANUAL_COMMERCIAL_FINANCE_SIGN_OFF_REQUIRED"),
        ]
        bt = b_types[i % len(b_types)] if blocked else ("CLEAN_BILLED_AND_GATE_RELEASED", True, "COMPLETED")
        cases = 350 + (i * 19) % 1200
        return {
            "outbound_delivery_no": str(809500000 + i),
            "sap_sales_order_no": str(4501000000 + i),
            "cfa_id": cfa["cfa_id"],
            "cfa_name": cfa["cfa_name"],
            "wd_or_customer_code": wd["wd_code"],
            "customer_name": wd["wd_name"],
            "channel": "General Trade WD",
            "loading_status": "TRUCK_LOADED_WAITING_AT_GATE" if blocked else "DISPATCHED_BEFORE_CUTOFF",
            "vehicle_reg_no": f"{cfa['state'][:2].upper()}14-CV-{(1000 + i) % 9999:04d}",
            "eod_cutoff_ist": "21:00",
            "minutes_to_cutoff": 20 + (i % 95),
            "sap_vl02n_pgi_status": "BLOCKED" if (blocked and i % 4 == 0) else "PGI_POSTED",
            "sap_vf01_billing_block": bt[0] if blocked else "NONE",
            "nic_einvoice_irn_status": "PENDING" if blocked else f"IRN_OK_{i:06d}",
            "nic_eway_bill_part_b_status": "PENDING" if blocked else f"EWB_1910{i:06d}",
            "blocker_code": bt[0],
            "auto_fixable_via_bapi": bt[1],
            "sap_bapi_endpoint": bt[2],
            "invoice_value_inr": round(cases * 1480.0, 2),
            "cases_loaded": cases,
        }

    stats.append(write_csv_and_seed("06_cfa_sap_eod_billing_irn_eway_cutoff", hero_06, 130000, row_06))

    # -------------------------------------------------------------------------
    # TABLE 07: Channel & RTM — MT / Q-Comm Slot & OTIF Copilot
    # -------------------------------------------------------------------------
    hero_07 = [
        {
            "asn_id": "ASN-QC-BLK-99101",
            "po_number": "BLK-MUM-PO-774120",
            "cfa_id": "CFA-MH-BHIW",
            "account_name": "Blinkit Mother Hub Bhiwandi-2",
            "channel_type": "Quick-Commerce",
            "booked_dock_slot_ist": "2026-11-15T10:00:00+05:30",
            "live_gps_eta_ist": "2026-11-15T10:42:00+05:30",
            "slot_tolerance_mins": 15,
            "projected_delay_mins": 42,
            "open_swap_slot_portal": "2026-11-15T11:15:00+05:30 (Blinkit Partner Portal Open)",
            "po_ordered_cases": 640,
            "cfa_ready_cases": 628,
            "case_fill_rate_pct": 98.1,
            "batch_mrsl_pct": 81.5,
            "po_invoice_value_inr": 985000.0,
            "contractual_otif_penalty_pct": 8.0,
            "at_risk_chargeback_inr": 78800.0,
            "otif_risk_driver": "NH3_THANE_CREEK_CONGESTION_SLOT_MISS",
        },
        {
            "asn_id": "ASN-QC-ZEP-99102",
            "po_number": "ZEP-BLR-PO-552019",
            "cfa_id": "CFA-KA-NELM",
            "account_name": "Zepto Mother Warehouse Whitefield",
            "channel_type": "Quick-Commerce",
            "booked_dock_slot_ist": "2026-11-15T11:30:00+05:30",
            "live_gps_eta_ist": "2026-11-15T11:18:00+05:30",
            "slot_tolerance_mins": 15,
            "projected_delay_mins": 0,
            "open_swap_slot_portal": "ON_TIME_KEEP_SLOT",
            "po_ordered_cases": 520,
            "cfa_ready_cases": 520,
            "case_fill_rate_pct": 100.0,
            "batch_mrsl_pct": 68.0,
            "po_invoice_value_inr": 790000.0,
            "contractual_otif_penalty_pct": 10.0,
            "at_risk_chargeback_inr": 79000.0,
            "otif_risk_driver": "BATCH_MRSL_68PCT_BELOW_ZEPTO_75PCT_GATE",
        },
        {
            "asn_id": "ASN-MT-DMT-99103",
            "po_number": "DMART-NCR-PO-319004",
            "cfa_id": "CFA-DL-KUND",
            "account_name": "DMart Regional DC Gurugram",
            "channel_type": "Modern Trade",
            "booked_dock_slot_ist": "2026-11-15T13:00:00+05:30",
            "live_gps_eta_ist": "2026-11-15T13:55:00+05:30",
            "slot_tolerance_mins": 30,
            "projected_delay_mins": 55,
            "open_swap_slot_portal": "2026-11-15T14:30:00+05:30 (Avenue Supermarts EDI Slot #19)",
            "po_ordered_cases": 1450,
            "cfa_ready_cases": 1420,
            "case_fill_rate_pct": 97.9,
            "batch_mrsl_pct": 83.0,
            "po_invoice_value_inr": 2280000.0,
            "contractual_otif_penalty_pct": 5.0,
            "at_risk_chargeback_inr": 114000.0,
            "otif_risk_driver": "BAY_LOADING_QUEUE_DELAY_NEEDS_EDI_SLOT_RESCHEDULE",
        },
    ]

    def row_07(i: int) -> Dict[str, Any]:
        cfa = cfas[i % len(cfas)]
        accts = [
            ("Blinkit Mother Hub", "Quick-Commerce", 15, 8.0),
            ("Zepto Dark-Store Feeder DC", "Quick-Commerce", 15, 8.0),
            ("Swiggy Instamart Mega Pod", "Quick-Commerce", 15, 7.5),
            ("DMart Regional DC", "Modern Trade", 30, 5.0),
            ("Reliance Smart Fulfillment Center", "Modern Trade", 30, 5.0),
            ("Amazon Fresh Grocery FC", "Modern Trade", 20, 6.0),
        ]
        ac = accts[i % len(accts)]
        late = (i % 8 == 0)
        delay = 38 if late else 4
        val = round(480000.0 + (i % 25) * 72000.0, 2)
        return {
            "asn_id": f"ASN-{100000 + i}",
            "po_number": f"PO-RET-{600000 + i}",
            "cfa_id": cfa["cfa_id"],
            "account_name": f"{ac[0]} ({cfa['city']})",
            "channel_type": ac[1],
            "booked_dock_slot_ist": f"2026-11-15T{(9 + i % 9):02d}:00:00+05:30",
            "live_gps_eta_ist": f"2026-11-15T{(9 + i % 9):02d}:{delay:02d}:00+05:30",
            "slot_tolerance_mins": ac[2],
            "projected_delay_mins": delay,
            "open_swap_slot_portal": f"2026-11-15T{(10 + i % 9):02d}:30:00+05:30" if late else "ON_TIME_KEEP_SLOT",
            "po_ordered_cases": 400 + (i % 700),
            "cfa_ready_cases": 395 + (i % 700),
            "case_fill_rate_pct": 98.8,
            "batch_mrsl_pct": 80.5,
            "po_invoice_value_inr": val,
            "contractual_otif_penalty_pct": ac[3],
            "at_risk_chargeback_inr": round(val * (ac[3] / 100.0), 2) if late else 0.0,
            "otif_risk_driver": "TRAFFIC_SLOT_DRIFT" if late else "ON_TRACK_OTIF",
        }

    stats.append(write_csv_and_seed("07_mt_qcomm_asn_dock_slots_and_otif", hero_07, 125000, row_07))

    # -------------------------------------------------------------------------
    # TABLE 08: Channel & RTM — Territory RTM Morning Pulse Gem (UNNATI + Vajra)
    # -------------------------------------------------------------------------
    hero_08 = [
        {
            "pulse_date": "2026-11-15",
            "territory_code": "TERR-WEST-PUNE-N",
            "territory_name": "Pune North & Pimpri-Chinchwad TM&D Territory",
            "zone": "West",
            "cfa_id": "CFA-MH-BHIW",
            "wd_code": "WD-MA-0001",
            "wd_name": "Mahavir Agencies (Mumbai MMR / Pune)",
            "unnati_overnight_orders": 312,
            "unnati_overnight_gmv_inr": 1485000.0,
            "unnati_7d_avg_gmv_inr": 960000.0,
            "vajra_scheduled_outlets": 440,
            "vajra_productive_calls": 248,
            "vajra_strike_rate_pct": 56.4,
            "lines_per_productive_call": 5.8,
            "top_stockout_sku": "Aashirvaad Shudh Chakki Atta 10kgx3",
            "wd_stockout_lines_count": 7,
            "active_trade_scheme": "Festive Combo 4%+2% Slab on Sunfeast Dark Fantasy + Bingo!",
            "pulse_alert_type": "UNNATI_SURGE_+55PCT_WITH_WD_ATTA_STOCKOUT_RISK",
        },
        {
            "pulse_date": "2026-11-15",
            "territory_code": "TERR-NORTH-LKO-C",
            "territory_name": "Lucknow Central & Kanpur Highway Beat",
            "zone": "North",
            "cfa_id": "CFA-UP-LKO1",
            "wd_code": "WD-UT-0007",
            "wd_name": "Awadh Distributors (Lucknow)",
            "unnati_overnight_orders": 144,
            "unnati_overnight_gmv_inr": 615000.0,
            "unnati_7d_avg_gmv_inr": 920000.0,
            "vajra_scheduled_outlets": 480,
            "vajra_productive_calls": 196,
            "vajra_strike_rate_pct": 40.8,
            "lines_per_productive_call": 3.4,
            "top_stockout_sku": "Sunfeast Yippee! Magic Masala 4-Pack",
            "wd_stockout_lines_count": 11,
            "active_trade_scheme": "Winter Noodle Display Contest (Rs 250/Kirana Hanger)",
            "pulse_alert_type": "VAJRA_BEAT_STRIKE_RATE_DROP_AND_SFA_ABSENTEEISM",
        },
        {
            "pulse_date": "2026-11-15",
            "territory_code": "TERR-EAST-KOL-S",
            "territory_name": "South Kolkata & Howrah Urban RTM",
            "zone": "East",
            "cfa_id": "CFA-WB-DANK",
            "wd_code": "WD-WE-0012",
            "wd_name": "Hooghly Enterprises (Kolkata)",
            "unnati_overnight_orders": 288,
            "unnati_overnight_gmv_inr": 1320000.0,
            "unnati_7d_avg_gmv_inr": 1110000.0,
            "vajra_scheduled_outlets": 410,
            "vajra_productive_calls": 334,
            "vajra_strike_rate_pct": 81.5,
            "lines_per_productive_call": 7.1,
            "top_stockout_sku": "Aashirvaad Svasti Mishti Doi 400g",
            "wd_stockout_lines_count": 4,
            "active_trade_scheme": "Svasti Chilled Visi-Cooler Loyalty Rebate 3%",
            "pulse_alert_type": "CHILLED_DAIRY_REPLENISHMENT_ACCELERATION_NEEDED",
        },
    ]

    def row_08(i: int) -> Dict[str, Any]:
        wd = wds[i % len(wds)]
        sched = 320 + (i % 180)
        prod = int(sched * (0.45 + (i % 38) / 100.0))
        gmv = round(420000.0 + (i % 30) * 38000.0, 2)
        avg_gmv = round(gmv * (0.85 if i % 6 == 0 else 1.04), 2)
        return {
            "pulse_date": f"2026-11-{(i % 15)+1:02d}",
            "territory_code": f"TERR-{wd['zone'][:3].upper()}-{1000 + (i % 450)}",
            "territory_name": f"{wd['city']} Beat Cluster #{(i % 12)+1}",
            "zone": wd["zone"],
            "cfa_id": wd["parent_cfa_id"],
            "wd_code": wd["wd_code"],
            "wd_name": wd["wd_name"],
            "unnati_overnight_orders": 95 + (i % 240),
            "unnati_overnight_gmv_inr": gmv,
            "unnati_7d_avg_gmv_inr": avg_gmv,
            "vajra_scheduled_outlets": sched,
            "vajra_productive_calls": prod,
            "vajra_strike_rate_pct": round(prod * 100.0 / sched, 1),
            "lines_per_productive_call": round(4.1 + (i % 35) * 0.1, 1),
            "top_stockout_sku": skus[i % len(skus)]["sku_name"],
            "wd_stockout_lines_count": (i % 9),
            "active_trade_scheme": "UNNATI Digital Slab 2.5% Instant Cashback",
            "pulse_alert_type": "BEAT_PRODUCTIVITY_DROP" if (prod / sched) < 0.52 else "HEALTHY_TERRITORY_PULSE",
        }

    stats.append(write_csv_and_seed("08_unnati_eb2b_vajra_sfa_morning_pulse", hero_08, 150000, row_08))

    # -------------------------------------------------------------------------
    # TABLE 09: Channel & RTM — Predictive WD Reorder & Dispatch Agent
    # -------------------------------------------------------------------------
    hero_09 = [
        {
            "wd_reorder_id": "WDR-20261115-001",
            "wd_code": "WD-MA-0001",
            "wd_name": "Mahavir Agencies (Mumbai MMR)",
            "parent_cfa_id": "CFA-MH-BHIW",
            "sku_id": atta_skus[0]["sku_id"],
            "sku_name": atta_skus[0]["sku_name"],
            "closing_dms_stock_cases": 185,
            "in_transit_primary_cases": 0,
            "avg_daily_secondary_sales_cases": 74.0,
            "unnati_surge_multiplier": 1.28,
            "current_doi_days": 2.0,
            "target_doi_norm_days": 12.0,
            "cfa_lead_time_days": 1.5,
            "finagg_credit_limit_lakh_inr": 85.0,
            "finagg_credit_used_lakh_inr": 52.4,
            "godown_free_space_cases": 1850,
            "case_billing_price_inr": 1320.0,
            "reorder_urgency": "CRITICAL_STOCKOUT_WITHIN_48H",
        },
        {
            "wd_reorder_id": "WDR-20261115-002",
            "wd_code": "WD-KA-0018",
            "wd_name": "Kaveri Distributors (Bengaluru)",
            "parent_cfa_id": "CFA-KA-NELM",
            "sku_id": snack_skus[2]["sku_id"],
            "sku_name": snack_skus[2]["sku_name"],
            "closing_dms_stock_cases": 140,
            "in_transit_primary_cases": 60,
            "avg_daily_secondary_sales_cases": 52.0,
            "unnati_surge_multiplier": 1.18,
            "current_doi_days": 3.3,
            "target_doi_norm_days": 12.0,
            "cfa_lead_time_days": 1.0,
            "finagg_credit_limit_lakh_inr": 48.0,
            "finagg_credit_used_lakh_inr": 44.8,
            "godown_free_space_cases": 980,
            "case_billing_price_inr": 815.0,
            "reorder_urgency": "NEEDS_FINAGG_OVERDRAFT_DRAW_TO_PREVENT_STOCKOUT",
        },
        {
            "wd_reorder_id": "WDR-20261115-003",
            "wd_code": "WD-WE-0012",
            "wd_name": "Hooghly Enterprises (Kolkata)",
            "parent_cfa_id": "CFA-WB-DANK",
            "sku_id": df_sku["sku_id"],
            "sku_name": df_sku["sku_name"],
            "closing_dms_stock_cases": 210,
            "in_transit_primary_cases": 0,
            "avg_daily_secondary_sales_cases": 64.0,
            "unnati_surge_multiplier": 1.32,
            "current_doi_days": 2.5,
            "target_doi_norm_days": 12.0,
            "cfa_lead_time_days": 1.0,
            "finagg_credit_limit_lakh_inr": 85.0,
            "finagg_credit_used_lakh_inr": 49.0,
            "godown_free_space_cases": 1620,
            "case_billing_price_inr": 1210.0,
            "reorder_urgency": "FESTIVE_SCHEME_PULL_AUTO_REPLENISH",
        },
    ]

    def row_09(i: int) -> Dict[str, Any]:
        wd = wds[i % len(wds)]
        sku = skus[(i * 3) % len(skus)]
        daily = round(18.0 + (i % 55) * 1.1, 1)
        stock = 60 + (i * 29) % 720
        doi = round(stock / max(daily, 1.0), 1)
        lim = wd["finagg_credit_limit_lakh_inr"]
        used = round(lim * (0.48 + (i % 45) * 0.01), 2)
        return {
            "wd_reorder_id": f"WDR-202611-{100000 + i}",
            "wd_code": wd["wd_code"],
            "wd_name": wd["wd_name"],
            "parent_cfa_id": wd["parent_cfa_id"],
            "sku_id": sku["sku_id"],
            "sku_name": sku["sku_name"],
            "closing_dms_stock_cases": stock,
            "in_transit_primary_cases": 0 if i % 3 != 0 else 120,
            "avg_daily_secondary_sales_cases": daily,
            "unnati_surge_multiplier": round(1.0 + (i % 5) * 0.06, 2),
            "current_doi_days": doi,
            "target_doi_norm_days": float(wd["target_doi_days"]),
            "cfa_lead_time_days": 1.0 if wd["distance_from_cfa_km"] < 80 else 2.0,
            "finagg_credit_limit_lakh_inr": lim,
            "finagg_credit_used_lakh_inr": used,
            "godown_free_space_cases": 650 + (i % 1500),
            "case_billing_price_inr": round(sku["mrp_per_case_inr"] * 0.82, 2),
            "reorder_urgency": "CRITICAL_STOCKOUT_WITHIN_48H" if doi < 4.0 else ("REORDER_BELOW_NORM" if doi < 8.5 else "ADEQUATE_DOI"),
        }

    stats.append(write_csv_and_seed("09_wd_stockist_doi_credit_and_reorders", hero_09, 135000, row_09))

    # -------------------------------------------------------------------------
    # TABLE 10: Fleet & Freight — Dynamic Rerouter (Maps Platform + EV + E-Way)
    # -------------------------------------------------------------------------
    hero_10 = [
        {
            "route_trip_id": "ZEN-TRIP-5501",
            "shipment_id": "SHP-PRI-90001",
            "vehicle_reg_no": "MH12-QW-4821",
            "carrier_id": "CAR-ITC-001",
            "vehicle_type": "32ft MXL Container",
            "is_ev": False,
            "ev_battery_soc_pct": 100.0,
            "origin_node": "ICML-MH-RANJ01 (Pune)",
            "dest_node": "CFA-MH-BHIW (Mumbai MMR)",
            "planned_corridor": "NH-48 Mumbai-Pune Ghat Section",
            "disruption_event": "LANDSLIDE_AND_TANKER_SPILL_KHANDALA_GHAT_3H40M_HALTS",
            "maps_live_delay_mins": 220,
            "alternate_corridor": "Tamhini Ghat / Old NH-48 Diversion via Chakan-Talegaon Bypass",
            "alternate_extra_km": 28.0,
            "alternate_time_saved_mins": 152,
            "municipal_no_entry_window": "08:00-11:00 Thane Octroi Naka",
            "eway_bill_no": "EWB-271099482101",
            "eway_hours_remaining": 3.2,
            "cargo_value_inr": 2680000.0,
        },
        {
            "route_trip_id": "ZEN-TRIP-5502",
            "shipment_id": "SHP-EV-41009",
            "vehicle_reg_no": "KA01-EV-9042",
            "carrier_id": "CAR-ITC-011",
            "vehicle_type": "Tata Ace EV 4W (Green Logistics)",
            "is_ev": True,
            "ev_battery_soc_pct": 31.0,
            "origin_node": "CFA-KA-NELM (Bengaluru)",
            "dest_node": "Zepto Whitefield + 4 Platinum UNNATI Kiranas",
            "planned_corridor": "Outer Ring Road Hebbal -> KR Puram",
            "disruption_event": "ORR_WATERLOGGING_DELAY_PLUS_EV_LOW_SOC_RANGE_DEFICIT",
            "maps_live_delay_mins": 85,
            "alternate_corridor": "STRR / Bellary Road + 18-Min Fast DC Top-Up at BESCOM Indiranagar Hub",
            "alternate_extra_km": 9.5,
            "alternate_time_saved_mins": 48,
            "municipal_no_entry_window": "EXEMPT_GREEN_PLATE_COMMERCIAL_EV",
            "eway_bill_no": "EWB-291088412099",
            "eway_hours_remaining": 9.5,
            "cargo_value_inr": 640000.0,
        },
        {
            "route_trip_id": "ZEN-TRIP-5503",
            "shipment_id": "SHP-PRI-90044",
            "vehicle_reg_no": "WB23-F-8820",
            "carrier_id": "CAR-ITC-002",
            "vehicle_type": "32ft MXL Container",
            "is_ev": False,
            "ev_battery_soc_pct": 100.0,
            "origin_node": "ICML-OR-KHOR02 (Bhubaneswar)",
            "dest_node": "CFA-WB-DANK (Kolkata)",
            "planned_corridor": "NH-16 Balasore - Kharagpur - Kolaghat",
            "disruption_event": "KOLAGHAT_BRIDGE_SINGLE_LANE_REPAIR_AND_KOLKATA_NO_ENTRY_CURFEW",
            "maps_live_delay_mins": 145,
            "alternate_corridor": "NH-16 -> Uluberia Spur Staging + Post-21:00 Vidyasagar Setu Window & EWB Extension",
            "alternate_extra_km": 14.0,
            "alternate_time_saved_mins": 95,
            "municipal_no_entry_window": "08:00-21:00 Kolkata Police Heavy Goods Restriction",
            "eway_bill_no": "EWB-211077309184",
            "eway_hours_remaining": 2.4,
            "cargo_value_inr": 2190000.0,
        },
    ]

    def row_10(i: int) -> Dict[str, Any]:
        cfa = cfas[i % len(cfas)]
        is_ev = (i % 5 == 0)
        car = ev_carriers[i % len(ev_carriers)] if is_ev else l1_mxl[i % len(l1_mxl)]
        disrupted = (i % 7 == 0)
        delay = 135 if disrupted else 12
        return {
            "route_trip_id": f"ZEN-TRIP-{20000 + i}",
            "shipment_id": f"SHP-PRI-{100000 + i}",
            "vehicle_reg_no": f"{cfa['state'][:2].upper()}09-{'EV' if is_ev else 'GD'}-{(1000 + i) % 9999:04d}",
            "carrier_id": car["carrier_id"],
            "vehicle_type": car["vehicle_type"],
            "is_ev": is_ev,
            "ev_battery_soc_pct": round(28.0 + (i % 65), 1) if is_ev else 100.0,
            "origin_node": f"{cfa['primary_icml_id']}",
            "dest_node": f"{cfa['cfa_id']} ({cfa['city']})",
            "planned_corridor": f"NH-{(i % 48)+1} Primary Trunk Corridor",
            "disruption_event": "MONSOON_HIGHWAY_CONGESTION_AND_CURFEW_CONFLICT" if disrupted else "CLEAR_CORRIDOR",
            "maps_live_delay_mins": delay,
            "alternate_corridor": "Expressway Ring Bypass via Maps Routes Matrix v2",
            "alternate_extra_km": 16.5 if disrupted else 0.0,
            "alternate_time_saved_mins": 88 if disrupted else 0,
            "municipal_no_entry_window": "EXEMPT_GREEN_PLATE_COMMERCIAL_EV" if is_ev else "17:00-21:00 City Peak Curfew",
            "eway_bill_no": f"EWB-{cfa['gst_state_code']}10{500000 + i}",
            "eway_hours_remaining": 2.8 if disrupted else 18.5,
            "cargo_value_inr": round(480000.0 if is_ev else 1950000.0, 2),
        }

    stats.append(write_csv_and_seed("10_zenith_fleet_gps_traffic_and_ev_routes", hero_10, 125000, row_10))

    # -------------------------------------------------------------------------
    # TABLE 11: Transport Procurement — Routing Guide Compliance Agent (Gem)
    # -------------------------------------------------------------------------
    hero_11 = [
        {
            "tender_id": "TND-202611-7701",
            "lane_id": "LANE-RANJ-BHIW",
            "lane_description": "Ranjangaon ICML -> Bhiwandi Mumbai Mother CFA (168 km)",
            "vehicle_type": "32ft MXL Container",
            "l1_contracted_carrier": "TCI Freight Primary Logistics #1",
            "l1_contract_rate_inr": 19800.0,
            "l1_tender_response": "REJECTED_NO_VEHICLE_PLACEMENT",
            "l2_backup_carrier": "CJ Darcl Primary FTL #1",
            "l2_contract_rate_inr": 21200.0,
            "l2_tender_response": "BYPASSED_BY_PLANNER_WITHOUT_WATERFALL_WAIT",
            "actual_awarded_carrier": "Spot Market Broker - Highway King Trans #1",
            "actual_awarded_tier": "SPOT",
            "actual_paid_freight_inr": 29400.0,
            "maverick_leakage_vs_l2_inr": 8200.0,
            "maverick_leakage_vs_l1_inr": 9600.0,
            "monthly_lane_spot_trips": 28,
            "compliance_violation": "MAVERICK_SPOT_BOOKING_SKIPPED_L2_WATERFALL",
        },
        {
            "tender_id": "TND-202611-7702",
            "lane_id": "LANE-HARI-LKO1",
            "lane_description": "Haridwar ICML -> Lucknow Amausi CFA (545 km)",
            "vehicle_type": "32ft MXL Container",
            "l1_contracted_carrier": "Mahindra Logistics Contract Fleet #1",
            "l1_contract_rate_inr": 44500.0,
            "l1_tender_response": "REJECTED_FESTIVE_BACKHAUL_IMBALANCE",
            "l2_backup_carrier": "RIVIGO / Gati Express Linehaul #1",
            "l2_contract_rate_inr": 47200.0,
            "l2_tender_response": "REJECTED_CAPACITY_CAP_EXCEEDED",
            "actual_awarded_carrier": "Spot Market Broker - Jai Hind Roadlines #1",
            "actual_awarded_tier": "SPOT",
            "actual_paid_freight_inr": 61800.0,
            "maverick_leakage_vs_l2_inr": 14600.0,
            "maverick_leakage_vs_l1_inr": 17300.0,
            "monthly_lane_spot_trips": 19,
            "compliance_violation": "CHRONIC_L1_TENDER_REJECTION_NEEDS_WATERFALL_REALLOCATION",
        },
        {
            "tender_id": "TND-202611-7703",
            "lane_id": "LANE-MALU-REDH",
            "lane_description": "Malur ICML -> Red Hills Chennai Mega CFA (310 km)",
            "vehicle_type": "32ft MXL Container",
            "l1_contracted_carrier": "Varuna Integrated Logistics #1",
            "l1_contract_rate_inr": 28600.0,
            "l1_tender_response": "BYPASSED_URGENT_MANUAL_INDENT",
            "l2_backup_carrier": "VRL Logistics Surface Linehaul #1",
            "l2_contract_rate_inr": 29900.0,
            "l2_tender_response": "NOT_TENDERED",
            "actual_awarded_carrier": "Spot Market Broker - Highway King Trans #2",
            "actual_awarded_tier": "SPOT",
            "actual_paid_freight_inr": 39500.0,
            "maverick_leakage_vs_l2_inr": 9600.0,
            "maverick_leakage_vs_l1_inr": 10900.0,
            "monthly_lane_spot_trips": 15,
            "compliance_violation": "UNAPPROVED_MANUAL_SPOT_INDENT_BYPASSED_L1_AND_L2",
        },
    ]

    def row_11(i: int) -> Dict[str, Any]:
        icml = icmls[i % len(icmls)]
        cfa = cfas[(i * 2) % len(cfas)]
        l1_r = round(22000.0 + (i % 35) * 1150.0, 2)
        l2_r = round(l1_r * 1.065, 2)
        is_spot = (i % 6 == 0)
        paid = round(l1_r * 1.36, 2) if is_spot else l1_r
        return {
            "tender_id": f"TND-202611-{20000 + i}",
            "lane_id": f"LANE-{icml['icml_id'][-6:]}-{cfa['cfa_id'][-4:]}",
            "lane_description": f"{icml['city']} -> {cfa['city']}",
            "vehicle_type": "32ft MXL Container",
            "l1_contracted_carrier": l1_mxl[i % len(l1_mxl)]["carrier_name"],
            "l1_contract_rate_inr": l1_r,
            "l1_tender_response": "REJECTED_NO_VEHICLE_PLACEMENT" if is_spot else "ACCEPTED_WITHIN_90M_SLA",
            "l2_backup_carrier": "CJ Darcl Primary FTL #1",
            "l2_contract_rate_inr": l2_r,
            "l2_tender_response": "BYPASSED_BY_PLANNER" if (is_spot and i % 12 == 0) else ("ACCEPTED" if is_spot else "NOT_REQUIRED"),
            "actual_awarded_carrier": spot_carriers[i % len(spot_carriers)]["carrier_name"] if is_spot else l1_mxl[i % len(l1_mxl)]["carrier_name"],
            "actual_awarded_tier": "SPOT" if is_spot else "L1",
            "actual_paid_freight_inr": paid,
            "maverick_leakage_vs_l2_inr": round(max(0.0, paid - l2_r), 2),
            "maverick_leakage_vs_l1_inr": round(max(0.0, paid - l1_r), 2),
            "monthly_lane_spot_trips": 12 if is_spot else 1,
            "compliance_violation": "MAVERICK_SPOT_BOOKING_SKIPPED_L2_WATERFALL" if is_spot else "COMPLIANT_L1_AWARD",
        }

    stats.append(write_csv_and_seed("11_carrier_routing_guide_tenders_and_spot", hero_11, 125000, row_11))

    # -------------------------------------------------------------------------
    # TABLE 12: Freight Controller — Freight Bill Audit Agent (Multimodal + Studio)
    # -------------------------------------------------------------------------
    hero_12 = [
        {
            "freight_invoice_id": "FINV-TCI-2026-9041",
            "lr_number": "LR-TCI-882910",
            "shipment_id": "SHP-PRI-90001",
            "carrier_id": "CAR-ITC-001",
            "carrier_name": "TCI Freight Primary Logistics #1",
            "lane_name": "Ranjangaon ICML -> Sanand Ahmedabad CFA (665 km)",
            "contract_base_freight_inr": 54200.0,
            "billed_base_freight_inr": 58900.0,
            "contract_diesel_fsc_pct": 4.2,
            "billed_diesel_fsc_pct": 7.8,
            "gps_verified_detention_hrs": 1.0,
            "billed_detention_hrs": 8.0,
            "detention_rate_per_hr_inr": 850.0,
            "pod_shortage_damaged_cases": 14,
            "pod_shortage_debit_value_inr": 20160.0,
            "duplicate_lr_claim_flag": False,
            "total_carrier_billed_inr": 70294.0,
            "verified_net_payable_inr": 37166.0,
            "recoverable_overcharge_and_osd_inr": 33128.0,
            "scanned_lr_doc": "DOC-LR-882910.png",
            "scanned_pod_doc": "DOC-POD-882910.png",
            "scanned_invoice_doc": "DOC-FINV-9041.png",
            "audit_exception_code": "QUAD_MISMATCH_SLAB_FSC_DETENTION_AND_POD_SHORTAGE",
        },
        {
            "freight_invoice_id": "FINV-HWK-2026-9042",
            "lr_number": "LR-HWK-771024",
            "shipment_id": "SHP-PRI-90018",
            "carrier_id": "CAR-ITC-015",
            "carrier_name": "Spot Market Broker - Highway King Trans #1",
            "lane_name": "Haridwar ICML -> Kundli NCR Mega CFA (215 km)",
            "contract_base_freight_inr": 26500.0,
            "billed_base_freight_inr": 26500.0,
            "contract_diesel_fsc_pct": 0.0,
            "billed_diesel_fsc_pct": 5.5,
            "gps_verified_detention_hrs": 0.0,
            "billed_detention_hrs": 12.0,
            "detention_rate_per_hr_inr": 1400.0,
            "pod_shortage_damaged_cases": 0,
            "pod_shortage_debit_value_inr": 0.0,
            "duplicate_lr_claim_flag": True,
            "total_carrier_billed_inr": 44757.5,
            "verified_net_payable_inr": 0.0,
            "recoverable_overcharge_and_osd_inr": 44757.5,
            "scanned_lr_doc": "DOC-LR-771024.png",
            "scanned_pod_doc": "DOC-POD-771024.png",
            "scanned_invoice_doc": "DOC-FINV-9042.png",
            "audit_exception_code": "DUPLICATE_LR_ALREADY_PAID_ON_VOUCHER_51008941",
        },
        {
            "freight_invoice_id": "FINV-VRL-2026-9043",
            "lr_number": "LR-VRL-664319",
            "shipment_id": "SHP-PRI-90019",
            "carrier_id": "CAR-ITC-002",
            "carrier_name": "VRL Logistics Surface Linehaul #1",
            "lane_name": "Panchla ICML -> Patna Fatuha CFA (585 km)",
            "contract_base_freight_inr": 49800.0,
            "billed_base_freight_inr": 49800.0,
            "contract_diesel_fsc_pct": 4.0,
            "billed_diesel_fsc_pct": 6.5,
            "gps_verified_detention_hrs": 2.0,
            "billed_detention_hrs": 9.5,
            "detention_rate_per_hr_inr": 850.0,
            "pod_shortage_damaged_cases": 6,
            "pod_shortage_debit_value_inr": 9540.0,
            "duplicate_lr_claim_flag": False,
            "total_carrier_billed_inr": 61112.0,
            "verified_net_payable_inr": 43952.0,
            "recoverable_overcharge_and_osd_inr": 17160.0,
            "scanned_lr_doc": "DOC-LR-664319.png",
            "scanned_pod_doc": "DOC-POD-664319.png",
            "scanned_invoice_doc": "DOC-FINV-9043.png",
            "audit_exception_code": "INFLATED_DETENTION_HOURS_AND_POD_WET_CARTONS",
        },
    ]

    def row_12(i: int) -> Dict[str, Any]:
        car = carriers[i % len(carriers)]
        cfa = cfas[i % len(cfas)]
        base = round(24000.0 + (i % 30) * 1450.0, 2)
        has_err = (i % 5 == 0)
        billed_base = round(base * (1.08 if has_err else 1.0), 2)
        c_fsc = 4.0
        b_fsc = 7.2 if has_err else 4.0
        g_det = 1.0 if has_err else 0.0
        b_det = 6.0 if has_err else 0.0
        det_r = float(car["detention_rate_per_hr_inr"])
        short_c = 5 if (has_err and i % 10 == 0) else 0
        short_v = round(short_c * 1420.0, 2)
        tot_billed = round(billed_base * (1.0 + b_fsc / 100.0) + b_det * det_r, 2)
        ver_pay = round(max(0.0, base * (1.0 + c_fsc / 100.0) + g_det * det_r - short_v), 2)
        return {
            "freight_invoice_id": f"FINV-2026-{300000 + i}",
            "lr_number": f"LR-ITC-{700000 + i}",
            "shipment_id": f"SHP-PRI-{100000 + i}",
            "carrier_id": car["carrier_id"],
            "carrier_name": car["carrier_name"],
            "lane_name": f"{cfa['primary_icml_id']} -> {cfa['cfa_id']} ({cfa['city']})",
            "contract_base_freight_inr": base,
            "billed_base_freight_inr": billed_base,
            "contract_diesel_fsc_pct": c_fsc,
            "billed_diesel_fsc_pct": b_fsc,
            "gps_verified_detention_hrs": g_det,
            "billed_detention_hrs": b_det,
            "detention_rate_per_hr_inr": det_r,
            "pod_shortage_damaged_cases": short_c,
            "pod_shortage_debit_value_inr": short_v,
            "duplicate_lr_claim_flag": False,
            "total_carrier_billed_inr": tot_billed,
            "verified_net_payable_inr": ver_pay,
            "recoverable_overcharge_and_osd_inr": round(tot_billed - ver_pay, 2),
            "scanned_lr_doc": "DOC-LR-882910.png",
            "scanned_pod_doc": "DOC-POD-882910.png",
            "scanned_invoice_doc": "DOC-FINV-9041.png",
            "audit_exception_code": "RATE_FSC_DETENTION_VARIANCE" if has_err else "THREE_WAY_MATCH_CLEAN",
        }

    stats.append(write_csv_and_seed("12_freight_lr_pod_invoices_and_claims", hero_12, 130000, row_12))
    return stats


def generate_multimodal_scanned_documents() -> List[Dict[str, Any]]:
    """Renders 24 realistic scanned logistics & cold-chain PNG documents via Pillow (or clean SVG/PNG fallback)."""
    docs_spec = [
        ("DOC-LR-882910.png", "LORRY RECEIPT / CONSIGNMENT NOTE (BILTY)", [
            "Transporter: TCI Freight Primary Logistics #1   |   LR No: LR-TCI-882910   |   Date: 14-Nov-2026",
            "Consignor: ITC Limited - Ranjangaon ICML (ICML-MH-RANJ01), MIDC Pune, Maharashtra (GSTIN: 27AAACI5950L1Z8)",
            "Consignee: ITC Clearing & Forwarding Depot - Sanand Ahmedabad CFA (CFA-GJ-SANJ) (GSTIN: 24AAACI5950L1Z4)",
            "Vehicle No: MH12-QW-4821 (32ft MXL Container)   |   NIC E-Way Bill: EWB-271099482101",
            "Packages: 1,170 Master Cartons (560 Cases Aashirvaad Atta 10kgx3 + 610 Cases Sunfeast Dark Fantasy)",
            "Gross Weight: 17,840 kg   |   Contracted Lane Tariff Ref: ITC-TM-WEST-2026-L1 (Base Rs 54,200)",
            "Driver Signature: R. Suryavanshi   |   ICML Dispatch Security Gate Seal: SEAL-RJ-992014 [INTACT]"
        ], "DISPATCHED - SUBJECT TO POD RECEIPT", False),
        ("DOC-POD-882910.png", "STAMPED PROOF OF DELIVERY (POD) & GATE UNLOADING RECEIPT", [
            "Receiving Depot: Sanand Gujarat State CFA (CFA-GJ-SANJ)   |   Ref LR No: LR-TCI-882910",
            "Gate Arrival (FASTag/ANPR): 15-Nov-2026 07:10 IST   |   Unloading Completed: 15-Nov-2026 10:10 IST",
            "Total Elapsed Yard Time: 3.0 Hours (Free Time: 2.0 Hours -> Verified Billable Detention = 1.0 Hour ONLY)",
            "Manifested Cartons: 1,170 Cases   |   Good Condition Received: 1,156 Cases",
            "EXCEPTION / OS&D REMARK: 14 Master Cartons Sunfeast Dark Fantasy 300g CRUSHED & WET at rear door!",
            "Debit Valuation: 14 Cases x Rs 1,440/case = Rs 20,160 OS&D Carrier Recovery Claim Logged (SAP QM Lot #8812)",
            "CFA Receiving Supervisor Stamp & Sign: K. Patel (CFA-GJ-SANJ Seal #04)"
        ], "RECEIVED WITH 14 CASES DAMAGE / SHORTAGE", True),
        ("DOC-FINV-9041.png", "CARRIER TAX INVOICE (FREIGHT & ACCESSORIALS)", [
            "Issuer: TCI Freight Primary Logistics #1   |   Invoice No: FINV-TCI-2026-9041   |   Ref LR: LR-TCI-882910",
            "Line 1 - Base Linehaul Charge (Billed Wrong Slab 22MT): Rs 58,900.00  [Contracted 32ft MXL = Rs 54,200.00]",
            "Line 2 - Diesel Escalation Surcharge @ 7.8%:            Rs  4,594.00  [Contracted IOCL Peg = 4.2% = Rs 2,276.40]",
            "Line 3 - Halting / Detention Claim (8.0 Hours @ Rs 850): Rs  6,800.00  [Zenith GPS + POD Verified = 1.0 Hr = Rs 850]",
            "Line 4 - Less POD Shortage / Damage Credit:             Rs      0.00  [Omitted Rs 20,160 POD Exception!]",
            "TOTAL BILLED BY CARRIER: Rs 70,294.00   |   AI-AUDITED NET PAYABLE: Rs 37,166.40 (Dispute Rs 33,127.60)"
        ], "AUDIT HOLD - OVERCHARGE & POD DEBIT PENDING", True),
        ("DOC-LR-771024.png", "SPOT MARKET LORRY RECEIPT (CONSIGNMENT NOTE)", [
            "Broker / Carrier: Highway King Trans #1   |   LR No: LR-HWK-771024   |   Date: 09-Nov-2026",
            "Lane: Haridwar ICML (ICML-UK-HARI04) -> Kundli NCR Mega CFA (CFA-DL-KUND) (215 km)",
            "Vehicle No: HR55-BT-6019 (32ft MXL)   |   GST RCM 5% Applicable on Unregistered Spot GTA",
            "Cargo: 980 Cases Savlon Handwash & Classmate Longbooks   |   Agreed Spot Memo Rate: Rs 26,500 All-In"
        ], "SPOT INDENT - ALL-IN FLAT RATE", False),
        ("DOC-POD-771024.png", "KUNDLI NCR CFA RECEIVING POD SLIP", [
            "Ref LR: LR-HWK-771024   |   Gate In: 09-Nov-2026 15:20 IST   |   Gate Out: 09-Nov-2026 16:55 IST",
            "Total Dwell: 1 Hr 35 Mins (Within 2-Hour Free Time -> ZERO Detention Applicable)",
            "Packages Received: 980 / 980 Clean   |   PRIOR PAYMENT ALERT: Already Settled on SAP Voucher #51008941!"
        ], "CLEAN POD - ALREADY PAID VOUCHER #51008941", True),
        ("DOC-FINV-9042.png", "DUPLICATE CARRIER FREIGHT BILL SUBMISSION", [
            "Carrier: Highway King Trans #1   |   Invoice No: FINV-HWK-2026-9042   |   Ref LR: LR-HWK-771024",
            "Billed Base Freight: Rs 26,500.00 + Uncontracted FSC 5.5% (Rs 1,457.50) + 12 Hrs Fake Detention (Rs 16,800.00)",
            "TOTAL CLAIMED: Rs 44,757.50   |   AI VERDICT: 100% BLOCK - DUPLICATE SUBMISSION OF PAID LR-HWK-771024!"
        ], "REJECTED - 100% DUPLICATE LR SUBMISSION", True),
        ("DOC-LR-664319.png", "LORRY RECEIPT - EASTERN CORRIDOR LINEHAUL", [
            "Transporter: VRL Logistics Surface Linehaul #1   |   LR No: LR-VRL-664319   |   Date: 13-Nov-2026",
            "Origin: Panchla ICML (ICML-WB-PANC03)   |   Destination: Patna Fatuha State CFA (CFA-BR-PATN)",
            "Vehicle: WB11-EK-3390   |   Cargo: 1,040 Cases Aashirvaad Atta & Sunfeast Marie Light",
            "Contracted Base Freight: Rs 49,800.00   |   Fuel Peg: 4.0%"
        ], "IN TRANSIT / DELIVERED", False),
        ("DOC-POD-664319.png", "PATNA FATUHA CFA STAMPED POD RECEIPT", [
            "Ref LR: LR-VRL-664319   |   Gate In: 14-Nov-2026 11:00 IST   |   Gate Out: 14-Nov-2026 15:00 IST",
            "Verified Dwell: 4.0 Hours (2.0 Hrs Free -> 2.0 Hours Valid Detention = Rs 1,700)",
            "EXCEPTION: 6 Cartons Sunfeast Marie Light TARPAULIN WATER SEEPAGE DAMAGE (Debit Rs 9,540)"
        ], "POD SHORTAGE / WET DAMAGE - 6 CASES", True),
        ("DOC-FINV-9043.png", "CARRIER FREIGHT INVOICE - VRL #9043", [
            "Invoice No: FINV-VRL-2026-9043   |   Ref LR: LR-VRL-664319",
            "Billed Base: Rs 49,800 + Billed FSC 6.5% (Rs 3,237) + Billed Detention 9.5 Hrs (Rs 8,075) = Rs 61,112",
            "AI Verified Payable: Rs 49,800 + 4.0% FSC (Rs 1,992) + 2.0 Hrs Detention (Rs 1,700) - Rs 9,540 OS&D = Rs 43,952"
        ], "SHORT-PAY VOUCHER STAGED - SAVE RS 17,160", True),
        ("DOC-STRIP-SHP-CLD-70001.png", "DRISHTI BLE REEFER THERMAL LOGGER STRIP CHART", [
            "Shipment: SHP-CLD-70001 (Kapurthala ICML -> Kundli NCR CFA)   |   SKU: ITC Master Chef Crispy Fries (-18C)",
            "Logger Serial: DRISHTI-BLE-99401   |   Activation Energy (Ea): 86.5 kJ/mol   |   Max Threshold: -15.0 C",
            "15-Min Trace (C): -18.4, -18.1, -17.8, -14.2, -11.6, -9.8, -8.9 [PEAK], -9.4, -11.2, -15.6, -17.9, -18.2",
            "Computed Arrhenius MKT: -13.18 C (Exceeds -15.0 C Spec for 105 Mins due to Evaporator Fan Slip near Karnal)",
            "QA Disposition: QUARANTINE PALLETS 14-18 AT REAR DOOR + FILE CARRIER COLD-CHAIN CLAIM"
        ], "THERMAL EXCURSION ALERT - MKT BREACH", True),
        ("DOC-STRIP-SHP-CLD-70002.png", "DRISHTI BLE CHILLED DAIRY LOGGER STRIP CHART", [
            "Shipment: SHP-CLD-70002 (Panchla ICML -> Patna CFA)   |   SKU: Aashirvaad Svasti Malai Paneer (2-8 C)",
            "15-Min Trace (C): 4.2, 4.5, 5.1, 9.4, 12.8, 14.1, 14.6 [PEAK], 13.9, 11.8, 8.4, 5.9, 4.6",
            "Root Cause: Reefer Switched Off by Driver During 2-Hour Highway Halt (4 Door Events Logged)",
            "Computed Arrhenius MKT: +10.42 C -> Shelf-Life Accelerated Loss = 6.4 Days -> REJECT LOT & DEBIT CARRIER"
        ], "CRITICAL SPOILAGE EXCURSION - REJECT LOT", True),
        ("DOC-STRIP-SHP-CLD-70003.png", "DRISHTI COOL-CHAIN LOGGER - FABELLE LUXURY CHOCOLATES", [
            "Shipment: SHP-CLD-70003 (Malur ICML -> Bhiwandi CFA)   |   SKU: Fabelle Choco Deck (16-20 C)",
            "15-Min Trace (C): 17.8, 18.1, 18.4, 21.6, 23.4, 24.1 [PEAK], 22.5, 19.8, 18.5, 18.1, 17.9, 18.0",
            "Computed Arrhenius MKT: +20.48 C -> Minor Cocoa-Butter Bloom Watch; Sensory QA Sample Required Before Release"
        ], "QA SENSORY HOLD - MINOR EXCURSION", False),
    ]
    # Add 12 more weighbridge, E-Way Bill & CFA manifest docs to reach 24 rich multimodal assets
    for idx in range(1, 13):
        docs_spec.append((
            f"DOC-WB-SLIP-90{idx:02d}.png",
            f"ICML AUTOMATED WEIGHBRIDGE & FASTAG GATE TICKET #90{idx:02d}",
            [
                f"Plant: ICML-MH-RANJ01 / ICML-PB-KAPU05   |   Ticket ID: WB-2026-90{idx:02d}   |   Date: 15-Nov-2026",
                f"Vehicle Reg: MH12-QW-{4800 + idx}   |   Tare Weight: {9650 + idx * 45} kg   |   Gross Weight: {26900 + idx * 80} kg",
                f"Net Payload: {17250 + idx * 35} kg (Within 18,000 kg 32ft MXL Payload & CMVR Rule 93 Axle Envelope)",
                f"NIC E-Way Bill Linked: EWB-27109948{2100 + idx}   |   Security Seal Verified via Gate Camera OCR"
            ],
            "WEIGHBRIDGE CERTIFIED - AXLE COMPLIANT",
            idx % 4 == 0,
        ))

    MM_DIR.mkdir(parents=True, exist_ok=True)
    manifest: List[Dict[str, Any]] = []

    try:
        from PIL import Image, ImageDraw
        pil_ok = True
    except Exception:
        pil_ok = False

    for fname, title, lines, stamp_text, is_exception in docs_spec:
        fpath = MM_DIR / fname
        if pil_ok:
            img = Image.new("RGB", (1180, 620), color=(250, 248, 242))
            draw = ImageDraw.Draw(img)
            # Outer scanned document border
            draw.rectangle([24, 24, 1156, 596], outline=(42, 54, 79), width=3)
            draw.rectangle([34, 34, 1146, 98], fill=(28, 49, 94))
            draw.text((52, 56), f"ITC LIMITED - TM&D ENTERPRISE DOCUMENT ARCHIVE  |  {title}", fill=(255, 255, 255))
            y = 126
            for ln in lines:
                is_err_ln = any(k in ln.upper() for k in ("EXCEPTION", "CRUSHED", "WET", "DUPLICATE", "OVERCHARGE", "PEAK", "REJECT", "DISPUTE"))
                col = (180, 24, 24) if is_err_ln else (28, 35, 45)
                draw.rectangle([48, y - 6, 1132, y + 40], outline=(218, 214, 202), width=1)
                draw.text((62, y + 8), ln, fill=col)
                y += 54
            # Rubber ink stamp box
            stamp_col = (192, 28, 28) if is_exception else (18, 118, 70)
            draw.rectangle([660, 505, 1128, 575], outline=stamp_col, width=3)
            draw.text((678, 532), f"STAMP: {stamp_text}", fill=stamp_col)
            draw.text((52, 548), f"Digital Checksum: SHA256-ITC-{fname.replace('.', '-')}  |  OCR Confidence: 99.4%", fill=(100, 110, 125))
            img.save(fpath, format="PNG", optimize=True)
        else:
            # Minimal valid 1x1 PNG header fallback if PIL missing
            fpath.write_bytes(
                b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde"
                b"\x00\x00\x00\x0cIDATx\x9cc\xf8\xcf\xc0\x00\x00\x03\x01\x01\x00\x18\xdd\x8d\xb0\x00\x00\x00\x00IEND\xaeB`\x82"
            )

        manifest.append({
            "document_filename": fname,
            "document_title": title,
            "stamp_verdict": stamp_text,
            "has_audit_exception": is_exception,
            "extracted_ocr_lines": lines,
            "ocr_confidence_pct": 99.4,
        })

    (MM_DIR / "multimodal_ground_truth_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    return manifest


def main() -> None:
    LAKE_DIR.mkdir(parents=True, exist_ok=True)
    SEEDS_DIR.mkdir(parents=True, exist_ok=True)
    MM_DIR.mkdir(parents=True, exist_ok=True)

    icmls = build_icml_plants()
    cfas = build_cfa_depots()
    skus = build_sku_master()
    wds = build_wholesale_dealers(cfas)
    carriers = build_carriers()

    backbone = {
        "enterprise": "ITC Limited — Fast-Moving Consumer Goods (FMCG) & Trade Marketing & Distribution (TM&D)",
        "generated_at_utc": "2026-11-15T06:30:00Z",
        "currency": "INR (Indian Rupees — Crores & Lakhs)",
        "systems_landscape": [
            "SAP S/4HANA Central ERP (SD, MM, FI-AR, VKM3 Credit, VF01 Billing)",
            "SAP Extended Warehouse Management (EWM) at ICML & Mega CFAs",
            "UNNATI eB2B Retailer Ordering App (~8,00,000+ Kirana Outlets + FinAgg Credit)",
            "Vajra Sales Force Automation (SFA) Field Beat Handhelds",
            "Zenith Primary & Secondary Transport Control Tower",
            "Drishti BLE Multi-Zone Cold-Chain IoT Telemetry",
            "NIC GST e-Invoice (IRN) & E-Way Bill Part-A / Part-B Portal APIs",
            "Google Maps Platform Routes Matrix v2 & WeatherNext 3 Forecasts",
        ],
        "counts": {
            "icml_mega_plants": len(icmls),
            "state_cfa_depots": len(cfas),
            "wholesale_dealers_wds": len(wds),
            "cpg_skus": len(skus),
            "contracted_and_spot_carriers": len(carriers),
        },
        "icml_plants": icmls,
        "cfa_depots": cfas,
        "sku_master": skus,
        "wholesale_dealers": wds,
        "carriers": carriers,
    }

    (SEEDS_DIR / "00_itc_network_backbone.json").write_text(json.dumps(backbone, indent=2), encoding="utf-8")
    (LAKE_DIR / "00_itc_network_backbone.json").write_text(json.dumps(backbone, indent=2), encoding="utf-8")

    table_stats = generate_all_12_tables(icmls, cfas, skus, wds, carriers)
    mm_docs = generate_multimodal_scanned_documents()

    total_rows = sum(s["rows"] for s in table_stats)
    total_mb = round(sum(s["size_mb"] for s in table_stats), 2)
    summary = {
        "total_transactional_rows": total_rows,
        "total_lake_csv_mb": total_mb,
        "multimodal_scanned_documents": len(mm_docs),
        "tables": table_stats,
    }
    (SEEDS_DIR / "lake_manifest.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"ITC TM&D Enterprise Lake Built: {total_rows:,} rows | {total_mb:.2f} MB | {len(mm_docs)} Multimodal PNG Docs")


if __name__ == "__main__":
    main()
