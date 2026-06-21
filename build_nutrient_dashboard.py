#!/usr/bin/env python3
"""
Naehrstoffbrudi Dashboard Generator
-----------------------------------
Zieht alle Eintraege aus der Notion-Datenbank "Lebensmittel-Analyse" (pro
Lebensmittel eine Zeile) und erzeugt eine statische naehrstoffe.html.

Aufbau analog zum Kalorienbrudi-Dashboard, aber eigenes Thema:
  - Switch Denis / Leni
  - Zeitfenster-Toggle: 7 Tage / 30 Tage / Gesamt
  - 4 Gesundheits-Checkpoints mit Ampel (Darmgesundheit, Low FODMAP,
    Saeure-Base, Cholesterin)
  - Mikronaehrstoffe als Ladebalken (% vom Tagesreferenzwert, gedeckelt bei
    100 %), sortierbar (schlechteste zuerst / beste zuerst)

Zielwerte = Tagesreferenzwerte; verglichen wird der Durchschnitt PRO
getracktem Tag im gewaehlten Zeitfenster.

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
DATA_SOURCE_ID = "be09a702-364a-4f0f-9548-5f4f32092dee"   # Lebensmittel-Analyse
NOTION_VERSION = "2025-09-03"
TOKEN = os.environ.get("NOTION_TOKEN")

# Pro Person: Geschlecht (fuer Referenzwerte) + Akzentfarben (Switch)
PERSON_CONFIG = {
    "Denis": {"sex": "m", "accent": "#2DD4BF", "accent2": "#0D9488"},
    "Leni":  {"sex": "w", "accent": "#F472B6", "accent2": "#DB2777"},
}

# Tages-Referenzwerte (DGE/D-A-CH, Erwachsene) je Geschlecht.
# --> Hier anpassen, wenn ihr andere Zielwerte wollt.
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

# Spalten, die pro Tag aufsummiert werden (Mikros + Cholesterin)
NUM_KEYS = list(REF["m"].keys()) + ["Cholesterin (mg)"]
# Ampel-Kategorien (Select: gut / neutral / schlecht)
CAT_KEYS = ["Darmgesundheit", "Low FODMAP", "Säure-Base"]


# ----------------------------------------------------------------------------
# Notion-Abfrage (mit Pagination)
# ----------------------------------------------------------------------------
def notion_query_all():
    url = "https://api.notion.com/v1/data_sources/%s/query" % DATA_SOURCE_ID
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


# ----------------------------------------------------------------------------
# Daten aufbereiten: pro Person -> pro Tag aggregiert
# ----------------------------------------------------------------------------
def build_data(pages):
    raw = {k: [] for k in PERSON_CONFIG}
    for pg in pages:
        props = pg.get("properties", {})
        person = select_name(props, "Person")
        if person not in raw:
            continue
        d = date_start(props, "Datum")
        if d is None:
            continue
        rec = {"d": d}
        for k in NUM_KEYS:
            rec[k] = num(props, k) or 0
        for c in CAT_KEYS:
            rec[c] = select_name(props, c)
        raw[person].append(rec)

    data = {}
    for person, cfg in PERSON_CONFIG.items():
        bydate = {}
        for e in raw[person]:
            day = bydate.get(e["d"])
            if day is None:
                day = {"d": e["d"], "n": 0,
                       "nut": {k: 0 for k in NUM_KEYS},
                       "cat": {c: [0, 0, 0] for c in CAT_KEYS}}
                bydate[e["d"]] = day
            day["n"] += 1
            for k in NUM_KEYS:
                day["nut"][k] += e[k]
            for c in CAT_KEYS:
                v = e[c]
                if v == "gut":
                    day["cat"][c][0] += 1
                elif v == "neutral":
                    day["cat"][c][1] += 1
                elif v == "schlecht":
                    day["cat"][c][2] += 1
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
    pages = notion_query_all()
    data = build_data(pages)
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    today_de = datetime.datetime.now(datetime.timezone.utc).strftime("%d.%m.%Y")
    html = (HTML_TEMPLATE
            .replace("__DATA_JSON__", json.dumps(data, ensure_ascii=False))
            .replace("__TODAY_ISO__", today)
            .replace("__BUILD_DATE__", today_de))
    with open("naehrstoffe.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("naehrstoffe.html geschrieben. Denis: %d Tage, Leni: %d Tage"
          % (len(data["Denis"]["days"]), len(data["Leni"]["days"])))


# ----------------------------------------------------------------------------
# HTML-Template (Daten werden ueber __DATA_JSON__ injiziert)
# ----------------------------------------------------------------------------
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Naehrstoffbrudi - Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#0B1512; --panel:#11201B; --panel2:#152821; --border:#23382F;
    --text:#E7F1EB; --muted:#8BA89B; --faint:#5C7468;
    --green:#46E08A; --amber:#FBBF24; --red:#FB6F84;
    --accent:#2DD4BF; --accent2:#0D9488;
    --display:'Space Grotesk',sans-serif;
    --body:'Inter',sans-serif;
    --mono:'DM Mono',monospace;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{background:var(--bg);color:var(--text);font-family:var(--body)}
  body{
    padding:26px;
    background-image:radial-gradient(circle at 8% -5%, rgba(45,212,191,.10), transparent 45%),
                     radial-gradient(circle at 100% 0%, rgba(70,224,138,.06), transparent 42%);
    min-height:100vh;
  }
  .grain{position:fixed;inset:0;pointer-events:none;opacity:.03;z-index:99;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");}
  .wrap{max-width:1080px;margin:0 auto}

  header{display:flex;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;gap:18px;margin-bottom:22px}
  .brand{display:flex;flex-direction:column;gap:3px}
  .brand .kicker{font-family:var(--mono);font-size:11px;letter-spacing:.30em;text-transform:uppercase;color:var(--accent)}
  .brand h1{font-family:var(--display);font-weight:700;font-size:34px;letter-spacing:-.02em;line-height:1;display:flex;align-items:center;gap:10px}
  .brand h1 .leaf{font-size:26px}
  .brand h1 b{color:var(--accent);transition:color .4s}
  .brand .crumb{font-family:var(--mono);font-size:10.5px;color:var(--faint);margin-top:3px}
  .brand .crumb a{color:var(--muted);text-decoration:none;border-bottom:1px dotted var(--faint)}
  .toggle{display:flex;background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:5px;gap:4px}
  .toggle button{font-family:var(--display);font-weight:600;font-size:15px;color:var(--muted);background:none;border:none;
    padding:9px 22px;border-radius:10px;cursor:pointer;transition:.25s;display:flex;align-items:center;gap:8px}
  .toggle button .dot{width:9px;height:9px;border-radius:50%}
  .toggle button[data-u="Denis"] .dot{background:#2DD4BF}
  .toggle button[data-u="Leni"] .dot{background:#F472B6}
  .toggle button.active{color:#0B1512}
  .toggle button.active[data-u="Denis"]{background:#2DD4BF}
  .toggle button.active[data-u="Leni"]{background:#F472B6}

  .timebar{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:14px;
    background:var(--panel);border:1px solid var(--border);border-radius:16px;padding:14px 18px;margin-bottom:20px}
  .timebar .tlabel{font-family:var(--mono);font-size:10.5px;letter-spacing:.20em;text-transform:uppercase;color:var(--faint)}
  .timebar .tsub{font-family:var(--mono);font-size:11px;color:var(--muted);margin-top:3px}
  .seg{display:flex;gap:5px;background:var(--panel2);border:1px solid var(--border);border-radius:11px;padding:4px}
  .seg button{font-family:var(--display);font-weight:600;font-size:13px;color:var(--muted);background:none;border:none;
    padding:8px 16px;border-radius:8px;cursor:pointer;transition:.2s;white-space:nowrap}
  .seg button.active{background:var(--accent);color:#0B1512}

  .sec-title{display:flex;align-items:baseline;gap:10px;margin:4px 2px 14px}
  .sec-title h2{font-family:var(--display);font-weight:600;font-size:18px;letter-spacing:-.01em}
  .sec-title .hint{font-family:var(--mono);font-size:11px;color:var(--faint)}

  .checks{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:30px}
  @media(max-width:820px){.checks{grid-template-columns:repeat(2,1fr)}}
  @media(max-width:460px){.checks{grid-template-columns:1fr}}
  .check{position:relative;background:var(--panel);border:1px solid var(--border);border-radius:16px;
    padding:16px 16px 15px;overflow:hidden}
  .check .topbar{position:absolute;top:0;left:0;width:100%;height:3px}
  .check.green .topbar{background:var(--green)} .check.amber .topbar{background:var(--amber)} .check.red .topbar{background:var(--red)}
  .check .ck-head{display:flex;align-items:center;gap:8px;margin-bottom:3px}
  .check .ck-dot{width:11px;height:11px;border-radius:50%;flex:none}
  .check.green .ck-dot{background:var(--green);box-shadow:0 0 10px rgba(70,224,138,.5)}
  .check.amber .ck-dot{background:var(--amber);box-shadow:0 0 10px rgba(251,191,36,.45)}
  .check.red .ck-dot{background:var(--red);box-shadow:0 0 10px rgba(251,111,132,.45)}
  .check .ck-name{font-family:var(--display);font-weight:600;font-size:14.5px}
  .check .ck-status{font-family:var(--display);font-weight:700;font-size:21px;letter-spacing:-.01em;margin-top:6px}
  .check.green .ck-status{color:var(--green)} .check.amber .ck-status{color:var(--amber)} .check.red .ck-status{color:var(--red)}
  .check .ck-detail{font-family:var(--mono);font-size:11px;color:var(--muted);margin-top:3px}
  .check .ck-help{font-size:11px;color:var(--faint);margin-top:9px;line-height:1.35}

  .panel{background:var(--panel);border:1px solid var(--border);border-radius:18px;padding:20px}
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
  .bfill.green{background:linear-gradient(90deg,rgba(70,224,138,.5),rgba(70,224,138,.95))}
  .bfill.amber{background:linear-gradient(90deg,rgba(251,191,36,.5),rgba(251,191,36,.95))}
  .bfill.red{background:linear-gradient(90deg,rgba(251,111,132,.55),rgba(251,111,132,.95))}
  .bfill.full{border-radius:6px}
  .bpct{font-family:var(--mono);font-size:12px;font-weight:500;text-align:right}
  .bpct.green{color:var(--green)} .bpct.amber{color:var(--amber)} .bpct.red{color:var(--red)}

  .sortbtns{display:flex;gap:5px;background:var(--panel2);border:1px solid var(--border);border-radius:10px;padding:4px}
  .sortbtns button{font-family:var(--mono);font-size:11px;color:var(--muted);background:none;border:none;
    padding:7px 12px;border-radius:7px;cursor:pointer;transition:.2s;white-space:nowrap}
  .sortbtns button.active{background:var(--accent);color:#0B1512;font-weight:500}

  .empty{text-align:center;padding:46px 20px;color:var(--faint);font-family:var(--mono);font-size:13px;line-height:1.7}
  .empty b{display:block;font-family:var(--display);font-size:19px;color:var(--muted);margin-bottom:6px}
  footer{margin-top:22px;text-align:center;font-family:var(--mono);font-size:10.5px;color:var(--faint);letter-spacing:.04em}
  .stagger{opacity:0;animation:rise .55s cubic-bezier(.2,.8,.2,1) forwards}
  @keyframes rise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
</style>
</head>
<body>
<div class="grain"></div>
<div class="wrap">
  <header>
    <div class="brand">
      <span class="kicker">Mikronaehrstoff-Analyse</span>
      <h1><span class="leaf">&#127807;</span>Naehrstoff<b id="userName">brudi</b></h1>
      <div class="crumb"><a href="index.html">&larr; Kalorienbrudi</a></div>
    </div>
    <div class="toggle" id="toggle">
      <button data-u="Denis" class="active"><span class="dot"></span>Denis</button>
      <button data-u="Leni"><span class="dot"></span>Leni</button>
    </div>
  </header>

  <div class="timebar">
    <div>
      <div class="tlabel">Zeitfenster</div>
      <div class="tsub" id="tsub"></div>
    </div>
    <div class="seg" id="pt">
      <button data-p="7" class="active">7 Tage</button>
      <button data-p="30">30 Tage</button>
      <button data-p="all">Gesamt</button>
    </div>
  </div>

  <div id="content"></div>
  <footer id="foot"></footer>
</div>

<script>
const DATA = __DATA_JSON__;
const TODAY = "__TODAY_ISO__";

// Ampel-Kategorien (Select gut/neutral/schlecht)
const CATS = [
  {key:"Darmgesundheit", help:"Ballaststoffe, Fermentiertes, Vielfalt = gut"},
  {key:"Low FODMAP",     help:"niedrig-FODMAP / gut vertraeglich = gut"},
  {key:"Säure-Base",     help:"basisch = gut, saeurebildend = schlecht"}
];
// Cholesterin-Schwellen (mg / Tag, weniger = besser)
const CHOL_GREEN=300, CHOL_AMBER=500;
// Kategorie-Score-Schwellen (0..100, gut=100/neutral=50/schlecht=0 gemittelt)
const CAT_GREEN=70, CAT_AMBER=50;
// Mikronaehrstoff-Balken-Schwellen (% vom Referenzwert)
const MIC_GREEN=90, MIC_AMBER=50;

const PERIODS={ "7":"letzte 7 Tage", "30":"letzte 30 Tage", "all":"gesamter Zeitraum" };
let curUser='Denis', curPeriod='7', curSort='worst';

function splitUnit(key){ const m=key.match(/^(.*) \\(([^)]+)\\)$/); return m?[m[1],m[2]]:[key,'']; }
function fmtNum(v){
  if(v>=100) return Math.round(v).toLocaleString('de');
  if(v>=10)  return (Math.round(v*10)/10).toLocaleString('de');
  return (Math.round(v*100)/100).toLocaleString('de');
}
function shiftISO(iso,days){ const d=new Date(iso+'T00:00'); d.setDate(d.getDate()+days); return d.toISOString().slice(0,10); }

function windowDays(u){
  if(curPeriod==='all') return u.days.slice();
  const n=parseInt(curPeriod,10);
  const cut=shiftISO(TODAY,-(n-1));
  return u.days.filter(x=>x.d>=cut);
}

function micColor(p){ return p>=MIC_GREEN?'green':(p>=MIC_AMBER?'amber':'red'); }

function render(){
  const u=DATA[curUser];
  document.documentElement.style.setProperty('--accent',u.accent);
  document.documentElement.style.setProperty('--accent2',u.accent2);
  document.getElementById('userName').textContent='brudi';
  const C=document.getElementById('content');

  const wd=windowDays(u);
  const nDays=wd.length;
  document.getElementById('tsub').textContent =
    PERIODS[curPeriod]+' \\u00b7 '+nDays+(nDays===1?' getrackter Tag':' getrackte Tage')+' \\u00b7 \\u00d8 pro Tag';

  if(!u.days.length){
    C.innerHTML='<div class="panel empty stagger"><b>Noch keine Eintraege fuer '+curUser+'</b>Sobald in der Lebensmittel-Analyse Zeilen<br>fuer '+curUser+' liegen, erscheint hier die Auswertung.</div>';
    document.getElementById('foot').textContent='Stand: __BUILD_DATE__ - keine Daten';
    return;
  }
  if(!nDays){
    C.innerHTML='<div class="panel empty stagger"><b>Keine Daten im Zeitfenster</b>Im '+PERIODS[curPeriod]+' wurde nichts getrackt.<br>Wechsle das Zeitfenster oben.</div>';
    document.getElementById('foot').textContent='Stand: __BUILD_DATE__';
    return;
  }

  // ---- Aggregation ueber das Fenster ----
  const sum={}; Object.keys(u.ref).forEach(k=>sum[k]=0); sum["Cholesterin (mg)"]=0;
  const votes={}; CATS.forEach(c=>votes[c.key]=[0,0,0]);
  wd.forEach(day=>{
    Object.keys(sum).forEach(k=>{ sum[k]+=(day.nut[k]||0); });
    CATS.forEach(c=>{ const v=day.cat[c.key]||[0,0,0]; votes[c.key][0]+=v[0]; votes[c.key][1]+=v[1]; votes[c.key][2]+=v[2]; });
  });
  const avg={}; Object.keys(sum).forEach(k=>avg[k]=sum[k]/nDays);

  // ---- Checkpoints ----
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
    checksHtml += checkCard(c.key, cls, status, detail, c.help, i);
  });
  // Cholesterin (weniger = besser)
  (function(){
    const ch=avg["Cholesterin (mg)"];
    const cls = ch<=CHOL_GREEN?'green':(ch<=CHOL_AMBER?'amber':'red');
    const status = cls==='green'?'Gut':(cls==='amber'?'Okay':'Hoch');
    const detail = '\\u00d8 '+Math.round(ch).toLocaleString('de')+' mg/Tag (Ziel \\u2264'+CHOL_GREEN+')';
    checksHtml += checkCard('Cholesterin', cls, status, detail, 'weniger ist besser - Ziel unter '+CHOL_GREEN+' mg/Tag', 3);
  })();

  // ---- Mikronaehrstoffe ----
  let micros=Object.keys(u.ref).map(k=>{
    const [name,unit]=splitUnit(k);
    const a=avg[k]||0, ref=u.ref[k];
    const pctRaw=ref>0?(a/ref*100):0;
    const pct=Math.min(100,pctRaw);
    return {key:k,name,unit,avg:a,ref,pct,pctRaw,color:micColor(pct)};
  });
  micros.sort((x,y)=> curSort==='worst' ? x.pct-y.pct : y.pct-x.pct);

  let barsHtml=micros.map((m,i)=>{
    const full=m.pct>=99.5?' full':'';
    return `<div class="brow stagger" style="animation-delay:${(0.02*i).toFixed(2)}s">
      <div class="bname"><span class="bn">${m.name}</span><span class="bamt">${fmtNum(m.avg)} / ${fmtNum(m.ref)} ${m.unit}</span></div>
      <div class="btrack"><div class="bfill ${m.color}${full}" style="width:${m.pct.toFixed(1)}%"></div></div>
      <div class="bpct ${m.color}">${Math.round(m.pctRaw)}%</div>
    </div>`;
  }).join('');

  C.innerHTML=`
    <div class="sec-title stagger"><h2>Gesundheits-Checkpoints</h2><span class="hint">Ampel im gewaehlten Zeitfenster</span></div>
    <div class="checks">${checksHtml}</div>

    <div class="panel stagger" style="animation-delay:.10s">
      <div class="micro-head">
        <div>
          <h2>Mikronaehrstoffe</h2>
          <div class="mh-sub">\\u00d8 pro Tag vs. Tagesreferenzwert \\u00b7 gedeckelt bei 100 %</div>
        </div>
        <div class="sortbtns" id="sort">
          <button data-s="worst" class="${curSort==='worst'?'active':''}">Schlechteste zuerst</button>
          <button data-s="best" class="${curSort==='best'?'active':''}">Beste zuerst</button>
        </div>
      </div>
      <div class="bars">${barsHtml}</div>
    </div>
  `;

  document.getElementById('sort').querySelectorAll('button').forEach(b=>b.onclick=()=>{curSort=b.dataset.s;render();});
  document.getElementById('foot').textContent =
    'Stand: __BUILD_DATE__ - '+curUser+' - '+PERIODS[curPeriod]+' - Zielwerte: DGE-Tagesreferenz ('+(curUser==='Denis'?'m':'w')+') - automatisch generiert';
}

function checkCard(name, cls, status, detail, help, i){
  return `<div class="check ${cls} stagger" style="animation-delay:${(0.02+0.03*i).toFixed(2)}s">
    <div class="topbar"></div>
    <div class="ck-head"><span class="ck-dot"></span><span class="ck-name">${name}</span></div>
    <div class="ck-status">${status}</div>
    <div class="ck-detail">${detail}</div>
    <div class="ck-help">${help}</div>
  </div>`;
}

document.getElementById('toggle').querySelectorAll('button').forEach(b=>{
  b.onclick=()=>{document.querySelectorAll('#toggle button').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');curUser=b.dataset.u;render();};
});
document.getElementById('pt').querySelectorAll('button').forEach(b=>{
  b.onclick=()=>{document.querySelectorAll('#pt button').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');curPeriod=b.dataset.p;render();};
});
render();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
