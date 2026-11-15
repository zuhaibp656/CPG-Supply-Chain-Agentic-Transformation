"""Google ADK + GlobalGemini Agent for Freight Bill Audit Agent (ITC TMD)."""
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
    _t_spec = _ilu.spec_from_file_location(f"12_freight_bill_audit_agent_tools", _here / "tools.py")
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

AGENT_ID = "itc_freight_bill_audit_agent"
AGENT_SLUG = "12_freight_bill_audit_agent"
AGENT_DISPLAY_NAME = "Freight Bill Audit Agent (ITC TMD)"
SHORT_LABEL = "Freight Bill Audit Agent"
FUNCTIONAL_AREA = "Fleet, Carrier & Freight Governance"
PERSONA_OWNER = "Freight Bill & Claims Controller"
NAMED_PERSONA = "Subhashish Mukherjee (National Freight Audit & Commercial Claims Controller — Kolkata)"
BUILD_MODE = "Multimodal + Agent Studio"
DEFAULT_MODEL = "gemini-3.1-pro-preview"

_WRITE_TOOLS = {
    "stage_governed_erp_or_portal_action": ["target_record_id", "proposed_action"],
}

SYSTEM_INSTRUCTION = """You are **Freight Bill Audit Agent (ITC TMD)**, built in `Multimodal + Agent Studio` mode for **Freight Bill & Claims Controller** (Subhashish Mukherjee (National Freight Audit & Commercial Claims Controller — Kolkata)) across **ITC Limited's Consumer Packaged Goods (CPG) Trade Marketing & Distribution (TM&D)** network (Fleet, Carrier & Freight Governance).

1. AUTONOMOUS DATA, SOLVER & VISUAL INTELLIGENCE (NO TECHNICAL PROMPTS NEEDED FROM USERS):
   - Users ask everyday operational questions in plain English—they will NEVER ask you to "make an A2UI chart", "build an HTML cockpit", or cite internal table/tool names.
   - On EVERY analytical, operational, or audit question, proactively call `run_deterministic_optimization_solver` (and `audit_multimodal_lr_pod_and_carrier_invoice` when checking physics, batch rules, portal slots, credit headroom, or scanned documents) so your answer is 100% grounded in deterministic math and our visual A2UI charts (bar charts, donut share charts, thermal traces) + interactive workbench render automatically!
   - Core Problem You Solve: Indian CPG freight settlement requires reconciling paper-heavy Lorry Receipts (Bilty), rubber-stamped CFA Proof-of-Delivery (POD) slips with handwritten wet/crushed carton remarks, contracted diesel escalation pegs, and GPS-verified gate detention hours.

2. CLEAR, BALANCED PLAIN-ENGLISH & INDIAN CURRENCY (`₹ Cr` / `₹ L`) STYLE:
   - Write in clear, approachable business English at a balanced medium length (130–195 words).
   - Spell out every domain abbreviation on first use (for example: Integrated Consumer Goods Manufacturing and Logistics (ICML), Clearing & Forwarding Agent (CFA), Wholesale Dealer (WD), On-Time In-Full (OTIF), Minimum Remaining Shelf-Life (MRSL), Mean Kinetic Temperature (MKT)).
   - Express ALL monetary figures in Indian Rupees using Crores (`₹ Cr`) and Lakhs (`₹ L`) or `₹`—never US Dollars.
   - Include ONE crisp, copy-ready Markdown table (`<= 5` columns) outside the visual card summarizing the top prioritized items, followed by 2–3 concrete recommended next steps.
   - Never mention internal JSON/CSV filenames, `snake_case` column names, or Python function names in your user-facing response.

3. HUMAN SIGN-OFF BOUNDARY & SAFETY GUARDRAILS:
   - Connected Enterprise System: SAP S/4HANA FI-AP (`MIRO` / `FB60` Short-Pay Voucher & GST RCM Ledger) + Carrier Dispute Portal
   - STOPS AT: Never releases bank NEFT/RTGS payouts or posts final carrier debit notes without Freight Bill Controller sign-off; blocks 100% of duplicate Lorry Receipt claims.
   - Never invoke `stage_governed_erp_or_portal_action` on read-only diagnostic questions. When the user asks to prepare, hold, reassign, block, or stage an action, generate a clean `idempotency_key` (e.g. `ITC-12-STAGE-001`), call `stage_governed_erp_or_portal_action`, and confirm the staged voucher awaiting human sign-off.
   - Strictly refuse any request to bypass safety, axle-weight, cold-chain quality, shelf-life, duplicate-invoice, or overdue credit controls.
"""


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Pre-execution contract & idempotency gate for write-back staging tools."""
    if tool_name in _WRITE_TOOLS:
        missing = [k for k in _WRITE_TOOLS[tool_name] if args.get(k) in (None, "")]
        if missing:
            return {"status": "BLOCKED_MISSING_INPUTS", "tool": tool_name, "missing_fields": missing}
        if not args.get("idempotency_key"):
            return {
                "status": "BLOCKED_MISSING_IDEMPOTENCY_KEY",
                "tool": tool_name,
                "message": "An explicit idempotency_key is required before staging an enterprise action.",
            }
    return None


class ItcFreightBillAuditAgent:
    """Deterministic Python orchestrator for Freight Bill Audit Agent (ITC TMD)."""

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
        q_low = (query or "").lower()
        deep_keywords = ("optimize", "consolidate", "ration", "allocate", "arrhenius", "mkt", "multimodal", "pod", "sap", "reroute", "simulate")
        chosen = "gemini-3.1-pro-preview" if (DEFAULT_MODEL == "gemini-3.1-pro-preview" or any(k in q_low for k in deep_keywords)) else "gemini-3.8-flash"
        return {"selected_model": chosen, "endpoint_location": "global", "build_mode": BUILD_MODE}

    def run_scenario(self, user_query: str = "") -> Dict[str, Any]:
        tools.reset_turn_state(user_query)
        routing = self.select_orchestrated_model(user_query)
        solved = tools.run_deterministic_optimization_solver("")
        special = tools.audit_multimodal_lr_pod_and_carrier_invoice("")
        a2ui = tools.render_a2ui_visual_chart_and_canvas("")
        rows = solved.get("freight_audit_vouchers", [])[:4]

        if rows:
            cols = list(rows[0].keys())[:4]
            hdr = "| " + " | ".join(c.replace("_", " ").title() for c in cols) + " |"
            sep = "| " + " | ".join(":---" for _ in cols) + " |"
            body = "\n".join("| " + " | ".join(str(r.get(c, "")) for c in cols) + " |" for r in rows)
            md_table = f"{hdr}\n{sep}\n{body}"
        else:
            md_table = "| Status | Impact |\n| :--- | :--- |\n| Verified | ₹0 |"

        headline_val = solved.get("total_recovered_display", "Verified")
        markdown = (
            f"**Freight Bill Audit Agent (ITC TMD)** completed a deterministic review across **ITC Limited's Trade Marketing & Distribution (TM&D)** "
            f"network for **Freight Bill & Claims Controller**, identifying **{headline_val}** in verified operational value.\n\n"
            f"{md_table}\n\n"
            f"- **Connected System Boundary**: SAP S/4HANA FI-AP (`MIRO` / `FB60` Short-Pay Voucher & GST RCM Ledger) + Carrier Dispute Portal\n"
            f"- **Human Sign-Off Gate**: Never releases bank NEFT/RTGS payouts or posts final carrier debit notes without Freight Bill Controller sign-off; blocks 100% of duplicate Lorry Receipt claims."
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
    from google.adk.agents.callback_context import CallbackContext
    from google.adk.apps import App
    from google.adk.models import Gemini
    from google.adk.models.llm_request import LlmRequest
    from google.adk.models.llm_response import LlmResponse
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

            if st.get("active") and st.get("rows") and "itc_tmd/cockpits/" not in existing_txt:
                urls = publish_cockpit_and_csv(
                    agent_slug=AGENT_SLUG,
                    agent_title=SHORT_LABEL,
                    persona_title=PERSONA_OWNER,
                    functional_area=FUNCTIONAL_AREA,
                    headline_value=str(st.get("headline") or "Verified"),
                    rows=list(st.get("rows") or []),
                    label_key="freight_invoice_id",
                    value_key="overcharge_and_pod_recovery_inr",
                )
                bullets = [
                    f"- 🌐 **[Open Interactive Visual Workbench & Simulator (Light/Dark HTML) ↗]({urls['html_url']})** — Live bar & donut breakdowns, What-If slider, and filterable ITC ledger.",
                    f"- 📥 **[Download Atomic Schedule for Google Sheets / SAP (CSV) ↗]({urls['csv_url']})** — Verified row-level export.",
                ]
                if st.get("doc_url"):
                    bullets.insert(
                        0,
                        f"- 🖼️ **[Inspect Scanned Document Evidence ({st.get('doc_label', 'PNG Scan')}) ↗]({st['doc_url']})** — High-resolution multimodal document scan.",
                    )
                nl = chr(10)
                footer = f"{nl}{nl}### 🌐 Interactive Visual Workbench & Evidence{nl}{nl}" + nl.join(bullets) + nl
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
            sid = f"itc-{uuid.uuid4().hex[:8]}"
            rows = list(st.get("rows") or [])
            banner = f"{len(rows)} verified ITC TM&D records · Headline Impact: {st.get('headline', 'Verified')}"
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
        description=f"[ITC TMD · Fleet, Carrier & Freight Governance] Freight Bill Audit Agent (Freight Bill & Claims Controller)",
        instruction=SYSTEM_INSTRUCTION,
        tools=list(tools.ALL_TOOLS),
        before_model_callback=_before_model_cb,
        after_model_callback=_after_model_cb,
        after_agent_callback=_after_agent_cb,
    )

    app = App(root_agent=root_agent, name=AGENT_ID)

    class ItcFreightBillAuditAdkApp(AdkApp):
        """Vertex AI Agent Engine wrapper for Freight Bill Audit Agent (ITC TMD)."""

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
    root_agent = ItcFreightBillAuditAgent()  # type: ignore
    app = None  # type: ignore
    ItcFreightBillAuditAdkApp = None  # type: ignore
