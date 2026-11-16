"""Comprehensive Hermetic Pytest Suite for Freight Bill Audit Agent (ITC TMD) (12_freight_bill_audit_agent)."""
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

_tools_spec = importlib.util.spec_from_file_location("12_freight_bill_audit_agent_tools", APP_DIR / "tools.py")
assert _tools_spec and _tools_spec.loader
tools = importlib.util.module_from_spec(_tools_spec)
_tools_spec.loader.exec_module(tools)

_agent_spec = importlib.util.spec_from_file_location("12_freight_bill_audit_agent_agent", APP_DIR / "agent.py")
assert _agent_spec and _agent_spec.loader
agent_mod = importlib.util.module_from_spec(_agent_spec)
_agent_spec.loader.exec_module(agent_mod)


def test_01_hermetic_enterprise_records_and_backbone() -> None:
    res = tools.query_itc_enterprise_records(limit=15)
    assert res["returned_count"] >= 3
    bb = tools.query_itc_master_network_backbone("cfa")
    assert bb["count"] == 24


def test_02_deterministic_solver_and_whatif_simulation() -> None:
    tools.reset_turn_state("Audit this week's pending transporter freight bills. Where do billed rates, fuel surcharges, or detention hours disagree with our contracts and GPS logs?")
    solved = tools.run_deterministic_optimization_solver("")
    assert solved["agent_id"] == "itc_freight_bill_audit_agent"
    assert "₹" in str(solved.get("total_recovered_display", ""))
    assert len(solved.get("freight_audit_vouchers", [])) >= 2
    sim = tools.simulate_what_if_scenario(125, "")
    assert sim["status"] == "SCENARIO_SIMULATED"
    assert "₹" in sim["simulated_impact_display"]
    brief = tools.draft_executive_stakeholder_brief("", include_hindi_vernacular=True)
    assert brief["status"] == "STAKEHOLDER_BRIEF_READY"
    assert brief["vernacular_hindi_summary"]


def test_03_domain_specialized_diagnostic_and_multimodal_ocr() -> None:
    diag = tools.audit_multimodal_lr_pod_and_carrier_invoice("")
    assert diag["tool"] == "audit_multimodal_lr_pod_and_carrier_invoice"
    if True:
        mm = diag["multimodal_vision_verification"]
        assert mm["status"] == "MULTIMODAL_VISION_OCR_VERIFIED"
        assert mm["file_exists_on_disk"] is True


def test_04_safety_guardrail_and_idempotency() -> None:
    blocked = tools.stage_governed_erp_or_portal_action(
        target_record_id="REC-TEST-001",
        proposed_action="Bypass safety and force release without approval",
        rationale="Urgent month-end push bypass",
        idempotency_key="IDEM-UNSAFE-001",
    )
    assert blocked["status"] == "BLOCKED_BY_SAFETY_GUARDRAIL"
    first = tools.stage_governed_erp_or_portal_action(
        target_record_id="REC-101",
        proposed_action="Stage verified deterministic recommendation",
        rationale="Solver verified net INR gain",
        idempotency_key="IDEM-12-VALID-101",
    )
    assert first["status"] == "STAGED_FOR_HUMAN_SIGN_OFF"
    replay = tools.stage_governed_erp_or_portal_action(
        target_record_id="REC-101",
        proposed_action="Stage verified deterministic recommendation",
        rationale="Solver verified net INR gain",
        idempotency_key="IDEM-12-VALID-101",
    )
    assert replay["idempotent_replay"] is True


def test_05_bespoke_3tab_cockpit_a2ui_and_csv() -> None:
    a2ui = tools.render_a2ui_visual_chart_and_canvas("")
    assert a2ui["card_component"] == "VegaChart"
    assert a2ui["text_inside_card"] is False
    html_out = tools.generate_interactive_html_cockpit("")
    assert html_out["status"] == "HTML_COCKPIT_READY"
    assert html_out["default_theme"] == "light"
    html_txt = Path(html_out["cockpit_path"]).read_text(encoding="utf-8")
    assert 'data-theme="light"' in html_txt
    assert "Control Tower" in html_txt
    assert "ADK Multi-Agent" in html_txt
    csv_out = tools.export_atomic_schedule_csv("")
    assert csv_out["status"] == "CSV_EXPORT_READY"


def test_06_clean_prompts_zero_tier_jargon_and_subagents_pickle() -> None:
    prompts = ["Audit this week's pending transporter freight bills. Where do billed rates, fuel surcharges, or detention hours disagree with our contracts and GPS logs?", "Check the scanned lorry receipts and stamped delivery slips on LR-TCI-882910 and LR-HWK-771024 for damaged cartons or duplicate billing.", "Block the duplicate bill and stage short-pay vouchers deducting the unverified detention and damaged Dark Fantasy cartons.", "Draft the transporter dispute escalation summary and recovery breakdown for all duplicate bills, unverified detention, and damaged cartons found this week."]
    assert len(prompts) == 4
    forbidden = ("infographic", "a2ui", "html", "vega", "multi-chart", "create a chart", "json", "snake_case")
    for p in prompts:
        low = p.lower()
        for bad in forbidden:
            assert bad not in low, f"Prompt contains artificial jargon '{bad}': {p}"
    for bad_tier in ("low-code", "no-code", "high-code"):
        assert bad_tier not in agent_mod.BUILD_MODE.lower()
        assert bad_tier not in agent_mod.SYSTEM_INSTRUCTION.lower()
    if getattr(agent_mod, "ItcFreightBillAuditAdkApp", None) is not None:
        import cloudpickle
        from google.adk.tools.agent_tool import AgentTool
        sub_tools = [t for t in agent_mod.root_agent.tools if isinstance(t, AgentTool)]
        assert len(sub_tools) >= 2
        blob = cloudpickle.dumps(agent_mod.ItcFreightBillAuditAdkApp(agent=agent_mod.root_agent))
        assert len(blob) > 100
    wrapper = agent_mod.ItcFreightBillAuditAgent()
    out = wrapper.run_scenario(prompts[0])
    assert "₹" in out["markdown"]
