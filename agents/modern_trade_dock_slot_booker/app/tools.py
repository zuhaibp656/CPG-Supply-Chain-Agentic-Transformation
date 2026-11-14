"""Deterministic CPG Data Lake & Governed MCP Tools for Modern Trade Appointment & Fill-Rate Agent (modern_trade_dock_slot_booker)."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cpg_runtime.lake_engine import (
    compute_deterministic_kpis,
    sample_domain_records,
    stage_governed_mcp_action,
)

AGENT_ID = "modern_trade_dock_slot_booker"
DEPT_ID = "logistics_fleet"
STOPS_AT = "Canceling committed Modern Trade purchase orders."


def query_cpg_modern_trade_dock_slot_booker_signals(search_filter: str = "", max_rows: int = 25) -> Dict[str, Any]:
    """Reads live CPG multi-echelon records: Retailer ASN appointment calendars, WMS wave completion %, and live route traffic ETA."""
    return sample_domain_records(DEPT_ID, filter_term=search_filter, limit=max_rows)


def run_modern_trade_dock_slot_booker_barrier_solver(search_filter: str = "") -> Dict[str, Any]:
    """Executes deterministic CPG optimization/audit math: Matches ready-to-ship loads against open retailer receiving slots and flags threatened PO cancellation cutoffs."""
    sampled = sample_domain_records(DEPT_ID, filter_term=search_filter, limit=40)
    kpis = compute_deterministic_kpis(AGENT_ID, DEPT_ID, sampled.get("sample_records", []))
    return {
        "agent_id": AGENT_ID,
        "agent_name": "Modern Trade Appointment & Fill-Rate Agent",
        "priority_tier": "P1",
        "source_table": sampled.get("source_table"),
        "using_full_200mb_lake": sampled.get("using_full_200mb_lake"),
        "kpi_summary": kpis,
        "top_records": sampled.get("sample_records", [])[:5],
    }


def stage_modern_trade_dock_slot_booker_erp_writeback(
    target_record_id: str,
    proposed_action: str,
    rationale: str = "",
) -> Dict[str, Any]:
    """Stages a policy-checked ERP/WMS/TMS/DMS action via Apigee MCP respecting Human Sign-Off."""
    return stage_governed_mcp_action(
        agent_id=AGENT_ID,
        stops_at_rule=STOPS_AT,
        proposed_action=proposed_action,
        target_record_id=target_record_id,
        user_rationale=rationale,
    )


ALL_TOOLS = [
    query_cpg_modern_trade_dock_slot_booker_signals,
    run_modern_trade_dock_slot_booker_barrier_solver,
    stage_modern_trade_dock_slot_booker_erp_writeback,
]
