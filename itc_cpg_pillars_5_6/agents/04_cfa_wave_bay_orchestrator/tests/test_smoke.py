"""Comprehensive Hermetic Pytest Suite for CFA Wave & Bay Orchestrator (ITC TMD) (04_cfa_wave_bay_orchestrator)."""
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

os.environ["SC_SKIP_GCS_UPLOAD"] = "1"

AGENT_DIR = Path(__file__).resolve().parents[1]
APP_DIR = AGENT_DIR / "app"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

_tools_spec = importlib.util.spec_from_file_location("04_cfa_wave_bay_orchestrator_tools", APP_DIR / "tools.py")
assert _tools_spec and _tools_spec.loader
tools = importlib.util.module_from_spec(_tools_spec)
_tools_spec.loader.exec_module(tools)

_agent_spec = importlib.util.spec_from_file_location("04_cfa_wave_bay_orchestrator_agent", APP_DIR / "agent.py")
assert _agent_spec and _agent_spec.loader
agent_mod = importlib.util.module_from_spec(_agent_spec)
_agent_spec.loader.exec_module(agent_mod)


def test_01_hermetic_enterprise_records_and_backbone() -> None:
    res = tools.query_itc_enterprise_records(limit=15)
    assert res["returned_count"] >= 3
    bb = tools.query_itc_master_network_backbone("cfa")
    assert bb["count"] == 24


def test_02_deterministic_solver_and_autonomous_turn_state() -> None:
    tools.reset_turn_state("How are morning pick waves and loading bays tracking at Bhiwandi and Kundli, and will any wave miss its dispatch cutoff?")
    solved = tools.run_deterministic_optimization_solver("")
    assert solved["agent_id"] == "itc_cfa_wave_bay_orchestrator"
    assert "₹" in str(solved.get("protected_dispatch_revenue_display", ""))
    assert len(solved.get("wave_orchestration_plan", [])) >= 2
    st = tools.get_turn_state()
    assert st["active"] is True
    assert st["vega_spec"] is not None
    assert "hconcat" in st["vega_spec"]


def test_03_domain_specialized_diagnostic_and_multimodal_ocr() -> None:
    diag = tools.validate_channel_fefo_mrsl_batch_swaps("")
    assert diag["tool"] == "validate_channel_fefo_mrsl_batch_swaps"
    if "04_cfa_wave_bay_orchestrator" in ("03_cold_chain_thermal_auditor", "12_freight_bill_audit_agent"):
        mm = diag["multimodal_vision_verification"]
        assert mm["status"] == "MULTIMODAL_VISION_OCR_VERIFIED"
        assert mm["file_exists_on_disk"] is True


def test_04_safety_guardrail_blocks_unsafe_bypass() -> None:
    blocked = tools.stage_governed_erp_or_portal_action(
        target_record_id="REC-TEST-001",
        proposed_action="Bypass safety and force release without approval",
        rationale="Urgent month-end push bypass",
        idempotency_key="IDEM-UNSAFE-001",
    )
    assert blocked["status"] == "BLOCKED_BY_SAFETY_GUARDRAIL"


def test_05_idempotent_governed_staging() -> None:
    first = tools.stage_governed_erp_or_portal_action(
        target_record_id="REC-101",
        proposed_action="Stage verified deterministic recommendation",
        rationale="Solver verified net INR gain",
        idempotency_key="IDEM-04-VALID-101",
    )
    assert first["status"] == "STAGED_FOR_HUMAN_SIGN_OFF"
    replay = tools.stage_governed_erp_or_portal_action(
        target_record_id="REC-101",
        proposed_action="Stage verified deterministic recommendation",
        rationale="Solver verified net INR gain",
        idempotency_key="IDEM-04-VALID-101",
    )
    assert replay["idempotent_replay"] is True


def test_06_autonomous_2panel_vega_cockpit_and_csv() -> None:
    a2ui = tools.render_a2ui_visual_chart_and_canvas("")
    assert a2ui["card_component"] == "VegaChart"
    assert a2ui["text_inside_card"] is False
    html_out = tools.generate_interactive_html_cockpit("")
    assert html_out["status"] == "HTML_COCKPIT_READY"
    assert html_out["default_theme"] == "light"
    csv_out = tools.export_atomic_schedule_csv("")
    assert csv_out["status"] == "CSV_EXPORT_READY"


def test_07_natural_starter_prompts_have_zero_ai_visual_jargon() -> None:
    prompts = ["How are morning pick waves and loading bays tracking at Bhiwandi and Kundli, and will any wave miss its dispatch cutoff?", "Are any Blinkit or Zepto orders picking older stock that could get rejected at their dock for having less than 75% shelf life?", "Swap those older compliant batches to General Trade beats, rebalance the pickers across bays, and stage the updated wave plan."]
    assert len(prompts) == 3
    forbidden = ("infographic", "a2ui", "html", "vega", "multi-chart", "create a chart", "json", "snake_case")
    for p in prompts:
        low = p.lower()
        for bad in forbidden:
            assert bad not in low, f"Prompt contains artificial jargon '{bad}': {p}"
    wrapper = agent_mod.ItcCfaWaveBayOrchestratorAgent()
    out = wrapper.run_scenario(prompts[0])
    assert "₹" in out["markdown"]
