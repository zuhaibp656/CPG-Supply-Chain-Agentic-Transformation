# CPG Supply Chain — Agentic Transformation Portal & 78-Agent Suite

Standalone **Consumer Packaged Goods (CPG)** multi-echelon supply chain transformation portal and 78-agent Google Agent Development Kit (ADK) repository (completely decoupled from the cross-industry original portal).

- **Live Hosted GitHub Pages Website**: https://zuhaibp656.github.io/CPG-Supply-Chain-Agentic-Transformation/
- **GitHub Repository**: https://github.com/zuhaibp656/CPG-Supply-Chain-Agentic-Transformation

---

## Quick Clone & Local Setup

```bash
git clone https://github.com/zuhaibp656/CPG-Supply-Chain-Agentic-Transformation.git
cd CPG-Supply-Chain-Agentic-Transformation

# Optional: Generate the full 235 MB (1.87M-row) INR multi-echelon demo data lake locally
python3 scripts/generate_cpg_demo_lake.py

# Serve the presentation portal locally (opens in Light Theme by default)
python3 -m http.server 8106
# Open http://127.0.0.1:8106/
```

---

## Portal Architecture & 17-Slide Journey (`00` – `16`)

### Stage 1 · Unified Executive Supply Chain Briefing (`index.html`, `pages/00..07`)
- Zero-scroll `100vh` presentation slides (`00` Executive Title Hero → `01` Capital Reality → `02` Six Value Flows → `03` Defense-in-Depth Barrier Model → `04` Velocity vs. Bandwidth Squeeze → `05` The Plug Is an Agent & ERP Coexistence → `06` Uploadable Live Demo Stage → `07` One Agent to Many).

### Stage 2 · 6 Supply Chain Operations Reference (SCOR) Pillars, 24 Sub-Pillars & 60 Personas (`pages/pillar.html`, `personas/`)
- **60 Named CPG Leaders & Multi-Agent Suites** (`personas/index.html`, `personas/dossier.html`, `pages/agent_blueprint.html`): Realistic Indian & international CPG leadership roster across Integrated Consumer Goods Manufacturing & Logistics (ICML) plants, Mother Hubs, Carrying & Forwarding Agent (CFA) depots, General Trade Distributor Management System (DMS), Modern Trade & Quick-Commerce dark stores.
- **4-Lever Indian Rupee (`₹ Crores` & `₹ Lakhs`) Value Model**: **₹2,199.3 Cr/yr** non-double-counted modeled estate impact on a ₹42,000 Cr Cost of Goods Sold (COGS) / ₹68,000 Cr Gross Revenue CPG benchmark.

### Stage 3 · From Personas to Production (`pages/08..15`)
- **`09` · How Agents Are Built (`pages/08_how_agents_are_built.html`)**: Live interactive **No-code** Gemini Enterprise chat, **Low-code** Agent Designer FEFO workflow, and **High-code** Google ADK Python deploy (`gemini-3.1-pro-preview`).
- **`10` · Google Cloud Architecture (`pages/09_agent_architecture.html`)**: 5-lane governed topology across Google Cloud, On-Premises ICML Plant Edge (Google Distributed Cloud), and Multi-Cloud (BigQuery Omni) + live 8-step request trace.
- **`11` · Model Choice (`pages/10_model_choice.html`)**: Interactive 2D Reasoning-Depth vs. Cost-per-Task zone plot across `Gemini 3.1 Pro`, `Gemini 3.8 Flash`, `Gemini Flash-Lite`, and open-weight `Gemma`.
- **`12` · Governance (`pages/11_governance.html`)**: Interactive 8-checkpoint control lane (IAM, Agent Registry, Model Armor, DLP, VPC Service Controls, Apigee MCP, Human Sign-Off, Cloud Audit Logs) + 5 live CPG scenarios.
- **`13` · Where People Meet the Agent (`pages/10_surfaces.html`)**: Interactive 4-surface workbench (Gemini Enterprise chat, Cloud Run Cockpit, embedded inside SAP S/4HANA / WMS, and 05:30 scheduled background flow).
- **`14` · Structural Resilience (`pages/12_structural_resilience.html`)**: Unbraced Point-Solution Silo Stack vs. Fortified 78-Agent CPG Mesh.
- **`15` · Why Google & Gartner (`pages/14_why_google_gartner.html`)**: Animated 6-layer Google Cloud AI stack (`ai_stack_layers.webm`) + 2026 Gartner® Magic Quadrant™ for Enterprise AI Assistants.
- **`16` · 100 Days to Proof of Value (`pages/15_100_days_pov.html`)**: Compounding Value-Over-Time SVG Trajectory Curve to ₹2,199.3 Cr/yr + verified Unilever, GE Appliances, and Home Depot citations (`pages/13_proof_and_cases.html`).

---

## 78 Google ADK Agents & 235 MB Demo Data Lake
- **60 Core Supply Chain Agents + 18 Newly Researched CPG Agents** in `agents/<agent_id>/`.
- **Demo Data Lake (`demo_data/`)**: `demo_data/seeds/` checked into Git for instant clones and cloud packaging; `demo_data/lake_full/` (~235.5 MB, `1,869,300` rows across 8 linked INR CSV/JSONL tables) generated via `python3 scripts/generate_cpg_demo_lake.py`.
- **Priority-0 (`P0`) Gemini Enterprise Queue (`scripts/deploy_p0_agents_to_ge.py` & `data/p0_ge_deployment_queue.json`)**: 25 highest-ROI `<60-day` payback agents staged for Gemini Enterprise deployment (`python3 scripts/deploy_p0_agents_to_ge.py` runs dry-run verification; add `--execute` when ready to deploy).
