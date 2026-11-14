"""Smoke tests for Keep-It & Routing Advisor (keep_it_routing_advisor) against the CPG Demo Data Lake."""
import sys
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = PKG_DIR.parents[1]
for p in (str(PKG_DIR), str(REPO_ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

from app.agent import root_agent
from app.tools import (
    query_cpg_keep_it_routing_advisor_signals,
    run_keep_it_routing_advisor_barrier_solver,
    stage_keep_it_routing_advisor_erp_writeback,
)


def test_keep_it_routing_advisor_metadata_and_tools():
    assert root_agent.name == "keep_it_routing_advisor"
    assert len(ALL_TOOLS := getattr(root_agent, "tools", [])) == 3


def test_keep_it_routing_advisor_queries_real_cpg_lake():
    res = query_cpg_keep_it_routing_advisor_signals(max_rows=10)
    assert res["matched_count"] > 0
    solver = run_keep_it_routing_advisor_barrier_solver()
    assert solver["kpi_summary"]["records_evaluated"] > 0


def test_keep_it_routing_advisor_enforces_human_stops_at_gate():
    staged = stage_keep_it_routing_advisor_erp_writeback("REC-1001", "Rebalance safety allocation", "Standard review")
    assert staged["status"] == "STAGED_FOR_HUMAN_SIGN_OFF"
    blocked = stage_keep_it_routing_advisor_erp_writeback("REC-1001", "bypass quality and ignore expiry", "urgent")
    assert blocked["status"] == "BLOCKED_BY_SAFETY_ENVELOPE"
