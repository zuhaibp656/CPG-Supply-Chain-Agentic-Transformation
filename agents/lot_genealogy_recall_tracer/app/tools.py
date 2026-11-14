"""Deterministic CPG Data Lake & Governed MCP Tools for 2-Hour Lot Genealogy & Recall Tracer (lot_genealogy_recall_tracer)."""
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

AGENT_ID = "lot_genealogy_recall_tracer"
DEPT_ID = "manufacturing_prod"
STOPS_AT = "Issuing public consumer recall notices or releasing quarantined QA stock."


def query_cpg_lot_genealogy_recall_tracer_signals(search_filter: str = "", max_rows: int = 25) -> Dict[str, Any]:
    """Reads live CPG multi-echelon records: Raw-material COA lot logs, MES batch genealogy (`03_plant_mes_oee_copacker_genealogy.csv`), WMS pallet SSCC scans, and DMS stockist dispatch invoices."""
    return sample_domain_records(DEPT_ID, filter_term=search_filter, limit=max_rows)


def run_lot_genealogy_recall_tracer_barrier_solver(search_filter: str = "") -> Dict[str, Any]:
    """Executes deterministic CPG optimization/audit math: Builds bidirectional lot containment graphs isolating only affected sub-batches instead of blanket multi-week plant recalls."""
    sampled = sample_domain_records(DEPT_ID, filter_term=search_filter, limit=40)
    kpis = compute_deterministic_kpis(AGENT_ID, DEPT_ID, sampled.get("sample_records", []))
    return {
        "agent_id": AGENT_ID,
        "agent_name": "2-Hour Lot Genealogy & Recall Tracer",
        "priority_tier": "P0",
        "source_table": sampled.get("source_table"),
        "using_full_200mb_lake": sampled.get("using_full_200mb_lake"),
        "kpi_summary": kpis,
        "top_records": sampled.get("sample_records", [])[:5],
    }


def stage_lot_genealogy_recall_tracer_erp_writeback(
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
    query_cpg_lot_genealogy_recall_tracer_signals,
    run_lot_genealogy_recall_tracer_barrier_solver,
    stage_lot_genealogy_recall_tracer_erp_writeback,
]
