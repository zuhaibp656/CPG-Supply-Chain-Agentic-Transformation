"""A2UI v0.9 VegaChart + RichTable Canvas Builder, CSV Exporter & Light-Theme HTML5 Cockpit Generator."""
from __future__ import annotations

import csv
import html
import io
import json
from pathlib import Path
from typing import Any, Dict, List


def build_a2ui_vega_and_canvas(
    agent_title: str,
    subtitle: str,
    rows: List[Dict[str, Any]],
    label_key: str,
    value_key: str,
    value_title_inr: str = "Impact (₹ INR)",
) -> Dict[str, Any]:
    """Builds a clean Vega-Lite v5 visual-only card spec + side-panel RichTable Canvas payload."""
    chart_data = []
    for idx, r in enumerate(rows[:8]):
        lbl = str(r.get(label_key) or f"Item {idx + 1}")[:34]
        try:
            val = float(r.get(value_key, 0.0) or 0.0)
        except Exception:
            val = float(idx + 1) * 10000.0
        chart_data.append({"entity": lbl, "metric_inr": round(val, 2)})

    vega_spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {"text": agent_title, "subtitle": subtitle, "anchor": "start", "fontSize": 15},
        "width": 520,
        "height": 260,
        "background": "#FFFFFF",
        "data": {"values": chart_data},
        "mark": {"type": "bar", "cornerRadiusEnd": 5, "color": "#1A73E8"},
        "encoding": {
            "y": {"field": "entity", "type": "nominal", "sort": "-x", "title": None},
            "x": {"field": "metric_inr", "type": "quantitative", "title": value_title_inr},
            "tooltip": [
                {"field": "entity", "type": "nominal", "title": "Entity"},
                {"field": "metric_inr", "type": "quantitative", "title": value_title_inr, "format": ",.0f"},
            ],
        },
    }

    return {
        "a2ui_version": "0.9",
        "card_component": "VegaChart",
        "text_inside_card": False,
        "vega_lite_spec": vega_spec,
        "canvas_rich_table": {
            "component": "RichTable",
            "title": f"{agent_title} — Verified Enterprise Ledger",
            "row_count": len(rows),
            "rows": rows[:15],
        },
    }


def export_verified_csv(agent_slug: str, rows: List[Dict[str, Any]], output_dir: Path) -> Dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / f"{agent_slug}_verified_schedule.csv"
    if not rows:
        out_file.write_text("status\nNO_ROWS\n", encoding="utf-8")
        return {"csv_path": str(out_file), "row_count": 0}

    cols = list(rows[0].keys())
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=cols)
    writer.writeheader()
    for r in rows:
        writer.writerow({k: (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in r.items()})
    out_file.write_text(buf.getvalue(), encoding="utf-8")
    return {
        "status": "CSV_EXPORT_READY",
        "csv_path": str(out_file),
        "row_count": len(rows),
        "columns": cols,
    }


def render_interactive_cockpit_html(
    agent_slug: str,
    agent_title: str,
    persona_title: str,
    functional_area: str,
    headline_metric_label: str,
    headline_metric_value: str,
    rows: List[Dict[str, Any]],
    output_dir: Path,
) -> Dict[str, Any]:
    """Compiles a self-contained Light-Theme Default (with Dark Toggle) Interactive HTML5 Cockpit."""
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / f"{agent_slug}_cockpit.html"
    cols = list(rows[0].keys())[:6] if rows else ["status"]

    th_html = "".join(f"<th>{html.escape(c.replace('_', ' ').title())}</th>" for c in cols)
    tr_html_list = []
    for r in rows[:15]:
        tds = "".join(f"<td>{html.escape(str(r.get(c, '')))}</td>" for c in cols)
        tr_html_list.append(f"<tr>{tds}</tr>")
    tbody_html = "\n".join(tr_html_list)

    doc = f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8" />
  <title>{html.escape(agent_title)} — ITC CPG TM&amp;D Cockpit</title>
  <style>
    :root {{
      --bg: #F8FAFC; --surface: #FFFFFF; --text: #0F172A; --muted: #475569;
      --border: #E2E8F0; --accent: #1A73E8; --emerald: #059669;
    }}
    html[data-theme="dark"] {{
      --bg: #0B1120; --surface: #111827; --text: #F8FAFC; --muted: #94A3B8;
      --border: #1E293B; --accent: #60A5FA; --emerald: #34D399;
    }}
    body {{ font-family: Inter, -apple-system, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 28px; }}
    .wrap {{ max-width: 1180px; margin: 0 auto; }}
    .hdr {{ display: flex; justify-content: space-between; align-items: center; background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 20px 24px; margin-bottom: 20px; }}
    .badge {{ font-size: 12px; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 0.06em; }}
    h1 {{ margin: 6px 0 4px; font-size: 24px; }}
    .kpi {{ background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 18px 22px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }}
    .kpi strong {{ font-size: 28px; color: var(--emerald); }}
    table {{ width: 100%; border-collapse: collapse; background: var(--surface); border-radius: 14px; overflow: hidden; border: 1px solid var(--border); }}
    th, td {{ text-align: left; padding: 12px 14px; border-bottom: 1px solid var(--border); font-size: 13px; }}
    th {{ font-weight: 700; color: var(--muted); background: rgba(26,115,232,0.05); }}
    button {{ cursor: pointer; border: 1px solid var(--border); background: var(--surface); color: var(--text); padding: 8px 14px; border-radius: 8px; font-weight: 600; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hdr">
      <div>
        <div class="badge">ITC Limited CPG · {html.escape(functional_area)}</div>
        <h1>{html.escape(agent_title)}</h1>
        <div style="color:var(--muted);font-size:14px;">Persona Owner: <strong>{html.escape(persona_title)}</strong></div>
      </div>
      <button onclick="document.documentElement.dataset.theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'">Toggle Light / Dark</button>
    </div>
    <div class="kpi">
      <div>
        <div style="font-size:13px;color:var(--muted);font-weight:600;">{html.escape(headline_metric_label)}</div>
        <div style="font-size:13px;color:var(--muted);">Deterministic Solver Output · Indian Rupees (₹ Crores / ₹ Lakhs)</div>
      </div>
      <strong>{html.escape(headline_metric_value)}</strong>
    </div>
    <table>
      <thead><tr>{th_html}</tr></thead>
      <tbody>{tbody_html}</tbody>
    </table>
  </div>
</body>
</html>"""
    out_file.write_text(doc, encoding="utf-8")
    return {
        "status": "HTML_COCKPIT_READY",
        "cockpit_path": str(out_file),
        "default_theme": "light",
    }
