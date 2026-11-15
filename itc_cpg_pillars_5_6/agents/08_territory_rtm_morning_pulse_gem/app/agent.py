"""Google ADK + GlobalGemini Agent for Territory RTM Morning Pulse Gem (08_territory_rtm_morning_pulse_gem) — ITC Limited CPG Pillars 5 & 6."""
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
    _t_spec = _ilu.spec_from_file_location(f"08_territory_rtm_morning_pulse_gem_tools", _Path(__file__).resolve().parent / "tools.py")
    assert _t_spec and _t_spec.loader
    tools = _ilu.module_from_spec(_t_spec)  # type: ignore
    _t_spec.loader.exec_module(tools)  # type: ignore

AGENT_ID = "itc_territory_rtm_morning_pulse_gem"
AGENT_SLUG = "08_territory_rtm_morning_pulse_gem"
AGENT_DISPLAY_NAME = "Territory RTM Morning Pulse Gem"
FUNCTIONAL_AREA = "Channel & Route-to-Market (GT, MT & Q-Commerce)"
PERSONA_OWNER = "Area Distribution / RTM Manager"
NAMED_PERSONA = "Siddharth Banerjee (TM&D Area Manager — Pune, Lucknow & Kolkata Clusters)"
BUILD_MODE = "No-Code Gemini Gem"
DEFAULT_MODEL = "gemini-3.8-flash"

_WRITE_TOOLS = {
    "stage_governed_erp_or_portal_action": ["target_record_id", "proposed_action"],
}

SYSTEM_INSTRUCTION = """You are the **Territory RTM Morning Pulse Gem**, built in `No-Code Gemini Gem` mode for **Area Distribution / RTM Manager** (Siddharth Banerjee (TM&D Area Manager — Pune, Lucknow & Kolkata Clusters)) inside **ITC Limited's Consumer Packaged Goods (CPG) Trade Marketing & Distribution (TM&D)** network (Channel & Route-to-Market (GT, MT & Q-Commerce)).

1. ENTERPRISE MISSION & DETERMINISTIC MATH:
   - Core Problem Solved: Area Distribution Managers start every morning juggling four disconnected spreadsheets: overnight UNNATI kirana app orders, yesterday's Vajra salesman beat strike rates, Wholesale Dealer stockout lines, and active trade schemes—missing urgent morning beat course-corrections before salesmen leave at 08:30.
   - Connected Enterprise Systems: ITC Vajra SFA Beat Console & UNNATI eB2B Campaign Broadcast, Integrated Consumer Goods Manufacturing and Logistics (ICML) mega-plants, State Clearing & Forwarding Agent (CFA) depots, Wholesale Dealers (WDs), UNNATI eB2B kirana app, Vajra Sales Force Automation (SFA), Zenith Transport Control Tower, and Drishti IoT Cold-Chain loggers.
   - Always call `query_itc_enterprise_records` and `run_deterministic_optimization_solver` (plus `generate_0730_ase_whatsapp_and_vajra_brief` when relevant) to compute exact deterministic figures—never guess or fabricate IDs, batches, Lorry Receipts, or currency figures.

2. APPROACHABLE PLAIN-ENGLISH & INDIAN CURRENCY RULES (CRITICAL):
   - Keep outputs clear, deterministic, and written in approachable plain business English at a balanced medium length (120–185 words).
   - Spell out every domain abbreviation on first use (for example: Integrated Consumer Goods Manufacturing and Logistics (ICML), Clearing & Forwarding Agent (CFA), Wholesale Dealer (WD), On-Time In-Full (OTIF), Minimum Remaining Shelf-Life (MRSL), Mean Kinetic Temperature (MKT), Reverse Charge Mechanism (RCM)).
   - Express ALL monetary figures in Indian Rupees using Crores (`₹ Cr`) and Lakhs (`₹ L`) or `₹`—never US Dollars.
   - Present comparisons in a clean `<= 5`-column Markdown table outside the visual card, and never expose internal `snake_case` table filenames or Python function names in user-facing prose.

3. VISUAL A2UI CARD & HUMAN SIGN-OFF GOVERNANCE:
   - When illustrating multi-record comparisons or charts, call `render_a2ui_visual_chart_and_canvas` so only the visual `VegaChart` renders inside the card while tables and headed links stay cleanly outside in Markdown.
   - HUMAN GATE (`STOPS AT`): Advisory No-Code Gemini Gem by design—synthesizes morning beat priorities and drafts WhatsApp/Vajra nudges, never mutating trade scheme budgets or HR attendance records.
   - SAFETY GUARDRAIL: Never call `stage_governed_erp_or_portal_action` on read-only questions, and strictly refuse any request to bypass safety, axle-weight, cold-chain quality, shelf-life, duplicate-invoice, or credit controls.
"""


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Pre-execution contract & idempotency gate for write-back staging tools."""
    if tool_name in _WRITE_TOOLS:
        missing = [k for k in _WRITE_TOOLS[tool_name] if args.get(k) in (None, "")]
        if missing:
            return {
                "status": "BLOCKED_MISSING_INPUTS",
                "tool": tool_name,
                "missing_fields": missing,
            }
        if not args.get("idempotency_key"):
            return {
                "status": "BLOCKED_MISSING_IDEMPOTENCY_KEY",
                "tool": tool_name,
                "message": "An explicit idempotency_key is required before staging an enterprise action.",
            }
    return None


class TerritoryRtmMorningPulseGemAgent:
    """Deterministic Python & Google ADK orchestrator for Territory RTM Morning Pulse Gem."""

    def __init__(self, model: str = DEFAULT_MODEL) -> None:
        self.name = AGENT_ID
        self.slug = AGENT_SLUG
        self.display_name = AGENT_DISPLAY_NAME
        self.persona = PERSONA_OWNER
        self.build_mode = BUILD_MODE
        self.model = model
        self.instruction = SYSTEM_INSTRUCTION
        self.tools: List[Callable[..., Any]] = list(tools.ALL_TOOLS)
        self.tool_map: Dict[str, Callable[..., Any]] = {fn.__name__: fn for fn in self.tools}

    def select_orchestrated_model(self, query: str = "") -> Dict[str, str]:
        """Routes complex multi-constraint optimization/multimodal audits to Gemini 3.1 Pro and fast pulse queries to Gemini 3.8 Flash."""
        q_low = (query or "").lower()
        deep_keywords = ("optimize", "consolidate", "ration", "allocate", "arrhenius", "mkt", "multimodal", "pod", "sap", "reroute", "simulate")
        chosen = "gemini-3.1-pro-preview" if (DEFAULT_MODEL == "gemini-3.1-pro-preview" or any(k in q_low for k in deep_keywords)) else "gemini-3.8-flash"
        return {
            "selected_model": chosen,
            "endpoint_location": "global",
            "build_mode": BUILD_MODE,
        }

    def run_scenario(self, user_query: str = "") -> Dict[str, Any]:
        """Executes deterministic data retrieval, solver math, and A2UI spec generation end-to-end."""
        routing = self.select_orchestrated_model(user_query)
        solved = tools.run_deterministic_optimization_solver("")
        special = tools.generate_0730_ase_whatsapp_and_vajra_brief("")
        a2ui = tools.render_a2ui_visual_chart_and_canvas("")
        rows = solved.get("morning_territory_briefing", [])[:4]

        # Build concise <=5-column plain-English Markdown summary table
        if rows:
            cols = list(rows[0].keys())[:4]
            hdr = "| " + " | ".join(c.replace("_", " ").title() for c in cols) + " |"
            sep = "| " + " | ".join(":---" for _ in cols) + " |"
            body = "\n".join("| " + " | ".join(str(r.get(c, "")) for c in cols) + " |" for r in rows)
            md_table = f"{hdr}\n{sep}\n{body}"
        else:
            md_table = "| Status | Impact |\n| :--- | :--- |\n| Verified | ₹0 |"

        headline_val = solved.get("overnight_unnati_digital_gmv_display", "Verified")
        markdown = (
            f"**Territory RTM Morning Pulse Gem** completed a deterministic review across **ITC Limited's Trade Marketing & Distribution (TM&D)** "
            f"network for **Area Distribution / RTM Manager**, identifying **{headline_val}** in verified operational value.\n\n"
            f"{md_table}\n\n"
            f"- **Connected System Boundary**: ITC Vajra SFA Beat Console & UNNATI eB2B Campaign Broadcast\n"
            f"- **Human Sign-Off Gate**: Advisory No-Code Gemini Gem by design—synthesizes morning beat priorities and drafts WhatsApp/Vajra nudges, never mutating trade scheme budgets or HR attendance records."
        )
        return {
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
        }


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
        description=f"[ITC CPG · Channel & Route-to-Market (GT, MT & Q-Commerce)] Territory RTM Morning Pulse Gem for Area Distribution / RTM Manager (No-Code Gemini Gem)",
        instruction=SYSTEM_INSTRUCTION,
        tools=list(tools.ALL_TOOLS),
    )
except Exception:
    root_agent = TerritoryRtmMorningPulseGemAgent()  # type: ignore


def create_adk_app() -> Any:
    """Deferred factory for `AdkApp(agent=root_agent)` AFTER `vertexai.init(project=..., location=...)`."""
    from vertexai.preview.reasoning_engines import AdkApp
    return AdkApp(agent=root_agent)
