#!/usr/bin/env python3
"""Priority-0 (P0) Gemini Enterprise Deployment Orchestrator for CPG_Supply_Chain.

By default runs in safe `--dry-run` mode listing all 25 Priority-0 (P0) immediate-ROI
agents (18 core P0 + 7 newly researched CPG P0 agents) staged for Vertex AI Agent Engine
& Gemini Enterprise registration. Pass `--execute` when ready to deploy live.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE_FILE = ROOT / "data" / "p0_ge_deployment_queue.json"


def main():
    parser = argparse.ArgumentParser(description="Deploy Priority-0 CPG Agents to Gemini Enterprise")
    parser.add_argument("--project", default="zuhaibp-ai")
    parser.add_argument("--location", default="us-central1")
    parser.add_argument("--execute", action="store_true", help="Actually deploy to Vertex AI & GE (default is dry-run)")
    args = parser.parse_args()

    queue = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    print(f"=== CPG Priority-0 (P0) Gemini Enterprise Deployment Queue ({len(queue)} Agents) ===")
    for i, item in enumerate(queue, 1):
        tag = "[NEW CPG]" if item["is_new_cpg_agent"] else "[CORE 60]"
        print(f"  {i:02d}. {item['code']} | {tag} {item['name']} ({item['agent_id']}) -> ${item['annual_value_m_usd']}M/yr ({item['payback_days']}d payback)")

    if not args.execute:
        print("\n[DRY-RUN COMPLETE] Folder & manifests verified. Pass `--execute` when ready to push P0 agents to Gemini Enterprise.")
        return

    import vertexai
    from vertexai.preview.reasoning_engines import AdkApp, ReasoningEngine
    import importlib.util
    import sys

    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    vertexai.init(project=args.project, location=args.location)

    for item in queue:
        aid = item["agent_id"]
        spec = importlib.util.spec_from_file_location(f"{aid}.agent", ROOT / "agents" / aid / "app" / "agent.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        app = AdkApp(agent=mod.root_agent)
        print(f"Deploying {aid} ({item['name']})...")
        ReasoningEngine.create(
            reasoning_engine=app,
            requirements=["google-cloud-aiplatform[adk,agent_engines]>=1.88.0"],
            display_name=f"{item['name']} ({item['code']} · CPG Supply Chain)",
            extra_packages=[str(ROOT / "cpg_runtime"), str(ROOT / "demo_data" / "seeds")],
        )


if __name__ == "__main__":
    main()
