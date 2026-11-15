"""Deterministic Python Tools for Territory RTM Morning Pulse Gem (08_territory_rtm_morning_pulse_gem) — ITC Limited CPG Pillars 5 & 6."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

AGENT_DIR = Path(__file__).resolve().parents[1]
SUITE_ROOT = AGENT_DIR.parents[1]
if str(SUITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SUITE_ROOT))

from common.itc_data_loader import (
    format_inr,
    inspect_multimodal_document,
    load_backbone,
    query_domain_table,
    stage_governed_enterprise_action,
)
from common.solvers import SOLVER_REGISTRY
from common.a2ui_and_cockpit import (
    build_a2ui_vega_and_canvas,
    export_verified_csv,
    render_interactive_cockpit_html,
)

AGENT_SLUG = "08_territory_rtm_morning_pulse_gem"
AGENT_ID = "itc_territory_rtm_morning_pulse_gem"
AGENT_NAME = "Territory RTM Morning Pulse Gem"
PERSONA_TITLE = "Area Distribution / RTM Manager"
FUNCTIONAL_AREA = "Channel & Route-to-Market (GT, MT & Q-Commerce)"
BUILD_MODE = "No-Code Gemini Gem"
TARGET_SYSTEM = "ITC Vajra SFA Beat Console & UNNATI eB2B Campaign Broadcast"
STOPS_AT_BOUNDARY = "Advisory No-Code Gemini Gem by design—synthesizes morning beat priorities and drafts WhatsApp/Vajra nudges, never mutating trade scheme budgets or HR attendance records."
PRIMARY_TABLE = "08_unnati_eb2b_vajra_sfa_morning_pulse"


def query_itc_enterprise_records(search_filter: str = "", limit: int = 30) -> Dict[str, Any]:
    """Queries ITC CPG enterprise records for Territory RTM Morning Pulse Gem from the 405 MB TM&D lake (or container seeds)."""
    return query_domain_table(PRIMARY_TABLE, search_filter=search_filter, limit=limit, agent_dir=AGENT_DIR)


def query_itc_master_network_backbone(entity_type: str = "all", search_filter: str = "") -> Dict[str, Any]:
    """Queries ITC Master Backbone: ICML mega-plants, State CFAs, Wholesale Dealers (WDs), SKUs, and Carriers."""
    bb = load_backbone()
    needle = (search_filter or "").strip().lower()
    mapping = {
        "icml": bb.get("icml_plants", []),
        "cfa": bb.get("cfa_depots", []),
        "sku": bb.get("sku_master", []),
        "wd": bb.get("wholesale_dealers", []),
        "carrier": bb.get("carriers", []),
    }
    if entity_type.lower() in mapping:
        items = mapping[entity_type.lower()]
        if needle:
            items = [x for x in items if needle in str(x).lower()]
        return {"entity_type": entity_type, "count": len(items), "records": items[:25]}
    return {"counts": bb.get("counts", {}), "systems_landscape": bb.get("systems_landscape", [])}


def run_deterministic_optimization_solver(search_filter: str = "") -> Dict[str, Any]:
    """Executes the exact deterministic mathematical/OR-Tools/physics solver for Territory RTM Morning Pulse Gem."""
    queried = query_domain_table(PRIMARY_TABLE, search_filter=search_filter, limit=40, agent_dir=AGENT_DIR)
    solver_fn = SOLVER_REGISTRY[AGENT_SLUG]
    result = solver_fn(queried.get("records", []))
    result["agent_id"] = AGENT_ID
    result["agent_name"] = AGENT_NAME
    result["build_mode"] = BUILD_MODE
    result["using_full_enterprise_lake"] = queried.get("using_full_enterprise_lake", False)
    return result


def generate_0730_ase_whatsapp_and_vajra_brief(reference_id: str = "") -> Dict[str, Any]:
    """Synthesizes a crisp, plain-English 07:30 IST Area Sales Executive (ASE) beat action card pairing overnight UNNATI surges with Vajra strike-rate gaps."""
    if AGENT_SLUG in ("03_cold_chain_thermal_auditor", "12_freight_bill_audit_agent"):
        default_doc = "DOC-STRIP-SHP-CLD-70001.png" if "03_" in AGENT_SLUG else "DOC-POD-882910.png"
        doc_name = reference_id if (reference_id and ".png" in reference_id.lower()) else default_doc
        ocr = inspect_multimodal_document(doc_name)
        solved = run_deterministic_optimization_solver("")
        return {
            "tool": "generate_0730_ase_whatsapp_and_vajra_brief",
            "multimodal_vision_verification": ocr,
            "headline_recovery_or_claim": solved.get("overnight_unnati_digital_gmv_display"),
            "top_audited_items": solved.get("morning_territory_briefing", [])[:3],
        }
    solved = run_deterministic_optimization_solver(reference_id)
    return {
        "tool": "generate_0730_ase_whatsapp_and_vajra_brief",
        "reference_filter": reference_id or "ALL_PRIORITY_EXCEPTIONS",
        "headline_impact_inr": solved.get("overnight_unnati_digital_gmv_display"),
        "verified_diagnostics": solved.get("morning_territory_briefing", [])[:4],
        "human_gate_boundary": STOPS_AT_BOUNDARY,
    }


def stage_governed_erp_or_portal_action(
    target_record_id: str,
    proposed_action: str,
    rationale: str = "",
    idempotency_key: str = "",
) -> Dict[str, Any]:
    """Stages a policy-checked write-back to ITC Vajra SFA Beat Console & UNNATI eB2B Campaign Broadcast with idempotency & human sign-off."""
    return stage_governed_enterprise_action(
        agent_id=AGENT_ID,
        target_system=TARGET_SYSTEM,
        action_type=proposed_action,
        target_record_id=target_record_id,
        payload={"proposed_action": proposed_action, "agent_slug": AGENT_SLUG},
        rationale=rationale or f"Deterministic recommendation from {AGENT_NAME}",
        stops_at_boundary=STOPS_AT_BOUNDARY,
        idempotency_key=idempotency_key,
    )


def render_a2ui_visual_chart_and_canvas(search_filter: str = "") -> Dict[str, Any]:
    """Renders A2UI v0.9 visual-only VegaChart card + side-panel RichTable Canvas."""
    solved = run_deterministic_optimization_solver(search_filter)
    rows = solved.get("morning_territory_briefing", [])
    return build_a2ui_vega_and_canvas(
        agent_title=AGENT_NAME,
        subtitle=f"{FUNCTIONAL_AREA} · Headline Impact: {solved.get('overnight_unnati_digital_gmv_display', 'Verified')}",
        rows=rows,
        label_key="territory_name",
        value_key="revenue_at_stake_inr",
        value_title_inr="Verified Impact / Metric (₹ INR)",
    )


def export_atomic_schedule_csv(search_filter: str = "") -> Dict[str, Any]:
    """Exports an atomic RFC-4180 CSV schedule ready for Google Sheets or SAP upload."""
    solved = run_deterministic_optimization_solver(search_filter)
    rows = solved.get("morning_territory_briefing", [])
    out_dir = AGENT_DIR / "artifacts_out"
    return export_verified_csv(AGENT_SLUG, rows, out_dir)


def generate_interactive_html_cockpit(search_filter: str = "") -> Dict[str, Any]:
    """Compiles a self-contained Light-Theme Default Interactive HTML5 Cockpit for Territory RTM Morning Pulse Gem."""
    solved = run_deterministic_optimization_solver(search_filter)
    rows = solved.get("morning_territory_briefing", [])
    out_dir = AGENT_DIR / "artifacts_out"
    return render_interactive_cockpit_html(
        agent_slug=AGENT_SLUG,
        agent_title=AGENT_NAME,
        persona_title=PERSONA_TITLE,
        functional_area=FUNCTIONAL_AREA,
        headline_metric_label="Verified Deterministic Impact",
        headline_metric_value=str(solved.get("overnight_unnati_digital_gmv_display", "₹0")),
        rows=rows,
        output_dir=out_dir,
    )


ALL_TOOLS = [
    query_itc_enterprise_records,
    query_itc_master_network_backbone,
    run_deterministic_optimization_solver,
    generate_0730_ase_whatsapp_and_vajra_brief,
    stage_governed_erp_or_portal_action,
    render_a2ui_visual_chart_and_canvas,
    export_atomic_schedule_csv,
    generate_interactive_html_cockpit,
]
