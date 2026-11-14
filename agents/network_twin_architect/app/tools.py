"""Deterministic CPG Data Lake & Governed MCP Tools for Cost-to-Serve Diagnostic (network_twin_architect)."""
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

AGENT_ID = "network_twin_architect"
DEPT_ID = "demand_sop"
STOPS_AT = "Never commits unapproved SAP IBP ledger mutations or overrides safety/contract policy without human sign-off."


def query_cpg_network_twin_architect_signals(search_filter: str = "", max_rows: int = 25) -> Dict[str, Any]:
    """Reads live CPG multi-echelon records: Attributes exact ocean, air, rail, drayage, pick, pack, cube & detention cost per order line Connected CPG systems: SAP IBP · DMS · Retail POS."""
    return sample_domain_records(DEPT_ID, filter_term=search_filter, limit=max_rows)


def run_network_twin_architect_barrier_solver(search_filter: str = "") -> Dict[str, Any]:
    """Executes deterministic CPG optimization/audit math: Optimizes DC territories, factory-to-customer bypass & 3PL overflow capacity in Mathematical Optimization Solver (MILP / CP-SAT) (BigQuery Activity-Based Landed Cost-to-Serve Attribution + Mathematical Optimization Solver (MILP / CP-SAT) Capacitated Facility Location & Multi-Modal Flow MILP)."""
    sampled = sample_domain_records(DEPT_ID, filter_term=search_filter, limit=40)
    kpis = compute_deterministic_kpis(AGENT_ID, DEPT_ID, sampled.get("sample_records", []))
    return {
        "agent_id": AGENT_ID,
        "agent_name": "Cost-to-Serve Diagnostic",
        "priority_tier": "P2",
        "source_table": sampled.get("source_table"),
        "using_full_200mb_lake": sampled.get("using_full_200mb_lake"),
        "kpi_summary": kpis,
        "top_records": sampled.get("sample_records", [])[:5],
    }


def stage_network_twin_architect_erp_writeback(
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
    query_cpg_network_twin_architect_signals,
    run_network_twin_architect_barrier_solver,
    stage_network_twin_architect_erp_writeback,
]
