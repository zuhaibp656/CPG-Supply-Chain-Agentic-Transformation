"""Deterministic CPG Data Lake & Governed MCP Tools for PIPO Run-Out Agent (eco_cutover_orchestrator)."""
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

AGENT_ID = "eco_cutover_orchestrator"
DEPT_ID = "demand_sop"
STOPS_AT = "Never commits unapproved SAP IBP ledger mutations or overrides safety/contract policy without human sign-off."


def query_cpg_eco_cutover_orchestrator_signals(search_filter: str = "", max_rows: int = 25) -> Dict[str, Any]:
    """Reads live CPG multi-echelon records: Finds the exact cutover date in Mathematical Optimization Solver (MILP / CP-SAT) that exhausts Rev-A stock and open ocean/air POs Connected CPG systems: SAP IBP · DMS · Retail POS."""
    return sample_domain_records(DEPT_ID, filter_term=search_filter, limit=max_rows)


def run_eco_cutover_orchestrator_barrier_solver(search_filter: str = "") -> Dict[str, Any]:
    """Executes deterministic CPG optimization/audit math: Reconciles Teamcenter PLM CAD redlines against SAP plant routings & work instructions (Low-Latency Transactional State DB eBOM-to-mBOM Graph Verifier + Mathematical Optimization Solver (MILP / CP-SAT) Multi-Plant BOM Burn-Down & Effectivity Date MILP)."""
    sampled = sample_domain_records(DEPT_ID, filter_term=search_filter, limit=40)
    kpis = compute_deterministic_kpis(AGENT_ID, DEPT_ID, sampled.get("sample_records", []))
    return {
        "agent_id": AGENT_ID,
        "agent_name": "PIPO Run-Out Agent",
        "priority_tier": "P1",
        "source_table": sampled.get("source_table"),
        "using_full_200mb_lake": sampled.get("using_full_200mb_lake"),
        "kpi_summary": kpis,
        "top_records": sampled.get("sample_records", [])[:5],
    }


def stage_eco_cutover_orchestrator_erp_writeback(
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
    query_cpg_eco_cutover_orchestrator_signals,
    run_eco_cutover_orchestrator_barrier_solver,
    stage_eco_cutover_orchestrator_erp_writeback,
]
