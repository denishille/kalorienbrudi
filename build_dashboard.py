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
import re
import sys
import json
import datetime
import urllib.request
import urllib.error
from collections import Counter, defaultdict

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

# Erlaubte relative Abweichung zwischen Tages-Total (Tagesuebersicht) und der
# Summe der Einzelposten (Lebensmittel-Analyse). Darueber -> Warn-Flag im Build.
KCAL_TOL = 0.05


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
    """Titel-Property als Klartext."""
    p = props.get(name) or {}
    arr = p.get("title") or []
    t = "".join(x.get("plain_text", "") for x in arr).strip()
    return t or None


def checkbox(props, name):
    p = props.get(name) or {}
    return bool(p.get("checkbox"))


# ----------------------------------------------------------------------------
# Konsistenzpruefung: Tages-Total (Tagesuebersicht) vs. Einzelposten-Summe
# (Lebensmittel-Analyse). Deckt Erfassungsfehler frueh im Build auf, ohne den
# Build abzubrechen - es werden nur Warnungen ausgegeben und Tage markiert.
# ----------------------------------------------------------------------------
def analyse_kcal_by_day(nutri_pages):
    """Pro (Person, Datum): Summe der Einzelposten-Kalorien aus der Analyse-DB."""
    by_day = defaultdict(float)
    for pg in nutri_pages:
        props = pg.get("properties", {})
        if checkbox(props, "Duplikat"):
            continue
        person = select_name(props, "Person")
        d = date_start(props, "Datum")
        if person is None or d is None:
            continue
        by_day[(person, d)] += num(props, "Kalorien (kcal)") or 0
    return by_day


# Deutsche Wochentage (Montag = Index 0), fuer den Datum-vs-Wochentag-Abgleich.
WD_DE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag",
         "Freitag", "Samstag", "Sonntag"]


def check_weekday_consistency(kcal_pages):
    """Vergleicht den im Titel 'Tag' erfassten Wochentag mit dem tatsaechlichen
    Wochentag des Datums (z. B. 'Mittwoch, 21.05.26', obwohl der 21.05. ein
    Donnerstag ist). Deckt Erfassungsfehler frueh auf und verhindert falsche
    Zeitachsen. Gibt eine sortierte Liste von Warntexten zurueck - der Build
    laeuft weiter (nur Warnung, kein Abbruch)."""
    warns = []
    for pg in kcal_pages:
        props = pg.get("properties", {})
        person = select_name(props, "Person")
        d = date_start(props, "Datum")
        tag = title_text(props, "Tag")
        if person not in PERSON_CONFIG or d is None or not tag:
            continue
        try:
            wd = WD_DE[datetime.date.fromisoformat(d).weekday()]
        except ValueError:
            continue
        if not tag.strip().startswith(wd):
            warns.append("%s %s: Wochentag '%s' != tatsaechlich %s"
                         % (person, d, tag, wd))
    warns.sort()
    return warns


def check_kcal_consistency(kcal_pages, analyse_kcal):
    """Vergleicht Tages-Total mit der Einzelposten-Summe pro (Person, Tag).
    Gibt eine sortierte Liste von Warntexten zurueck (kein Build-Abbruch)."""
    warns = []
    for pg in kcal_pages:
        props = pg.get("properties", {})
        person = select_name(props, "Person")
        d = date_start(props, "Datum")
        total = num(props, "Kalorien (kcal)")
        if person not in PERSON_CONFIG or d is None or total is None:
            continue
        key = (person, d)
        if key in analyse_kcal:
            s = analyse_kcal[key]
            if s and abs(s - total) / max(total, 1) > KCAL_TOL:
                warns.append("%s %s: Total %d != Analyse-Summe %d kcal"
                             % (person, d, round(total), round(s)))
        else:
            warns.append("%s %s: keine Lebensmittel-Analyse-Zeilen (Trennung fehlt)"
                         % (person, d))
    warns.sort()
    return warns


# ----------------------------------------------------------------------------
# Sammelposten-Heuristik: verdaechtige, nicht getrennte Analyse-Zeilen erkennen.
# Zusammengesetzte Gerichte ("Bowl", "Pad Krapao Basis", "... mit ...") sollten
# in Einzel-Zutaten aufgeteilt sein, sonst sind die Makros pro Zutat nicht
# belastbar. Marken-/Fertigprodukte bleiben bewusst EINE Zeile (kein Split).
# Das Flag bricht den Build nicht ab - es warnt und wird im Dashboard angezeigt.
# ----------------------------------------------------------------------------
COMPOSITE_HINTS = [" mit ", " + ", " und ", " auf "]
# Marken/Fertigprodukte: bleiben EINE Zeile, nicht als Sammelposten flaggen.
BRAND_HINTS = ["rewe", "ehrmann", "gustavo", "nuii", "ben & jerry", "koelln",
               "kellogg", "biscoff", "finello", "buko", "billie green", "arla",
               "oakberry", "esn", "clearwhey", "clear whey", "fritz", "toblerone",
               "langnese", "prep my meal", "kinder", "oreo", "taifun", "bonduelle",
               "koro", "ppura", "skyr", "harzer", "riegel", "mousse"]


def looks_like_composite(name):
    """True, wenn der Name nach einem zusammengesetzten Gericht/Sammelposten
    aussieht und NICHT als Markenprodukt erkannt wird. Klammer-Zusaetze
    (Mengen, Zutaten-Erlaeuterungen) werden vor der Pruefung entfernt."""
    low = re.sub(r"\([^)]*\)", "", (name or "")).lower().strip()
    if not low:
        return False
    if any(b in low for b in BRAND_HINTS):
        return False
    return any(k in low for k in COMPOSITE_HINTS) or low.count(",") >= 1


def check_composite_items(nutri_pages):
    """Sammelt verdaechtige Sammelposten pro Person. Gibt (warns, counts) zurueck:
    warns = sortierte Warntexte (kein Build-Abbruch), counts = {Person: Anzahl}."""
    warns, counts = [], defaultdict(int)
    for pg in nutri_pages:
        props = pg.get("properties", {})
        if checkbox(props, "Duplikat"):
            continue
        person = select_name(props, "Person")
        name = title_text(props, "Lebensmittel")
        d = date_start(props, "Datum")
        if person not in NUTRI_CONFIG or not name:
            continue
        if looks_like_composite(name):
            counts[person] += 1
            warns.append("%s %s: '%s' evtl. Sammelposten - in Einzel-Zutaten aufteilen?"
                         % (person, d or "?", name))
    warns.sort()
    return warns, counts


# ----------------------------------------------------------------------------
# Lebensmittel-Namen clustern (nur fuer Top/Flop-Anzeige; Naehrstoff-Summen
# rechnen weiter ueber die Zahlenspalten und bleiben unberuehrt).
# "100ml Milch 1,8%" == "Milch 1,8% (250ml)" == "Milch fettarm" usw.
# ----------------------------------------------------------------------------
_PARENS = re.compile(r"\s*\([^)]*\)")
_NUMUNIT = re.compile(r"^(?:~?\d+(?:[.,]\d+)?(?:/\d+)?|[½¼¾⅓⅔⅛])\s*(?:x|g|kg|ml|l)?$", re.I)
_UNIT_WORDS = {
    "g", "kg", "ml", "l", "el", "tl", "x", "st", "stk", "stück", "stücke",
    "scheibe", "scheiben", "portion", "portionen", "packung", "packungen",
    "kugel", "kugeln", "hand", "hände", "handvoll", "löffel", "teller",
    "becher", "glas", "gläser", "dose", "dosen", "riegel", "tasse", "tassen",
    "prise", "prisen", "paar", "ein", "eine", "achtel", "viertel",
}
_SIZE_WORDS = {
    "klein", "kleine", "kleiner", "kleines", "groß", "große", "großer",
    "großes", "gross", "grosse", "halbe", "halber", "halbes", "gehäuft",
    "gehäufte", "abgepackte", "abgepackter", "mini",
}
# Manuell gepflegte Cluster (links: Varianten, rechts: Anzeigename).
# Bei neuen Dubletten in den Tops/Flops hier einfach eine Zeile ergaenzen.
_ALIAS_SRC = {
    "eier": "Ei", "eier in wenig öl": "Ei", "ei mit ölspray": "Ei",
    "spiegeleier": "Spiegelei", "espressi": "Espresso",
    "milch": "Milch (fettarm)", "milch fettarm": "Milch (fettarm)",
    "fettarme milch": "Milch (fettarm)", "milch 1,5%": "Milch (fettarm)",
    "milch 1,8%": "Milch (fettarm)",
    "joghurt": "Joghurt (fettarm)", "joghurt fettarm": "Joghurt (fettarm)",
    "fettarmer joghurt": "Joghurt (fettarm)", "joghurt 1,5%": "Joghurt (fettarm)",
    "joghurt 1,8%": "Joghurt (fettarm)", "naturjoghurt": "Joghurt (fettarm)",
    "naturjoghurt 1,8%": "Joghurt (fettarm)",
    "skyr": "Skyr", "arla skyr": "Skyr",
    "biscoff": "Biscoff Creme", "biscoff creme": "Biscoff Creme",
    "lotus biscoff creme": "Biscoff Creme",
    "biscoff eis am stiel": "Biscoff Eis",
    "esn clear whey zitrone": "ESN Clear Whey Zitrone",
    "esn clearwhey zitrone": "ESN Clear Whey Zitrone",
    "esn isoclear zitrone": "ESN Clear Whey Zitrone",
    "finello high protein": "Finello Mozzarella",
    "finello high protein mozzarella": "Finello Mozzarella",
    "finello protein mozzarella": "Finello Mozzarella",
    "finello mozzarella": "Finello Mozzarella",
    "käse light": "Käse light", "light-käse": "Käse light",
    "käseaufschnitt leicht": "Käse light", "käseaufschnitt light": "Käse light",
    "käse fettreduziert": "Käse light",
    "gouda lite": "Gouda light", "gouda light": "Gouda light",
    "mozzarella light": "Mozzarella light", "light mozzarella": "Mozzarella light",
    "buko": "Buko Balance", "buko balance": "Buko Balance",
    "buko balance frischkäse": "Buko Balance",
    "harzer käse": "Harzer Käse", "quäse harzer käse": "Harzer Käse",
    "kellogg's tresor müsli": "Kellogg's Tresor",
    "flat white hafer": "Flat White (Hafermilch)",
    "flat white hafermilch": "Flat White (Hafermilch)",
    "flat white mit hafermilch": "Flat White (Hafermilch)",
    "cappuccino mit hafermilch": "Cappuccino (Hafermilch)",
    "hafercappuccino": "Cappuccino (Hafermilch)",
    "hähnchenbrust bio": "Hähnchenbrust",
    "erdnuss-soja-dip": "Erdnuss-Dip", "erdnussmus-soja-dip": "Erdnuss-Dip",
    "erdnusssauce": "Erdnuss-Dip",
    "aioli-paste": "Aioli", "aioli-joghurt-soße": "Aioli-Joghurt-Dip",
    "ehrmann high protein choco mousse": "Ehrmann Protein Schokomousse",
    "ehrmann high protein schokomousse": "Ehrmann Protein Schokomousse",
    "ben & jerry's cookie eis": "Ben & Jerry's Eis",
    "ben & jerry's eis": "Ben & Jerry's Eis",
    "nuii eis pekannuss caramel": "Nuii Eis",
    "joghurtsauce": "Joghurtsoße",
}


def _squash(s):
    """Vergleichs-Key: kleingeschrieben, ohne Leerzeichen/Bindestriche etc."""
    return re.sub(r"[^0-9a-zäöüß%]", "", s.casefold())


ALIAS_KEY = {}
ALIAS_DISPLAY = {}
for _src, _dst in _ALIAS_SRC.items():
    ALIAS_KEY[_squash(_src)] = _squash(_dst)
    ALIAS_DISPLAY[_squash(_dst)] = _dst


def clean_food_name(t):
    """Mengen-/Groessenangaben vorne, hinten und in Klammern entfernen."""
    s = _PARENS.sub("", t).strip()
    words = s.split()
    while words:
        w = words[0].casefold().strip(".")
        if _NUMUNIT.match(words[0]) or w in _UNIT_WORDS or w in _SIZE_WORDS:
            words.pop(0)
        else:
            break
    while words and _NUMUNIT.match(words[-1]):
        words.pop()
    return " ".join(words) or t.strip()


def make_canon(names):
    """Map: Original-Titel -> kanonischer Anzeigename (geclustert)."""
    cleaned = {nm: clean_food_name(nm) for nm in set(names)}
    key_of, variants = {}, defaultdict(Counter)
    for nm, c in cleaned.items():
        k = _squash(c)
        k = ALIAS_KEY.get(k, k)
        key_of[nm] = k
        variants[k][ALIAS_DISPLAY.get(k, c)] += 1
    # Plural -> Singular zusammenfuehren (Bananen->Banane, Wraps->Wrap)
    redirect = {}
    for k in list(variants):
        if k and k[-1] in "sn" and k[:-1] in variants:
            variants[k[:-1]].update(variants.pop(k))
            redirect[k] = k[:-1]
    disp = {k: min(cnt.most_common(), key=lambda t: (-t[1], len(t[0])))[0]
            for k, cnt in variants.items()}
    return {nm: disp[redirect.get(k, k)] for nm, k in key_of.items()}


# ----------------------------------------------------------------------------
# Kalorien-Daten aufbereiten
# ----------------------------------------------------------------------------
def build_kcal_data(pages, analyse_kcal=None):
    analyse_kcal = analyse_kcal or {}
    raw = {k: [] for k in PERSON_CONFIG}
    # Tage, die in Notion existieren, aber keine Kalorien tragen (v.a. Leni):
    # werden NICHT gewertet, aber gezaehlt und im Dashboard gekennzeichnet.
    skipped = {k: [] for k in PERSON_CONFIG}
    for pg in pages:
        props = pg.get("properties", {})
        person = select_name(props, "Person")
        if person not in raw:
            continue
        d = date_start(props, "Datum")
        kcal = num(props, "Kalorien (kcal)")
        if d is None:
            continue
        if kcal is None:
            skipped[person].append(d)
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
        days = []
        mismatch = 0
        mismatch_list = []
        for e in entries:
            day = {"d": e["d"], "kcal": e["kcal"], "p": e["p"], "c": e["c"], "f": e["f"]}
            s = analyse_kcal.get((person, e["d"]))
            if s and abs(s - e["kcal"]) / max(e["kcal"], 1) > KCAL_TOL:
                day["flag"] = True
                mismatch += 1
                mismatch_list.append({"d": e["d"], "t": round(e["kcal"]), "s": round(s)})
            days.append(day)
        # Fallback auf Standardwerte, wenn Notion die Spalte durchgehend leer laesst.
        goal_from_data = any(e["goalIntake"] for e in entries)
        ziel_from_data = any(e["zielWeight"] for e in entries)
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
            "quality": {
                "trackedDays": len(days),
                "skippedDays": len(skipped[person]),
                "skippedList": sorted(skipped[person]),
                "mismatchDays": mismatch,
                "mismatchList": mismatch_list,
                "goalFromData": goal_from_data,
                "zielFromData": ziel_from_data,
                "weightFromData": bool(weights),
            },
        }
    return data


# ----------------------------------------------------------------------------
# Naehrstoff-Daten aufbereiten: pro Person -> pro Tag aggregiert
# cf = pro Kategorie [positive Lebensmittel, negative Lebensmittel] des Tages
# ----------------------------------------------------------------------------
def build_nutri_data(pages, composite_counts=None):
    composite_counts = composite_counts or {}
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
        canon = make_canon([e["name"] for e in raw[person] if e.get("name")])
        bydate = {}
        for e in raw[person]:
            day = bydate.get(e["d"])
            if day is None:
                day = {"d": e["d"], "n": 0,
                       "nut": {k: 0 for k in NUM_KEYS},
                       "cat": {c: [0, 0, 0] for c in CAT_KEYS},
                       "cf": {c: [[], []] for c in CAT_KEYS},
                       "chol": {}}
                bydate[e["d"]] = day
            day["n"] += 1
            for k in NUM_KEYS:
                day["nut"][k] += e[k]
            nm = canon.get(e.get("name"))
            mg = e.get("Cholesterin (mg)") or 0
            if nm and mg:
                day["chol"][nm] = day["chol"].get(nm, 0) + mg
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
        # Top-Quellen je Naehrstoff aus dem eigenen Log (Klick auf Balken)
        nut_src = {k: {} for k in NUM_KEYS}
        for e in raw[person]:
            nm = canon.get(e.get("name"))
            if not nm or nm.startswith("Ausgleich"):
                continue
            for k in NUM_KEYS:
                v = e[k]
                if v and v > 0:
                    t = nut_src[k].setdefault(nm, [0.0, 0])
                    t[0] += v
                    t[1] += 1
        nut_top = {}
        for k, foods in nut_src.items():
            best = sorted(foods.items(), key=lambda x: -x[1][0])[:3]
            nut_top[k] = [[n, round(t[0] / t[1], 2)] for n, t in best]
        data[person] = {
            "accent": cfg["accent"], "accent2": cfg["accent2"],
            "ref": REF[cfg["sex"]],
            "days": days,
            "nutTop": nut_top,
            "quality": {
                "compositeItems": composite_counts.get(person, 0),
            },
        }
    return data


# ----------------------------------------------------------------------------
# Hauptlogik
# ----------------------------------------------------------------------------
def main():
    if not TOKEN:
        sys.stderr.write("Fehler: NOTION_TOKEN ist nicht gesetzt.\n")
        sys.exit(1)
    kcal_pages = notion_query_all(DATA_SOURCE_KCAL)
    nutri_pages = notion_query_all(DATA_SOURCE_NUTRI)
    analyse_kcal = analyse_kcal_by_day(nutri_pages)
    comp_warns, comp_counts = check_composite_items(nutri_pages)
    kcal = build_kcal_data(kcal_pages, analyse_kcal)
    nutri = build_nutri_data(nutri_pages, comp_counts)

    # Warn-Flag: Tages-Total vs. Einzelposten-Summe (bricht den Build nicht ab).
    warns = check_kcal_consistency(kcal_pages, analyse_kcal)
    if warns:
        sys.stderr.write("WARNUNG: %d Tag(e) mit Total<->Analyse-Abweichung:\n" % len(warns))
        for w in warns:
            sys.stderr.write("  - %s\n" % w)

    # Warn-Flag: erfasster Wochentag vs. echtes Datum (bricht den Build nicht ab).
    wd_warns = check_weekday_consistency(kcal_pages)
    if wd_warns:
        sys.stderr.write("WARNUNG: %d Tag(e) mit falschem Wochentag:\n" % len(wd_warns))
        for w in wd_warns:
            sys.stderr.write("  - %s\n" % w)

    # Warn-Flag: verdaechtige Sammelposten (nicht getrennte Analyse-Zeilen).
    if comp_warns:
        sys.stderr.write("WARNUNG: %d verdaechtige(r) Sammelposten (Zutaten-Trennung fehlt evtl.):\n"
                         % len(comp_warns))
        for w in comp_warns:
            sys.stderr.write("  - %s\n" % w)

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
    skipped_total = sum(kcal[p]["quality"]["skippedDays"] for p in PERSON_CONFIG)
    print("Konsistenz: %d Warnung(en) Total<->Analyse, %d Wochentag-Abweichung(en), "
          "%d verdaechtige(r) Sammelposten, %d Tag(e) ohne Kalorien uebersprungen"
          % (len(warns), len(wd_warns), len(comp_warns), skipped_total))


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
    --text:#EDE6D8; --muted:#B4AB9A; --faint:#8E8577;
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
    padding:26px;padding-top:92px;
    background-image:radial-gradient(circle at 12% 0%, rgba(77,166,255,.06), transparent 42%),
                     radial-gradient(circle at 100% 100%, rgba(255,111,181,.05), transparent 40%);
    min-height:100vh;transition:background-color .35s,color .35s;
  }
  .grain{position:fixed;inset:0;pointer-events:none;opacity:.035;z-index:99;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");}
  .wrap{max-width:1080px;margin:0 auto}

  /* ---- fixe Top-Navigation ---- */
  .topnav{position:fixed;top:0;left:0;right:0;z-index:60;
    background:rgba(33,29,23,.92);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
    border-bottom:1px solid var(--border);box-shadow:0 6px 24px rgba(0,0,0,.25)}
  .tn-inner{max-width:1080px;margin:0 auto;padding:10px 26px;display:flex;align-items:center;
    justify-content:space-between;gap:14px;flex-wrap:wrap}
  .topnav .pagenav{margin-bottom:0}
  .pagenav button svg{width:15px;height:15px;stroke:currentColor;fill:none;stroke-width:1.8;
    stroke-linecap:round;stroke-linejoin:round;opacity:.85;flex:none}
  .topnav .toggle{padding:4px;border-radius:12px;background:var(--panel2)}
  .topnav .toggle button{padding:7px 14px;font-size:13.5px}

  header{display:flex;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;gap:18px;margin-bottom:22px}
  .brand{display:flex;flex-direction:column;gap:2px}
  .brand .kicker{font-family:var(--mono);font-size:11px;letter-spacing:.30em;text-transform:uppercase;color:var(--muted)}
  .brand h1{font-family:var(--display);font-weight:800;font-size:33px;letter-spacing:-.02em;line-height:1}
  .brand h1 b{color:var(--accent);transition:color .4s}

  .pagenav{display:flex;align-items:center;gap:11px}
  .pagenav button{display:inline-flex;align-items:center;gap:7px;font-family:var(--mono);font-size:11px;letter-spacing:.18em;text-transform:uppercase;
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

  .panel{background:var(--panel);border:1px solid var(--border);border-radius:18px;padding:24px}
  .panel .label{font-family:var(--mono);font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--faint);margin-bottom:14px}

  /* ===================== KALORIEN-SEITE ===================== */
  .top{display:grid;grid-template-columns:300px 1fr;gap:16px;margin-bottom:16px}
  @media(max-width:780px){.top{grid-template-columns:1fr}}
  .goals .goalrow{display:flex;align-items:baseline;justify-content:space-between;padding:13px 0;border-bottom:1px solid rgba(237,230,216,.08)}
  .goals .goalrow:last-child{border-bottom:none}
  .goals .gk{font-size:14px;color:var(--muted)}
  .goals .gv{font-family:var(--mono);font-size:18px;font-weight:500;color:var(--text);text-align:right}
  .goals .gv small{font-size:12px;color:var(--faint)}
  .goals .gv.accent{color:var(--accent)}
  .goals .gv.macro{font-size:13px}
  .goals .gv.macro b{color:var(--text);font-weight:500}
  .goals .gv .std{font-family:var(--mono);font-size:10px;color:var(--faint);margin-left:4px}
  .goals .dq-note{margin-top:14px;background:rgba(240,192,74,.10);border:1px solid rgba(240,192,74,.32);
    border-radius:12px;padding:11px 14px;font-family:var(--body);font-size:12px;line-height:1.6;color:var(--amber)}
  .goals .dq-note a{color:var(--amber);font-weight:500;text-decoration:none;display:inline-block;margin-top:6px;border-bottom:1px solid rgba(240,192,74,.5);cursor:pointer}
  .dq-details{margin-top:9px;padding-top:4px;border-top:1px solid rgba(240,192,74,.25)}
  .dq-details .dqd-h{font-family:var(--mono);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--amber);margin:8px 0 3px}
  .dq-details .dqd-row{display:flex;justify-content:space-between;gap:12px;font-size:11.5px;color:var(--text);line-height:1.6;flex-wrap:wrap}
  .goals .dq-note .dqh{color:var(--faint);letter-spacing:.14em;text-transform:uppercase;font-size:9.5px;display:block;margin-bottom:5px}
  .goals .dq-note div{color:var(--muted)}
  .goals .dq-note b{color:var(--text);font-weight:500}
  .progress{margin-bottom:16px;padding-bottom:15px;border-bottom:1px dashed var(--border)}
  .progress .prow{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:8px}
  .progress .pk{font-size:13px;color:var(--text);font-weight:500}
  .progress .ppct{font-family:var(--mono);font-size:17px;font-weight:500;color:var(--accent)}
  .progress .ptrack{height:10px;background:var(--panel2);border-radius:6px;overflow:hidden;border:1px solid var(--border)}
  .progress .pfill{height:100%;border-radius:6px;background:linear-gradient(90deg,var(--accent2),var(--accent));transition:width .7s cubic-bezier(.2,.8,.2,1)}
  .progress .pcap{margin-top:8px;font-family:var(--body);font-size:12px;color:var(--muted);line-height:1.5}
  .progress .pcap b{color:var(--text);font-weight:500}
  /* Semantik-Status (gruen/gelb/rot) - identisch fuer Denis UND Leni */
  .progress .prow .ppct.green{color:var(--green)} .progress .prow .ppct.amber{color:var(--amber)} .progress .prow .ppct.red{color:var(--red)}
  .status-pill{display:inline-flex;align-items:center;gap:6px;font-family:var(--body);font-weight:500;font-size:11px;
    padding:4px 10px;border-radius:999px;letter-spacing:.01em;white-space:nowrap}
  .status-pill .sp-dot{width:7px;height:7px;border-radius:50%}
  .status-pill.green{color:var(--green);background:rgba(91,209,106,.12)} .status-pill.green .sp-dot{background:var(--green)}
  .status-pill.amber{color:var(--amber);background:rgba(240,192,74,.12)} .status-pill.amber .sp-dot{background:var(--amber)}
  .status-pill.red{color:var(--red);background:rgba(255,92,87,.12)} .status-pill.red .sp-dot{background:var(--red)}
  .progress .prow.pstatus{margin-top:10px;margin-bottom:0}
  .kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
  @media(max-width:780px){.kpis{grid-template-columns:repeat(2,1fr)}}
  .kpi{background:var(--panel);border:1px solid var(--border);border-radius:18px;padding:20px;position:relative;overflow:hidden}
  .kpi .bar{position:absolute;top:0;left:0;width:100%;height:3px}
  .kpi.green .bar{background:var(--green)} .kpi.amber .bar{background:var(--amber)}
  .kpi.red .bar{background:var(--red)} .kpi.total .bar{background:var(--accent)}
  .kpi .num{font-family:var(--display);font-weight:800;font-size:44px;line-height:1;letter-spacing:-.03em;position:relative;z-index:2;margin-top:2px}
  .kpi.green .num{color:var(--green)} .kpi.amber .num{color:var(--amber)}
  .kpi.red .num{color:var(--red)} .kpi.total .num{color:var(--text)}
  .kpi .cap{margin-top:7px;font-size:13px;color:var(--text);line-height:1.25;font-weight:500;position:relative;z-index:2}
  .kpi .sub{font-size:11.5px;color:var(--muted);margin-top:2px;line-height:1.25;position:relative;z-index:2}
  .chart-title{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;margin-bottom:6px}
  .chart-title h2{font-family:var(--display);font-weight:600;font-size:19px;letter-spacing:-.01em}
  .chart-sub{font-size:12.5px;color:var(--muted);margin-bottom:18px}
  .dvg{display:flex;flex-direction:column;gap:9px}
  .dvg .drow{display:grid;grid-template-columns:84px 1fr 84px;align-items:center;gap:10px}
  .dvg .dday{font-family:var(--body);font-size:12.5px;color:var(--muted);text-align:right;white-space:nowrap}
  .dvg .track{position:relative;height:26px;background:var(--panel2);border-radius:7px;overflow:hidden}
  .dvg .zero{position:absolute;top:0;bottom:0;left:50%;width:1.5px;background:var(--text);opacity:.35;z-index:2}
  .dvg .grid{position:absolute;top:0;bottom:0;width:1px;background:var(--border);opacity:.7}
  .dvg .fill{position:absolute;top:3px;bottom:3px;border-radius:5px;transition:.5s cubic-bezier(.2,.8,.2,1)}
  .dvg .fill.green{background:linear-gradient(90deg,rgba(91,209,106,.35),rgba(91,209,106,.85))}
  .dvg .fill.amber{background:linear-gradient(90deg,rgba(240,192,74,.85),rgba(240,192,74,.4))}
  .dvg .fill.red{background:linear-gradient(90deg,rgba(255,92,87,.9),rgba(255,92,87,.4))}
  .dvg .dval{font-family:var(--mono);font-size:12px;font-weight:500;white-space:nowrap;text-align:left}
  .dvg .dval.green{color:var(--green)} .dvg .dval.amber{color:var(--amber)} .dvg .dval.red{color:var(--red)}
  .dvg .dflag{color:var(--amber);font-size:11px;margin-left:5px;cursor:help}
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
  .wklabel{flex:1;max-width:130px;font-family:var(--body);font-size:12px;color:var(--muted);text-align:center;line-height:1.35}
  .wklabel small{display:block;color:var(--faint);font-size:9.5px}

  /* ===================== NAEHRSTOFF-SEITE ===================== */
  .timebar{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:14px;
    background:var(--panel);border:1px solid var(--border);border-radius:16px;padding:14px 18px;margin-bottom:20px}
  .timebar .tlabel{font-family:var(--mono);font-size:10.5px;letter-spacing:.20em;text-transform:uppercase;color:var(--faint)}
  .timebar .tsub{font-family:var(--body);font-size:12.5px;color:var(--muted);margin-top:3px}
  .tseg{display:flex;gap:5px;background:var(--panel2);border:1px solid var(--border);border-radius:11px;padding:4px}
  .tseg button{font-family:var(--display);font-weight:600;font-size:13px;color:var(--muted);background:none;border:none;
    padding:8px 16px;border-radius:8px;cursor:pointer;transition:.2s;white-space:nowrap}
  .tseg button.active{background:var(--accent);color:var(--darkink)}
  .sec-title{display:flex;align-items:baseline;gap:10px;margin:4px 2px 14px}
  .sec-title h2{font-family:var(--display);font-weight:600;font-size:18px;letter-spacing:-.01em}
  .sec-title .hint{font-family:var(--body);font-size:12.5px;color:var(--faint)}
  .checks{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:30px}
  @media(max-width:820px){.checks{grid-template-columns:repeat(2,1fr)}}
  @media(max-width:460px){.checks{grid-template-columns:1fr}}
  .check{position:relative;background:var(--panel);border:1px solid var(--border);border-radius:16px;padding:20px 20px 18px;overflow:hidden}
  .check .topbar{position:absolute;top:0;left:0;width:100%;height:3px}
  .check.green .topbar{background:var(--green)} .check.amber .topbar{background:var(--amber)} .check.red .topbar{background:var(--red)}
  .check.green{border-color:rgba(91,209,106,.45)} .check.amber{border-color:rgba(240,192,74,.45)} .check.red{border-color:rgba(255,92,87,.5)}
  .check .ck-head{display:flex;align-items:center;gap:8px;margin-bottom:3px}
  .check .ck-dot{width:11px;height:11px;border-radius:50%;flex:none}
  .check.green .ck-dot{background:var(--green);box-shadow:0 0 10px rgba(91,209,106,.5)}
  .check.amber .ck-dot{background:var(--amber);box-shadow:0 0 10px rgba(240,192,74,.45)}
  .check.red .ck-dot{background:var(--red);box-shadow:0 0 10px rgba(255,92,87,.45)}
  .check .ck-name{font-family:var(--display);font-weight:600;font-size:14.5px}
  .check .ck-status{font-family:var(--display);font-weight:700;font-size:23px;letter-spacing:-.01em;margin-top:6px}
  .check.green .ck-status{color:var(--green)} .check.amber .ck-status{color:var(--amber)} .check.red .ck-status{color:var(--red)}
  .check .ck-detail{font-family:var(--mono);font-size:11px;color:var(--muted);margin-top:3px}
  .check .ck-help{font-size:11px;color:var(--faint);margin-top:9px;line-height:1.35;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .check .ck-score{margin-left:auto;font-family:var(--mono);font-size:11px;font-weight:600;padding:3px 9px;border-radius:999px;flex:none}
  .check.green .ck-score{color:var(--green);background:rgba(91,209,106,.14)}
  .check.amber .ck-score{color:var(--amber);background:rgba(240,192,74,.14)}
  .check.red .ck-score{color:var(--red);background:rgba(255,92,87,.16)}
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
  .micro-head .mh-sub{font-family:var(--body);font-size:12.5px;color:var(--faint);margin-top:2px}
  .bars{display:flex;flex-direction:column;gap:5px}
  .brow{display:grid;grid-template-columns:150px 1fr 50px;align-items:center;gap:12px;padding:6px 8px;border-radius:9px;transition:background .15s}
  .brow:hover{background:rgba(237,230,216,.05)}
  .brow{cursor:pointer}
  .bsrc{padding:2px 10px 10px;font-size:11.5px;line-height:1.55;color:var(--muted)}
  .bsrc b{color:var(--text);font-weight:500}
  @media(max-width:560px){.brow{grid-template-columns:120px 1fr 44px;gap:8px}}
  .bname{display:flex;flex-direction:column;gap:1px;min-width:0}
  .bname .bn{font-size:13px;font-weight:500;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .bname .bamt{font-family:var(--mono);font-size:10px;color:var(--faint);white-space:nowrap}
  .btrack{position:relative;height:22px;background:var(--panel2);border:1px solid var(--border);border-radius:7px;overflow:hidden}
  .btrack::after{content:'';position:absolute;right:0;top:0;bottom:0;width:2px;background:rgba(237,230,216,.14)}
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

  /* ---- SVG-Chart (Wochendurchschnitt) ---- */
  .plot .wsvg{display:block;width:100%;height:auto;overflow:visible}
  .wsbar{fill:url(#wgrad)}
  .wsval{fill:var(--text);font-family:var(--mono);font-size:13px;font-weight:500;text-anchor:middle}
  .wsref{stroke:var(--green);stroke-width:1.5;stroke-dasharray:5 4;opacity:.9}
  .wsreft{fill:var(--green);font-family:var(--mono);font-size:11px;text-anchor:start}

  /* ---- SVG-Gauge (Gesamtdeckung Mikronaehrstoffe) auf der Naehrstoff-Seite ----
     Echtes Chart-Element, damit die Seite auch bei Leni-Datenluecken rendert. */
  .cov-gauge{display:flex;align-items:center;gap:26px;margin-bottom:18px;padding-bottom:16px;border-bottom:1px dashed var(--border)}
  .cov-gauge svg{width:120px;height:120px;flex:none;display:block;overflow:visible}
  .cov-gauge .cg-ring{fill:none;stroke:var(--panel2);stroke-width:9}
  .cov-gauge .cg-val{fill:none;stroke-width:9;stroke-linecap:round;transform:rotate(-90deg);transform-origin:50% 50%;transition:stroke-dasharray .7s cubic-bezier(.2,.8,.2,1)}
  .cov-gauge .cg-num{font-family:var(--display);font-weight:800;font-size:21px;fill:var(--text);text-anchor:middle;dominant-baseline:central}
  .cov-gauge .cg-txt{min-width:0;flex:1}
  .cov-gauge .cg-txt h3{font-family:var(--display);font-weight:600;font-size:15px;margin-bottom:4px}
  .cov-gauge .cg-txt p{font-family:var(--body);font-size:12.5px;color:var(--muted);line-height:1.55}
  .cov-gauge .cg-txt p b{color:var(--text);font-weight:500}


  /* ---- Empty-State: einladende Card mit CTA statt toter Leerflaeche ---- */
  .empty-card{display:flex;flex-direction:column;align-items:center;justify-content:center;
    text-align:center;gap:4px;padding:30px 24px;min-height:170px}
  .empty-card .ec-icon{width:42px;height:42px;margin-bottom:8px;color:var(--accent);opacity:.92}
  .empty-card h2{font-family:var(--display);font-weight:800;font-size:19px;letter-spacing:-.01em;color:var(--text)}
  .empty-card p{font-family:var(--body);font-size:13px;line-height:1.55;color:var(--muted);max-width:380px}
  .empty-card .ec-cta{margin-top:14px;display:inline-flex;align-items:center;gap:9px;
    font-family:var(--display);font-weight:600;font-size:14.5px;color:var(--darkink);
    background:var(--accent);border:none;border-radius:12px;padding:12px 22px;cursor:pointer;
    text-decoration:none;transition:transform .15s,filter .2s}
  .empty-card .ec-cta:hover{filter:brightness(1.08);transform:translateY(-1px)}
  .empty-card .ec-cta svg{width:17px;height:17px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}

  /* ---- shared ---- */
  footer{margin-top:22px;text-align:center;font-family:var(--body);font-size:12px;color:var(--faint);letter-spacing:.02em}
  .stagger{opacity:0;animation:rise .6s cubic-bezier(.2,.8,.2,1) forwards}
  @keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
</style>
</head>
<body>
<div class="grain"></div>
<nav class="topnav">
  <div class="tn-inner">
    <nav class="pagenav" id="pageswitch">
      <button data-pg="kcal" class="active"><svg viewBox="0 0 24 24"><path d="M12 22c4-2 6-5 6-8 0-4-3-6-3-9-2 1-3 3-3 5-1-1-2-3-1.5-5C7 7 6 10 6 14c0 3 2 6 6 8z"/></svg>Kalorien</button>
      <span class="navsep">/</span>
      <button data-pg="nutri"><svg viewBox="0 0 24 24"><path d="M4 20C4 11 9 6 20 4c-1 11-6 16-14 16"/><path d="M4 20c3-6 7-10 12-12"/></svg>Nährstoffe</button>
    </nav>
    <div class="toggle" id="toggle">
      <button data-u="Denis" class="active"><span class="dot"></span>Denis</button>
      <button data-u="Leni"><span class="dot"></span>Leni</button>
    </div>
  </div>
</nav>
<div class="wrap">
  <header>
    <div class="brand">
      <span class="kicker" id="kicker">Kalorienbrudi</span>
      <h1 id="title">Dashboard <b>Denis</b></h1>
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

/* ============================ EMPTY-STATE ============================ */
/* Zentrierte Card mit Icon + CTA statt toter Leerflaeche. */
const NOTION_URL='https://www.notion.so/';
const IC_ADD='<svg class="ec-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8.4v7.2M8.4 12h7.2"/></svg>';
const IC_CLOCK='<svg class="ec-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5.2l3.4 2"/></svg>';
const IC_PLUS='<svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>';
const IC_EYE='<svg viewBox="0 0 24 24"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>';
/* KPI-Icons (Status-Signal je Kachel) + Warn-Icon fuer Advisory-Banner */
function emptyCard(icon,title,msg,cta){
  return '<div class="panel empty-card stagger">'+icon
       +'<h2>'+title+'</h2><p>'+msg+'</p>'+(cta||'')+'</div>';
}
function ctaLink(label){
  return '<a class="ec-cta" href="'+NOTION_URL+'" target="_blank" rel="noopener">'+IC_PLUS+label+'</a>';
}

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
    C.innerHTML=emptyCard(IC_ADD,'Noch keine Einträge für '+curUser,
      'Sobald '+curUser+' Mahlzeiten in Notion einträgt, erscheinen hier die Auswertungen automatisch.',
      ctaLink('Ersten Eintrag hinzufügen'));
    document.getElementById('foot').textContent='Stand: __BUILD_DATE__ · keine Daten';
    return;
  }
  const t=targets(u);
  const q=u.quality||{};
  const dqItems=[];
  if(q.skippedDays) dqItems.push('<div><b>'+q.skippedDays+'</b> Tag(e) ohne Kalorien-Eintrag \\u2013 nicht gewertet</div>');
  if(q.mismatchDays) dqItems.push('<div><b>'+q.mismatchDays+'</b> Tag(e): Total weicht von Einzelposten-Summe ab</div>');
  if(q.zielFromData===false) dqItems.push('<div>Zielgewicht ist Standardwert (nicht aus Notion)</div>');
  if(q.goalFromData===false) dqItems.push('<div>Kalorienziel ist Standardwert (nicht aus Notion)</div>');
  let dqDetail='';
  if((q.mismatchList||[]).length) dqDetail+='<div class="dqd-h">Abweichende Tage (Total \\u2260 Einzelposten)</div>'+q.mismatchList.map(m=>'<div class="dqd-row"><span>'+fmtDay(m.d)+'</span><span>'+m.t.toLocaleString('de')+' \\u2260 '+m.s.toLocaleString('de')+' kcal</span></div>').join('');
  if((q.skippedList||[]).length) dqDetail+='<div class="dqd-h">Ohne Kalorien-Eintrag</div><div class="dqd-row"><span>'+q.skippedList.map(fmtDay).join(', ')+'</span></div>';
  const dqNote = dqItems.length ? '<div class="dq-note"><span class="dqh">\\u26a0 Datenqualit\\u00e4t</span>'+dqItems.join('')
    +(dqDetail?'<a id="dqtoggle" href="javascript:void(0)">Details ansehen \\u2193</a><div class="dq-details" id="dqdetails" hidden>'+dqDetail+'</div>':'')
    +'</div>' : '';
  const counts={green:0,amber:0,red:0};
  u.days.forEach(x=>counts[classify(u,x.kcal)]++);
  const total=u.days.length, pctNum=n=>total?Math.round(n/total*100):0, pct=n=>total?pctNum(n)+'%':'-';
  /* Semantik-Status identisch fuer Denis UND Leni: Anteil gruener Tage. */
  const greenShare=total?counts.green/total:0;
  const trackCls=greenShare>=0.5?'green':(greenShare>=0.25?'amber':'red');
  const trackTxt=trackCls==='green'?'Auf Kurs':(trackCls==='amber'?'Wackelig':'Nachschärfen');
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
          <div class="prow"><span class="pk">Fortschritt zum Ziel</span><span class="ppct ${trackCls}">${Math.round(prog)} %</span></div>
          <div class="ptrack"><div class="pfill" style="width:${prog}%"></div></div>
          <div class="pcap"><b>${Math.round(saved).toLocaleString('de')}</b> / ${totalNeeded.toLocaleString('de')} kcal gespart - noch <b>${daysLeft} Tage</b> bei ${u.deficitTarget} kcal Defizit/Tag</div>
          <div class="prow pstatus"><span class="pk">Status</span><span class="status-pill ${trackCls}"><span class="sp-dot"></span>${trackTxt} · ${pct(counts.green)} im grünen Bereich</span></div>
        </div>
        <div class="goalrow"><span class="gk">Ziel</span><span class="gv">Abnehmen</span></div>
        <div class="goalrow"><span class="gk">Kalorienziel</span><span class="gv accent">${u.goalIntake.toLocaleString('de')} <small>kcal</small>${q.goalFromData===false?'<span class="std">Std.</span>':''}</span></div>
        <div class="goalrow"><span class="gk">Geplantes Defizit</span><span class="gv">${u.deficitTarget.toLocaleString('de')} <small>kcal</small></span></div>
        <div class="goalrow"><span class="gk">Erhaltungsbedarf</span><span class="gv">${maintenance(u).toLocaleString('de')} <small>kcal</small></span></div>
        <div class="goalrow"><span class="gk">Makro-Ziel</span><span class="gv macro"><b>${t.p}</b>P - <b>${t.f}</b>F - <b>${t.c}</b>C <small>g</small></span></div>
        <div class="goalrow"><span class="gk">Startgewicht</span><span class="gv">${u.startWeight!=null?u.startWeight.toLocaleString('de')+' <small>kg</small>':'-'}</span></div>
        <div class="goalrow"><span class="gk">Aktuelles Gewicht</span><span class="gv">${u.weight!=null?u.weight.toLocaleString('de')+' <small>kg</small>':'-'}</span></div>
        <div class="goalrow"><span class="gk">Zielgewicht</span><span class="gv">${u.zielWeight!=null?u.zielWeight.toLocaleString('de')+' <small>kg</small>':'-'}${q.zielFromData===false?'<span class="std">Std.</span>':''}</span></div>
        <div class="goalrow"><span class="gk">Letzter Eintrag</span><span class="gv" style="font-size:14px">${fmtDay(u.days[u.days.length-1].d)}</span></div>
        ${dqNote}
      </div>
      <div class="kpis">
        <div class="kpi green stagger" title="Gr\u00fcn = Tag unter Kalorienziel (+ Puffer)" style="animation-delay:.06s"><div class="bar"></div><div class="num">${counts.green}</div><div class="cap">Ziel erreicht</div><div class="sub">${pct(counts.green)} der Tage</div></div>
        <div class="kpi amber stagger" title="Gelb = \u00fcber Ziel, aber unter Erhaltungsbedarf" style="animation-delay:.10s"><div class="bar"></div><div class="num">${counts.amber}</div><div class="cap">Im Defizit</div><div class="sub">${pct(counts.amber)} der Tage</div></div>
        <div class="kpi red stagger" title="Rot = \u00fcber Erhaltungsbedarf" style="animation-delay:.14s"><div class="bar"></div><div class="num">${counts.red}</div><div class="cap">\u00dcber Bedarf</div><div class="sub">${pct(counts.red)} der Tage</div></div>
        <div class="kpi total stagger" title="Alle getrackten Tage" style="animation-delay:.18s"><div class="bar"></div><div class="num">${total}</div><div class="cap">Tage getrackt</div><div class="sub">seit ${fmtDay(u.days[0].d)}</div></div>
      </div>
    </div>

    <div class="panel stagger" style="animation-delay:.22s;margin-bottom:16px">
      <div class="chart-title"><h2>Kaloriendifferenz - letzte 7 Tage</h2></div>
      <div class="dvg">
        ${last7.map(x=>{
          const diff=x.kcal-u.goalIntake, cls=classify(u,x.kcal);
          const w=Math.min(Math.abs(diff)/maxAbs*48,48);
          const style=diff<=0?`right:50%;width:${w}%`:`left:50%;width:${w}%`;
          const sign=diff>0?'+':'';
          const flag=x.flag?' <span class="dflag" title="Tages-Total weicht von der Einzelposten-Summe (Analyse) ab">\\u26a0</span>':'';
          return `<div class="drow"><div class="dday">${fmtDay(x.d)}</div>
            <div class="track"><div class="zero"></div><div class="fill ${cls}" style="${style}"></div></div>
            <div class="dval ${cls}">${sign}${diff} kcal${flag}</div></div>`;
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
  const dqa=document.getElementById('dqtoggle');
  if(dqa) dqa.onclick=()=>{const d=document.getElementById('dqdetails');d.hidden=!d.hidden;dqa.textContent=d.hidden?'Details ansehen \u2193':'Details ausblenden \u2191';};
  const agg=periodAgg(u.days,curPeriod);
  drawWeekly(PERIOD_LIMIT>0?agg.slice(-PERIOD_LIMIT):agg,u,t);
  document.getElementById('foot').textContent='Stand: __BUILD_DATE__ · '+total+' Tage · Verhältnis 30 % P / 30 % F / 40 % C · automatisch generiert';
}
function drawWeekly(weeks,u,t){
  const plot=document.getElementById('plot'), wkl=document.getElementById('wkl');
  const H=150, tgt=t[curMetric];
  const maxV=Math.max(...weeks.map(w=>w[curMetric]),tgt)*1.18||1;
  const grp=curPeriod==='W'?'Kalenderwoche':curPeriod==='M'?'Monat':'Jahr';
  document.getElementById('msub').textContent=METRICS[curMetric].label+' \\u00d8 pro Tag, gruppiert nach '+grp+' ('+METRICS[curMetric].unit+') \\u00b7 gestrichelt: Ziel '+tgt+' '+METRICS[curMetric].unit;
  /* Als echtes SVG-Chart rendern (skalierbar, an fixe Achse gebunden). */
  const W=Math.max(Math.round(plot.clientWidth)||640,260), VH=185;
  const base=VH-3, top0=26;                 // Platz oben fuer die Wertelabels
  const n=Math.max(weeks.length,1);
  const colW=W/n, barW=Math.min(colW*0.5,72);
  const yOf=v=>base-Math.round(v/maxV*H);
  const refY=yOf(tgt);
  const bars=weeks.map((w,i)=>{
    const cx=colW*(i+0.5), val=w[curMetric];
    const y=Math.max(yOf(val),top0), h=Math.max(base-y,3);
    let ly=y-8;                                   // Kollision mit Ziellinie vermeiden
    if(Math.abs(ly-refY)<12) ly=Math.min(ly,refY-14);
    if(ly<12) ly=12;
    return '<rect class="wsbar" x="'+(cx-barW/2).toFixed(1)+'" y="'+y.toFixed(1)+'" width="'+barW.toFixed(1)+'" height="'+h.toFixed(1)+'" rx="8"/>'
         +'<text class="wsval" x="'+cx.toFixed(1)+'" y="'+ly.toFixed(1)+'">'+val.toLocaleString('de')+'</text>';
  }).join('');
  const ref='<line class="wsref" x1="0" y1="'+refY+'" x2="'+W+'" y2="'+refY+'"/>'
          +'<text class="wsreft" x="4" y="'+(refY<20?refY+14:refY-6)+'">Ziel '+tgt+'</text>';
  plot.innerHTML='<svg class="wsvg" width="'+W+'" height="'+VH+'" viewBox="0 0 '+W+' '+VH+'" preserveAspectRatio="xMidYMid meet" role="img" aria-label="'+METRICS[curMetric].label+' \\u00d8 pro '+grp+'">'
    +'<defs><linearGradient id="wgrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="'+u.accent+'"/><stop offset="1" stop-color="'+u.accent2+'"/></linearGradient></defs>'
    +ref+bars+'</svg>';
  wkl.innerHTML=weeks.map(w=>`<div class="wklabel">${w.range}<small>${w.n} ${w.n===1?'Tag':'Tage'}</small></div>`).join('');
}

/* ============================ NAEHRSTOFFE ============================ */
const CATS=[
  {key:"Darmgesundheit", help:"Ballaststoffe, Fermentiertes, Vielfalt = gut"},
  {key:"Low FODMAP",     help:"niedrig-FODMAP / gut verträglich = gut"},
  {key:"Säure-Base",     help:"basisch = gut, säurebildend = schlecht"}
];
const CHOL_GREEN=300, CHOL_AMBER=500;
const CAT_GREEN=70, CAT_AMBER=50;
const MIC_GREEN=90, MIC_AMBER=50;
const NPERIODS={ "7":"letzte 7 Tage", "30":"letzte 30 Tage", "all":"gesamter Zeitraum" };
const NEMPTY={ "7":"In den letzten 7 Tagen wurde nichts getrackt.",
               "30":"In den letzten 30 Tagen wurde nichts getrackt.",
               "all":"Im gesamten Zeitraum wurde nichts getrackt." };
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
function covGauge(cov,color){
  /* Donut-Gauge als echtes SVG: Ring + gefaerbter Fortschrittsbogen + Prozent. */
  const r=40, C=2*Math.PI*r, v=Math.max(0,Math.min(100,cov)), dash=v/100*C;
  return '<svg viewBox="0 0 100 100" role="img" aria-label="Gesamtdeckung Mikron\\u00e4hrstoffe '+Math.round(v)+' Prozent">'
    +'<circle class="cg-ring" cx="50" cy="50" r="'+r+'"/>'
    +'<circle class="cg-val" cx="50" cy="50" r="'+r+'" stroke="var(--'+color+')" stroke-dasharray="'+dash.toFixed(1)+' '+C.toFixed(1)+'"/>'
    +'<text class="cg-num" x="50" y="50">'+Math.round(v)+'%</text></svg>';
}
function topFoods(windowDays){
  /* pro Kategorie: Haeufigkeit je Lebensmittel zaehlen, Top 4 positiv + Flop 4 negativ */
  const out={};
  CATS.forEach(c=>{
    const pos={},neg={};
    windowDays.forEach(day=>{
      const f=(day.cf&&day.cf[c.key])||[[],[]];
      f[0].forEach(n=>pos[n]=(pos[n]||0)+1);
      f[1].forEach(n=>neg[n]=(neg[n]||0)+1);
    });
    const top=o=>Object.entries(o).sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])).slice(0,4);
    out[c.key]={pos:top(pos),neg:top(neg)};
  });
  return out;
}
function topChol(windowDays){
  /* groesste Cholesterin-Quellen (mg summiert) im Zeitfenster */
  const m={};
  windowDays.forEach(day=>{
    const c=day.chol||{};
    Object.keys(c).forEach(n=>m[n]=(m[n]||0)+c[n]);
  });
  return Object.entries(m).sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])).slice(0,4);
}
function tipHtml(t){
  const li=a=>a.length
    ?'<ul>'+a.map(([n,k])=>'<li>'+n+(k>1?' <small>\\u00d7'+k+'</small>':'')+'</li>').join('')+'</ul>'
    :'<div class="none">keine</div>';
  return '<div class="ck-tip">'
       +'<div class="col"><div class="tt pos">\\u25b2 Top 4</div>'+li(t.pos)+'</div>'
       +'<div class="col"><div class="tt neg">\\u25bc Flop 4</div>'+li(t.neg)+'</div>'
       +'</div>';
}
function tipCholHtml(items){
  const li=items.length
    ?'<ul>'+items.map(([n,mg])=>'<li>'+n+' <small>'+Math.round(mg).toLocaleString('de')+' mg</small></li>').join('')+'</ul>'
    :'<div class="none">keine</div>';
  return '<div class="ck-tip"><div class="col"><div class="tt neg">\\u25bc Top 4 Quellen</div>'+li+'</div></div>';
}
function checkCard(name, cls, status, detail, help, i, tip, chip){
  return `<div class="check ${cls}${tip?' has-tip':''} stagger" style="animation-delay:${(0.02+0.03*i).toFixed(2)}s"${tip?' tabindex="0"':''}>
    <div class="topbar"></div>
    <div class="ck-head"><span class="ck-dot"></span><span class="ck-name">${name}</span>${chip?'<span class="ck-score">'+chip+'</span>':''}</div>
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
    C.innerHTML=emptyCard(IC_ADD,'Noch keine Einträge für '+curUser,
      'Sobald in der Lebensmittel-Analyse Zeilen für '+curUser+' liegen, erscheint hier die Auswertung.',
      ctaLink('Ersten Eintrag hinzufügen'));
    document.getElementById('foot').textContent='Stand: __BUILD_DATE__ · keine Daten';
    return;
  }
  /* Fallback bei fehlenden Daten (z.B. Leni-Datenlücken): ist das gewählte
     Zeitfenster leer, es gibt aber überhaupt Einträge, zeige den gesamten
     erfassten Zeitraum - so rendert die Auswertung inkl. Chart trotzdem,
     statt in einer toten Leerfläche zu enden. */
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
    const cta = curNPeriod!=='all'
      ? '<button class="ec-cta" id="ecall">'+IC_EYE+'Gesamten Zeitraum anzeigen</button>'
      : '';
    C.innerHTML=timebar+emptyCard(IC_CLOCK,'Keine Daten im Zeitfenster',
      NEMPTY[curNPeriod]+' Wechsle das Zeitfenster oben – oder zeig gleich den gesamten Zeitraum.',
      cta);
    document.getElementById('ntime').querySelectorAll('button').forEach(b=>b.onclick=()=>{curNPeriod=b.dataset.p;renderNutri();});
    const ecall=document.getElementById('ecall');
    if(ecall) ecall.onclick=()=>{curNPeriod='all';renderNutri();};
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
    let cls,status,detail,chip='';
    if(!tot){ cls='amber'; status='-'; detail='keine Angaben'; }
    else{
      const score=(v[0]*100 + v[1]*50)/tot;
      cls = score>=CAT_GREEN?'green':(score>=CAT_AMBER?'amber':'red');
      status = cls==='green'?'Gut':(cls==='amber'?'Okay':'Kritisch');
      detail = v[0]+' gut \\u00b7 '+v[1]+' neutral \\u00b7 '+v[2]+' schlecht';
      chip = Math.round(score)+'/100';
    }
    checksHtml += checkCard(c.key, cls, status, detail, c.help, i, tipHtml(foods[c.key]), chip);
  });
  (function(){
    const ch=avg["Cholesterin (mg)"];
    const cls = ch<=CHOL_GREEN?'green':(ch<=CHOL_AMBER?'amber':'red');
    const status = cls==='green'?'Gut':(cls==='amber'?'Okay':'Hoch');
    const detail = '\\u00d8 '+Math.round(ch).toLocaleString('de')+' mg/Tag (Ziel \\u2264'+CHOL_GREEN+')';
    checksHtml += checkCard('Cholesterin', cls, status, detail, 'weniger ist besser - Ziel unter '+CHOL_GREEN+' mg/Tag', 3, tipCholHtml(topChol(wd)), Math.round(ch)+' mg');
  })();

  let micros=Object.keys(u.ref).map(k=>{
    const [name,unit]=splitUnit(k);
    const a=avg[k]||0, ref=u.ref[k];
    const pctRaw=ref>0?(a/ref*100):0, pct=Math.min(100,pctRaw);
    return {key:k,name,unit,avg:a,ref,pct,pctRaw,color:micColor(pct)};
  });
  /* Gesamtdeckung als echtes SVG-Chart (Donut) - garantiert ein gerendertes
     Chart-Element auf der Nährstoff-Seite, auch bei Leni-Datenlücken. */
  const cov = micros.length ? micros.reduce((s,m)=>s+m.pct,0)/micros.length : 0;
  const covColor = micColor(cov);
  const gaugeSvg = covGauge(cov, covColor);
  const covGaugeHtml = `<div class="cov-gauge stagger">${gaugeSvg}
    <div class="cg-txt"><h3>Gesamtdeckung</h3>
    <p>Ø <b>${Math.round(cov)} %</b> der DGE-Tagesreferenz über ${micros.length} Mikronährstoffe · gedeckelt bei 100 %</p></div></div>`;

  micros.sort((x,y)=> curSort==='worst' ? x.pctRaw-y.pctRaw : y.pctRaw-x.pctRaw);
  let barsHtml=micros.map((m,i)=>{
    const full=m.pct>=99.5?' full':'';
    const src=(u.nutTop&&u.nutTop[m.key])||[];
    const srcHtml=src.length
      ? 'Gute Quellen aus deinem Log: '+src.map(x=>'<b>'+x[0]+'</b> (\\u00d8 '+fmtN(x[1])+' '+m.unit+')').join(' \\u00b7 ')
      : 'Noch keine Quelle mit '+m.name+' im Log.';
    return `<div class="brow stagger" style="animation-delay:${(0.02*i).toFixed(2)}s" title="Klick zeigt Lebensmittel-Quellen">
      <div class="bname"><span class="bn">${m.name}</span><span class="bamt">${fmtN(m.avg)} / ${fmtN(m.ref)} ${m.unit}</span></div>
      <div class="btrack"><div class="bfill ${m.color}${full}" style="width:${m.pct.toFixed(1)}%"></div></div>
      <div class="bpct ${m.color}">${Math.round(m.pctRaw)}%</div>
    </div><div class="bsrc" hidden>${srcHtml}</div>`;
  }).join('');

  C.innerHTML = timebar + `
    <div class="sec-title stagger"><h2>Gesundheits-Checkpoints</h2><span class="hint">Ampel im gewählten Zeitfenster \\u00b7 Hover zeigt Top-Lebensmittel</span></div>
    <div class="checks">${checksHtml}</div>
    <div class="panel stagger" style="animation-delay:.10s">
      ${covGaugeHtml}
      <div class="micro-head">
        <div><h2>Mikronährstoffe</h2><div class="mh-sub">\\u00d8 pro Tag vs. Tagesreferenzwert \\u00b7 gedeckelt bei 100 %</div></div>
        <div class="sortbtns" id="nsort">
          <button data-s="worst" class="${curSort==='worst'?'active':''}">Schlechteste zuerst</button>
          <button data-s="best" class="${curSort==='best'?'active':''}">Beste zuerst</button>
        </div>
      </div>
      <div class="bars" id="nbars">${barsHtml}</div>
    </div>`;

  document.getElementById('ntime').querySelectorAll('button').forEach(b=>b.onclick=()=>{curNPeriod=b.dataset.p;renderNutri();});
  document.getElementById('nsort').querySelectorAll('button').forEach(b=>b.onclick=()=>{curSort=b.dataset.s;renderNutri();});
  document.querySelectorAll('#nbars .brow').forEach(el=>{el.onclick=()=>{const s=el.nextElementSibling;if(s&&s.classList.contains('bsrc'))s.hidden=!s.hidden;};});
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
/* SVG-Chart an die Fensterbreite koppeln: bei Resize neu vermessen/zeichnen. */
let _rzT;
window.addEventListener('resize',()=>{clearTimeout(_rzT);_rzT=setTimeout(renderAll,180);});
renderAll();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
