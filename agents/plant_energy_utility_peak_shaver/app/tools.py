"""Deterministic CPG Data Lake & Governed MCP Tools for Plant Boiler & Tariff Peak-Shaver (plant_energy_utility_peak_shaver)."""
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

AGENT_ID = "plant_energy_utility_peak_shaver"
DEPT_ID = "manufacturing_prod"
STOPS_AT = "Changing pasteurization kill-step temperatures or overriding cold-room food-safety bounds."


def query_cpg_plant_energy_utility_peak_shaver_signals(search_filter: str = "", max_rows: int = 25) -> Dict[str, Any]:
    """Reads live CPG multi-echelon records: 15-min smart-meter kWh telemetry, state Time-of-Day electricity tariffs, solar output forecasts, and finite line schedule (`03_plant_mes_oee_copacker_genealogy.csv`)."""
    return sample_domain_records(DEPT_ID, filter_term=search_filter, limit=max_rows)


def run_plant_energy_utility_peak_shaver_barrier_solver(search_filter: str = "") -> Dict[str, Any]:
    """Executes deterministic CPG optimization/audit math: Shifts non-critical thermal/chiller pull-downs out of peak-tariff blocks via CP-SAT without delaying scheduled case output."""
    sampled = sample_domain_records(DEPT_ID, filter_term=search_filter, limit=40)
    kpis = compute_deterministic_kpis(AGENT_ID, DEPT_ID, sampled.get("sample_records", []))
    return {
        "agent_id": AGENT_ID,
        "agent_name": "Plant Boiler & Tariff Peak-Shaver",
        "priority_tier": "P1",
        "source_table": sampled.get("source_table"),
        "using_full_200mb_lake": sampled.get("using_full_200mb_lake"),
        "kpi_summary": kpis,
        "top_records": sampled.get("sample_records", [])[:5],
    }


def stage_plant_energy_utility_peak_shaver_erp_writeback(
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
    query_cpg_plant_energy_utility_peak_shaver_signals,
    run_plant_energy_utility_peak_shaver_barrier_solver,
    stage_plant_energy_utility_peak_shaver_erp_writeback,
]
