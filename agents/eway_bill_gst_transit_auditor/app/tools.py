"""Deterministic CPG Data Lake & Governed MCP Tools for E-Way Bill & Transit Tax Compliance Shield (eway_bill_gst_transit_auditor)."""
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

AGENT_ID = "eway_bill_gst_transit_auditor"
DEPT_ID = "logistics_fleet"
STOPS_AT = "Submitting statutory tax declarations with unverified vehicle numbers."


def query_cpg_eway_bill_gst_transit_auditor_signals(search_filter: str = "", max_rows: int = 25) -> Dict[str, Any]:
    """Reads live CPG multi-echelon records: NIC E-Way Bill API validity timestamps, Samsara/GPS truck telemetry, SAP GST invoice HSN codes (`05_tms_shipments_eway_freight_audit.csv`)."""
    return sample_domain_records(DEPT_ID, filter_term=search_filter, limit=max_rows)


def run_eway_bill_gst_transit_auditor_barrier_solver(search_filter: str = "") -> Dict[str, Any]:
    """Executes deterministic CPG optimization/audit math: Flags trucks within 4 hours of E-Way Bill expiry due to highway congestion or breakdown and prepares Part-B extension drafts."""
    sampled = sample_domain_records(DEPT_ID, filter_term=search_filter, limit=40)
    kpis = compute_deterministic_kpis(AGENT_ID, DEPT_ID, sampled.get("sample_records", []))
    return {
        "agent_id": AGENT_ID,
        "agent_name": "E-Way Bill & Transit Tax Compliance Shield",
        "priority_tier": "P0",
        "source_table": sampled.get("source_table"),
        "using_full_200mb_lake": sampled.get("using_full_200mb_lake"),
        "kpi_summary": kpis,
        "top_records": sampled.get("sample_records", [])[:5],
    }


def stage_eway_bill_gst_transit_auditor_erp_writeback(
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
    query_cpg_eway_bill_gst_transit_auditor_signals,
    run_eway_bill_gst_transit_auditor_barrier_solver,
    stage_eway_bill_gst_transit_auditor_erp_writeback,
]
