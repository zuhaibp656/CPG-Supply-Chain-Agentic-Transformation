"""Deterministic CPG Data Lake & Governed MCP Tools for Commodity Index Advisor (commodity_index_advisor)."""
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

AGENT_ID = "commodity_index_advisor"
DEPT_ID = "sourcing_procurement"
STOPS_AT = "Never commits unapproved SAP Ariba ledger mutations or overrides safety/contract policy without human sign-off."


def query_cpg_commodity_index_advisor_signals(search_filter: str = "", max_rows: int = 25) -> Dict[str, Any]:
    """Reads live CPG multi-echelon records: Computes raw material, cycle time, labor, SG&A & inbound ocean/air freight should-cost Connected CPG systems: SAP Ariba · S/4HANA MM · Mandi Feeds."""
    return sample_domain_records(DEPT_ID, filter_term=search_filter, limit=max_rows)


def run_commodity_index_advisor_barrier_solver(search_filter: str = "") -> Dict[str, Any]:
    """Executes deterministic CPG optimization/audit math: Extracts & aligns 40+ heterogeneous PDF/Excel supplier quotes onto one Operational SQL & Vector DB (On-Prem / Cloud) matrix (BigQuery Parametric BOM Cost Tear-Down + Document AI Quote Parser + Mathematical Optimization Solver (MILP / CP-SAT) Combinatorial MILP Award Split Solver)."""
    sampled = sample_domain_records(DEPT_ID, filter_term=search_filter, limit=40)
    kpis = compute_deterministic_kpis(AGENT_ID, DEPT_ID, sampled.get("sample_records", []))
    return {
        "agent_id": AGENT_ID,
        "agent_name": "Commodity Index Advisor",
        "priority_tier": "P1",
        "source_table": sampled.get("source_table"),
        "using_full_200mb_lake": sampled.get("using_full_200mb_lake"),
        "kpi_summary": kpis,
        "top_records": sampled.get("sample_records", [])[:5],
    }


def stage_commodity_index_advisor_erp_writeback(
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
    query_cpg_commodity_index_advisor_signals,
    run_commodity_index_advisor_barrier_solver,
    stage_commodity_index_advisor_erp_writeback,
]
