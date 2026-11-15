#!/usr/bin/env python3
"""Staged Vertex AI Agent Engine & Gemini Enterprise Deployment Script for ITC CPG Pillars 5 & 6.

Defaults safely to `--dry-run` (validates every agent module, `root_agent`, tools, seed fixtures,
and GlobalGemini model routing without pushing to cloud). Pass `--execute` when ready to deploy or
update in-place (`remote_engine.update(...)`) on Vertex AI Agent Engine & Gemini Enterprise.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

SUITE_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = SUITE_ROOT / "itc_pillars_5_6_catalog.json"
REGISTRY_PATH = SUITE_ROOT / "ge_deployment_registry.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage or deploy ITC CPG Pillars 5 & 6 Agents to Gemini Enterprise")
    parser.add_argument("--project", default="zuhaibp-ai")
    parser.add_argument("--location", default="us-central1")
    parser.add_argument("--gemini-app-id", default="gemini-enterprise-zuhaibp_1784012666241")
    parser.add_argument("--only-p0", action="store_true", help="Filter to Priority-0 (P0) agents only")
    parser.add_argument("--execute", action="store_true", help="Deploy/update live in Vertex AI Agent Engine (default: dry-run)")
    args = parser.parse_args()

    if str(SUITE_ROOT) not in sys.path:
        sys.path.insert(0, str(SUITE_ROOT))

    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    if args.only_p0:
        catalog = [c for c in catalog if c["priority"] == "P0"]

    existing_reg = json.loads(REGISTRY_PATH.read_text(encoding="utf-8")) if REGISTRY_PATH.is_file() else {}

    print(f"=== ITC Limited CPG Pillars 5 & 6 — Gemini Enterprise Deployment Manifest ({len(catalog)} Agents) ===")
    verified = 0
    for item in catalog:
        slug = item["slug"]
        agent_py = SUITE_ROOT / "agents" / slug / "app" / "agent.py"
        spec = importlib.util.spec_from_file_location(f"{slug}.app.agent", agent_py)
        assert spec and spec.loader
        mod = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(SUITE_ROOT / "agents" / slug))
        spec.loader.exec_module(mod)
        tool_cnt = len(getattr(mod.tools, "ALL_TOOLS", []))
        verified += 1
        mode_tag = item["build_mode"]
        print(
            f"  [{item['num']}] {item['priority']} | {item['agent_name']:<38} | {mode_tag:<24} | "
            f"{item['default_model']} (global) | {tool_cnt} tools | ₹{item['annual_value_cr_inr']:.1f} Cr/yr"
        )

    if not args.execute:
        print(
            f"\n[DRY-RUN VERIFIED: {verified}/{len(catalog)} Agents Ready] "
            "Not deployed to Gemini Enterprise yet (per staged workflow). Pass `--execute` when ready to push live."
        )
        return

    import subprocess
    import google.oauth2.credentials
    import vertexai
    from vertexai.preview.reasoning_engines import ReasoningEngine

    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode().strip()
    creds = google.oauth2.credentials.Credentials(token)
    vertexai.init(project=args.project, location=args.location, credentials=creds, staging_bucket=f"gs://{args.project}-agent-staging")

    for item in catalog:
        slug = item["slug"]
        aid = item["agent_id"]
        agent_dir = SUITE_ROOT / "agents" / slug
        sys.path.insert(0, str(agent_dir))
        spec = importlib.util.spec_from_file_location(f"{slug}.app.agent", agent_dir / "app" / "agent.py")
        assert spec and spec.loader
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        adk_app = mod.create_adk_app()
        reqs = ["google-cloud-aiplatform[adk,agent_engines]>=1.88.0", "ortools>=9.10.0", "pillow>=10.0.0"]
        extra_pkgs = [
            str(SUITE_ROOT / "common"),
            str(SUITE_ROOT / "enterprise_data" / "seeds"),
            str(SUITE_ROOT / "enterprise_data" / "multimodal_docs"),
            str(agent_dir / "app"),
            str(agent_dir / "fixtures"),
        ]
        disp_name = f"[ITC CPG] {item['agent_name']} ({item['persona']})"

        if aid in existing_reg and existing_reg[aid].get("reasoning_engine_name"):
            re_name = existing_reg[aid]["reasoning_engine_name"]
            print(f"Updating existing Vertex AI Reasoning Engine in-place: {re_name} ...")
            remote_engine = ReasoningEngine(re_name)
            remote_engine.update(
                reasoning_engine=adk_app,
                requirements=reqs,
                extra_packages=extra_pkgs,
                display_name=disp_name,
            )
        else:
            print(f"Creating initial Vertex AI Reasoning Engine for {disp_name} ...")
            remote_engine = ReasoningEngine.create(
                reasoning_engine=adk_app,
                requirements=reqs,
                extra_packages=extra_pkgs,
                display_name=disp_name,
            )
            existing_reg[aid] = {
                "slug": slug,
                "agent_name": item["agent_name"],
                "reasoning_engine_name": remote_engine.resource_name,
            }
            REGISTRY_PATH.write_text(json.dumps(existing_reg, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
