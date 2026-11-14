# CPG Supply Chain — Agentic Transformation Portal & 78-Agent Suite

Standalone Consumer Packaged Goods (CPG) multi-echelon supply chain transformation repository (decoupled from the cross-industry original portal).

## Architecture & Contents
- **25-Minute Presentation Briefing (`index.html`, `pages/00..07`)**: Zero-scroll `100vh` presentation slides tracing Capital Reality → Six Value Flows → Defense-in-Depth Barrier Model → Velocity Squeeze → The AI Plug & ERP Coexistence → Uploadable Live Demo Stage → One Agent to Many.
- **60 Named CPG Leaders & Multi-Agent Suites (`personas/index.html`, `personas/dossier.html`)**: 60 CPG personas (realistic Indian & international leadership roster across ICML plants, Mother Hubs, Carrying & Forwarding Agent (CFA) depots, General Trade DMS, Modern Trade & Quick-Commerce) paired with their **2-to-4 Agent Suites** (`Reads`, `Does`, `Returns`, `Stops At`, `Safety Envelope`) and 4-lever non-double-counted financial value model.
- **78 Google ADK CPG Agents (`agents/<agent_id>/`)**:
  - **60 Core Supply Chain Agents** (preserved by ID/name, re-architected around CPG multi-echelon barriers & human sign-off gates).
  - **18 Newly Researched CPG Agents** covering Quick-Commerce 10-min dark-store sensing, Festival & Monsoon surge planning, RGM Price-Pack architecture, Farm-Gate Mandi commodity procurement, Packaging Artwork & Allergen compliance, Supplier Dynamic Discounting, Plant Tariff Peak-Shaving, Co-Packer Laminate Scrap auditing, 2-Hour Lot Genealogy & Recall tracing, Dynamic FEFO MRSL shelf-life allocation, DMS Stockist Secondary Balancing, Urban Micro-Slotting, E-Way Bill Transit Tax shielding, Modern Trade Dock Slot booking, Rural Van Beat Load optimization, Cold-Chain MKT Salvage, Grey-Market Diversion sensing, and EPR Plastic Credit reconciliation.
- **234 MB Multi-Echelon CPG Demo Data Lake (`demo_data/`)**:
  - `demo_data/lake_full/` (~234 MB, `1,869,300` rows across 8 linked CSV/JSONL tables) on local disk, reproducible anytime via `python3 scripts/generate_cpg_demo_lake.py`.
  - `demo_data/seeds/` checked into Git for lightweight cloud packaging.
- **Priority-0 (`P0`) Gemini Enterprise Queue (`scripts/deploy_p0_agents_to_ge.py` & `data/p0_ge_deployment_queue.json`)**: 25 highest-ROI `<60-day` payback agents staged for Gemini Enterprise deployment (`python3 scripts/deploy_p0_agents_to_ge.py` runs dry-run verification; add `--execute` when ready to deploy).
