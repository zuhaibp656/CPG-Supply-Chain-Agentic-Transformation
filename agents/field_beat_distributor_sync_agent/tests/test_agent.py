"""Smoke tests for JBP Negotiation Agent (field_beat_distributor_sync_agent) against the CPG Demo Data Lake."""
import sys
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = PKG_DIR.parents[1]
for p in (str(PKG_DIR), str(REPO_ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

from app.agent import root_agent
from app.tools import (
    query_cpg_field_beat_distributor_sync_agent_signals,
    run_field_beat_distributor_sync_agent_barrier_solver,
    stage_field_beat_distributor_sync_agent_erp_writeback,
)


def test_field_beat_distributor_sync_agent_metadata_and_tools():
    assert root_agent.name == "field_beat_distributor_sync_agent"
    assert len(ALL_TOOLS := getattr(root_agent, "tools", [])) == 3


def test_field_beat_distributor_sync_agent_queries_real_cpg_lake():
    res = query_cpg_field_beat_distributor_sync_agent_signals(max_rows=10)
    assert res["matched_count"] > 0
    solver = run_field_beat_distributor_sync_agent_barrier_solver()
    assert solver["kpi_summary"]["records_evaluated"] > 0


def test_field_beat_distributor_sync_agent_enforces_human_stops_at_gate():
    staged = stage_field_beat_distributor_sync_agent_erp_writeback("REC-1001", "Rebalance safety allocation", "Standard review")
    assert staged["status"] == "STAGED_FOR_HUMAN_SIGN_OFF"
    blocked = stage_field_beat_distributor_sync_agent_erp_writeback("REC-1001", "bypass quality and ignore expiry", "urgent")
    assert blocked["status"] == "BLOCKED_BY_SAFETY_ENVELOPE"
