#!/usr/bin/env python3
"""
Kalorienbrudi Dashboard Generator
---------------------------------
Zieht alle Eintraege aus der Notion-Datenbank und erzeugt eine statische index.html.
Benoetigt nur die Python-Standardbibliothek (urllib) – kein pip install.

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
DATA_SOURCE_ID = "a748d265-3bbe-448b-b4e8-c8111c208c46"
NOTION_VERSION = "2025-09-03"   # Version mit /v1/data_sources Endpunkten
TOKEN = os.environ.get("NOTION_TOKEN")

# Pro Person fixe Einstellungen, die nicht in Notion stehen
PERSON_CONFIG = {
    "Denis": {"accent": "#4DA6FF", "accent2": "#1E6FD9", "deficitTarget": 1000,
              "greenBuf": 95, "zielWeight": 80, "goalIntake": 1900},
    "Leni":  {"accent": "#FF6FB5", "accent2": "#D94D92", "deficitTarget": 500,
              "greenBuf": 75, "zielWeight": 60, "goalIntake": 1500},
}


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
# Daten aufbereiten
# ----------------------------------------------------------------------------
def build_data(pages):
    raw = {k: [] for k in PERSON_CONFIG}
    for pg in pages:
        props = pg.get("properties", {})
        person = select_name(props, "Person")
        if person not in raw:
            continue
        d = date_start(props, "Datum")
        kcal = num(props, "Kalorien (kcal)")
        if d is None or kcal is None:
            continue  # Tage ohne Datum oder ohne Essen ueberspringen
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
        data[person] = {
            "accent": cfg["accent"], "accent2": cfg["accent2"],
            "goalIntake": goal, "deficitTarget": cfg["deficitTarget"],
            "weight": weight, "startWeight": start_weight,
            "zielWeight": ziel, "greenBuf": cfg["greenBuf"],
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
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%d.%m.%Y")
    html = (HTML_TEMPLATE
            .replace("__DATA_JSON__", json.dumps(data, ensure_ascii=False))
            .replace("__BUILD_DATE__", today))
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html geschrieben. Denis: %d Tage, Leni: %d Tage"
          % (len(data["Denis"]["days"]), len(data["Leni"]["days"])))


# ----------------------------------------------------------------------------
# HTML-Template (Daten werden ueber __DATA_JSON__ injiziert)
# ----------------------------------------------------------------------------
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kalorienbrudi - Dashboard</title>
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
  }
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{background:var(--bg);color:var(--text);font-family:var(--body)}
  body{
    padding:26px;
    background-image:radial-gradient(circle at 12% 0%, rgba(77,166,255,.06), transparent 42%),
                     radial-gradient(circle at 100% 100%, rgba(255,111,181,.05), transparent 40%);
    min-height:100vh;
  }
  .grain{position:fixed;inset:0;pointer-events:none;opacity:.035;z-index:99;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");}
  .wrap{max-width:1080px;margin:0 auto}

  header{display:flex;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;gap:18px;margin-bottom:24px}
  .brand{display:flex;flex-direction:column;gap:2px}
  .brand .kicker{font-family:var(--mono);font-size:11px;letter-spacing:.32em;text-transform:uppercase;color:var(--muted)}
  .brand h1{font-family:var(--display);font-weight:800;font-size:34px;letter-spacing:-.02em;line-height:1}
  .brand h1 b{color:var(--accent);transition:color .4s}
  .toggle{display:flex;background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:5px;gap:4px}
  .toggle button{font-family:var(--display);font-weight:600;font-size:15px;color:var(--muted);background:none;border:none;
    padding:9px 22px;border-radius:10px;cursor:pointer;transition:.25s;display:flex;align-items:center;gap:8px}
  .toggle button .dot{width:9px;height:9px;border-radius:50%}
  .toggle button[data-u="Denis"] .dot{background:#4DA6FF}
  .toggle button[data-u="Leni"] .dot{background:#FF6FB5}
  .toggle button.active{color:#15130F}
  .toggle button.active[data-u="Denis"]{background:#4DA6FF}
  .toggle button.active[data-u="Leni"]{background:#FF6FB5}

  .top{display:grid;grid-template-columns:300px 1fr;gap:16px;margin-bottom:16px}
  @media(max-width:780px){.top{grid-template-columns:1fr}}
  .panel{background:var(--panel);border:1px solid var(--border);border-radius:18px;padding:20px}
  .panel .label{font-family:var(--mono);font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--faint);margin-bottom:14px}

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
  .metric-toggle button.active{background:var(--accent);color:#15130F;border-color:var(--accent);font-weight:500}
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
  <header>
    <div class="brand">
      <span class="kicker">Kalorienbrudi</span>
      <h1>Dashboard <b id="userName">Denis</b></h1>
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
const DATA = __DATA_JSON__;
const RATIO={p:0.30,f:0.30,c:0.40};
const METRICS={kcal:{label:'Kalorien',unit:'kcal'},p:{label:'Protein',unit:'g'},f:{label:'Fett',unit:'g'},c:{label:'Carbs',unit:'g'}};

/* ============================================================
   EINSTELLUNG: wie viele der LETZTEN Perioden unten anzeigen
   3 = letzte 3 (Wochen / Monate / Jahre, je nach Auswahl)
   0 = alle anzeigen (kein Limit)
   ============================================================ */
const PERIOD_LIMIT = 3;

let curUser='Denis', curMetric='kcal', curPeriod='W';

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

function render(){
  const u=DATA[curUser];
  document.documentElement.style.setProperty('--accent',u.accent);
  document.documentElement.style.setProperty('--accent2',u.accent2);
  document.getElementById('userName').textContent=curUser;
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
  const saved=u.days.reduce((s,x)=>s+(maint-x.kcal),0);
  const sw=(u.startWeight!=null?u.startWeight:u.weight);
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
  document.getElementById('mt').querySelectorAll('button').forEach(b=>b.onclick=()=>{curMetric=b.dataset.m;render();});
  document.getElementById('pt').querySelectorAll('button').forEach(b=>b.onclick=()=>{curPeriod=b.dataset.p;render();});
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

document.getElementById('toggle').querySelectorAll('button').forEach(b=>{
  b.onclick=()=>{document.querySelectorAll('#toggle button').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');curUser=b.dataset.u;curMetric='kcal';render();};
});
render();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
