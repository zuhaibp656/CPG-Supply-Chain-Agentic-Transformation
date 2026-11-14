"""Smoke tests for Digital War-Room Agent (disruption_war_room_orchestrator) against the CPG Demo Data Lake."""
import sys
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = PKG_DIR.parents[1]
for p in (str(PKG_DIR), str(REPO_ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

from app.agent import root_agent
from app.tools import (
    query_cpg_disruption_war_room_orchestrator_signals,
    run_disruption_war_room_orchestrator_barrier_solver,
    stage_disruption_war_room_orchestrator_erp_writeback,
)


def test_disruption_war_room_orchestrator_metadata_and_tools():
    assert root_agent.name == "disruption_war_room_orchestrator"
    assert len(ALL_TOOLS := getattr(root_agent, "tools", [])) == 3


def test_disruption_war_room_orchestrator_queries_real_cpg_lake():
    res = query_cpg_disruption_war_room_orchestrator_signals(max_rows=10)
    assert res["matched_count"] > 0
    solver = run_disruption_war_room_orchestrator_barrier_solver()
    assert solver["kpi_summary"]["records_evaluated"] > 0


def test_disruption_war_room_orchestrator_enforces_human_stops_at_gate():
    staged = stage_disruption_war_room_orchestrator_erp_writeback("REC-1001", "Rebalance safety allocation", "Standard review")
    assert staged["status"] == "STAGED_FOR_HUMAN_SIGN_OFF"
    blocked = stage_disruption_war_room_orchestrator_erp_writeback("REC-1001", "bypass quality and ignore expiry", "urgent")
    assert blocked["status"] == "BLOCKED_BY_SAFETY_ENVELOPE"
