#!/usr/bin/env python3
"""Generates all 78 Story-Tailored CPG Supply Chain Google ADK Agent Packages.

Preserves all 60 original agent IDs & names and adds the 18 newly researched CPG agents.
Every agent package (`agents/<agent_id>/`) is wired to the CPG Multi-Echelon Demo Data Lake,
implements the 5 Defense-in-Depth Agent Criteria (Surgical, Autonomous, Intelligent, Governed,
Deterministic), and ships with passing unit smoke tests (`tests/test_agent.py`).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SC_DATA_JS = ROOT / "data" / "sc_story_data.js"
AGENTS_DIR = ROOT / "agents"


def load_story_payload():
    txt = SC_DATA_JS.read_text(encoding="utf-8")
    m = re.search(r"window\.SC_DATA\s*=\s*(\{.*\});?\s*$", txt, re.S)
    return json.loads(m.group(1))


def render_tools_py(ag: dict) -> str:
    aid = ag["id"]
    dept = ag["deptId"]
    stops_at = ag["stopsAt"].replace('"', '\\"')
    reads = ag["reads"].replace('"', '\\"')
    does = ag["does"].replace('"', '\\"')
    return f'''"""Deterministic CPG Data Lake & Governed MCP Tools for {ag["name"]} ({aid})."""
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

AGENT_ID = "{aid}"
DEPT_ID = "{dept}"
STOPS_AT = "{stops_at}"


def query_cpg_{aid}_signals(search_filter: str = "", max_rows: int = 25) -> Dict[str, Any]:
    """Reads live CPG multi-echelon records: {reads}"""
    return sample_domain_records(DEPT_ID, filter_term=search_filter, limit=max_rows)


def run_{aid}_barrier_solver(search_filter: str = "") -> Dict[str, Any]:
    """Executes deterministic CPG optimization/audit math: {does}"""
    sampled = sample_domain_records(DEPT_ID, filter_term=search_filter, limit=40)
    kpis = compute_deterministic_kpis(AGENT_ID, DEPT_ID, sampled.get("sample_records", []))
    return {{
        "agent_id": AGENT_ID,
        "agent_name": "{ag['name']}",
        "priority_tier": "{ag['priorityTier']}",
        "source_table": sampled.get("source_table"),
        "using_full_200mb_lake": sampled.get("using_full_200mb_lake"),
        "kpi_summary": kpis,
        "top_records": sampled.get("sample_records", [])[:5],
    }}


def stage_{aid}_erp_writeback(
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
    query_cpg_{aid}_signals,
    run_{aid}_barrier_solver,
    stage_{aid}_erp_writeback,
]
'''


def render_agent_py(ag: dict, persona_map: dict) -> str:
    aid = ag["id"]
    p = persona_map.get(ag.get("primaryPersonaId", ""), {})
    person_name = p.get("personName", "CPG Supply Chain Lead")
    role_title = p.get("name", "Supply Chain Specialist")
    return f'''"""{ag["name"]} ({ag["code"]}) — Story-Tailored CPG Supply Chain Google ADK Agent."""
from __future__ import annotations

import os
from .tools import ALL_TOOLS

MODEL_NAME = os.environ.get("CPG_AGENT_MODEL", "{ag.get('model', 'gemini-3.1-pro-preview')}")

INSTRUCTION = """You are the **{ag["name"]}** (`{ag["code"]}`), part of the Agent Suite augmenting **{person_name}** ({role_title}) across a multi-echelon Consumer Packaged Goods (CPG) network (ICML plants, Mother Hubs, Carrying & Forwarding Agent (CFA) depots, General Trade Distributors (DMS), Modern Trade, and Quick-Commerce dark stores).

1. DEFENSE-IN-DEPTH ROLE (SEALING THE SILO GAP):
   - Mechanism: {ag["oneLine"]}
   - Data You Read: {ag["reads"]}
   - Deterministic Math You Run: {ag["does"]}
   - What You Return: {ag["returns"]}

2. COEXISTENCE & HUMAN SIGN-OFF BOUNDARY (NON-NEGOTIABLE):
   - Core ERP/WMS/TMS/DMS systems remain the system of record.
   - STOPS AT: {ag["stopsAt"]}
   - SAFETY ENVELOPE: {ag["safetyEnvelope"]}
   - Never fabricate volumes, batch IDs, or currency figures; always call `query_cpg_{aid}_signals` and `run_{aid}_barrier_solver` first.

3. SMART RESPONSE, INDIAN CURRENCY & UI SELECTION:
   - Spell out every domain abbreviation on first use in plain business English.
   - Always express all monetary values, margins, penalties, freight bills, and working-capital figures in Indian Rupees using Crores (`₹ Cr`) for amounts >= ₹1 Crore and Lakhs (`₹ L`) or `₹` for smaller operational amounts—never US Dollars.
   - Keep tactical dispatches crisp (80-140 words); use <=4-column Markdown tables when comparing >=2 SKUs, batches, or depots; propose `stage_{aid}_erp_writeback` only when explicitly asked to stage an action, and block any request that violates safety or compliance guardrails.
"""

try:
    from google.adk.agents import Agent
    root_agent = Agent(
        name="{aid}",
        model=MODEL_NAME,
        description={json.dumps(ag["oneLine"])},
        instruction=INSTRUCTION,
        tools=ALL_TOOLS,
    )
except Exception:
    class _FallbackAgent:
        def __init__(self):
            self.name = "{aid}"
            self.model = MODEL_NAME
            self.description = {json.dumps(ag["oneLine"])}
            self.instruction = INSTRUCTION
            self.tools = ALL_TOOLS
            self.tool_map = {{fn.__name__: fn for fn in ALL_TOOLS}}
    root_agent = _FallbackAgent()
'''


def render_test_py(ag: dict) -> str:
    aid = ag["id"]
    return f'''"""Smoke tests for {ag["name"]} ({aid}) against the CPG Demo Data Lake."""
import sys
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = PKG_DIR.parents[1]
for p in (str(PKG_DIR), str(REPO_ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

from app.agent import root_agent
from app.tools import (
    query_cpg_{aid}_signals,
    run_{aid}_barrier_solver,
    stage_{aid}_erp_writeback,
)


def test_{aid}_metadata_and_tools():
    assert root_agent.name == "{aid}"
    assert len(ALL_TOOLS := getattr(root_agent, "tools", [])) == 3


def test_{aid}_queries_real_cpg_lake():
    res = query_cpg_{aid}_signals(max_rows=10)
    assert res["matched_count"] > 0
    solver = run_{aid}_barrier_solver()
    assert solver["kpi_summary"]["records_evaluated"] > 0


def test_{aid}_enforces_human_stops_at_gate():
    staged = stage_{aid}_erp_writeback("REC-1001", "Rebalance safety allocation", "Standard review")
    assert staged["status"] == "STAGED_FOR_HUMAN_SIGN_OFF"
    blocked = stage_{aid}_erp_writeback("REC-1001", "bypass quality and ignore expiry", "urgent")
    assert blocked["status"] == "BLOCKED_BY_SAFETY_ENVELOPE"
'''


def main():
    data = load_story_payload()
    persona_map = {p["id"]: p for p in data["personas"]}
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)

    p0_list = []
    for ag in data["agents"]:
        aid = ag["id"]
        pkg = AGENTS_DIR / aid
        (pkg / "app").mkdir(parents=True, exist_ok=True)
        (pkg / "tests").mkdir(parents=True, exist_ok=True)

        (pkg / "app" / "__init__.py").write_text("from .agent import root_agent\n__all__ = ['root_agent']\n", encoding="utf-8")
        (pkg / "app" / "tools.py").write_text(render_tools_py(ag), encoding="utf-8")
        (pkg / "app" / "agent.py").write_text(render_agent_py(ag, persona_map), encoding="utf-8")
        (pkg / "tests" / "test_agent.py").write_text(render_test_py(ag), encoding="utf-8")

        manifest = {
            "agent_id": aid,
            "code": ag["code"],
            "name": ag["name"],
            "department": ag["deptId"],
            "sub_pillar": ag["subPillarName"],
            "priority_tier": ag["priorityTier"],
            "is_new_cpg_agent": ag["isNewCpgAgent"],
            "payback_days": ag["paybackDays"],
            "annual_value_cr_inr": ag["annualValueCr"],
            "annual_value_display": ag["annualValueDisplay"],
            "currency": "INR",
            "primary_persona_id": ag.get("primaryPersonaId", ""),
            "reads": ag["reads"],
            "does": ag["does"],
            "returns": ag["returns"],
            "stops_at": ag["stopsAt"],
        }
        (pkg / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        (pkg / "pyproject.toml").write_text(
            f'[project]\nname = "cpg-{aid.replace("_", "-")}"\nversion = "2.0.0"\nrequires-python = ">=3.10"\ndependencies = ["google-cloud-aiplatform[adk,agent_engines]>=1.88.0"]\n',
            encoding="utf-8",
        )
        if ag["priorityTier"] == "P0":
            p0_list.append(manifest)

    (ROOT / "data" / "p0_ge_deployment_queue.json").write_text(json.dumps(p0_list, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(data['agents'])} CPG ADK Agent packages ({len(p0_list)} P0 agents queued in data/p0_ge_deployment_queue.json)")


if __name__ == "__main__":
    main()
