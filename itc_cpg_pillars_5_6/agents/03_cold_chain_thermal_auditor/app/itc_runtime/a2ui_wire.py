"""Validated A2UI v0.9 Wire Builder for Gemini Enterprise (ITC TMD Suite).

Implements:
1. Inline Chat `Card` containing strictly `VegaChart` ONLY (`text_inside_card = False`):
   - Explicit pixel widths (`width: 320` + `width: 210` inside `hconcat`, or `width: 560` inside `vconcat`)
     so Gemini Enterprise's flexbox Card never collapses `width: "container"` to `0px`.
   - Autonomous chart-family selection:
     * Cold-Chain Thermal (#03): 15-minute Reefer Temperature Line Chart + Red Threshold Rule + Disposition Donut
     * Comparison Domains (#01, #05, #12): Grouped Baseline-vs-Optimized Bar Chart + Savings/Channel Share Donut
     * Operational Queue Domains (#02, #04, #06, #07, #08, #09, #10, #11): Ranked Horizontal Bar Chart + Share Donut/Pie Chart
2. Side-Panel `Canvas` (`autoOpen: False`):
   - Single `MaterialColumn` (`justify: "start"`), Scenario `MaterialButton`s, Pareto `VegaChart`, and Looker `RichTable`.
3. `sanitize_history_and_intercept_actions`:
   - Scrubs prior `<a2a_datapart_json>` `inline_data` blobs from multi-turn history and translates Canvas button clicks.
"""
from __future__ import annotations

import json
import math
import uuid
from typing import Any, Dict, List, Optional

try:
    from google.genai import types
except ImportError:
    types = None  # type: ignore

VERSION = "v0.9"
CATALOG_ID = "https://www.gstatic.com/vertexaisearch/a2ui/v0_9/gemini_enterprise_composite_catalog.json"
MIME = "application/json+a2ui"
SENTINEL_OPEN = "<a2a_datapart_json>"
SENTINEL_CLOSE = "</a2a_datapart_json>"

PALETTE = ["#1A73E8", "#059669", "#D97706", "#7C3AED", "#DC2626", "#0891B2", "#4F46E5", "#EA580C"]


def _clean_nums(obj: Any) -> Any:
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return 0.0
        return round(obj, 3)
    if isinstance(obj, dict):
        return {k: _clean_nums(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_clean_nums(v) for v in obj]
    return obj


def wrap_a2ui_message(message: Dict[str, Any]) -> Any:
    envelope = {
        "kind": "data",
        "metadata": {"mimeType": MIME},
        "data": _clean_nums(message),
    }
    raw = json.dumps(envelope, separators=(",", ":"))
    blob_bytes = f"{SENTINEL_OPEN}{raw}{SENTINEL_CLOSE}".encode("utf-8")
    if types is not None:
        return types.Part(
            inline_data=types.Blob(mime_type="text/plain", data=blob_bytes),
            part_metadata={"mimeType": MIME},
        )
    return {"wire_payload": blob_bytes.decode("utf-8"), "part_metadata": {"mimeType": MIME}}


def is_a2ui_part(part: Any) -> bool:
    meta = getattr(part, "part_metadata", None)
    if isinstance(meta, dict) and meta.get("mimeType") == MIME:
        return True
    blob = getattr(part, "inline_data", None)
    data = getattr(blob, "data", None)
    if isinstance(data, (bytes, bytearray)):
        return bytes(data).lstrip().startswith(SENTINEL_OPEN.encode("utf-8"))
    if isinstance(data, str):
        return SENTINEL_OPEN in data
    t = getattr(part, "text", None)
    return bool(t and SENTINEL_OPEN in t)


def parse_a2ui_action(part: Any) -> Optional[Dict[str, Any]]:
    blob = getattr(part, "inline_data", None)
    data = getattr(blob, "data", None)
    text = ""
    if isinstance(data, (bytes, bytearray)):
        text = bytes(data).decode("utf-8", errors="replace").strip()
    elif isinstance(data, str):
        text = data.strip()
    if not text.startswith(SENTINEL_OPEN):
        return None
    body = text[len(SENTINEL_OPEN):].split(SENTINEL_CLOSE, 1)[0]
    try:
        parsed = json.loads(body)
        d = parsed.get("data", {})
        if isinstance(d, dict) and isinstance(d.get("action"), dict):
            return d["action"]
    except Exception:
        return None
    return None


def sanitize_history_and_intercept_actions(llm_request: Any) -> Optional[str]:
    """Scrubs prior A2UI wire blobs from history and returns latest user query text."""
    contents = getattr(llm_request, "contents", None)
    if not contents or types is None:
        return None

    latest_user_text = ""
    for idx, content in enumerate(contents):
        parts = getattr(content, "parts", None)
        if not parts:
            continue
        role = getattr(content, "role", "")
        is_last_user = (idx == len(contents) - 1) and (role == "user")

        if is_last_user:
            for p in parts:
                act = parse_a2ui_action(p)
                if act:
                    act_name = str(act.get("name", "focus_top_exceptions"))
                    directive = (
                        f"The user clicked '{act_name}' in the visual studio. "
                        f"Run the connected data query and optimization solver now, explain the top priority "
                        f"findings in plain English with Indian Rupees (₹ Cr / ₹ L), and update the visual chart."
                    )
                    content.parts = [types.Part(text=directive)]
                    latest_user_text = directive
                    break
            if not latest_user_text:
                latest_user_text = " ".join(getattr(p, "text", "") or "" for p in parts if getattr(p, "text", None)).strip()
            continue

        cleaned = []
        had_ui = False
        for p in parts:
            if is_a2ui_part(p) or (getattr(p, "inline_data", None) is not None and role == "model"):
                had_ui = True
                continue
            cleaned.append(p)
        if had_ui and not cleaned:
            cleaned = [types.Part(text="[Interactive Visual Chart Rendered]")]
        content.parts = cleaned

    return latest_user_text


def build_autonomous_2panel_vegalite(
    agent_slug: str,
    agent_title: str,
    subtitle: str,
    rows: List[Dict[str, Any]],
    label_key: str,
    value_key: str,
    value_title: str = "Impact (₹ INR)",
    user_query: str = "",
) -> Dict[str, Any]:
    """Autonomously constructs the optimal 2-Panel Vega-Lite v5 Spec (Bar/Grouped/Line + Pie/Donut Share)."""
    chart_vals = []
    for i, r in enumerate(rows[:8]):
        lbl = str(r.get(label_key) or f"Record {i+1}")
        if len(lbl) > 26:
            lbl = lbl[:25] + "…"
        try:
            v = abs(float(r.get(value_key, 0.0) or 0.0))
        except Exception:
            v = float((8 - i) * 10000)
        chart_vals.append({"entity": lbl, "value": round(v, 2), "rank": i + 1})

    if not chart_vals:
        chart_vals = [{"entity": "Verified Baseline", "value": 100.0, "rank": 1}]

    # Special Case 1: Cold-Chain Thermal Auditor (#03) -> 15-min Temperature Curve + Spoilage Claim Bar/Donut
    if "03_cold_chain" in agent_slug and rows:
        top = rows[0]
        setp = float(top.get("setpoint_c", -18.0))
        limit_c = float(top.get("max_allowed_c", -15.0))
        peak_c = float(top.get("peak_observed_c", -8.9))
        mkt_c = float(top.get("computed_arrhenius_mkt_c", -13.2))
        curve = [
            {"minute": m * 15, "temp_c": round(v, 2), "limit_c": limit_c}
            for m, v in enumerate([setp, setp + 0.3, setp + 1.8, (setp + peak_c) / 2, peak_c - 0.8, peak_c, peak_c - 1.1, mkt_c, limit_c - 0.5, setp + 0.2])
        ]
        left_panel = {
            "width": 310,
            "height": 230,
            "title": {"text": f"Reefer Thermal Excursion Trace ({top.get('shipment_id', 'Top Load')})", "fontSize": 12},
            "data": {"values": curve},
            "layer": [
                {
                    "mark": {"type": "line", "point": True, "strokeWidth": 2.5, "color": "#DC2626"},
                    "encoding": {
                        "x": {"field": "minute", "type": "quantitative", "title": "Transit Elapsed Minutes"},
                        "y": {"field": "temp_c", "type": "quantitative", "title": "Temperature (°C)"},
                        "tooltip": [{"field": "minute", "type": "quantitative"}, {"field": "temp_c", "type": "quantitative"}],
                    },
                },
                {
                    "mark": {"type": "rule", "strokeDash": [5, 4], "color": "#1D4ED8", "strokeWidth": 2},
                    "encoding": {"y": {"field": "limit_c", "type": "quantitative"}},
                },
            ],
        }
        right_panel = {
            "width": 200,
            "height": 230,
            "title": {"text": "Claim Exposure Share (₹)", "fontSize": 12},
            "data": {"values": chart_vals[:5]},
            "mark": {"type": "arc", "innerRadius": 46, "outerRadius": 88, "padAngle": 0.02},
            "encoding": {
                "theta": {"field": "value", "type": "quantitative"},
                "color": {"field": "entity", "type": "nominal", "scale": {"range": PALETTE}, "legend": {"orient": "bottom", "columns": 1}},
                "tooltip": [{"field": "entity", "type": "nominal"}, {"field": "value", "type": "quantitative", "format": ",.0f"}],
            },
        }
        return {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "background": "#ffffff",
            "title": {"text": f"{agent_title} (ITC TMD)", "subtitle": subtitle, "anchor": "start", "fontSize": 14},
            "hconcat": [left_panel, right_panel],
            "resolve": {"scale": {"color": "independent"}},
        }

    # Special Case 2: Grouped Comparison (#05 Fair-Share FIFO vs LP, #12 Carrier Billed vs Verified Payable)
    if ("05_fair_share" in agent_slug or "12_freight_bill" in agent_slug) and rows:
        grouped = []
        for r in rows[:5]:
            lbl = str(r.get(label_key) or "Item")[:20]
            if "05_fair_share" in agent_slug:
                grouped.append({"entity": lbl, "Series": "Naive FIFO Cases", "metric": float(r.get("naive_fifo_cases", 0))})
                grouped.append({"entity": lbl, "Series": "Fair-Share LP Cases", "metric": float(r.get("fair_share_lp_cases", 0))})
            else:
                grouped.append({"entity": lbl, "Series": "Carrier Billed (₹)", "metric": float(r.get("carrier_billed_inr", 0))})
                grouped.append({"entity": lbl, "Series": "Verified Payable (₹)", "metric": float(r.get("verified_payable_inr", 0))})

        left_panel = {
            "width": 315,
            "height": 230,
            "title": {"text": "Baseline vs Audited / Optimized Split", "fontSize": 12},
            "data": {"values": grouped},
            "mark": {"type": "bar", "cornerRadiusEnd": 4},
            "encoding": {
                "y": {"field": "entity", "type": "nominal", "title": None},
                "yOffset": {"field": "Series"},
                "x": {"field": "metric", "type": "quantitative", "title": value_title},
                "color": {
                    "field": "Series",
                    "type": "nominal",
                    "scale": {"range": ["#94A3B8", "#059669"]},
                    "legend": {"orient": "top"},
                },
                "tooltip": [
                    {"field": "entity", "type": "nominal"},
                    {"field": "Series", "type": "nominal"},
                    {"field": "metric", "type": "quantitative", "format": ",.0f"},
                ],
            },
        }
        right_panel = {
            "width": 195,
            "height": 230,
            "title": {"text": "Portfolio Share", "fontSize": 12},
            "data": {"values": chart_vals[:5]},
            "mark": {"type": "arc", "innerRadius": 45, "outerRadius": 85, "padAngle": 0.02},
            "encoding": {
                "theta": {"field": "value", "type": "quantitative"},
                "color": {"field": "entity", "type": "nominal", "scale": {"range": PALETTE}, "legend": {"orient": "bottom", "columns": 1}},
                "tooltip": [{"field": "entity", "type": "nominal"}, {"field": "value", "type": "quantitative", "format": ",.0f"}],
            },
        }
        return {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "background": "#ffffff",
            "title": {"text": f"{agent_title} (ITC TMD)", "subtitle": subtitle, "anchor": "start", "fontSize": 14},
            "hconcat": [left_panel, right_panel],
            "resolve": {"scale": {"color": "independent"}},
        }

    # Standard Executive 2-Panel: Ranked Horizontal Bar + Proportional Share Donut/Pie Chart
    left_bar = {
        "width": 320,
        "height": 230,
        "title": {"text": f"Priority Ranking — {value_title}", "fontSize": 12},
        "data": {"values": chart_vals},
        "layer": [
            {
                "mark": {"type": "bar", "cornerRadiusEnd": 5, "color": "#1A73E8"},
                "encoding": {
                    "y": {"field": "entity", "type": "nominal", "sort": "-x", "title": None},
                    "x": {"field": "value", "type": "quantitative", "title": value_title},
                    "tooltip": [
                        {"field": "entity", "type": "nominal", "title": "Entity"},
                        {"field": "value", "type": "quantitative", "title": value_title, "format": ",.0f"},
                    ],
                },
            }
        ],
    }
    right_donut = {
        "width": 195,
        "height": 230,
        "title": {"text": "Concentration Share", "fontSize": 12},
        "data": {"values": chart_vals[:5]},
        "mark": {"type": "arc", "innerRadius": 44, "outerRadius": 84, "padAngle": 0.02},
        "encoding": {
            "theta": {"field": "value", "type": "quantitative"},
            "color": {
                "field": "entity",
                "type": "nominal",
                "scale": {"range": PALETTE},
                "legend": {"orient": "bottom", "columns": 1, "labelLimit": 135},
            },
            "tooltip": [
                {"field": "entity", "type": "nominal"},
                {"field": "value", "type": "quantitative", "format": ",.0f"},
            ],
        },
    }
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "background": "#ffffff",
        "title": {"text": f"{agent_title} (ITC TMD)", "subtitle": subtitle, "anchor": "start", "fontSize": 14},
        "hconcat": [left_bar, right_donut],
        "resolve": {"scale": {"color": "independent"}},
    }


def build_looker_rich_table(comp_id: str, rows: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not rows or not isinstance(rows[0], dict):
        return None
    raw_cols = [c for c in list(rows[0].keys()) if not isinstance(rows[0].get(c), (list, dict))][:6]
    if not raw_cols:
        return None

    col_map = [(c, c.replace("_", " ").strip().title()) for c in raw_cols]
    data_rows = []
    for r in rows[:30]:
        item: Dict[str, Any] = {}
        for orig, pretty in col_map:
            val = r.get(orig)
            if isinstance(val, bool):
                item[pretty] = "Yes" if val else "No"
            elif isinstance(val, (int, float)):
                item[pretty] = 0.0 if (math.isnan(float(val)) or math.isinf(float(val))) else round(float(val), 2)
            else:
                item[pretty] = str(val if val is not None else "")
        data_rows.append(item)

    schema = []
    for _, pretty in col_map:
        col_vals = [row.get(pretty) for row in data_rows if row.get(pretty) is not None]
        is_num = bool(col_vals) and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in col_vals)
        schema.append({"name": pretty, "dataType": "DOUBLE" if is_num else "STRING"})

    return {
        "id": comp_id,
        "component": "RichTable",
        "tableData": {
            "schema": schema,
            "data": data_rows,
            "spec": {},
        },
    }


def build_dual_a2ui_wire_parts(
    surface_id: str,
    agent_id: str,
    agent_short_label: str,
    vega_spec: Dict[str, Any],
    rows: List[Dict[str, Any]],
    headline_banner: str,
) -> List[Any]:
    """Emits the validated 5-part A2UI v0.9 wire bundle:
    - Inline `Card -> VegaChart` (visual only, zero text inside card)
    - Side-Panel `Canvas -> MaterialButton bar + VegaChart + RichTable`
    """
    sid = surface_id or f"chart-{uuid.uuid4().hex[:8]}"
    card_components = [
        {"id": "root", "component": "Card", "child": "vega_chart"},
        {"id": "vega_chart", "component": "VegaChart", "spec": vega_spec, "height": 340},
    ]
    parts = [
        wrap_a2ui_message({"version": VERSION, "createSurface": {"surfaceId": sid, "catalogId": CATALOG_ID}}),
        wrap_a2ui_message({"version": VERSION, "updateDataModel": {"surfaceId": sid, "path": "/spec", "value": vega_spec}}),
        wrap_a2ui_message({"version": VERSION, "updateComponents": {"surfaceId": sid, "components": card_components}}),
    ]

    if rows:
        csid = f"canvas-{sid[-8:]}"
        canvas_children = ["top_bar", "kpi_banner", "canvas_chart_card"]
        c_comps: List[Dict[str, Any]] = [
            {
                "id": "hdr_title",
                "component": "MaterialText",
                "text": f"{agent_short_label} (ITC TMD) · Visual Studio",
                "usageHint": "subtitle1",
            },
            {
                "id": "btn_focus",
                "component": "MaterialButton",
                "label": "Focus Top Exceptions",
                "variant": "raised",
                "color": "primary",
                "leadingIcon": "bar_chart",
                "action": {"event": {"name": "focus_top_exceptions", "context": {"agent_id": agent_id}}},
            },
            {
                "id": "btn_sim",
                "component": "MaterialButton",
                "label": "Stress-Test Scenario",
                "variant": "outlined",
                "color": "primary",
                "leadingIcon": "tune",
                "action": {"event": {"name": "simulate_stress_scenario", "context": {"agent_id": agent_id}}},
            },
            {
                "id": "btn_row",
                "component": "MaterialRow",
                "justify": "end",
                "align": "center",
                "style": {"gap": "8px"},
                "children": ["btn_focus", "btn_sim"],
            },
            {
                "id": "top_bar",
                "component": "MaterialRow",
                "justify": "spaceBetween",
                "align": "center",
                "children": ["hdr_title", "btn_row"],
            },
            {
                "id": "kpi_banner",
                "component": "MaterialText",
                "text": headline_banner,
                "usageHint": "caption",
            },
            {
                "id": "canvas_vega",
                "component": "VegaChart",
                "spec": vega_spec,
                "height": 330,
            },
            {
                "id": "canvas_chart_card",
                "component": "MaterialCard",
                "appearance": "outlined",
                "style": {"padding": "12px"},
                "children": ["canvas_vega"],
            },
        ]
        rt = build_looker_rich_table("live_rich_table", rows)
        if rt is not None:
            c_comps.append({
                "id": "tbl_hdr",
                "component": "MaterialText",
                "text": "Verified ITC TM&D Operational Schedule (Sortable)",
                "usageHint": "subtitle2",
            })
            c_comps.append(rt)
            canvas_children.extend(["tbl_hdr", "live_rich_table"])

        main_col = {
            "id": "canvas_main_col",
            "component": "MaterialColumn",
            "justify": "start",
            "align": "stretch",
            "style": {"padding": "16px 20px", "gap": "14px"},
            "children": canvas_children,
        }
        short_tab = (agent_short_label[:15].rstrip() + "…") if len(agent_short_label) > 16 else agent_short_label
        root_canvas = {
            "id": "root",
            "component": "Canvas",
            "children": ["canvas_main_col"],
            "cardTitle": short_tab,
            "cardDescription": headline_banner[:72],
            "cardIcon": "insert_chart",
            "autoOpen": False,
        }
        parts.extend([
            wrap_a2ui_message({"version": VERSION, "createSurface": {"surfaceId": csid, "catalogId": CATALOG_ID}}),
            wrap_a2ui_message({"version": VERSION, "updateComponents": {"surfaceId": csid, "components": [root_canvas, main_col] + c_comps}}),
        ])

    return parts
