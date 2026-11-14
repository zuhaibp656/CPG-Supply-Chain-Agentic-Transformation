"""Deterministic CPG Data Lake & Governed MCP Tools for Aisle-Aligned Pallet (aisle_aligned_pallet_agent)."""
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

AGENT_ID = "aisle_aligned_pallet_agent"
DEPT_ID = "logistics_fleet"
STOPS_AT = "Never commits unapproved Oracle OTM ledger mutations or overrides safety/contract policy without human sign-off."


def query_cpg_aisle_aligned_pallet_agent_signals(search_filter: str = "", max_rows: int = 25) -> Dict[str, Any]:
    """Reads live CPG multi-echelon records: Eliminates volumetric chargeable-weight penalties via 3D fuselage contour & CoG packing Connected CPG systems: Oracle OTM · SAP TM · NIC E-Way API."""
    return sample_domain_records(DEPT_ID, filter_term=search_filter, limit=max_rows)


def run_aisle_aligned_pallet_agent_barrier_solver(search_filter: str = "") -> Dict[str, Any]:
    """Executes deterministic CPG optimization/audit math: Optimizes BSA forwarder commitments, passenger belly consolidations & spot charters (Mathematical Optimization Solver (MILP / CP-SAT) 3D Contoured ULD (LD3/PMC) Weight-Balance Packer + Belly-vs-Charter Allotment MILP + ADS-B Flight Connection Guard)."""
    sampled = sample_domain_records(DEPT_ID, filter_term=search_filter, limit=40)
    kpis = compute_deterministic_kpis(AGENT_ID, DEPT_ID, sampled.get("sample_records", []))
    return {
        "agent_id": AGENT_ID,
        "agent_name": "Aisle-Aligned Pallet",
        "priority_tier": "P1",
        "source_table": sampled.get("source_table"),
        "using_full_200mb_lake": sampled.get("using_full_200mb_lake"),
        "kpi_summary": kpis,
        "top_records": sampled.get("sample_records", [])[:5],
    }


def stage_aisle_aligned_pallet_agent_erp_writeback(
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
    query_cpg_aisle_aligned_pallet_agent_signals,
    run_aisle_aligned_pallet_agent_barrier_solver,
    stage_aisle_aligned_pallet_agent_erp_writeback,
]
