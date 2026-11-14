"""Deterministic CPG Data Lake & Governed MCP Tools for Phantom Inventory Sensor (planogram_merchandising_vision_auditor)."""
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

AGENT_ID = "planogram_merchandising_vision_auditor"
DEPT_ID = "inventory_warehouse"
STOPS_AT = "Never commits unapproved Manhattan WMS ledger mutations or overrides safety/contract policy without human sign-off."


def query_cpg_planogram_merchandising_vision_auditor_signals(search_filter: str = "", max_rows: int = 25) -> Dict[str, Any]:
    """Reads live CPG multi-echelon records: Automatically cleans, de-skews, and aligns wide-angle shelf photos uploaded by field reps Connected CPG systems: Manhattan WMS · SAP EWM · DMS Stock."""
    return sample_domain_records(DEPT_ID, filter_term=search_filter, limit=max_rows)


def run_planogram_merchandising_vision_auditor_barrier_solver(search_filter: str = "") -> Dict[str, Any]:
    """Executes deterministic CPG optimization/audit math: Counts brand facings, detects eye-level placements, and calculates exact Share-of-Shelf vs. competitors (Vertex AI Multimodal Vision Object & Facing Detection + Share-of-Shelf Planogram Compliance Classifier)."""
    sampled = sample_domain_records(DEPT_ID, filter_term=search_filter, limit=40)
    kpis = compute_deterministic_kpis(AGENT_ID, DEPT_ID, sampled.get("sample_records", []))
    return {
        "agent_id": AGENT_ID,
        "agent_name": "Phantom Inventory Sensor",
        "priority_tier": "P0",
        "source_table": sampled.get("source_table"),
        "using_full_200mb_lake": sampled.get("using_full_200mb_lake"),
        "kpi_summary": kpis,
        "top_records": sampled.get("sample_records", [])[:5],
    }


def stage_planogram_merchandising_vision_auditor_erp_writeback(
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
    query_cpg_planogram_merchandising_vision_auditor_signals,
    run_planogram_merchandising_vision_auditor_barrier_solver,
    stage_planogram_merchandising_vision_auditor_erp_writeback,
]
