"""Hermetic Deterministic Python & Multimodal Tools for Load Consolidation Agent (ITC TMD)."""
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

AGENT_SLUG = "01_load_consolidation_agent"
AGENT_ID = "itc_load_consolidation_agent"
AGENT_NAME = "Load Consolidation Agent"
GE_DISPLAY_NAME = "Load Consolidation Agent (ITC TMD)"
PERSONA_TITLE = "Primary Transport Planner"
FUNCTIONAL_AREA = "Primary Logistics & Plant Dispatch (Factory -> CFA / Depot)"
BUILD_MODE = "Low-Code Agent Studio"
TARGET_SYSTEM = "SAP Transportation Management (SAP TM) & Zenith Indent Portal"
STOPS_AT_BOUNDARY = "Never auto-tenders overloaded vehicles violating Central Motor Vehicles Rules (CMVR) Rule 93 axle limits or commits SAP TM shipment cost docs without Primary Transport Planner sign-off."
PRIMARY_TABLE = "01_icml_primary_dispatch_waves_and_cartons"

# Lightweight per-turn state for autonomous A2UI chart, Canvas RichTable & GCS artifact emission
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


def _record_visual_context(solved: Dict[str, Any]) -> None:
    rows = list(solved.get("composite_load_plans", []) or [])
    headline = str(solved.get("net_freight_savings_display", "Verified"))
    spec = build_autonomous_2panel_vegalite(
        agent_slug=AGENT_SLUG,
        agent_title=AGENT_NAME,
        subtitle=f"{FUNCTIONAL_AREA} · Verified Impact: {headline}",
        rows=rows,
        label_key="composite_load_id",
        value_key="freight_saved_inr",
        value_title="Impact / Metric (₹ INR)",
        user_query=str(_TURN_STATE.get("user_query", "")),
    )
    _TURN_STATE["active"] = True
    _TURN_STATE["rows"] = rows
    _TURN_STATE["headline"] = headline
    _TURN_STATE["vega_spec"] = spec


def query_itc_enterprise_records(search_filter: str = "", limit: int = 30) -> Dict[str, Any]:
    """Queries ITC Limited TM&D operational records for Load Consolidation Agent."""
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
    """Executes the deterministic mathematical / OR-Tools / physics solver for Load Consolidation Agent."""
    queried = query_domain_table(PRIMARY_TABLE, search_filter=search_filter, limit=40, agent_dir=_agent_root())
    solver_fn = SOLVER_REGISTRY[AGENT_SLUG]
    result = solver_fn(queried.get("records", []))
    result["agent_id"] = AGENT_ID
    result["agent_name"] = AGENT_NAME
    result["build_mode"] = BUILD_MODE
    result["using_full_enterprise_lake"] = queried.get("using_full_enterprise_lake", False)
    _record_visual_context(result)
    return result


def verify_cmvr_rule93_axle_and_crush_physics(reference_id: str = "") -> Dict[str, Any]:
    """Verifies Central Motor Vehicles Rules (CMVR) Rule 93 front steering (<=7,500 kg) & rear drive (<=11,500 kg) axle weights and top-tier carton crush limits (<=85 kg on Bingo! / <=155 kg on Sunfeast)."""
    if AGENT_SLUG in ("03_cold_chain_thermal_auditor", "12_freight_bill_audit_agent"):
        default_doc = "DOC-STRIP-SHP-CLD-70001.png" if "03_" in AGENT_SLUG else "DOC-POD-882910.png"
        ref_clean = (reference_id or "").strip()
        if "771024" in ref_clean:
            doc_name = "DOC-POD-771024.png"
        elif "664319" in ref_clean:
            doc_name = "DOC-POD-664319.png"
        elif "70002" in ref_clean or "patna" in ref_clean.lower() or "paneer" in ref_clean.lower():
            doc_name = "DOC-STRIP-SHP-CLD-70002.png"
        elif ref_clean.lower().endswith(".png"):
            doc_name = ref_clean
        else:
            doc_name = default_doc

        ocr = inspect_multimodal_document(doc_name, agent_dir=_agent_root())
        png_path = resolve_multimodal_png_path(ocr["document_filename"], agent_dir=_agent_root())
        if png_path is not None:
            img_url = publish_multimodal_doc_image(png_path)
            if img_url:
                _TURN_STATE["doc_url"] = img_url
                _TURN_STATE["doc_label"] = f"{ocr['document_filename']} ({ocr['document_title']})"
        solved = run_deterministic_optimization_solver("")
        return {
            "tool": "verify_cmvr_rule93_axle_and_crush_physics",
            "multimodal_vision_verification": ocr,
            "scanned_document_view_url": _TURN_STATE.get("doc_url", ""),
            "headline_recovery_or_claim": solved.get("net_freight_savings_display"),
            "top_audited_items": solved.get("composite_load_plans", [])[:3],
        }

    solved = run_deterministic_optimization_solver(reference_id)
    return {
        "tool": "verify_cmvr_rule93_axle_and_crush_physics",
        "reference_filter": reference_id or "ALL_PRIORITY_EXCEPTIONS",
        "headline_impact_inr": solved.get("net_freight_savings_display"),
        "verified_diagnostics": solved.get("composite_load_plans", [])[:4],
        "human_gate_boundary": STOPS_AT_BOUNDARY,
    }


def stage_governed_erp_or_portal_action(
    target_record_id: str,
    proposed_action: str,
    rationale: str = "",
    idempotency_key: str = "",
) -> Dict[str, Any]:
    """Stages a policy-checked write-back to SAP Transportation Management (SAP TM) & Zenith Indent Portal with idempotency & human sign-off."""
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
        "headline_impact": solved.get("net_freight_savings_display"),
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
        label_key="composite_load_id",
        value_key="freight_saved_inr",
        local_dir=local_out,
    )
    return {
        "status": "CSV_EXPORT_READY",
        "csv_path": str(local_out / f"{AGENT_SLUG}_verified_schedule.csv"),
        "csv_download_url": urls["csv_url"],
        "row_count": len(_TURN_STATE.get("rows") or []),
    }


def generate_interactive_html_cockpit(search_filter: str = "") -> Dict[str, Any]:
    """Compiles & publishes the Light-Theme Default Interactive HTML5 Cockpit (with Bar + Donut views & What-If slider)."""
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
        label_key="composite_load_id",
        value_key="freight_saved_inr",
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
    verify_cmvr_rule93_axle_and_crush_physics,
    stage_governed_erp_or_portal_action,
    render_a2ui_visual_chart_and_canvas,
    export_atomic_schedule_csv,
    generate_interactive_html_cockpit,
]
