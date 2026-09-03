#!/usr/bin/env python3
"""
Notion -> Supabase: die letzte Bruecke.

Der Build liest inzwischen ausschliesslich Supabase. Die Eingabe laeuft aber
noch ueber den /brudi-Skill nach Notion - dieses Skript holt sie herueber.
Es ist damit die EINZIGE verbliebene Notion-Abhaengigkeit im Projekt.

Sobald die Eingabe direkt auf Supabase schreibt, koennen diese Datei, der
Workflow supabase-sync.yml und das Secret NOTION_TOKEN ersatzlos weg.

Laeuft in GitHub Actions und nicht lokal: die Claude-Sandbox erreicht
supabase.co nicht (Egress-Proxy lehnt CONNECT ab), ein Runner schon.

Env:
  NOTION_TOKEN           Notion Internal Integration Token
  SUPABASE_URL           https://<projekt>.supabase.co
  SUPABASE_SERVICE_KEY   service_role-Key (umgeht RLS, nur in Actions)
"""

import json
import os
import sys
import urllib.error
import urllib.request

# Die Spaltenzuordnung gehoert zum Ziel-Schema und steht deshalb dort, wo sie
# dauerhaft gebraucht wird. Hier nur ausgeliehen, damit es sie nur einmal gibt.
from build_dashboard import NUTRIENT_COLUMNS, CATEGORY_COLUMNS

# --- Notion ----------------------------------------------------------------
# Bewusst hier und nicht in build_dashboard: der Build ist notionfrei, und
# beim Abschalten faellt diese Datei als Ganzes weg.
DATA_SOURCE_KCAL = "a748d265-3bbe-448b-b4e8-c8111c208c46"   # Tagesuebersicht
DATA_SOURCE_NUTRI = "be09a702-364a-4f0f-9548-5f4f32092dee"  # Lebensmittel-Analyse
NOTION_VERSION = "2025-09-03"
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")

SUPABASE_URL = (os.environ.get("SUPABASE_URL") or "").rstrip("/")
SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")
CHUNK = 500


def notion_query_all(data_source_id):
    """Alle Seiten einer Notion-Datenquelle (mit Pagination)."""
    url = "https://api.notion.com/v1/data_sources/%s/query" % data_source_id
    headers = {
        "Authorization": "Bearer %s" % NOTION_TOKEN,
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
            sys.stderr.write("Notion-Fehler %s: %s\n"
                             % (e.code, e.read().decode("utf-8", "replace")))
            raise
        results.extend(data.get("results", []))
        if not data.get("has_more"):
            return results
        cursor = data.get("next_cursor")


def num(props, name):
    p = props.get(name)
    return p.get("number") if p else None


def select_name(props, name):
    sel = (props.get(name) or {}).get("select")
    return sel.get("name") if sel else None


def date_start(props, name):
    d = (props.get(name) or {}).get("date")
    return d.get("start")[:10] if d and d.get("start") else None


def title_text(props, name):
    arr = (props.get(name) or {}).get("title") or []
    return "".join(x.get("plain_text", "") for x in arr).strip() or None


def checkbox(props, name):
    return bool((props.get(name) or {}).get("checkbox"))


# --- Supabase ---------------------------------------------------------------
def upsert(table, rows):
    """Zeilen in Bloecken upserten, Konflikt auf notion_id."""
    if not rows:
        print("  %s: nichts zu schreiben" % table)
        return 0
    url = "%s/rest/v1/%s?on_conflict=notion_id" % (SUPABASE_URL, table)
    headers = {
        "apikey": SERVICE_KEY,
        "Authorization": "Bearer %s" % SERVICE_KEY,
        "Content-Type": "application/json",
        # merge-duplicates macht den Lauf wiederholbar, minimal=keine Rueckgabe
        "Prefer": "resolution=merge-duplicates,return=minimal",
    }
    written = 0
    for i in range(0, len(rows), CHUNK):
        block = rows[i:i + CHUNK]
        req = urllib.request.Request(
            url, data=json.dumps(block, ensure_ascii=False).encode("utf-8"),
            headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req) as resp:
                resp.read()
        except urllib.error.HTTPError as e:
            sys.stderr.write("Supabase-Fehler %s bei %s: %s\n"
                             % (e.code, table, e.read().decode("utf-8", "replace")))
            raise
        written += len(block)
        print("  %s: %d/%d" % (table, written, len(rows)))
    return written


def build_tage_rows(pages):
    """Tagesuebersicht. Zeilen ohne Person oder Datum sind nicht zuzuordnen
    und werden uebersprungen statt halb geschrieben."""
    rows, skipped = [], 0
    for pg in pages:
        props = pg.get("properties", {})
        person, datum = select_name(props, "Person"), date_start(props, "Datum")
        if not person or not datum:
            skipped += 1
            continue
        rows.append({
            "notion_id": pg["id"],
            "person": person,
            "datum": datum,
            "tag": title_text(props, "Tag"),
            "kalorien_kcal": num(props, "Kalorien (kcal)"),
            "protein_g": num(props, "Protein (g)"),
            "kohlenhydrate_g": num(props, "Kohlenhydrate (g)"),
            "fett_g": num(props, "Fett (g)"),
            "kalorienziel_kcal": num(props, "Kalorienziel (kcal)"),
            "gewicht_kg": num(props, "Gewicht (kg)"),
            "zielgewicht": num(props, "Zielgewicht"),
        })
    return rows, skipped


def build_analyse_rows(pages):
    """Lebensmittel-Analyse. Das Duplikat-Kennzeichen wird mitgenommen statt
    gefiltert - was Duplikat ist, entscheidet die Auswertung, nicht der Sync."""
    rows, skipped = [], 0
    for pg in pages:
        props = pg.get("properties", {})
        person, datum = select_name(props, "Person"), date_start(props, "Datum")
        if not person or not datum:
            skipped += 1
            continue
        row = {
            "notion_id": pg["id"],
            "person": person,
            "datum": datum,
            "lebensmittel": title_text(props, "Lebensmittel"),
            "duplikat": checkbox(props, "Duplikat"),
            "kalorien_kcal": num(props, "Kalorien (kcal)"),
        }
        for prop, col in NUTRIENT_COLUMNS.items():
            row[col] = num(props, prop)
        for prop, col in CATEGORY_COLUMNS.items():
            row[col] = select_name(props, prop)
        rows.append(row)
    return rows, skipped


def main():
    missing = [n for n, v in (("NOTION_TOKEN", NOTION_TOKEN),
                              ("SUPABASE_URL", SUPABASE_URL),
                              ("SUPABASE_SERVICE_KEY", SERVICE_KEY)) if not v]
    if missing:
        sys.stderr.write("Fehler: %s nicht gesetzt.\n" % ", ".join(missing))
        sys.exit(1)

    print("Notion lesen ...")
    tage_pages = notion_query_all(DATA_SOURCE_KCAL)
    analyse_pages = notion_query_all(DATA_SOURCE_NUTRI)
    print("  %d Tageszeilen, %d Analysezeilen" % (len(tage_pages), len(analyse_pages)))

    tage_rows, tage_skipped = build_tage_rows(tage_pages)
    analyse_rows, analyse_skipped = build_analyse_rows(analyse_pages)

    print("Nach Supabase schreiben ...")
    n_tage = upsert("tagesuebersicht", tage_rows)
    n_analyse = upsert("lebensmittel_analyse", analyse_rows)

    print("Fertig: %d Tageszeilen, %d Analysezeilen gespiegelt." % (n_tage, n_analyse))
    if tage_skipped or analyse_skipped:
        print("Uebersprungen (ohne Person oder Datum): %d Tages-, %d Analysezeilen."
              % (tage_skipped, analyse_skipped))


if __name__ == "__main__":
    main()
