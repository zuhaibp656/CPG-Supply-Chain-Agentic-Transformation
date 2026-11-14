"""Deterministic CPG Data Lake & Governed MCP Tools for Farm-Gate Agri & Mandi Procurement Agent (farmgate_agri_commodity_hedger)."""
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

AGENT_ID = "farmgate_agri_commodity_hedger"
DEPT_ID = "sourcing_procurement"
STOPS_AT = "Executing commodity futures derivatives or committing physical forward contracts above buyer authority."


def query_cpg_farmgate_agri_commodity_hedger_signals(search_filter: str = "", max_rows: int = 25) -> Dict[str, Any]:
    """Reads live CPG multi-echelon records: e-Choupal / mandi arrival volumes, moisture & gluten lab grades, Earth Engine crop NDVI, and supplier forward quotes (`02_po_grn_three_way_match_sourcing.csv`)."""
    return sample_domain_records(DEPT_ID, filter_term=search_filter, limit=max_rows)


def run_farmgate_agri_commodity_hedger_barrier_solver(search_filter: str = "") -> Dict[str, Any]:
    """Executes deterministic CPG optimization/audit math: Scores physical buy-vs-wait windows and optimizes multi-mandi procurement splits factoring inward freight to ICML mills."""
    sampled = sample_domain_records(DEPT_ID, filter_term=search_filter, limit=40)
    kpis = compute_deterministic_kpis(AGENT_ID, DEPT_ID, sampled.get("sample_records", []))
    return {
        "agent_id": AGENT_ID,
        "agent_name": "Farm-Gate Agri & Mandi Procurement Agent",
        "priority_tier": "P0",
        "source_table": sampled.get("source_table"),
        "using_full_200mb_lake": sampled.get("using_full_200mb_lake"),
        "kpi_summary": kpis,
        "top_records": sampled.get("sample_records", [])[:5],
    }


def stage_farmgate_agri_commodity_hedger_erp_writeback(
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
    query_cpg_farmgate_agri_commodity_hedger_signals,
    run_farmgate_agri_commodity_hedger_barrier_solver,
    stage_farmgate_agri_commodity_hedger_erp_writeback,
]
