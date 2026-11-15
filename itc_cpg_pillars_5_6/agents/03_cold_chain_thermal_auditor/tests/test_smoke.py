"""Comprehensive Pytest Suite for Cold-Chain Thermal Auditor (03_cold_chain_thermal_auditor)."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parents[1]
SUITE_ROOT = AGENT_DIR.parents[1]
if str(SUITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SUITE_ROOT))

_tools_spec = importlib.util.spec_from_file_location("03_cold_chain_thermal_auditor_tools", AGENT_DIR / "app" / "tools.py")
assert _tools_spec and _tools_spec.loader
tools = importlib.util.module_from_spec(_tools_spec)
_tools_spec.loader.exec_module(tools)

_agent_spec = importlib.util.spec_from_file_location("03_cold_chain_thermal_auditor_agent", AGENT_DIR / "app" / "agent.py")
assert _agent_spec and _agent_spec.loader
agent_mod = importlib.util.module_from_spec(_agent_spec)
sys.modules["tools"] = tools
_agent_spec.loader.exec_module(agent_mod)


def test_01_enterprise_records_and_backbone_query() -> None:
    res = tools.query_itc_enterprise_records(limit=15)
    assert res["returned_count"] >= 3
    assert len(res["records"]) >= 3
    bb = tools.query_itc_master_network_backbone("cfa")
    assert bb["count"] == 24


def test_02_deterministic_solver_accuracy_and_inr() -> None:
    solved = tools.run_deterministic_optimization_solver("")
    assert solved["agent_id"] == "itc_cold_chain_thermal_auditor"
    assert "₹" in str(solved.get("recoverable_carrier_claims_display", ""))
    assert len(solved.get("thermal_audit_ledger", [])) >= 2


def test_03_domain_specialized_diagnostic_tool() -> None:
    diag = tools.inspect_drishti_strip_chart_multimodal("")
    assert diag["tool"] == "inspect_drishti_strip_chart_multimodal"
    if "03_cold_chain_thermal_auditor" in ("03_cold_chain_thermal_auditor", "12_freight_bill_audit_agent"):
        mm = diag["multimodal_vision_verification"]
        assert mm["status"] == "MULTIMODAL_VISION_OCR_VERIFIED"
        assert mm["file_exists_on_disk"] is True
        assert len(mm["extracted_ocr_lines"]) >= 3


def test_04_safety_guardrail_blocks_unsafe_bypass() -> None:
    blocked = tools.stage_governed_erp_or_portal_action(
        target_record_id="REC-TEST-001",
        proposed_action="Bypass safety and force release without approval",
        rationale="Urgent month-end push bypass",
        idempotency_key="IDEM-UNSAFE-001",
    )
    assert blocked["status"] == "BLOCKED_BY_SAFETY_GUARDRAIL"


def test_05_idempotent_governed_staging_and_contract_gate() -> None:
    missing_idem = agent_mod.enforce_tool_contract(
        "stage_governed_erp_or_portal_action",
        {"target_record_id": "REC-101", "proposed_action": "Stage verified plan"},
    )
    assert missing_idem is not None
    assert missing_idem["status"] == "BLOCKED_MISSING_IDEMPOTENCY_KEY"

    first = tools.stage_governed_erp_or_portal_action(
        target_record_id="REC-101",
        proposed_action="Stage verified deterministic recommendation",
        rationale="Solver verified net INR gain",
        idempotency_key="IDEM-03-VALID-101",
    )
    assert first["status"] == "STAGED_FOR_HUMAN_SIGN_OFF"
    assert first["idempotent_replay"] is False

    replay = tools.stage_governed_erp_or_portal_action(
        target_record_id="REC-101",
        proposed_action="Stage verified deterministic recommendation",
        rationale="Solver verified net INR gain",
        idempotency_key="IDEM-03-VALID-101",
    )
    assert replay["idempotent_replay"] is True
    assert replay["staging_voucher_id"] == first["staging_voucher_id"]


def test_06_a2ui_vega_card_csv_and_light_cockpit() -> None:
    a2ui = tools.render_a2ui_visual_chart_and_canvas("")
    assert a2ui["card_component"] == "VegaChart"
    assert a2ui["text_inside_card"] is False
    assert len(a2ui["vega_lite_spec"]["data"]["values"]) >= 2

    csv_out = tools.export_atomic_schedule_csv("")
    assert csv_out["status"] == "CSV_EXPORT_READY"
    assert Path(csv_out["csv_path"]).is_file()

    html_out = tools.generate_interactive_html_cockpit("")
    assert html_out["status"] == "HTML_COCKPIT_READY"
    assert html_out["default_theme"] == "light"
    assert 'data-theme="light"' in Path(html_out["cockpit_path"]).read_text(encoding="utf-8")


def test_07_end_to_end_scenario_and_global_model_routing() -> None:
    wrapper = agent_mod.ColdChainThermalAuditorAgent()
    out = wrapper.run_scenario("Audit our inbound frozen Master Chef, Svasti dairy, and Fabelle chocolate reefer shipments—which loads breached Mean Kinetic Temperature limits and need quarantine or a carrier spoilage claim?")
    assert out["agent_id"] == "itc_cold_chain_thermal_auditor"
    assert out["model_routing"]["endpoint_location"] == "global"
    assert out["model_routing"]["selected_model"] in ("gemini-3.1-pro-preview", "gemini-3.8-flash")
    assert "₹" in out["markdown"]
