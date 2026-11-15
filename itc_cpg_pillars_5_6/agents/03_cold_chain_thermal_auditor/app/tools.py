"""Deterministic Python Tools for Cold-Chain Thermal Auditor (03_cold_chain_thermal_auditor) — ITC Limited CPG Pillars 5 & 6."""
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

AGENT_SLUG = "03_cold_chain_thermal_auditor"
AGENT_ID = "itc_cold_chain_thermal_auditor"
AGENT_NAME = "Cold-Chain Thermal Auditor"
PERSONA_TITLE = "Cold-Chain & Transit QA Lead"
FUNCTIONAL_AREA = "Primary Logistics & Plant Dispatch (Factory -> CFA / Depot)"
BUILD_MODE = "Low-Code Agent Studio"
TARGET_SYSTEM = "SAP Quality Management (SAP QM `BAPI_INSPLOT_SETUSAGEDECISION`) & Carrier Claims Portal"
STOPS_AT_BOUNDARY = "Never auto-releases thermally abused frozen, dairy, or chocolate lots into unrestricted CFA stock without QA Lead usage decision."
PRIMARY_TABLE = "03_drishti_reefer_iot_thermal_telemetry"


def query_itc_enterprise_records(search_filter: str = "", limit: int = 30) -> Dict[str, Any]:
    """Queries ITC CPG enterprise records for Cold-Chain Thermal Auditor from the 405 MB TM&D lake (or container seeds)."""
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
    """Executes the exact deterministic mathematical/OR-Tools/physics solver for Cold-Chain Thermal Auditor."""
    queried = query_domain_table(PRIMARY_TABLE, search_filter=search_filter, limit=40, agent_dir=AGENT_DIR)
    solver_fn = SOLVER_REGISTRY[AGENT_SLUG]
    result = solver_fn(queried.get("records", []))
    result["agent_id"] = AGENT_ID
    result["agent_name"] = AGENT_NAME
    result["build_mode"] = BUILD_MODE
    result["using_full_enterprise_lake"] = queried.get("using_full_enterprise_lake", False)
    return result


def inspect_drishti_strip_chart_multimodal(reference_id: str = "") -> Dict[str, Any]:
    """Performs multimodal OCR & strip-chart inspection on scanned Drishti BLE thermal logger printouts (`DOC-STRIP-SHP-CLD-*.png`) to corroborate carrier negligence claims."""
    if AGENT_SLUG in ("03_cold_chain_thermal_auditor", "12_freight_bill_audit_agent"):
        default_doc = "DOC-STRIP-SHP-CLD-70001.png" if "03_" in AGENT_SLUG else "DOC-POD-882910.png"
        doc_name = reference_id if (reference_id and ".png" in reference_id.lower()) else default_doc
        ocr = inspect_multimodal_document(doc_name)
        solved = run_deterministic_optimization_solver("")
        return {
            "tool": "inspect_drishti_strip_chart_multimodal",
            "multimodal_vision_verification": ocr,
            "headline_recovery_or_claim": solved.get("recoverable_carrier_claims_display"),
            "top_audited_items": solved.get("thermal_audit_ledger", [])[:3],
        }
    solved = run_deterministic_optimization_solver(reference_id)
    return {
        "tool": "inspect_drishti_strip_chart_multimodal",
        "reference_filter": reference_id or "ALL_PRIORITY_EXCEPTIONS",
        "headline_impact_inr": solved.get("recoverable_carrier_claims_display"),
        "verified_diagnostics": solved.get("thermal_audit_ledger", [])[:4],
        "human_gate_boundary": STOPS_AT_BOUNDARY,
    }


def stage_governed_erp_or_portal_action(
    target_record_id: str,
    proposed_action: str,
    rationale: str = "",
    idempotency_key: str = "",
) -> Dict[str, Any]:
    """Stages a policy-checked write-back to SAP Quality Management (SAP QM `BAPI_INSPLOT_SETUSAGEDECISION`) & Carrier Claims Portal with idempotency & human sign-off."""
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
    rows = solved.get("thermal_audit_ledger", [])
    return build_a2ui_vega_and_canvas(
        agent_title=AGENT_NAME,
        subtitle=f"{FUNCTIONAL_AREA} · Headline Impact: {solved.get('recoverable_carrier_claims_display', 'Verified')}",
        rows=rows,
        label_key="shipment_id",
        value_key="carrier_spoilage_claim_inr",
        value_title_inr="Verified Impact / Metric (₹ INR)",
    )


def export_atomic_schedule_csv(search_filter: str = "") -> Dict[str, Any]:
    """Exports an atomic RFC-4180 CSV schedule ready for Google Sheets or SAP upload."""
    solved = run_deterministic_optimization_solver(search_filter)
    rows = solved.get("thermal_audit_ledger", [])
    out_dir = AGENT_DIR / "artifacts_out"
    return export_verified_csv(AGENT_SLUG, rows, out_dir)


def generate_interactive_html_cockpit(search_filter: str = "") -> Dict[str, Any]:
    """Compiles a self-contained Light-Theme Default Interactive HTML5 Cockpit for Cold-Chain Thermal Auditor."""
    solved = run_deterministic_optimization_solver(search_filter)
    rows = solved.get("thermal_audit_ledger", [])
    out_dir = AGENT_DIR / "artifacts_out"
    return render_interactive_cockpit_html(
        agent_slug=AGENT_SLUG,
        agent_title=AGENT_NAME,
        persona_title=PERSONA_TITLE,
        functional_area=FUNCTIONAL_AREA,
        headline_metric_label="Verified Deterministic Impact",
        headline_metric_value=str(solved.get("recoverable_carrier_claims_display", "₹0")),
        rows=rows,
        output_dir=out_dir,
    )


ALL_TOOLS = [
    query_itc_enterprise_records,
    query_itc_master_network_backbone,
    run_deterministic_optimization_solver,
    inspect_drishti_strip_chart_multimodal,
    stage_governed_erp_or_portal_action,
    render_a2ui_visual_chart_and_canvas,
    export_atomic_schedule_csv,
    generate_interactive_html_cockpit,
]
