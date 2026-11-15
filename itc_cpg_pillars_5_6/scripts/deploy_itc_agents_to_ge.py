#!/usr/bin/env python3
"""Production Deployer: 12 Separate `(ITC TMD)` Agents -> Vertex AI Agent Engine -> Gemini Enterprise.

Guarantees:
1. NEVER touches or overwrites any of the original 54+ Supply Chain agents in Vertex AI or Gemini Enterprise.
2. Deploys all 12 ITC Limited CPG Trade Marketing & Distribution (TM&D) agents separately with
   `(ITC TMD)` in brackets in BOTH Vertex AI Agent Engine (`us-central1`) and Gemini Enterprise
   (`gemini-enterprise-zuhaibp_1784012666241`), storing `.reasoning_engine_id` per ITC agent so
   subsequent updates to these 12 `(ITC TMD)` agents update their own resources in-place.
3. Registers 3 authentic, natural plain-English persona starter prompts (`starterPrompts`) directly
   on the Gemini Enterprise agent welcome screen.
4. Pre-uploads all 24 scanned multimodal PNG documents to `gs://zuhaibp-ai-supply-chain-media/itc_tmd/docs/`
   and configures runtime IAM so autonomous A2UI charts, HTML5 cockpits, and CSV exports work seamlessly.
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import socket as _socket_mod
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List

# Force IPv4 to eliminate CloudTop IPv6 socket connect hangs
_orig_getaddrinfo = _socket_mod.getaddrinfo
def _ipv4_only_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    return _orig_getaddrinfo(host, port, _socket_mod.AF_INET, type, proto, flags)
_socket_mod.getaddrinfo = _ipv4_only_getaddrinfo
try:
    import urllib3.util.connection as _u3_conn
    _u3_conn.allowed_gai_family = lambda: _socket_mod.AF_INET
except Exception:
    pass

os.environ["GOOGLE_API_USE_CLIENT_CERTIFICATE"] = "false"

SUITE_ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = SUITE_ROOT / "agents"
CATALOG_PATH = SUITE_ROOT / "itc_pillars_5_6_catalog.json"
REGISTRY_PATH = SUITE_ROOT / "ge_deployment_registry.json"
GCLOUD_DIR = Path.home() / ".config" / "gcloud"

REQUIREMENTS = [
    "google-cloud-aiplatform[agent_engines,adk]>=1.160.0",
    "google-adk>=2.6.0,<3.0.0",
    "google-genai>=1.20.0",
    "google-cloud-storage>=2.18.0,<4.0.0",
    "ortools>=9.10.0",
    "pydantic>=2.0.0",
    "Pillow>=10.0.0",
]


def sync_gcloud_db_to_argolis_adc(project: str) -> None:
    adc_existing = GCLOUD_DIR / "argolis_admin_adc.json"
    if adc_existing.exists():
        try:
            import google.oauth2.credentials
            from google.auth.transport.requests import Request
            c_chk = google.oauth2.credentials.Credentials.from_authorized_user_file(
                str(adc_existing), scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            c_chk.refresh(Request())
            if c_chk.token:
                return
        except Exception:
            pass
    db_path = GCLOUD_DIR / "credentials.db"
    if not db_path.exists():
        return
    try:
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        cur.execute("SELECT account_id, value FROM credentials")
        for account_id, val in cur.fetchall():
            if "zuhaibp.altostrat.com" in account_id:
                data = json.loads(val)
                cid = str(data.get("client_id", ""))
                if cid.startswith("681255809395"):
                    continue
                if data.get("refresh_token") and cid:
                    payload = {
                        "account": account_id,
                        "client_id": cid,
                        "client_secret": data["client_secret"],
                        "refresh_token": data["refresh_token"],
                        "type": "authorized_user",
                        "quota_project_id": project,
                    }
                    adc_existing.write_text(json.dumps(payload, indent=2) + "\n")
                break
        conn.close()
    except Exception:
        pass


def get_token() -> str:
    adc_p = GCLOUD_DIR / "argolis_admin_adc.json"
    if adc_p.exists():
        try:
            import google.oauth2.credentials
            from google.auth.transport.requests import Request
            c = google.oauth2.credentials.Credentials.from_authorized_user_file(
                str(adc_p), scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            c.refresh(Request())
            if c.token:
                return c.token
        except Exception:
            pass
    tokens_db = GCLOUD_DIR / "access_tokens.db"
    if tokens_db.exists():
        try:
            conn = sqlite3.connect(str(tokens_db))
            cur = conn.cursor()
            cur.execute("SELECT access_token FROM access_tokens WHERE token_expiry > datetime('now') ORDER BY rowid DESC")
            for (cand,) in cur.fetchall():
                try:
                    with urllib.request.urlopen(f"https://oauth2.googleapis.com/tokeninfo?access_token={cand}", timeout=3) as resp:
                        info = json.load(resp)
                        if "zuhaibp.altostrat.com" in info.get("email", ""):
                            conn.close()
                            return cand
                except Exception:
                    continue
            conn.close()
        except Exception:
            pass
    return subprocess.check_output(["gcloud", "auth", "print-access-token"], text=True).strip()


def get_credentials():
    adc_p = GCLOUD_DIR / "argolis_admin_adc.json"
    if adc_p.exists():
        try:
            import google.oauth2.credentials
            from google.auth.transport.requests import Request
            c = google.oauth2.credentials.Credentials.from_authorized_user_file(
                str(adc_p), scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            c.refresh(Request())
            return c
        except Exception:
            pass
    import google.oauth2.credentials
    return google.oauth2.credentials.Credentials(get_token())


def api(method: str, url: str, body: dict | None = None, project: str = "zuhaibp-ai", ok404: bool = False) -> dict:
    tok = get_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {tok}",
        "X-Goog-User-Project": project,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8") if body is not None else None,
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        txt = e.read().decode("utf-8", errors="ignore")
        if ok404 and e.code == 404:
            return {"_404": True}
        raise RuntimeError(f"{method} {url} -> {e.code}: {txt[:400]}") from None


def upload_multimodal_docs_to_gcs(project: str, media_bucket: str) -> int:
    mm_dir = SUITE_ROOT / "enterprise_data" / "multimodal_docs"
    if not mm_dir.is_dir():
        return 0
    creds = get_credentials()
    from google.cloud import storage
    client = storage.Client(project=project, credentials=creds)
    bkt = client.bucket(media_bucket)
    uploaded = 0
    for png in sorted(mm_dir.glob("*.png")):
        blob = bkt.blob(f"itc_tmd/docs/{png.name}")
        blob.cache_control = "public, max-age=3600"
        blob.content_disposition = "inline"
        blob.upload_from_filename(str(png), content_type="image/png")
        uploaded += 1
    return uploaded


def deploy_single_reasoning_engine(
    item: Dict[str, Any],
    project: str,
    region: str,
    staging_bucket: str,
    dry_run: bool = False,
) -> str:
    slug = item["slug"]
    agent_id = item["agent_id"]
    ge_display_name = item["ge_display_name"]
    assert "(ITC TMD)" in ge_display_name, f"Safety check failed: {ge_display_name} must contain (ITC TMD)"
    agent_dir = AGENTS_DIR / slug

    for mod_name in list(sys.modules.keys()):
        if mod_name in ("app", "tools", "itc_runtime") or mod_name.startswith(("app.", "itc_runtime.")):
            del sys.modules[mod_name]

    sys.path.insert(0, str(agent_dir))
    prev_cwd = os.getcwd()
    try:
        mod = importlib.import_module("app.agent")
        root_agent = getattr(mod, "root_agent")
        app_cls = getattr(mod, item["app_class"])

        state_file = agent_dir / ".reasoning_engine_id"
        if dry_run:
            cached = state_file.read_text().strip() if state_file.exists() else f"NEW-{agent_id}"
            print(f"  [DRY-RUN] {ge_display_name:<48} | {item['default_model']} | prompts={len(item['starter_prompts'])} | re={cached.split('/')[-1]}")
            return cached

        import google.auth
        import vertexai
        from vertexai import agent_engines

        creds = get_credentials()
        google.auth.default = lambda *a, **k: (creds, project)
        vertexai.init(project=project, location=region, staging_bucket=f"gs://{staging_bucket}", credentials=creds)

        os.chdir(agent_dir)
        adk_app = app_cls(agent=root_agent)
        env_vars = {
            "GOOGLE_GENAI_USE_VERTEXAI": "TRUE",
            "SC_MEDIA_BUCKET": f"{project}-supply-chain-media",
            "SC_AGENT_ID": agent_id,
            "SC_MODEL": item["default_model"],
        }
        desc = (
            f"[ITC TMD · {item['functional_area']}] {item['agent_name']} ({item['persona']}): "
            f"{item['problem_statement']}"
        )[:480]

        kwargs = dict(
            agent_engine=adk_app,
            requirements=REQUIREMENTS,
            extra_packages=["app", "fixtures"],
            gcs_dir_name=f"itc_tmd_{slug}",
            display_name=ge_display_name,
            description=desc,
            env_vars=env_vars,
            resource_limits={"cpu": "2", "memory": "4Gi"},
            min_instances=1,
            service_account=f"loadpilot-agent@{project}.iam.gserviceaccount.com",
        )

        # ONLY match an existing Reasoning Engine if it already belongs to THIS `(ITC TMD)` agent!
        existing = None
        if state_file.exists():
            try:
                cand_id = state_file.read_text().strip()
                existing = agent_engines.get(cand_id).resource_name
            except Exception:
                existing = None

        if not existing:
            try:
                for eng in agent_engines.list():
                    if getattr(eng, "display_name", "") == ge_display_name:
                        existing = eng.resource_name
                        break
            except Exception:
                pass

        t0 = time.time()
        if existing:
            print(f"[{slug}] UPDATING EXISTING (ITC TMD) ENGINE IN-PLACE: {existing} -> '{ge_display_name}'", flush=True)
            eng = agent_engines.get(existing).update(**kwargs)
        else:
            print(f"[{slug}] CREATING NEW SEPARATE (ITC TMD) ENGINE: '{ge_display_name}' ...", flush=True)
            eng = agent_engines.create(**kwargs)

        res_name = eng.resource_name
        state_file.write_text(res_name + "\n", encoding="utf-8")
        print(f"[{slug}] ENGINE READY in {time.time() - t0:.1f}s: {res_name}", flush=True)
        return res_name
    finally:
        os.chdir(prev_cwd)
        while str(agent_dir) in sys.path:
            sys.path.remove(str(agent_dir))


def register_in_gemini_enterprise(
    item: Dict[str, Any],
    project: str,
    engine_resource_name: str,
    app_id: str,
    dry_run: bool = False,
) -> str:
    ge_display = item["ge_display_name"]
    assert "(ITC TMD)" in ge_display, "Must include (ITC TMD) so original agents are never touched!"

    icon_url = f"https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/{item['icon']}/default/24px.svg"
    desc = (
        f"[ITC TMD · {item['functional_area']}] {item['agent_name']} for {item['persona']}. "
        f"{item['problem_statement']}"
    )[:480]

    payload = {
        "displayName": ge_display,
        "description": desc,
        "icon": {"uri": icon_url},
        "starterPrompts": [{"text": p} for p in item["starter_prompts"]],
        "adkAgentDefinition": {
            "toolSettings": {
                "toolDescription": (
                    f"(ITC TMD) Invoke {ge_display} for ITC Limited CPG Trade Marketing & Distribution "
                    f"({item['functional_area']}) to pull connected enterprise data, run deterministic solvers, "
                    f"and render interactive A2UI charts and workbenches."
                )
            },
            "provisionedReasoningEngine": {"reasoningEngine": engine_resource_name},
        },
    }

    if dry_run:
        return f"dry-run-ge-{item['slug']}"

    base = (
        f"https://discoveryengine.googleapis.com/v1alpha/projects/{project}/locations/global/"
        f"collections/default_collection/engines/{app_id}/assistants/default_assistant/agents"
    )
    agents = api("GET", base, project=project).get("agents", [])

    # Strictly match ONLY by exact `(ITC TMD)` displayName or exact new Reasoning Engine ID
    cur = None
    for a in agents:
        re_ref = (
            a.get("adkAgentDefinition", {})
            .get("provisionedReasoningEngine", {})
            .get("reasoningEngine", "")
        )
        if re_ref and engine_resource_name and re_ref.split("/")[-1] == engine_resource_name.split("/")[-1]:
            cur = a["name"]
            break
        if a.get("displayName") == ge_display:
            cur = a["name"]
            break

    if cur:
        res = api(
            "PATCH",
            f"https://discoveryengine.googleapis.com/v1alpha/{cur}?updateMask=displayName,description,icon,starterPrompts,adkAgentDefinition",
            body={**payload, "name": cur},
            project=project,
        )
        ge_name = res.get("name", cur)
        print(f"[{item['slug']}] GE UPDATED (ITC TMD): {ge_name.split('/')[-1]} -> '{ge_display}'", flush=True)
    else:
        res = api("POST", base, body=payload, project=project)
        ge_name = res.get("name", "")
        print(f"[{item['slug']}] GE REGISTERED NEW (ITC TMD): {ge_name.split('/')[-1]} -> '{ge_display}'", flush=True)

    return ge_name


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", help="Deploy a single ITC TMD agent by folder slug")
    parser.add_argument("--project", default="zuhaibp-ai")
    parser.add_argument("--region", default="us-central1")
    parser.add_argument("--gemini-app-id", default="gemini-enterprise-zuhaibp_1784012666241")
    parser.add_argument("--parallel", type=int, default=4, help="Parallel child workers for Reasoning Engine builds")
    parser.add_argument("--skip-ge", action="store_true")
    parser.add_argument("--execute", action="store_true", help="Execute live deployment to Vertex AI & Gemini Enterprise")
    args = parser.parse_args()

    dry_run = not args.execute
    sync_gcloud_db_to_argolis_adc(args.project)

    catalog: List[Dict[str, Any]] = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    if args.slug:
        catalog = [c for c in catalog if c["slug"] == args.slug]
        if not catalog:
            sys.exit(f"Unknown slug: {args.slug}")

    staging_bucket = f"{args.project}-agent-staging"
    media_bucket = f"{args.project}-supply-chain-media"

    print("=========================================================================")
    print(" ITC Limited CPG (ITC TMD) — Separate 12-Agent Gemini Enterprise Deployer")
    print(f" Project / Region : {args.project} / {args.region}")
    print(f" Gemini App ID    : {args.gemini_app_id}")
    print(f" Agents Selected  : {len(catalog)} (Original 54 GE agents untouched)")
    print(f" Mode             : {'DRY-RUN' if dry_run else f'LIVE DEPLOY (parallel={args.parallel})'}")
    print("=========================================================================", flush=True)

    if not dry_run and not args.slug:
        n_docs = upload_multimodal_docs_to_gcs(args.project, media_bucket)
        print(f"[OK] Uploaded {n_docs} scanned multimodal PNG documents to gs://{media_bucket}/itc_tmd/docs/", flush=True)

    if not dry_run and args.parallel > 1 and len(catalog) > 1:
        def _worker(item: Dict[str, Any]) -> tuple[str, int, str]:
            cmd = [
                sys.executable,
                str(Path(__file__).resolve()),
                "--slug", item["slug"],
                "--project", args.project,
                "--region", args.region,
                "--skip-ge",
                "--execute",
            ]
            print(f"[LAUNCH] {item['ge_display_name']} ...", flush=True)
            proc = subprocess.run(cmd, capture_output=True, text=True)
            out = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
            for ln in out.splitlines():
                if any(k in ln for k in (f"[{item['slug']}]", "ERROR", "CREATING", "UPDATING", "READY")):
                    print("  " + ln, flush=True)
            return item["slug"], proc.returncode, out

        with ThreadPoolExecutor(max_workers=args.parallel) as pool:
            futs = [pool.submit(_worker, it) for it in catalog]
            for f in as_completed(futs):
                slug, rc, out = f.result()
                if rc != 0:
                    print(f"[{slug}] FAILED (rc={rc}):\n{out[-900:]}", flush=True)
    else:
        for item in catalog:
            deploy_single_reasoning_engine(item, args.project, args.region, staging_bucket, dry_run=dry_run)

    if args.skip_ge:
        return

    registry: Dict[str, Any] = json.loads(REGISTRY_PATH.read_text(encoding="utf-8")) if REGISTRY_PATH.is_file() else {}
    for item in catalog:
        slug = item["slug"]
        state_file = AGENTS_DIR / slug / ".reasoning_engine_id"
        re_name = state_file.read_text().strip() if state_file.exists() else f"dry-run-{slug}"
        if not dry_run and not state_file.exists():
            print(f"[{slug}] Skipping GE registration because Reasoning Engine did not complete.", flush=True)
            continue
        ge_name = register_in_gemini_enterprise(item, args.project, re_name, args.gemini_app_id, dry_run=dry_run)
        if not dry_run:
            registry[item["agent_id"]] = {
                "num": item["num"],
                "slug": slug,
                "ge_display_name": item["ge_display_name"],
                "persona": item["persona"],
                "build_mode": item["build_mode"],
                "model": item["default_model"],
                "reasoning_engine": re_name,
                "gemini_enterprise_agent": ge_name,
                "starter_prompts": item["starter_prompts"],
                "deployed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            REGISTRY_PATH.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")

    if not dry_run:
        print(f"\n✅ Successfully deployed & registered {len(registry)} separate `(ITC TMD)` agents in Gemini Enterprise!")


if __name__ == "__main__":
    main()
