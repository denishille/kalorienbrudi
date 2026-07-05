#!/usr/bin/env python3
"""
Kalorienbrudi + Naehrstoffbrudi Dashboard Generator
---------------------------------------------------
Zieht alle Eintraege aus ZWEI Notion-Datenbanken und erzeugt EINE statische
index.html mit Umschalter oben (Kalorien <-> Naehrstoffe).

  - Kalorien:   "Tagesuebersicht"      (eine Zeile pro Tag/Person)
  - Naehrstoffe:"Lebensmittel-Analyse"  (eine Zeile pro Lebensmittel)

Benoetigt nur die Python-Standardbibliothek (urllib) - kein pip install.

Env:
  NOTION_TOKEN   Notion Internal Integration Token (als GitHub-Secret hinterlegen)
"""

import os
import sys
import json
import datetime
import urllib.request
import urllib.error

# ----------------------------------------------------------------------------
# Konfiguration
# ----------------------------------------------------------------------------
DATA_SOURCE_KCAL = "a748d265-3bbe-448b-b4e8-c8111c208c46"   # Tagesuebersicht
DATA_SOURCE_NUTRI = "be09a702-364a-4f0f-9548-5f4f32092dee"  # Lebensmittel-Analyse
NOTION_VERSION = "2025-09-03"
TOKEN = os.environ.get("NOTION_TOKEN")

# --- Kalorien: pro Person fixe Einstellungen ---
PERSON_CONFIG = {
    "Denis": {"accent": "#4DA6FF", "accent2": "#1E6FD9", "deficitTarget": 1000,
              "greenBuf": 95, "zielWeight": 80, "goalIntake": 1900},
    "Leni":  {"accent": "#FF6FB5", "accent2": "#D94D92", "deficitTarget": 500,
              "greenBuf": 75, "zielWeight": 60, "goalIntake": 1500},
}

# --- Naehrstoffe: pro Person Geschlecht + Akzent (eigene Farben fuer die Seite) ---
NUTRI_CONFIG = {
    "Denis": {"sex": "m", "accent": "#4DA6FF", "accent2": "#1E6FD9"},
    "Leni":  {"sex": "w", "accent": "#FF6FB5", "accent2": "#D94D92"},
}

# Tages-Referenzwerte (DGE/D-A-CH, Erwachsene) je Geschlecht. Hier anpassbar.
REF = {
    "m": {
        "Ballaststoffe (g)": 30, "Calcium (mg)": 1000, "Eisen (mg)": 10,
        "Folat (µg)": 300, "Jod (µg)": 200, "Kalium (mg)": 4000,
        "Magnesium (mg)": 350, "Omega-3 (g)": 1.6, "Selen (µg)": 70,
        "Vitamin A (µg)": 850, "Vitamin B12 (µg)": 4, "Vitamin C (mg)": 110,
        "Vitamin D (µg)": 20, "Vitamin E (mg)": 14, "Vitamin K (µg)": 70,
        "Zink (mg)": 11,
    },
    "w": {
        "Ballaststoffe (g)": 30, "Calcium (mg)": 1000, "Eisen (mg)": 15,
        "Folat (µg)": 300, "Jod (µg)": 200, "Kalium (mg)": 4000,
        "Magnesium (mg)": 300, "Omega-3 (g)": 1.1, "Selen (µg)": 60,
        "Vitamin A (µg)": 700, "Vitamin B12 (µg)": 4, "Vitamin C (mg)": 95,
        "Vitamin D (µg)": 20, "Vitamin E (mg)": 12, "Vitamin K (µg)": 60,
        "Zink (mg)": 8,
    },
}
NUM_KEYS = list(REF["m"].keys()) + ["Cholesterin (mg)"]
CAT_KEYS = ["Darmgesundheit", "Low FODMAP", "Säure-Base"]


# ----------------------------------------------------------------------------
# Notion-Abfrage (mit Pagination) - parametrisiert auf die Datenquelle
# ----------------------------------------------------------------------------
def notion_query_all(data_source_id):
    url = "https://api.notion.com/v1/data_sources/%s/query" % data_source_id
    headers = {
        "Authorization": "Bearer %s" % TOKEN,
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    results, cursor = [], None
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                     headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            sys.stderr.write("Notion API Fehler %s: %s\n" % (e.code, e.read().decode("utf-8")))
            raise
        results.extend(data.get("results", []))
        if data.get("has_more"):
            cursor = data.get("next_cursor")
        else:
            break
    return results


def num(props, name):
    p = props.get(name)
    if not p:
        return None
    return p.get("number")


def select_name(props, name):
    p = props.get(name) or {}
    sel = p.get("select")
    return sel.get("name") if sel else None


def date_start(props, name):
    p = props.get(name) or {}
    d = p.get("date")
    return d.get("start")[:10] if d and d.get("start") else None


def title_text(props, name):
    """Titel-Property als Klartext, Mengenangabe in Klammern am Ende entfernt."""
    p = props.get(name) or {}
    arr = p.get("title") or []
    t = "".join(x.get("plain_text", "") for x in arr).strip()
    if t.endswith(")") and " (" in t:
        t = t.rsplit(" (", 1)[0]
    return t or None


# ----------------------------------------------------------------------------
# Kalorien-Daten aufbereiten
# ----------------------------------------------------------------------------
def build_kcal_data(pages):
    raw = {k: [] for k in PERSON_CONFIG}
    for pg in pages:
        props = pg.get("properties", {})
        person = select_name(props, "Person")
        if person not in raw:
            continue
        d = date_start(props, "Datum")
        kcal = num(props, "Kalorien (kcal)")
        if d is None or kcal is None:
            continue
        raw[person].append({
            "d": d,
            "kcal": kcal,
            "p": num(props, "Protein (g)") or 0,
            "c": num(props, "Kohlenhydrate (g)") or 0,
            "f": num(props, "Fett (g)") or 0,
            "goalIntake": num(props, "Kalorienziel (kcal)"),
            "weight": num(props, "Gewicht (kg)"),
            "zielWeight": num(props, "Zielgewicht"),
        })

    data = {}
    for person, cfg in PERSON_CONFIG.items():
        entries = sorted(raw[person], key=lambda x: x["d"])
        days = [{"d": e["d"], "kcal": e["kcal"], "p": e["p"], "c": e["c"], "f": e["f"]}
                for e in entries]
        goal = next((e["goalIntake"] for e in reversed(entries) if e["goalIntake"]), cfg["goalIntake"])
        weights = [e["weight"] for e in entries if e["weight"] is not None]
        weight = weights[-1] if weights else None
        start_weight = weights[0] if weights else weight
        ziel = next((e["zielWeight"] for e in reversed(entries) if e["zielWeight"]), cfg["zielWeight"])
        weighted = [(e["d"], e["weight"]) for e in entries if e["weight"] is not None]
        if weighted:
            anchor_weight = min(w for _, w in weighted)
            anchor_date = min(d for d, w in weighted if w == anchor_weight)
        else:
            anchor_weight, anchor_date = None, None
        data[person] = {
            "accent": cfg["accent"], "accent2": cfg["accent2"],
            "goalIntake": goal, "deficitTarget": cfg["deficitTarget"],
            "weight": weight, "startWeight": start_weight,
            "zielWeight": ziel, "greenBuf": cfg["greenBuf"],
            "anchorWeight": anchor_weight, "anchorDate": anchor_date,
            "days": days,
        }
    return data


# ----------------------------------------------------------------------------
# Naehrstoff-Daten aufbereiten: pro Person -> pro Tag aggregiert
# cf = pro Kategorie [positive Lebensmittel, negative Lebensmittel] des Tages
# ----------------------------------------------------------------------------
def build_nutri_data(pages):
    raw = {k: [] for k in NUTRI_CONFIG}
    for pg in pages:
        props = pg.get("properties", {})
        person = select_name(props, "Person")
        if person not in raw:
            continue
        d = date_start(props, "Datum")
        if d is None:
            continue
        rec = {"d": d, "name": title_text(props, "Lebensmittel")}
        for k in NUM_KEYS:
            rec[k] = num(props, k) or 0
        for c in CAT_KEYS:
            rec[c] = select_name(props, c)
        raw[person].append(rec)

    data = {}
    for person, cfg in NUTRI_CONFIG.items():
        bydate = {}
        for e in raw[person]:
            day = bydate.get(e["d"])
            if day is None:
                day = {"d": e["d"], "n": 0,
                       "nut": {k: 0 for k in NUM_KEYS},
                       "cat": {c: [0, 0, 0] for c in CAT_KEYS},
                       "cf": {c: [[], []] for c in CAT_KEYS}}
                bydate[e["d"]] = day
            day["n"] += 1
            for k in NUM_KEYS:
                day["nut"][k] += e[k]
            nm = e.get("name")
            for c in CAT_KEYS:
                v = e[c]
                if v == "gut":
                    day["cat"][c][0] += 1
                    if nm:
                        day["cf"][c][0].append(nm)
                elif v == "neutral":
                    day["cat"][c][1] += 1
                elif v == "schlecht":
                    day["cat"][c][2] += 1
                    if nm:
                        day["cf"][c][1].append(nm)
        days = [bydate[k] for k in sorted(bydate)]
        data[person] = {
            "accent": cfg["accent"], "accent2": cfg["accent2"],
            "ref": REF[cfg["sex"]],
            "days": days,
        }
    return data


# ----------------------------------------------------------------------------
# Hauptlogik
# ----------------------------------------------------------------------------
def main():
    if not TOKEN:
        sys.stderr.write("Fehler: NOTION_TOKEN ist nicht gesetzt.\n")
        sys.exit(1)
    kcal = build_kcal_data(notion_query_all(DATA_SOURCE_KCAL))
    nutri = build_nutri_data(notion_query_all(DATA_SOURCE_NUTRI))
    today_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    today_de = datetime.datetime.now(datetime.timezone.utc).strftime("%d.%m.%Y")
    html = (HTML_TEMPLATE
            .replace("__DATA_KCAL__", json.dumps(kcal, ensure_ascii=False))
            .replace("__DATA_NUTRI__", json.dumps(nutri, ensure_ascii=False))
            .replace("__TODAY_ISO__", today_iso)
            .replace("__BUILD_DATE__", today_de))
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html geschrieben. Kalorien Denis %d / Leni %d | Naehrstoffe Denis %d / Leni %d"
          % (len(kcal["Denis"]["days"]), len(kcal["Leni"]["days"]),
             len(nutri["Denis"]["days"]), len(nutri["Leni"]["days"])))


# ----------------------------------------------------------------------------
# HTML-Template
# ----------------------------------------------------------------------------
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Brudi-Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=DM+Mono:wght@400;500&family=Familjen+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#15130F; --panel:#1E1B16; --panel2:#211D17; --border:#322C23;
    --text:#EDE6D8; --muted:#9A9182; --faint:#6B6356;
    --green:#5BD16A; --amber:#F0C04A; --red:#FF5C57;
    --accent:#4DA6FF; --accent2:#1E6FD9;
    --display:'Bricolage Grotesque',sans-serif;
    --body:'Familjen Grotesk',sans-serif;
    --mono:'DM Mono',monospace;
    --darkink:#15130F;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{background:var(--bg);color:var(--text);font-family:var(--body)}
  body{
    padding:26px;
    background-image:radial-gradient(circle at 12% 0%, rgba(77,166,255,.06), transparent 42%),
                     radial-gradient(circle at 100% 100%, rgba(255,111,181,.05), transparent 40%);
    min-height:100vh;transition:background-color .35s,color .35s;
  }
  .grain{position:fixed;inset:0;pointer-events:none;opacity:.035;z-index:99;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");}
  .wrap{max-width:1080px;margin:0 auto}

  header{display:flex;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;gap:18px;margin-bottom:22px}
  .brand{display:flex;flex-direction:column;gap:2px}
  .brand .kicker{font-family:var(--mono);font-size:11px;letter-spacing:.30em;text-transform:uppercase;color:var(--muted)}
  .brand h1{font-family:var(--display);font-weight:800;font-size:33px;letter-spacing:-.02em;line-height:1}
  .brand h1 b{color:var(--accent);transition:color .4s}

  .pagenav{display:flex;align-items:center;gap:11px;margin-bottom:16px}
  .pagenav button{font-family:var(--mono);font-size:11px;letter-spacing:.18em;text-transform:uppercase;
    color:var(--faint);background:none;border:none;cursor:pointer;padding:2px 0;transition:.2s}
  .pagenav button:hover{color:var(--muted)}
  .pagenav button.active{color:var(--accent)}
  .pagenav .navsep{color:var(--faint);font-family:var(--mono);font-size:11px}

  .toggle{display:flex;background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:5px;gap:4px}
  .toggle button{font-family:var(--display);font-weight:600;font-size:15px;color:var(--muted);background:none;border:none;
    padding:9px 20px;border-radius:10px;cursor:pointer;transition:.25s;display:flex;align-items:center;gap:8px}
  .toggle button .dot{width:9px;height:9px;border-radius:50%}
  .toggle button[data-u="Denis"] .dot{background:#4DA6FF}
  .toggle button[data-u="Leni"] .dot{background:#FF6FB5}
  .toggle button.active{color:var(--darkink)}
  .toggle button.active[data-u="Denis"]{background:#4DA6FF}
  .toggle button.active[data-u="Leni"]{background:#FF6FB5}

  .panel{background:var(--panel);border:1px solid var(--border);border-radius:18px;padding:20px}
  .panel .label{font-family:var(--mono);font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--faint);margin-bottom:14px}

  /* ===================== KALORIEN-SEITE ===================== */
  .top{display:grid;grid-template-columns:300px 1fr;gap:16px;margin-bottom:16px}
  @media(max-width:780px){.top{grid-template-columns:1fr}}
  .goals .goalrow{display:flex;align-items:baseline;justify-content:space-between;padding:10px 0;border-bottom:1px dashed var(--border)}
  .goals .goalrow:last-child{border-bottom:none}
  .goals .gk{font-size:14px;color:var(--muted)}
  .goals .gv{font-family:var(--mono);font-size:18px;font-weight:500;color:var(--text);text-align:right}
  .goals .gv small{font-size:12px;color:var(--faint)}
  .goals .gv.accent{color:var(--accent)}
  .goals .gv.macro{font-size:13px}
  .goals .gv.macro b{color:var(--text);font-weight:500}
  .progress{margin-bottom:16px;padding-bottom:15px;border-bottom:1px dashed var(--border)}
  .progress .prow{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:8px}
  .progress .pk{font-size:13px;color:var(--text);font-weight:500}
  .progress .ppct{font-family:var(--mono);font-size:17px;font-weight:500;color:var(--accent)}
  .progress .ptrack{height:10px;background:var(--panel2);border-radius:6px;overflow:hidden;border:1px solid var(--border)}
  .progress .pfill{height:100%;border-radius:6px;background:linear-gradient(90deg,var(--accent2),var(--accent));transition:width .7s cubic-bezier(.2,.8,.2,1)}
  .progress .pcap{margin-top:8px;font-family:var(--mono);font-size:10.5px;color:var(--muted);line-height:1.5}
  .progress .pcap b{color:var(--text);font-weight:500}
  .kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
  @media(max-width:780px){.kpis{grid-template-columns:repeat(2,1fr)}}
  .kpi{background:var(--panel);border:1px solid var(--border);border-radius:18px;padding:18px 18px 16px;position:relative;overflow:hidden}
  .kpi .bar{position:absolute;top:0;left:0;width:100%;height:3px}
  .kpi.green .bar{background:var(--green)} .kpi.amber .bar{background:var(--amber)}
  .kpi.red .bar{background:var(--red)} .kpi.total .bar{background:var(--accent)}
  .kpi .num{font-family:var(--display);font-weight:800;font-size:46px;line-height:1;letter-spacing:-.03em}
  .kpi.green .num{color:var(--green)} .kpi.amber .num{color:var(--amber)}
  .kpi.red .num{color:var(--red)} .kpi.total .num{color:var(--text)}
  .kpi .cap{margin-top:7px;font-size:13px;color:var(--text);line-height:1.25;font-weight:500}
  .kpi .sub{font-size:11.5px;color:var(--muted);margin-top:2px;line-height:1.25}
  .kpi .pct{font-family:var(--mono);font-size:11px;color:var(--faint);margin-top:6px}
  .chart-title{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;margin-bottom:6px}
  .chart-title h2{font-family:var(--display);font-weight:600;font-size:19px;letter-spacing:-.01em}
  .chart-sub{font-size:12.5px;color:var(--muted);margin-bottom:18px}
  .dvg{display:flex;flex-direction:column;gap:9px}
  .dvg .drow{display:grid;grid-template-columns:84px 1fr 84px;align-items:center;gap:10px}
  .dvg .dday{font-family:var(--mono);font-size:12px;color:var(--muted);text-align:right;white-space:nowrap}
  .dvg .track{position:relative;height:26px;background:var(--panel2);border-radius:7px;overflow:hidden}
  .dvg .zero{position:absolute;top:0;bottom:0;left:50%;width:1px;background:var(--faint);opacity:.6;z-index:2}
  .dvg .fill{position:absolute;top:3px;bottom:3px;border-radius:5px;transition:.5s cubic-bezier(.2,.8,.2,1)}
  .dvg .fill.green{background:linear-gradient(90deg,rgba(91,209,106,.35),rgba(91,209,106,.85))}
  .dvg .fill.amber{background:linear-gradient(90deg,rgba(240,192,74,.85),rgba(240,192,74,.4))}
  .dvg .fill.red{background:linear-gradient(90deg,rgba(255,92,87,.9),rgba(255,92,87,.4))}
  .dvg .dval{font-family:var(--mono);font-size:12px;font-weight:500;white-space:nowrap;text-align:left}
  .dvg .dval.green{color:var(--green)} .dvg .dval.amber{color:var(--amber)} .dvg .dval.red{color:var(--red)}
  .metric-toggle{display:flex;gap:5px;flex-wrap:nowrap}
  .metric-toggle button{font-family:var(--mono);font-size:11px;letter-spacing:.02em;color:var(--muted);background:var(--panel2);
    border:1px solid var(--border);padding:7px 12px;border-radius:9px;cursor:pointer;transition:.2s;white-space:nowrap}
  .metric-toggle button.active{background:var(--accent);color:var(--darkink);border-color:var(--accent);font-weight:500}
  .chart-controls{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:6px}
  .seg button{min-width:30px;text-align:center;font-weight:500}
  .weekly{display:flex;flex-direction:column}
  .plot{position:relative;height:185px;display:flex;align-items:flex-end;justify-content:space-around;gap:18px;overflow:visible}
  .refline{position:absolute;left:0;right:0;border-top:1.5px dashed var(--green);z-index:4;pointer-events:none}
  .refline span{position:absolute;right:0;top:-15px;font-family:var(--mono);font-size:10px;color:var(--green);background:var(--panel);padding:0 4px}
  .wcol{flex:1;max-width:130px;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:flex-end}
  .wbar{width:60%;border-radius:8px 8px 0 0;background:linear-gradient(180deg,var(--accent),var(--accent2));
    transition:height .55s cubic-bezier(.2,.8,.2,1),background .3s;min-height:3px}
  .wval{font-family:var(--mono);font-size:13px;font-weight:500;color:var(--text);margin-bottom:6px}
  .wklabels{display:flex;justify-content:space-around;gap:18px;margin-top:10px}
  .wklabel{flex:1;max-width:130px;font-family:var(--mono);font-size:11px;color:var(--muted);text-align:center;line-height:1.35}
  .wklabel small{display:block;color:var(--faint);font-size:9.5px}

  /* ===================== NAEHRSTOFF-SEITE ===================== */
  .timebar{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:14px;
    background:var(--panel);border:1px solid var(--border);border-radius:16px;padding:14px 18px;margin-bottom:20px}
  .timebar .tlabel{font-family:var(--mono);font-size:10.5px;letter-spacing:.20em;text-transform:uppercase;color:var(--faint)}
  .timebar .tsub{font-family:var(--mono);font-size:11px;color:var(--muted);margin-top:3px}
  .tseg{display:flex;gap:5px;background:var(--panel2);border:1px solid var(--border);border-radius:11px;padding:4px}
  .tseg button{font-family:var(--display);font-weight:600;font-size:13px;color:var(--muted);background:none;border:none;
    padding:8px 16px;border-radius:8px;cursor:pointer;transition:.2s;white-space:nowrap}
  .tseg button.active{background:var(--accent);color:var(--darkink)}
  .sec-title{display:flex;align-items:baseline;gap:10px;margin:4px 2px 14px}
  .sec-title h2{font-family:var(--display);font-weight:600;font-size:18px;letter-spacing:-.01em}
  .sec-title .hint{font-family:var(--mono);font-size:11px;color:var(--faint)}
  .checks{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:30px}
  @media(max-width:820px){.checks{grid-template-columns:repeat(2,1fr)}}
  @media(max-width:460px){.checks{grid-template-columns:1fr}}
  .check{position:relative;background:var(--panel);border:1px solid var(--border);border-radius:16px;padding:16px 16px 15px;overflow:hidden}
  .check .topbar{position:absolute;top:0;left:0;width:100%;height:3px}
  .check.green .topbar{background:var(--green)} .check.amber .topbar{background:var(--amber)} .check.red .topbar{background:var(--red)}
  .check .ck-head{display:flex;align-items:center;gap:8px;margin-bottom:3px}
  .check .ck-dot{width:11px;height:11px;border-radius:50%;flex:none}
  .check.green .ck-dot{background:var(--green);box-shadow:0 0 10px rgba(91,209,106,.5)}
  .check.amber .ck-dot{background:var(--amber);box-shadow:0 0 10px rgba(240,192,74,.45)}
  .check.red .ck-dot{background:var(--red);box-shadow:0 0 10px rgba(255,92,87,.45)}
  .check .ck-name{font-family:var(--display);font-weight:600;font-size:14.5px}
  .check .ck-status{font-family:var(--display);font-weight:700;font-size:21px;letter-spacing:-.01em;margin-top:6px}
  .check.green .ck-status{color:var(--green)} .check.amber .ck-status{color:var(--amber)} .check.red .ck-status{color:var(--red)}
  .check .ck-detail{font-family:var(--mono);font-size:11px;color:var(--muted);margin-top:3px}
  .check .ck-help{font-size:11px;color:var(--faint);margin-top:9px;line-height:1.35}
  /* --- Hover-Quickinfo: Top-Lebensmittel pro Kategorie --- */
  .check.has-tip{cursor:help}
  .check .ck-tip{position:absolute;inset:0;background:var(--panel2);padding:13px 15px;z-index:3;
    opacity:0;pointer-events:none;transition:opacity .18s ease;overflow:auto;display:flex;gap:14px}
  .check.has-tip:hover .ck-tip,.check.has-tip:focus-within .ck-tip{opacity:1;pointer-events:auto}
  .check .ck-tip .col{flex:1;min-width:0}
  .check .ck-tip .tt{font-family:var(--mono);font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;margin-bottom:4px}
  .check .ck-tip .tt.pos{color:var(--green)}
  .check .ck-tip .tt.neg{color:var(--red)}
  .check .ck-tip ul{list-style:none;margin:0;padding:0}
  .check .ck-tip li{font-size:11.5px;color:var(--text);line-height:1.5;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .check .ck-tip li small{font-family:var(--mono);font-size:10px;color:var(--faint)}
  .check .ck-tip .none{font-size:11px;color:var(--faint)}
  .micro-head{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:16px}
  .micro-head h2{font-family:var(--display);font-weight:600;font-size:18px}
  .micro-head .mh-sub{font-family:var(--mono);font-size:11px;color:var(--faint);margin-top:2px}
  .bars{display:flex;flex-direction:column;gap:11px}
  .brow{display:grid;grid-template-columns:150px 1fr 50px;align-items:center;gap:12px}
  @media(max-width:560px){.brow{grid-template-columns:120px 1fr 44px;gap:8px}}
  .bname{display:flex;flex-direction:column;gap:1px;min-width:0}
  .bname .bn{font-size:13px;font-weight:500;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .bname .bamt{font-family:var(--mono);font-size:10px;color:var(--faint);white-space:nowrap}
  .btrack{position:relative;height:22px;background:var(--panel2);border:1px solid var(--border);border-radius:7px;overflow:hidden}
  .bfill{position:absolute;top:0;left:0;height:100%;border-radius:6px 0 0 6px;transition:width .6s cubic-bezier(.2,.8,.2,1)}
  .bfill.green{background:linear-gradient(90deg,rgba(91,209,106,.45),rgba(91,209,106,.95))}
  .bfill.amber{background:linear-gradient(90deg,rgba(240,192,74,.5),rgba(240,192,74,.95))}
  .bfill.red{background:linear-gradient(90deg,rgba(255,92,87,.55),rgba(255,92,87,.95))}
  .bfill.full{border-radius:6px}
  .bpct{font-family:var(--mono);font-size:12px;font-weight:500;text-align:right}
  .bpct.green{color:var(--green)} .bpct.amber{color:var(--amber)} .bpct.red{color:var(--red)}
  .sortbtns{display:flex;gap:5px;background:var(--panel2);border:1px solid var(--border);border-radius:10px;padding:4px}
  .sortbtns button{font-family:var(--mono);font-size:11px;color:var(--muted);background:none;border:none;
    padding:7px 12px;border-radius:7px;cursor:pointer;transition:.2s;white-space:nowrap}
  .sortbtns button.active{background:var(--accent);color:var(--darkink);font-weight:500}

  /* ---- shared ---- */
  .empty{text-align:center;padding:48px 20px;color:var(--faint);font-family:var(--mono);font-size:13px;line-height:1.7}
  .empty b{display:block;font-family:var(--display);font-size:20px;color:var(--muted);margin-bottom:6px}
  footer{margin-top:22px;text-align:center;font-family:var(--mono);font-size:10.5px;color:var(--faint);letter-spacing:.05em}
  .stagger{opacity:0;animation:rise .6s cubic-bezier(.2,.8,.2,1) forwards}
  @keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
</style>
</head>
<body>
<div class="grain"></div>
<div class="wrap">
  <nav class="pagenav" id="pageswitch">
    <button data-pg="kcal" class="active">Kalorien</button>
    <span class="navsep">/</span>
    <button data-pg="nutri">Nährstoffe</button>
  </nav>
  <header>
    <div class="brand">
      <span class="kicker" id="kicker">Kalorienbrudi</span>
      <h1 id="title">Dashboard <b>Denis</b></h1>
    </div>
    <div class="toggle" id="toggle">
      <button data-u="Denis" class="active"><span class="dot"></span>Denis</button>
      <button data-u="Leni"><span class="dot"></span>Leni</button>
    </div>
  </header>
  <div id="content"></div>
  <footer id="foot"></footer>
</div>

<script>
const DATA_KCAL = __DATA_KCAL__;
const DATA_NUTRI = __DATA_NUTRI__;
const TODAY = "__TODAY_ISO__";

let curPage='kcal', curUser='Denis';

/* ============================ KALORIEN ============================ */
const RATIO={p:0.30,f:0.30,c:0.40};
const METRICS={kcal:{label:'Kalorien',unit:'kcal'},p:{label:'Protein',unit:'g'},f:{label:'Fett',unit:'g'},c:{label:'Carbs',unit:'g'}};
const PERIOD_LIMIT = 3;
let curMetric='kcal', curPeriod='W';
const WD=['So','Mo','Di','Mi','Do','Fr','Sa'];
function fmtDay(iso){const dt=new Date(iso+'T00:00');return WD[dt.getDay()]+' '+String(dt.getDate()).padStart(2,'0')+'.'+String(dt.getMonth()+1).padStart(2,'0')+'.';}
function maintenance(u){return u.goalIntake+u.deficitTarget;}
function classify(u,kcal){if(kcal<=u.goalIntake+u.greenBuf)return'green';if(kcal<=maintenance(u))return'amber';return'red';}
function targets(u){return{kcal:u.goalIntake,p:Math.round(u.goalIntake*RATIO.p/4),f:Math.round(u.goalIntake*RATIO.f/9),c:Math.round(u.goalIntake*RATIO.c/4)};}
function mondayOf(iso){const dt=new Date(iso+'T00:00');const day=(dt.getDay()+6)%7;dt.setDate(dt.getDate()-day);return dt;}
function isoShort(dt){return String(dt.getDate()).padStart(2,'0')+'.'+String(dt.getMonth()+1).padStart(2,'0')+'.';}
const MONTHS=['Jan','Feb','Mrz','Apr','Mai','Jun','Jul','Aug','Sep','Okt','Nov','Dez'];
const PERIODS={W:'Woche',M:'Monat',J:'Jahr'};
function periodKey(iso,mode){
  const dt=new Date(iso+'T00:00');
  if(mode==='J')return String(dt.getFullYear());
  if(mode==='M')return dt.getFullYear()+'-'+String(dt.getMonth()+1).padStart(2,'0');
  return mondayOf(iso).toISOString().slice(0,10);
}
function periodLabel(k,mode){
  if(mode==='J')return k;
  if(mode==='M'){const p=k.split('-');return MONTHS[+p[1]-1]+' '+p[0];}
  const mon=new Date(k+'T00:00'),sun=new Date(mon);sun.setDate(sun.getDate()+6);
  return isoShort(mon)+'-'+isoShort(sun);
}
function periodAgg(days,mode){
  const g={};
  days.forEach(x=>{const k=periodKey(x.d,mode);(g[k]=g[k]||[]).push(x);});
  return Object.keys(g).sort().map(k=>{
    const a=g[k],n=a.length,av=key=>Math.round(a.reduce((s,x)=>s+x[key],0)/n);
    return{n,range:periodLabel(k,mode),kcal:av('kcal'),p:av('p'),f:av('f'),c:av('c')};
  });
}
function renderKcal(){
  const u=DATA_KCAL[curUser];
  document.documentElement.style.setProperty('--accent',u.accent);
  document.documentElement.style.setProperty('--accent2',u.accent2);
  const C=document.getElementById('content');
  if(!u.days||u.days.length===0){
    C.innerHTML='<div class="panel empty stagger"><b>Noch keine Eintraege fuer '+curUser+'</b>Sobald '+curUser+' Mahlzeiten eintraegt,<br>erscheinen hier die Auswertungen.</div>';
    document.getElementById('foot').textContent='Stand: __BUILD_DATE__ - keine Daten';
    return;
  }
  const t=targets(u);
  const counts={green:0,amber:0,red:0};
  u.days.forEach(x=>counts[classify(u,x.kcal)]++);
  const total=u.days.length, pct=n=>total?Math.round(n/total*100)+'%':'-';
  const last7=u.days.slice(-7).reverse();
  const maxAbs=Math.max(...last7.map(x=>Math.abs(x.kcal-u.goalIntake)),300)*1.04;
  const maint=u.goalIntake+u.deficitTarget;
  const anchorW=(u.anchorWeight!=null?u.anchorWeight:u.weight);
  const sw=(u.startWeight!=null?u.startWeight:anchorW);
  const savedByWeight=(sw!=null&&anchorW!=null)?(sw-anchorW)*7000:0;
  const savedSinceAnchor=u.days.reduce((s,x)=>s+((u.anchorDate==null||x.d>=u.anchorDate)?(maint-x.kcal):0),0);
  const saved=savedByWeight+savedSinceAnchor;
  const totalNeeded=(sw!=null&&u.zielWeight!=null)?(sw-u.zielWeight)*7000:0;
  const prog=totalNeeded>0?Math.max(0,Math.min(100,saved/totalNeeded*100)):0;
  const remain=Math.max(0,totalNeeded-saved);
  const daysLeft=Math.abs(Math.round(remain/u.deficitTarget));

  C.innerHTML=`
    <div class="top">
      <div class="panel goals stagger" style="animation-delay:.02s">
        <div class="label">Aktuelles Ziel</div>
        <div class="progress">
          <div class="prow"><span class="pk">Fortschritt zum Ziel</span><span class="ppct">${Math.round(prog)} %</span></div>
          <div class="ptrack"><div class="pfill" style="width:${prog}%"></div></div>
          <div class="pcap"><b>${Math.round(saved).toLocaleString('de')}</b> / ${totalNeeded.toLocaleString('de')} kcal gespart - noch <b>${daysLeft} Tage</b> bei ${u.deficitTarget} kcal Defizit/Tag</div>
        </div>
        <div class="goalrow"><span class="gk">Ziel</span><span class="gv">Abnehmen</span></div>
        <div class="goalrow"><span class="gk">Kalorienziel</span><span class="gv accent">${u.goalIntake.toLocaleString('de')} <small>kcal</small></span></div>
        <div class="goalrow"><span class="gk">Geplantes Defizit</span><span class="gv">${u.deficitTarget.toLocaleString('de')} <small>kcal</small></span></div>
        <div class="goalrow"><span class="gk">Erhaltungsbedarf</span><span class="gv">${maintenance(u).toLocaleString('de')} <small>kcal</small></span></div>
        <div class="goalrow"><span class="gk">Makro-Ziel</span><span class="gv macro"><b>${t.p}</b>P - <b>${t.f}</b>F - <b>${t.c}</b>C <small>g</small></span></div>
        <div class="goalrow"><span class="gk">Startgewicht</span><span class="gv">${u.startWeight!=null?u.startWeight.toLocaleString('de')+' <small>kg</small>':'-'}</span></div>
        <div class="goalrow"><span class="gk">Aktuelles Gewicht</span><span class="gv">${u.weight!=null?u.weight.toLocaleString('de')+' <small>kg</small>':'-'}</span></div>
        <div class="goalrow"><span class="gk">Zielgewicht</span><span class="gv">${u.zielWeight!=null?u.zielWeight.toLocaleString('de')+' <small>kg</small>':'-'}</span></div>
        <div class="goalrow"><span class="gk">Letzter Eintrag</span><span class="gv" style="font-size:14px">${fmtDay(u.days[u.days.length-1].d)}</span></div>
      </div>
      <div class="kpis">
        <div class="kpi green stagger" style="animation-delay:.06s"><div class="bar"></div><div class="num">${counts.green}</div><div class="cap">Ziel erreicht</div><div class="sub">im gruenen Bereich</div><div class="pct">${pct(counts.green)} der Tage</div></div>
        <div class="kpi amber stagger" style="animation-delay:.10s"><div class="bar"></div><div class="num">${counts.amber}</div><div class="cap">Im Defizit</div><div class="sub">ueber Ziel, unter Bedarf</div><div class="pct">${pct(counts.amber)} der Tage</div></div>
        <div class="kpi red stagger" style="animation-delay:.14s"><div class="bar"></div><div class="num">${counts.red}</div><div class="cap">Ueber Bedarf</div><div class="sub">ueber Erhaltungsbedarf</div><div class="pct">${pct(counts.red)} der Tage</div></div>
        <div class="kpi total stagger" style="animation-delay:.18s"><div class="bar"></div><div class="num">${total}</div><div class="cap">Tage getrackt</div><div class="sub">insgesamt</div><div class="pct">seit ${fmtDay(u.days[0].d)}</div></div>
      </div>
    </div>

    <div class="panel stagger" style="animation-delay:.22s;margin-bottom:16px">
      <div class="chart-title"><h2>Kaloriendifferenz - letzte 7 Tage</h2></div>
      <div class="chart-sub">Differenz zum Tagesziel von ${u.goalIntake.toLocaleString('de')} kcal - links = drunter, rechts = drueber (neueste oben)</div>
      <div class="dvg">
        ${last7.map(x=>{
          const diff=x.kcal-u.goalIntake, cls=classify(u,x.kcal);
          const w=Math.min(Math.abs(diff)/maxAbs*48,48);
          const style=diff<=0?`right:50%;width:${w}%`:`left:50%;width:${w}%`;
          const sign=diff>0?'+':'';
          return `<div class="drow"><div class="dday">${fmtDay(x.d)}</div>
            <div class="track"><div class="zero"></div><div class="fill ${cls}" style="${style}"></div></div>
            <div class="dval ${cls}">${sign}${diff} kcal</div></div>`;
        }).join('')}
      </div>
    </div>

    <div class="panel stagger" style="animation-delay:.26s">
      <div class="chart-title"><h2>${curPeriod==='W'?'Wochendurchschnitt':curPeriod==='M'?'Monatsdurchschnitt':'Jahresdurchschnitt'}</h2></div>
      <div class="chart-controls">
        <div class="metric-toggle seg" id="pt">
          ${Object.keys(PERIODS).map(p=>`<button data-p="${p}" class="${p===curPeriod?'active':''}" title="${PERIODS[p]}">${p}</button>`).join('')}
        </div>
        <div class="metric-toggle" id="mt">
          ${Object.keys(METRICS).map(m=>`<button data-m="${m}" class="${m===curMetric?'active':''}">${METRICS[m].label}</button>`).join('')}
        </div>
      </div>
      <div class="chart-sub" id="msub"></div>
      <div class="weekly"><div class="plot" id="plot"></div><div class="wklabels" id="wkl"></div></div>
    </div>
  `;
  document.getElementById('mt').querySelectorAll('button').forEach(b=>b.onclick=()=>{curMetric=b.dataset.m;renderKcal();});
  document.getElementById('pt').querySelectorAll('button').forEach(b=>b.onclick=()=>{curPeriod=b.dataset.p;renderKcal();});
  const agg=periodAgg(u.days,curPeriod);
  drawWeekly(PERIOD_LIMIT>0?agg.slice(-PERIOD_LIMIT):agg,u,t);
  document.getElementById('foot').textContent='Stand: __BUILD_DATE__ - '+total+' Tage - Verhaeltnis 30 % P / 30 % F / 40 % C - automatisch generiert';
}
function drawWeekly(weeks,u,t){
  const plot=document.getElementById('plot'), wkl=document.getElementById('wkl');
  const H=158, tgt=t[curMetric];
  const maxV=Math.max(...weeks.map(w=>w[curMetric]),tgt)*1.18;
  const grp=curPeriod==='W'?'Kalenderwoche':curPeriod==='M'?'Monat':'Jahr';
  document.getElementById('msub').textContent=METRICS[curMetric].label+' \\u00d8 pro Tag, gruppiert nach '+grp+' ('+METRICS[curMetric].unit+') - gestrichelt: Ziel '+tgt+' '+METRICS[curMetric].unit;
  plot.innerHTML=weeks.map(w=>{
    const h=Math.round(w[curMetric]/maxV*H);
    return `<div class="wcol"><div class="wval">${w[curMetric].toLocaleString('de')}</div><div class="wbar" style="height:${h}px"></div></div>`;
  }).join('');
  const refpx=Math.round(tgt/maxV*H);
  const rl=document.createElement('div');rl.className='refline';rl.style.bottom=refpx+'px';
  rl.innerHTML='<span>Ziel '+tgt+'</span>';plot.appendChild(rl);
  wkl.innerHTML=weeks.map(w=>`<div class="wklabel">${w.range}<small>${w.n} ${w.n===1?'Tag':'Tage'}</small></div>`).join('');
}

/* ============================ NAEHRSTOFFE ============================ */
const CATS=[
  {key:"Darmgesundheit", help:"Ballaststoffe, Fermentiertes, Vielfalt = gut"},
  {key:"Low FODMAP",     help:"niedrig-FODMAP / gut vertraeglich = gut"},
  {key:"Säure-Base",     help:"basisch = gut, saeurebildend = schlecht"}
];
const CHOL_GREEN=300, CHOL_AMBER=500;
const CAT_GREEN=70, CAT_AMBER=50;
const MIC_GREEN=90, MIC_AMBER=50;
const NPERIODS={ "7":"letzte 7 Tage", "30":"letzte 30 Tage", "all":"gesamter Zeitraum" };
let curNPeriod='7', curSort='worst';
function splitUnit(key){ const m=key.match(/^(.*) \\(([^)]+)\\)$/); return m?[m[1],m[2]]:[key,'']; }
function fmtN(v){ if(v>=100)return Math.round(v).toLocaleString('de'); if(v>=10)return (Math.round(v*10)/10).toLocaleString('de'); return (Math.round(v*100)/100).toLocaleString('de'); }
function shiftISO(iso,days){ const d=new Date(iso+'T00:00'); d.setDate(d.getDate()+days); return d.toISOString().slice(0,10); }
function nWindowDays(u){
  if(curNPeriod==='all') return u.days.slice();
  const n=parseInt(curNPeriod,10), cut=shiftISO(TODAY,-(n-1));
  return u.days.filter(x=>x.d>=cut);
}
function micColor(p){ return p>=MIC_GREEN?'green':(p>=MIC_AMBER?'amber':'red'); }
function topFoods(windowDays){
  /* pro Kategorie: Haeufigkeit je Lebensmittel zaehlen, Top 3 positiv + Top 3 negativ */
  const out={};
  CATS.forEach(c=>{
    const pos={},neg={};
    windowDays.forEach(day=>{
      const f=(day.cf&&day.cf[c.key])||[[],[]];
      f[0].forEach(n=>pos[n]=(pos[n]||0)+1);
      f[1].forEach(n=>neg[n]=(neg[n]||0)+1);
    });
    const top=o=>Object.entries(o).sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])).slice(0,3);
    out[c.key]={pos:top(pos),neg:top(neg)};
  });
  return out;
}
function tipHtml(t){
  const li=a=>a.length
    ?'<ul>'+a.map(([n,k])=>'<li>'+n+(k>1?' <small>\\u00d7'+k+'</small>':'')+'</li>').join('')+'</ul>'
    :'<div class="none">keine</div>';
  return '<div class="ck-tip">'
       +'<div class="col"><div class="tt pos">\\u25b2 Top 3</div>'+li(t.pos)+'</div>'
       +'<div class="col"><div class="tt neg">\\u25bc Flop 3</div>'+li(t.neg)+'</div>'
       +'</div>';
}
function checkCard(name, cls, status, detail, help, i, tip){
  return `<div class="check ${cls}${tip?' has-tip':''} stagger" style="animation-delay:${(0.02+0.03*i).toFixed(2)}s"${tip?' tabindex="0"':''}>
    <div class="topbar"></div>
    <div class="ck-head"><span class="ck-dot"></span><span class="ck-name">${name}</span></div>
    <div class="ck-status">${status}</div>
    <div class="ck-detail">${detail}</div>
    <div class="ck-help">${help}</div>
    ${tip||''}
  </div>`;
}
function renderNutri(){
  const u=DATA_NUTRI[curUser];
  document.documentElement.style.setProperty('--accent',u.accent);
  document.documentElement.style.setProperty('--accent2',u.accent2);
  const C=document.getElementById('content');

  if(!u.days.length){
    C.innerHTML='<div class="panel empty stagger"><b>Noch keine Eintraege fuer '+curUser+'</b>Sobald in der Lebensmittel-Analyse Zeilen<br>fuer '+curUser+' liegen, erscheint hier die Auswertung.</div>';
    document.getElementById('foot').textContent='Stand: __BUILD_DATE__ - keine Daten';
    return;
  }
  const wd=nWindowDays(u), nDays=wd.length;
  const fmtDt=iso=>{const p=iso.split('-');return p[2]+'.'+p[1]+'.'+p[0];};
  const tsub = nDays
    ? fmtDt(wd[0].d)+' \\u2013 '+fmtDt(wd[wd.length-1].d)+' \\u00b7 '+nDays+(nDays===1?' getrackter Tag':' getrackte Tage')+' \\u00b7 \\u00d8 pro Tag'
    : NPERIODS[curNPeriod]+' \\u00b7 keine Daten';

  const timebar = `
    <div class="timebar stagger">
      <div><div class="tlabel">Zeitfenster</div><div class="tsub">${tsub}</div></div>
      <div class="tseg" id="ntime">
        <button data-p="7" class="${curNPeriod==='7'?'active':''}">7 Tage</button>
        <button data-p="30" class="${curNPeriod==='30'?'active':''}">30 Tage</button>
        <button data-p="all" class="${curNPeriod==='all'?'active':''}">Gesamt</button>
      </div>
    </div>`;

  if(!nDays){
    C.innerHTML=timebar+'<div class="panel empty stagger"><b>Keine Daten im Zeitfenster</b>Im '+NPERIODS[curNPeriod]+' wurde nichts getrackt.<br>Wechsle das Zeitfenster oben.</div>';
    document.getElementById('ntime').querySelectorAll('button').forEach(b=>b.onclick=()=>{curNPeriod=b.dataset.p;renderNutri();});
    document.getElementById('foot').textContent='Stand: __BUILD_DATE__';
    return;
  }

  const sum={}; Object.keys(u.ref).forEach(k=>sum[k]=0); sum["Cholesterin (mg)"]=0;
  const votes={}; CATS.forEach(c=>votes[c.key]=[0,0,0]);
  wd.forEach(day=>{
    Object.keys(sum).forEach(k=>{ sum[k]+=(day.nut[k]||0); });
    CATS.forEach(c=>{ const v=day.cat[c.key]||[0,0,0]; votes[c.key][0]+=v[0]; votes[c.key][1]+=v[1]; votes[c.key][2]+=v[2]; });
  });
  const avg={}; Object.keys(sum).forEach(k=>avg[k]=sum[k]/nDays);
  const foods=topFoods(wd);

  let checksHtml='';
  CATS.forEach((c,i)=>{
    const v=votes[c.key], tot=v[0]+v[1]+v[2];
    let cls,status,detail;
    if(!tot){ cls='amber'; status='-'; detail='keine Angaben'; }
    else{
      const score=(v[0]*100 + v[1]*50)/tot;
      cls = score>=CAT_GREEN?'green':(score>=CAT_AMBER?'amber':'red');
      status = cls==='green'?'Gut':(cls==='amber'?'Okay':'Kritisch');
      detail = Math.round(score)+' / 100 \\u00b7 '+v[0]+'/'+v[1]+'/'+v[2]+' (g/n/s)';
    }
    checksHtml += checkCard(c.key, cls, status, detail, c.help, i, tipHtml(foods[c.key]));
  });
  (function(){
    const ch=avg["Cholesterin (mg)"];
    const cls = ch<=CHOL_GREEN?'green':(ch<=CHOL_AMBER?'amber':'red');
    const status = cls==='green'?'Gut':(cls==='amber'?'Okay':'Hoch');
    const detail = '\\u00d8 '+Math.round(ch).toLocaleString('de')+' mg/Tag (Ziel \\u2264'+CHOL_GREEN+')';
    checksHtml += checkCard('Cholesterin', cls, status, detail, 'weniger ist besser - Ziel unter '+CHOL_GREEN+' mg/Tag', 3);
  })();

  let micros=Object.keys(u.ref).map(k=>{
    const [name,unit]=splitUnit(k);
    const a=avg[k]||0, ref=u.ref[k];
    const pctRaw=ref>0?(a/ref*100):0, pct=Math.min(100,pctRaw);
    return {name,unit,avg:a,ref,pct,pctRaw,color:micColor(pct)};
  });
  micros.sort((x,y)=> curSort==='worst' ? x.pct-y.pct : y.pct-x.pct);
  let barsHtml=micros.map((m,i)=>{
    const full=m.pct>=99.5?' full':'';
    return `<div class="brow stagger" style="animation-delay:${(0.02*i).toFixed(2)}s">
      <div class="bname"><span class="bn">${m.name}</span><span class="bamt">${fmtN(m.avg)} / ${fmtN(m.ref)} ${m.unit}</span></div>
      <div class="btrack"><div class="bfill ${m.color}${full}" style="width:${m.pct.toFixed(1)}%"></div></div>
      <div class="bpct ${m.color}">${Math.round(m.pctRaw)}%</div>
    </div>`;
  }).join('');

  C.innerHTML = timebar + `
    <div class="sec-title stagger"><h2>Gesundheits-Checkpoints</h2><span class="hint">Ampel im gewaehlten Zeitfenster \\u00b7 Hover zeigt Top-Lebensmittel</span></div>
    <div class="checks">${checksHtml}</div>
    <div class="panel stagger" style="animation-delay:.10s">
      <div class="micro-head">
        <div><h2>Mikronaehrstoffe</h2><div class="mh-sub">\\u00d8 pro Tag vs. Tagesreferenzwert \\u00b7 gedeckelt bei 100 %</div></div>
        <div class="sortbtns" id="nsort">
          <button data-s="worst" class="${curSort==='worst'?'active':''}">Schlechteste zuerst</button>
          <button data-s="best" class="${curSort==='best'?'active':''}">Beste zuerst</button>
        </div>
      </div>
      <div class="bars">${barsHtml}</div>
    </div>`;

  document.getElementById('ntime').querySelectorAll('button').forEach(b=>b.onclick=()=>{curNPeriod=b.dataset.p;renderNutri();});
  document.getElementById('nsort').querySelectorAll('button').forEach(b=>b.onclick=()=>{curSort=b.dataset.s;renderNutri();});
  document.getElementById('foot').textContent='Stand: __BUILD_DATE__ - '+curUser+' - '+NPERIODS[curNPeriod]+' - Zielwerte: DGE-Tagesreferenz ('+(curUser==='Denis'?'m':'w')+') - automatisch generiert';
}

/* ============================ STEUERUNG ============================ */
function renderAll(){
  const nutri = curPage==='nutri';
  document.querySelectorAll('#pageswitch button').forEach(b=>b.classList.toggle('active', b.dataset.pg===curPage));
  document.getElementById('kicker').textContent = nutri ? 'Nährstoffbrudi' : 'Kalorienbrudi';
  document.getElementById('title').innerHTML = 'Dashboard <b>'+curUser+'</b>';
  if(nutri) renderNutri(); else renderKcal();
}
document.getElementById('pageswitch').querySelectorAll('button').forEach(b=>{
  b.onclick=()=>{curPage=b.dataset.pg;renderAll();};
});
document.getElementById('toggle').querySelectorAll('button').forEach(b=>{
  b.onclick=()=>{document.querySelectorAll('#toggle button').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');curUser=b.dataset.u;curMetric='kcal';renderAll();};
});
renderAll();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
