"""Hermetic Deterministic Python & Multimodal Tools for Predictive WD Reorder & Dispatch Agent (ITC TMD)."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from .itc_runtime.itc_data_loader import (
        inspect_multimodal_document,
        load_backbone,
        query_domain_table,
        resolve_multimodal_png_path,
        stage_governed_enterprise_action,
    )
    from .itc_runtime.solvers import SOLVER_REGISTRY
    from .itc_runtime.a2ui_wire import build_autonomous_2panel_vegalite
    from .itc_runtime.gcs_publisher import publish_cockpit_and_csv, publish_multimodal_doc_image
except ImportError:
    from itc_runtime.itc_data_loader import (  # type: ignore
        inspect_multimodal_document,
        load_backbone,
        query_domain_table,
        resolve_multimodal_png_path,
        stage_governed_enterprise_action,
    )
    from itc_runtime.solvers import SOLVER_REGISTRY  # type: ignore
    from itc_runtime.a2ui_wire import build_autonomous_2panel_vegalite  # type: ignore
    from itc_runtime.gcs_publisher import publish_cockpit_and_csv, publish_multimodal_doc_image  # type: ignore

AGENT_SLUG = "09_predictive_wd_reorder_dispatch_agent"
AGENT_ID = "itc_predictive_wd_reorder_dispatch_agent"
AGENT_NAME = "Predictive WD Reorder & Dispatch Agent"
GE_DISPLAY_NAME = "Predictive WD Reorder & Dispatch Agent (ITC TMD)"
PERSONA_TITLE = "Wholesale Dealer (WD) / Stockist Ops Mgr"
FUNCTIONAL_AREA = "Channel & Route-to-Market (GT, MT & Q-Commerce)"
BUILD_MODE = "Google ADK + Python Solvers"
TARGET_SYSTEM = "ITC Distribution Management System (DMS) -> SAP S/4HANA Primary Sales Order (`VA01`) & FinAgg Credit API"
STOPS_AT_BOUNDARY = "Never converts draft primary orders into firm SAP billing without Wholesale Dealer OTP/portal consent or FinAgg/bank credit-line confirmation."
PRIMARY_TABLE = "09_wd_stockist_doi_credit_and_reorders"

_TURN_STATE: Dict[str, Any] = {
    "active": False,
    "user_query": "",
    "vega_spec": None,
    "rows": [],
    "headline": "",
    "doc_url": "",
    "doc_label": "",
}


def _agent_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _format_inr(amount_inr: float) -> str:
    val = float(amount_inr or 0.0)
    sign = "-" if val < 0 else ""
    av = abs(val)
    if av >= 10_000_000.0:
        return f"{sign}₹{av / 10_000_000.0:.2f} Cr"
    if av >= 100_000.0:
        return f"{sign}₹{av / 100_000.0:.2f} L"
    return f"{sign}₹{av:,.0f}"


def reset_turn_state(user_query: str = "") -> None:
    _TURN_STATE["active"] = False
    _TURN_STATE["user_query"] = user_query
    _TURN_STATE["vega_spec"] = None
    _TURN_STATE["rows"] = []
    _TURN_STATE["headline"] = ""
    _TURN_STATE["doc_url"] = ""
    _TURN_STATE["doc_label"] = ""


def get_turn_state() -> Dict[str, Any]:
    return dict(_TURN_STATE)


def _record_visual_context(solved: Dict[str, Any], override_rows: Optional[List[Dict[str, Any]]] = None, override_headline: str = "") -> None:
    rows = list(override_rows if override_rows is not None else (solved.get("wd_dispatch_recommendations", []) or []))
    headline = override_headline or str(solved.get("total_auto_replenishment_billing_display", "Verified"))
    spec = build_autonomous_2panel_vegalite(
        agent_slug=AGENT_SLUG,
        agent_title=AGENT_NAME,
        subtitle=f"{FUNCTIONAL_AREA} · Verified Impact: {headline}",
        rows=rows,
        label_key="wd_name",
        value_key="order_billing_value_inr",
        value_title="Impact / Metric (₹ INR)",
        user_query=str(_TURN_STATE.get("user_query", "")),
    )
    _TURN_STATE["active"] = True
    _TURN_STATE["rows"] = rows
    _TURN_STATE["headline"] = headline
    _TURN_STATE["vega_spec"] = spec


def query_itc_enterprise_records(search_filter: str = "", limit: int = 30) -> Dict[str, Any]:
    """Queries ITC Limited TM&D operational records for Predictive WD Reorder & Dispatch Agent with flexible keyword matching."""
    res = query_domain_table(PRIMARY_TABLE, search_filter=search_filter, limit=limit, agent_dir=_agent_root())
    if res.get("records") and not _TURN_STATE.get("active"):
        solved = SOLVER_REGISTRY[AGENT_SLUG](res["records"])
        _record_visual_context(solved)
    return res


def query_itc_master_network_backbone(entity_type: str = "all", search_filter: str = "") -> Dict[str, Any]:
    """Queries ITC Master Network Backbone: ICML mega-plants, State CFAs, Wholesale Dealers (WDs), SKUs, and Carriers."""
    bb = load_backbone(agent_dir=_agent_root())
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
    """Executes the deterministic mathematical / OR-Tools / physics solver for Predictive WD Reorder & Dispatch Agent."""
    queried = query_domain_table(PRIMARY_TABLE, search_filter=search_filter, limit=40, agent_dir=_agent_root())
    solver_fn = SOLVER_REGISTRY[AGENT_SLUG]
    result = solver_fn(queried.get("records", []))
    result["agent_id"] = AGENT_ID
    result["agent_name"] = AGENT_NAME
    result["build_mode"] = BUILD_MODE
    result["using_full_enterprise_lake"] = queried.get("using_full_enterprise_lake", False)
    _record_visual_context(result)
    return result


def verify_finagg_credit_and_godown_cube_fit(reference_id: str = "") -> Dict[str, Any]:
    """Checks each Wholesale Dealer's open credit limit, FinAgg/SBI dealer-finance drawdown eligibility, and physical godown case capacity before staging primary SAP replenishment."""
    solved = run_deterministic_optimization_solver(reference_id)
    rows = solved.get("wd_dispatch_recommendations", [])
    flagged = [r for r in rows if any(k in str(r).upper() for k in ("RISK", "HOLD", "BLOCK", "BREACH", "SPOT", "REJECT", "SWAP", "CRITICAL"))] or rows
    return {
        "tool": "verify_finagg_credit_and_godown_cube_fit",
        "reference_filter": reference_id or "ALL_PRIORITY_EXCEPTIONS",
        "headline_impact_inr": solved.get("total_auto_replenishment_billing_display"),
        "exception_count": len(flagged),
        "verified_diagnostics": flagged[:5],
        "human_gate_boundary": STOPS_AT_BOUNDARY,
    }


def simulate_what_if_scenario(adjustment_pct: int = 120, focus_filter: str = "") -> Dict[str, Any]:
    """Simulates a live operational what-if scenario (volume surge, stock shortage, rate shift, or capacity reallocation)."""
    solved = run_deterministic_optimization_solver(focus_filter)
    base_rows = list(solved.get("wd_dispatch_recommendations", []) or [])
    if -50 <= adjustment_pct <= 50 and adjustment_pct != 0:
        factor = round(1.0 + (adjustment_pct / 100.0), 4)
        delta_pct = float(adjustment_pct)
    else:
        factor = round(max(0.25, adjustment_pct / 100.0), 4)
        delta_pct = round((factor - 1.0) * 100.0, 1)

    sim_rows: List[Dict[str, Any]] = []
    base_total = 0.0
    sim_total = 0.0
    for r in base_rows:
        rc = dict(r)
        try:
            bv = float(rc.get("order_billing_value_inr", 0.0) or 0.0)
        except Exception:
            bv = 0.0
        sv = round(bv * factor, 2)
        base_total += bv
        sim_total += sv
        rc["order_billing_value_inr"] = sv
        rc["baseline_value_inr"] = round(bv, 2)
        rc["scenario_delta_inr"] = round(sv - bv, 2)
        sim_rows.append(rc)

    sim_headline = _format_inr(sim_total) if sim_total else str(solved.get("total_auto_replenishment_billing_display", "Verified"))
    _record_visual_context(solved, override_rows=sim_rows, override_headline=sim_headline)
    return {
        "status": "SCENARIO_SIMULATED",
        "focus_filter": focus_filter or "FULL_PORTFOLIO",
        "adjustment_factor": factor,
        "scenario_delta_pct": delta_pct,
        "baseline_impact_inr": round(base_total, 2),
        "baseline_impact_display": _format_inr(base_total),
        "simulated_impact_inr": round(sim_total, 2),
        "simulated_impact_display": sim_headline,
        "net_change_display": _format_inr(sim_total - base_total),
        "top_simulated_items": sim_rows[:5],
        "human_gate_boundary": STOPS_AT_BOUNDARY,
    }


def draft_executive_stakeholder_brief(focus_filter: str = "", include_hindi_vernacular: bool = False) -> Dict[str, Any]:
    """Drafts an escalation, transporter dispute, or field-beat morning brief (optionally bilingual Hindi + English)."""
    solved = run_deterministic_optimization_solver(focus_filter)
    rows = list(solved.get("wd_dispatch_recommendations", []) or [])[:4]
    headline = str(solved.get("total_auto_replenishment_billing_display", "Verified"))
    action_lines = [
        f"{idx + 1}. {r.get('wd_name', 'Item')}: {_format_inr(float(r.get('order_billing_value_inr', 0.0) or 0.0))}"
        for idx, r in enumerate(rows)
    ]
    hindi_note = ""
    if include_hindi_vernacular:
        hindi_note = (
            f"Namaste Team — Aaj ke {AGENT_NAME} review mein {len(rows)} mukhya priority items ({headline} impact) chune gaye hain. "
            f"Kripya top priority dispatches aur approval gate par turant action lein: " + "; ".join(action_lines[:3])
        )
    return {
        "status": "STAKEHOLDER_BRIEF_READY",
        "agent_name": AGENT_NAME,
        "persona_owner": PERSONA_TITLE,
        "headline_value_display": headline,
        "priority_actions": action_lines,
        "vernacular_hindi_summary": hindi_note or None,
        "approval_gate": STOPS_AT_BOUNDARY,
    }


def stage_governed_erp_or_portal_action(
    target_record_id: str,
    proposed_action: str,
    rationale: str = "",
    idempotency_key: str = "",
) -> Dict[str, Any]:
    """Stages a policy-checked write-back to ITC Distribution Management System (DMS) -> SAP S/4HANA Primary Sales Order (`VA01`) & FinAgg Credit API with idempotency & human sign-off."""
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
    """Prepares the autonomous 2-Panel Vega-Lite v5 visual card (Bar/Grouped/Line + Donut) and Looker RichTable Canvas."""
    solved = run_deterministic_optimization_solver(search_filter)
    return {
        "a2ui_version": "0.9",
        "card_component": "VegaChart",
        "text_inside_card": False,
        "vega_lite_spec": _TURN_STATE["vega_spec"],
        "row_count": len(_TURN_STATE["rows"]),
        "headline_impact": solved.get("total_auto_replenishment_billing_display"),
    }


def export_atomic_schedule_csv(search_filter: str = "") -> Dict[str, Any]:
    """Exports an atomic RFC-4180 CSV schedule to local disk and Cloud Storage for Google Sheets / SAP."""
    if not _TURN_STATE.get("rows"):
        run_deterministic_optimization_solver(search_filter)
    local_out = Path("/tmp") / "itc_tmd_artifacts" / AGENT_SLUG
    urls = publish_cockpit_and_csv(
        agent_slug=AGENT_SLUG,
        agent_title=AGENT_NAME,
        persona_title=PERSONA_TITLE,
        functional_area=FUNCTIONAL_AREA,
        headline_value=str(_TURN_STATE.get("headline") or "Verified"),
        rows=list(_TURN_STATE.get("rows") or []),
        label_key="wd_name",
        value_key="order_billing_value_inr",
        doc_url=str(_TURN_STATE.get("doc_url") or ""),
        doc_label=str(_TURN_STATE.get("doc_label") or ""),
        local_dir=local_out,
    )
    return {
        "status": "CSV_EXPORT_READY",
        "csv_path": str(local_out / f"{AGENT_SLUG}_verified_schedule.csv"),
        "csv_download_url": urls["csv_url"],
        "row_count": len(_TURN_STATE.get("rows") or []),
    }


def generate_interactive_html_cockpit(search_filter: str = "") -> Dict[str, Any]:
    """Compiles & publishes the Light-Theme Default 3-Tab Executive HTML5 Control Tower Cockpit."""
    if not _TURN_STATE.get("rows"):
        run_deterministic_optimization_solver(search_filter)
    local_out = Path("/tmp") / "itc_tmd_artifacts" / AGENT_SLUG
    urls = publish_cockpit_and_csv(
        agent_slug=AGENT_SLUG,
        agent_title=AGENT_NAME,
        persona_title=PERSONA_TITLE,
        functional_area=FUNCTIONAL_AREA,
        headline_value=str(_TURN_STATE.get("headline") or "Verified"),
        rows=list(_TURN_STATE.get("rows") or []),
        label_key="wd_name",
        value_key="order_billing_value_inr",
        doc_url=str(_TURN_STATE.get("doc_url") or ""),
        doc_label=str(_TURN_STATE.get("doc_label") or ""),
        local_dir=local_out,
    )
    return {
        "status": "HTML_COCKPIT_READY",
        "cockpit_path": str(local_out / f"{AGENT_SLUG}_cockpit.html"),
        "cockpit_view_url": urls["html_url"],
        "csv_download_url": urls["csv_url"],
        "default_theme": "light",
    }


ALL_TOOLS = [
    query_itc_enterprise_records,
    query_itc_master_network_backbone,
    run_deterministic_optimization_solver,
    verify_finagg_credit_and_godown_cube_fit,
    simulate_what_if_scenario,
    draft_executive_stakeholder_brief,
    stage_governed_erp_or_portal_action,
    render_a2ui_visual_chart_and_canvas,
    export_atomic_schedule_csv,
    generate_interactive_html_cockpit,
]
