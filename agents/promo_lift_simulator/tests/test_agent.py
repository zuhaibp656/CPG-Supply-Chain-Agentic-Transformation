"""Smoke tests for Promo ROI Simulator (promo_lift_simulator) against the CPG Demo Data Lake."""
import sys
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = PKG_DIR.parents[1]
for p in (str(PKG_DIR), str(REPO_ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

from app.agent import root_agent
from app.tools import (
    query_cpg_promo_lift_simulator_signals,
    run_promo_lift_simulator_barrier_solver,
    stage_promo_lift_simulator_erp_writeback,
)


def test_promo_lift_simulator_metadata_and_tools():
    assert root_agent.name == "promo_lift_simulator"
    assert len(ALL_TOOLS := getattr(root_agent, "tools", [])) == 3


def test_promo_lift_simulator_queries_real_cpg_lake():
    res = query_cpg_promo_lift_simulator_signals(max_rows=10)
    assert res["matched_count"] > 0
    solver = run_promo_lift_simulator_barrier_solver()
    assert solver["kpi_summary"]["records_evaluated"] > 0


def test_promo_lift_simulator_enforces_human_stops_at_gate():
    staged = stage_promo_lift_simulator_erp_writeback("REC-1001", "Rebalance safety allocation", "Standard review")
    assert staged["status"] == "STAGED_FOR_HUMAN_SIGN_OFF"
    blocked = stage_promo_lift_simulator_erp_writeback("REC-1001", "bypass quality and ignore expiry", "urgent")
    assert blocked["status"] == "BLOCKED_BY_SAFETY_ENVELOPE"
