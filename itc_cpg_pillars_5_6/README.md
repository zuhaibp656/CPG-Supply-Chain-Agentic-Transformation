# ITC Limited CPG — Pillars 5 & 6 Agent Suite (`itc_cpg_pillars_5_6/`)

Standalone, production-grade **ITC Limited Consumer Packaged Goods (CPG) Trade Marketing & Distribution (TM&D)** agent suite covering **12 specialized Distribution, CFA, Channel Route-to-Market, and Freight Governance Agents** paired with a **405 MB (`1.60M`-row) multi-table + 24-document multimodal enterprise demo data lake**.

- **Research & Reuse Provenance**: See [`RESEARCH_AND_REUSE_MATRIX.md`](./RESEARCH_AND_REUSE_MATRIX.md)
- **Models (`GlobalGemini`, `location="global"`)**: `gemini-3.1-pro-preview` (10 multi-constraint solver & multimodal agents) and `gemini-3.8-flash` (2 sub-2-second No-Code Gemini Gems)
- **Website & Cloud Isolation**: Cleanly isolated in `itc_cpg_pillars_5_6/` (not displayed on the base website yet; staged for Gemini Enterprise testing via `scripts/deploy_itc_agents_to_ge.py`).

## Quick Verification Commands

```bash
# 1. Regenerate the full 405 MB (1.60M-row) ITC TM&D lake + 24 scanned PNG docs locally
.venv/bin/python itc_cpg_pillars_5_6/scripts/generate_itc_tmd_enterprise_lake.py

# 2. Run all 84 pytest unit, solver, multimodal OCR, idempotency & safety-gate tests across all 12 agents
.venv/bin/pytest itc_cpg_pillars_5_6/agents -q

# 3. Validate Gemini Enterprise deployment readiness (safe dry-run; does not push live)
.venv/bin/python itc_cpg_pillars_5_6/scripts/deploy_itc_agents_to_ge.py
```
