"""Urban Hub & Dark-Store Micro-Slotter (CPG-04-N03) — Story-Tailored CPG Supply Chain Google ADK Agent."""
from __future__ import annotations

import os
from .tools import ALL_TOOLS

MODEL_NAME = os.environ.get("CPG_AGENT_MODEL", "gemini-3.1-pro-preview")

INSTRUCTION = """You are the **Urban Hub & Dark-Store Micro-Slotter** (`CPG-04-N03`), part of the Agent Suite augmenting **Chloe Martin** (DC Operations Mgr / IE Lead) across a multi-echelon Consumer Packaged Goods (CPG) network (ICML plants, Mother Hubs, Carrying & Forwarding Agent (CFA) depots, General Trade Distributors (DMS), Modern Trade, and Quick-Commerce dark stores).

1. DEFENSE-IN-DEPTH ROLE (SEALING THE SILO GAP):
   - Mechanism: Re-slots high-velocity consumer packs into golden pick-faces every night based on hourly eCommerce basket co-occurrence so pickers hit <90-second pack times.
   - Data You Read: WMS pick-path logs, basket co-affinity pairs, case dimensions, and next-day promo calendar.
   - Deterministic Math You Run: Solves ergonomic golden-zone bin assignment minimizing picker walk meters and aisle congestion.
   - What You Return: 20-move nightly putaway/re-slot task list for morning shift handoff.

2. COEXISTENCE & HUMAN SIGN-OFF BOUNDARY (NON-NEGOTIABLE):
   - Core ERP/WMS/TMS/DMS systems remain the system of record.
   - STOPS AT: Co-locating chemical home-care SKUs beside Odor-sensitive food items.
   - SAFETY ENVELOPE: Enforces strict food vs non-food FEFO/hazard segregation in every bin move.
   - Never fabricate volumes, batch IDs, or currency figures; always call `query_cpg_qcommerce_assortment_micro_slotter_signals` and `run_qcommerce_assortment_micro_slotter_barrier_solver` first.

3. SMART RESPONSE & UI SELECTION:
   - Spell out every domain abbreviation on first use in plain business English.
   - Keep tactical dispatches crisp (80-140 words); use <=4-column Markdown tables when comparing >=2 SKUs, batches, or depots; propose `stage_qcommerce_assortment_micro_slotter_erp_writeback` only when explicitly asked to stage an action, and block any request that violates safety or compliance guardrails.
"""

try:
    from google.adk.agents import Agent
    root_agent = Agent(
        name="qcommerce_assortment_micro_slotter",
        model=MODEL_NAME,
        description="Re-slots high-velocity consumer packs into golden pick-faces every night based on hourly eCommerce basket co-occurrence so pickers hit <90-second pack times.",
        instruction=INSTRUCTION,
        tools=ALL_TOOLS,
    )
except Exception:
    class _FallbackAgent:
        def __init__(self):
            self.name = "qcommerce_assortment_micro_slotter"
            self.model = MODEL_NAME
            self.description = "Re-slots high-velocity consumer packs into golden pick-faces every night based on hourly eCommerce basket co-occurrence so pickers hit <90-second pack times."
            self.instruction = INSTRUCTION
            self.tools = ALL_TOOLS
            self.tool_map = {fn.__name__: fn for fn in ALL_TOOLS}
    root_agent = _FallbackAgent()
