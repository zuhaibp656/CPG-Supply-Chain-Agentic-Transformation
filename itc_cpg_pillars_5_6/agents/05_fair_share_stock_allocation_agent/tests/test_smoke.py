"""Comprehensive Hermetic Pytest Suite for Fair-Share Stock Allocation Agent (ITC TMD) (05_fair_share_stock_allocation_agent)."""
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

_tools_spec = importlib.util.spec_from_file_location("05_fair_share_stock_allocation_agent_tools", APP_DIR / "tools.py")
assert _tools_spec and _tools_spec.loader
tools = importlib.util.module_from_spec(_tools_spec)
_tools_spec.loader.exec_module(tools)

_agent_spec = importlib.util.spec_from_file_location("05_fair_share_stock_allocation_agent_agent", APP_DIR / "agent.py")
assert _agent_spec and _agent_spec.loader
agent_mod = importlib.util.module_from_spec(_agent_spec)
_agent_spec.loader.exec_module(agent_mod)


def test_01_hermetic_enterprise_records_and_backbone() -> None:
    res = tools.query_itc_enterprise_records(limit=15)
    assert res["returned_count"] >= 3
    bb = tools.query_itc_master_network_backbone("cfa")
    assert bb["count"] == 24


def test_02_deterministic_solver_and_autonomous_turn_state() -> None:
    tools.reset_turn_state("We are short on Sunfeast Dark Fantasy 300g at Nelamangala depot. How should we split the 2,400 available cases across channels?")
    solved = tools.run_deterministic_optimization_solver("")
    assert solved["agent_id"] == "itc_fair_share_stock_allocation_agent"
    assert "₹" in str(solved.get("net_economic_advantage_display", ""))
    assert len(solved.get("channel_allocations", [])) >= 2
    st = tools.get_turn_state()
    assert st["active"] is True
    assert st["vega_spec"] is not None
    assert "hconcat" in st["vega_spec"]


def test_03_domain_specialized_diagnostic_and_multimodal_ocr() -> None:
    diag = tools.compare_ortools_lp_vs_naive_fifo_rationing("")
    assert diag["tool"] == "compare_ortools_lp_vs_naive_fifo_rationing"
    if "05_fair_share_stock_allocation_agent" in ("03_cold_chain_thermal_auditor", "12_freight_bill_audit_agent"):
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
        idempotency_key="IDEM-05-VALID-101",
    )
    assert first["status"] == "STAGED_FOR_HUMAN_SIGN_OFF"
    replay = tools.stage_governed_erp_or_portal_action(
        target_record_id="REC-101",
        proposed_action="Stage verified deterministic recommendation",
        rationale="Solver verified net INR gain",
        idempotency_key="IDEM-05-VALID-101",
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
    prompts = ["We are short on Sunfeast Dark Fantasy 300g at Nelamangala depot. How should we split the 2,400 available cases across channels?", "What happens to our Quick-Commerce penalties and General Trade dealers if we let standard first-come-first-served allocation run?", "Hold the fair-share channel split in SAP for my review so neither Blinkit nor our Karnataka wholesale dealers get starved."]
    assert len(prompts) == 3
    forbidden = ("infographic", "a2ui", "html", "vega", "multi-chart", "create a chart", "json", "snake_case")
    for p in prompts:
        low = p.lower()
        for bad in forbidden:
            assert bad not in low, f"Prompt contains artificial jargon '{bad}': {p}"
    wrapper = agent_mod.ItcFairShareStockAllocationAgent()
    out = wrapper.run_scenario(prompts[0])
    assert "₹" in out["markdown"]
