#!/usr/bin/env python3
"""
Notion -> Supabase spiegeln.

Uebergangswerkzeug fuer den Umzug: solange die Eintraege noch ueber den
/brudi-Skill in Notion landen, holt dieser Lauf sie nach Supabase. Sobald die
Eingabe direkt auf Supabase schreibt, wird das Skript ueberfluessig.

Laeuft absichtlich in GitHub Actions und nicht lokal: die Claude-Sandbox
erreicht supabase.co nicht (Egress-Proxy), ein Runner schon.

Die Notion-Seite wird nicht neu implementiert, sondern aus build_dashboard
importiert - eine Aenderung an den Feldern wirkt damit an beiden Stellen.

Env:
  NOTION_TOKEN           Notion Internal Integration Token
  SUPABASE_URL           z. B. https://<projekt>.supabase.co
  SUPABASE_SERVICE_KEY   service_role-Key (umgeht RLS, nur in Actions)
"""

import json
import os
import sys
import urllib.error
import urllib.request

from build_dashboard import (
    DATA_SOURCE_KCAL, DATA_SOURCE_NUTRI, notion_query_all,
    num, select_name, date_start, title_text, checkbox,
)

SUPABASE_URL = (os.environ.get("SUPABASE_URL") or "").rstrip("/")
SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")
CHUNK = 500

# Notion-Property -> Supabase-Spalte. Einheiten wandern in den Spaltennamen,
# damit in SQL keine Klammern und Sonderzeichen zu quoten sind.
NUTRIENT_COLUMNS = {
    "Ballaststoffe (g)": "ballaststoffe_g",
    "Calcium (mg)": "calcium_mg",
    "Eisen (mg)": "eisen_mg",
    "Folat (µg)": "folat_ug",
    "Jod (µg)": "jod_ug",
    "Kalium (mg)": "kalium_mg",
    "Magnesium (mg)": "magnesium_mg",
    "Omega-3 (g)": "omega3_g",
    "Selen (µg)": "selen_ug",
    "Vitamin A (µg)": "vitamin_a_ug",
    "Vitamin B12 (µg)": "vitamin_b12_ug",
    "Vitamin C (mg)": "vitamin_c_mg",
    "Vitamin D (µg)": "vitamin_d_ug",
    "Vitamin E (mg)": "vitamin_e_mg",
    "Vitamin K (µg)": "vitamin_k_ug",
    "Zink (mg)": "zink_mg",
    "Cholesterin (mg)": "cholesterin_mg",
}
CATEGORY_COLUMNS = {
    "Darmgesundheit": "darmgesundheit",
    "Low FODMAP": "low_fodmap",
    "Säure-Base": "saeure_base",
}


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
            body = e.read().decode("utf-8", "replace")
            sys.stderr.write("Supabase-Fehler %s bei %s: %s\n" % (e.code, table, body))
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
    missing = [n for n, v in (("NOTION_TOKEN", os.environ.get("NOTION_TOKEN")),
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
