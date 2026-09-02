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
    "Denis": {"accent": "#3669B4", "kicker": "brudi", "deficitTarget": 1000,
              "greenBuf": 95, "zielWeight": 80, "goalIntake": 1900},
    "Leni":  {"accent": "#AB4878", "kicker": "schwester", "deficitTarget": 500,
              "greenBuf": 75, "zielWeight": 60, "goalIntake": 1500},
}

# --- Naehrstoffe: pro Person Geschlecht + Akzent (eigene Farben fuer die Seite) ---
NUTRI_CONFIG = {
    "Denis": {"sex": "m", "accent": "#3669B4"},
    "Leni":  {"sex": "w", "accent": "#AB4878"},
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
_PREP_WORDS = {
    "gegrillt", "gegrillte", "gegrillter", "gegrilltes", "gebraten",
    "gebratene", "gebratener", "gekocht", "gekochte", "gekochtes",
    "gedünstet", "gedünstete", "angebraten", "angebratene", "roh", "rohe",
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
    "spiegelei": "Ei", "spiegeleier": "Ei", "rührei": "Ei", "rühreier": "Ei",
    "grillgemüse": "Gemüse", "ofengemüse": "Gemüse",
    "gemischtes gemüse": "Gemüse", "gemüsemix": "Gemüse",
    "gemüse & salat": "Gemüse", "espressi": "Espresso",
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
        if _NUMUNIT.match(words[0]) or w in _UNIT_WORDS or w in _SIZE_WORDS or w in _PREP_WORDS:
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
        data[person] = {
            "accent": cfg["accent"], "kicker": cfg["kicker"],
            "goalIntake": goal, "deficitTarget": cfg["deficitTarget"],
            "weight": weight, "startWeight": start_weight,
            "zielWeight": ziel, "greenBuf": cfg["greenBuf"],
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
            "accent": cfg["accent"],
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
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="light dark">
<title>Brudi</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  /* ==========================================================================
     Designsystem
     - EINE Schrift (Inter), Zahlen durchgaengig tabular -> keine Sprungwerte.
     - Farbe traegt Bedeutung: Akzent nur fuer Auswahl + Datenflaechen,
       Semantikfarben nur fuer Status. Alles andere ist Tinte auf Papier.
     - Flaechen: wenige grosse "Sheets" mit Haarlinien statt vieler Kaertchen.
     ========================================================================== */
  :root{
    color-scheme:light;
    --paper:#F3F1EC;
    --surface:#FFFFFF;
    --surface-2:#F7F5F1;
    --surface-3:#EFECE5;
    --line:#E5E1D9;
    --line-2:#D3CEC3;
    --ink:#1B1A17;
    --ink-2:#5D584F;
    --ink-3:#8B857A;
    --pos:#2E7D57;  --pos-bg:rgba(46,125,87,.10);
    --warn:#A8761E; --warn-bg:rgba(168,118,30,.12);
    --neg:#B84A3E;  --neg-bg:rgba(184,74,62,.10);
    --accent-raw:#3669B4;
    --accent:var(--accent-raw);
    --accent-ink:#FFFFFF;
    --accent-bg:color-mix(in srgb, var(--accent-raw) 13%, var(--paper));
    /* Grosse Flaechen wirken bei gleichem Farbwert schwerer als duenne Schrift,
       deshalb bekommen die Diagrammbalken etwas mehr Helligkeit. Bewusst knapp:
       85% waren auf den alten, deutlich bunteren Akzent kalibriert und heben die
       Helligkeit um 0.072 (OKLCH L) - ein sichtbar eigenes Blau. Gegen die jetzt
       ruhigere Basis genuegen 93% (+0.034), der Ton bleibt derselbe. */
    --accent-fill:color-mix(in srgb, var(--accent-raw) 93%, #FFFFFF);
    --shadow:0 1px 2px rgba(27,26,23,.04), 0 6px 18px rgba(27,26,23,.045);
    --r:12px;
    --font:'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;
    --nav-h:72px;
  }
  :root.dark{
      color-scheme:dark;
      --paper:#121210;
      --surface:#1A1A17;
      --surface-2:#21201C;
      --surface-3:#272621;
      --line:#2D2B26;
      --line-2:#3B3833;
      --ink:#EDEAE2;
      --ink-2:#A8A296;
      --ink-3:#777166;
      --pos:#5FC38E;  --pos-bg:rgba(95,195,142,.13);
      --warn:#DDA950; --warn-bg:rgba(221,169,80,.14);
      --neg:#EC7A6C;  --neg-bg:rgba(236,122,108,.13);
      --accent:color-mix(in srgb, var(--accent-raw) 68%, #FFFFFF);
      --accent-ink:#12120F;
      --accent-bg:color-mix(in srgb, var(--accent-raw) 26%, var(--paper));
      /* Auf dunklem Grund ist --accent bereits aufgehellt - das reicht hier. */
      --accent-fill:var(--accent);
      --shadow:0 1px 2px rgba(0,0,0,.35), 0 6px 18px rgba(0,0,0,.28);
  }

  *{margin:0;padding:0;box-sizing:border-box}
  html{-webkit-text-size-adjust:100%}
  body{
    background:var(--paper);color:var(--ink);font-family:var(--font);
    font-size:15px;line-height:1.5;
    -webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;
    padding:calc(var(--nav-h) + 30px) 20px 40px;min-height:100vh;
  }
  .num{font-variant-numeric:tabular-nums;font-feature-settings:'tnum' 1}
  h1,h2,h3{font-weight:600;letter-spacing:-.015em;line-height:1.2}
  button{font:inherit;color:inherit;background:none;border:none;cursor:pointer}
  :focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:6px}
  @media (prefers-reduced-motion:reduce){
    *,*::before,*::after{animation-duration:.001ms!important;transition-duration:.001ms!important}
  }

  .wrap{max-width:1040px;margin:0 auto}

  /* ---------- Topbar ---------- */
  .topbar{position:fixed;top:0;left:0;right:0;z-index:50;height:var(--nav-h);
    background:color-mix(in srgb, var(--paper) 82%, transparent);
    backdrop-filter:saturate(1.6) blur(12px);-webkit-backdrop-filter:saturate(1.6) blur(12px);
    border-bottom:1px solid var(--line)}
  .topbar-in{max-width:1040px;margin:0 auto;height:100%;padding:0 20px;
    display:flex;align-items:center;gap:16px}
  .mark{font-weight:700;font-size:16.5px;letter-spacing:-.03em;flex:none}
  .mark i{font-style:normal;color:var(--accent)}
  .tabs{display:flex;gap:2px;margin-left:auto}
  .tabs button{padding:9px 15px;border-radius:9px;font-size:14.5px;font-weight:500;
    color:var(--ink-2);transition:background .15s,color .15s}
  .tabs button:hover{color:var(--ink);background:var(--surface-3)}
  .tabs button[aria-selected="true"]{color:var(--accent);background:var(--accent-bg);font-weight:600}
  .icon-btn{display:flex;align-items:center;justify-content:center;width:36px;height:36px;
    border-radius:9px;color:var(--ink-2);flex:none;transition:background .15s,color .15s}
  .icon-btn:hover{background:var(--surface-3);color:var(--ink)}
  .icon-btn svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:1.7;
    stroke-linecap:round;stroke-linejoin:round}
  /* Gezeigt wird das Ziel-Theme, nicht das aktuelle. */
  .icon-btn .i-sun{display:none}
  :root.dark .icon-btn .i-sun{display:block}
  :root.dark .icon-btn .i-moon{display:none}
  /* Bei zwei Personen genuegt ein direkter Umschalter - kein Menue. */
  .who-btn{display:flex;align-items:center;gap:8px;flex:none;padding:8px 12px 8px 10px;
    border-radius:9px;font-size:14.5px;font-weight:500;transition:background .15s}
  .who-btn:hover{background:var(--surface-3)}
  .who-btn .swap{width:14px;height:14px;stroke:var(--ink-3);fill:none;stroke-width:2;
    stroke-linecap:round;stroke-linejoin:round;transition:stroke .15s}
  .who-btn:hover .swap{stroke:var(--ink-2)}
  .dot{width:9px;height:9px;border-radius:50%;flex:none;background:var(--accent)}
  @media(max-width:520px){
    :root{--nav-h:64px}
    .mark{display:none}
    /* Ohne Wortmarke stehen die Tabs links; der freie Platz gehoert dann vor
       die rechte Gruppe, damit Nutzer-Menue und Theme-Knopf am Rand kleben. */
    .tabs{margin-left:0}
    .who-btn{margin-left:auto}
    .topbar-in{gap:8px;padding:0 14px}
    .tabs button{padding:8px 11px;font-size:13.5px}
  }

  /* ---------- Seitenkopf ---------- */
  .pagehead{display:flex;align-items:flex-end;justify-content:space-between;
    gap:20px;flex-wrap:wrap;margin-bottom:22px}
  .eyebrow{font-size:11.5px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;
    color:var(--ink-3)}
  .pagehead h1{font-size:clamp(26px,5vw,34px);margin-top:5px}
  .pagehead .lead{font-size:13.5px;color:var(--ink-2);margin-top:4px}

  /* ---------- Sheets ---------- */
  .sheet{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);
    box-shadow:var(--shadow);margin-bottom:16px;overflow:hidden}
  .sheet-head{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;
    flex-wrap:wrap;padding:18px 20px 0}
  .sheet-head h2{font-size:17px}
  .sheet-head .sub{font-size:13px;color:var(--ink-2);margin-top:3px}
  .sheet-body{padding:16px 20px 20px}

  /* ---------- Segmentierte Steuerung ---------- */
  .seg{display:flex;gap:2px;padding:3px;background:var(--surface-2);
    border:1px solid var(--line);border-radius:9px;flex:none}
  .seg button{padding:5px 11px;border-radius:6px;font-size:12.5px;font-weight:500;
    color:var(--ink-2);white-space:nowrap;transition:background .15s,color .15s}
  .seg button:hover{color:var(--ink)}
  .seg button[aria-pressed="true"]{background:var(--surface);color:var(--ink);font-weight:600;
    box-shadow:0 1px 2px rgba(27,26,23,.07)}
  .controls{display:flex;gap:8px;flex-wrap:wrap;align-items:center}

  /* ---------- Hero: Fortschritt ---------- */
  .hero{display:grid;grid-template-columns:1.35fr 1fr}
  @media(max-width:720px){.hero{grid-template-columns:1fr}}
  .hero-main{padding:20px}
  .hero-side{padding:20px;border-left:1px solid var(--line);background:var(--surface-2)}
  @media(max-width:720px){.hero-side{border-left:none;border-top:1px solid var(--line)}}
  .hero-num{display:flex;align-items:baseline;gap:6px;margin:10px 0 12px}
  .hero-num b{font-size:46px;font-weight:600;letter-spacing:-.04em;line-height:1}
  .hero-num span{font-size:17px;font-weight:500;color:var(--ink-3)}
  .meter{height:6px;border-radius:3px;background:var(--surface-3);overflow:hidden}
  .meter i{display:block;height:100%;border-radius:3px;background:var(--accent);
    transition:width .6s cubic-bezier(.2,.7,.2,1)}
  .hero-cap{font-size:13px;color:var(--ink-2);margin-top:11px;line-height:1.55}
  .hero-cap b{color:var(--ink);font-weight:600}

  .chip{display:inline-flex;align-items:center;gap:6px;padding:4px 10px;border-radius:999px;
    font-size:12.5px;font-weight:600}
  .chip i{width:6px;height:6px;border-radius:50%;background:currentColor;flex:none}
  .chip.pos{color:var(--pos);background:var(--pos-bg)}
  .chip.warn{color:var(--warn);background:var(--warn-bg)}
  .chip.neg{color:var(--neg);background:var(--neg-bg)}

  /* Gewichts-Schiene: Start -> aktuell -> Ziel auf einer Achse */
  .rail{margin-top:18px}
  .rail-top{display:flex;justify-content:space-between;font-size:12px;color:var(--ink-3);
    margin-bottom:7px}
  .rail-track{position:relative;height:3px;border-radius:2px;background:var(--surface-3)}
  .rail-done{position:absolute;left:0;top:0;bottom:0;border-radius:2px;background:var(--accent);opacity:.35}
  .rail-pin{position:absolute;top:50%;width:11px;height:11px;border-radius:50%;
    background:var(--accent);border:2.5px solid var(--surface-2);transform:translate(-50%,-50%)}
  .rail-now{margin-top:9px;font-size:13px;color:var(--ink-2)}
  .rail-now b{color:var(--ink);font-weight:600;font-size:15px}

  .facts{margin-top:18px;padding-top:14px;border-top:1px solid var(--line)}
  .fact{display:flex;align-items:baseline;justify-content:space-between;gap:12px;padding:5px 0;
    font-size:13px}
  .fact dt{color:var(--ink-2)}
  .fact dd{font-weight:600;color:var(--ink)}
  .fact dd small{font-weight:500;color:var(--ink-3);font-size:11.5px;margin-left:2px}
  .est{font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;
    color:var(--ink-3);background:var(--surface-3);padding:1px 5px;border-radius:4px;margin-left:5px}

  /* ---------- Statistik-Zeile ---------- */
  .stats{display:grid;grid-template-columns:repeat(4,1fr)}
  @media(max-width:640px){.stats{grid-template-columns:repeat(2,1fr)}}
  .stat{padding:18px 20px;border-left:1px solid var(--line)}
  .stat:first-child{border-left:none}
  @media(max-width:640px){
    .stat:nth-child(odd){border-left:none}
    .stat:nth-child(n+3){border-top:1px solid var(--line)}
  }
  .stat-num{font-size:30px;font-weight:600;letter-spacing:-.035em;line-height:1;display:block}
  .stat.pos .stat-num{color:var(--pos)} .stat.warn .stat-num{color:var(--warn)}
  .stat.neg .stat-num{color:var(--neg)}
  .stat-lab{display:block;font-size:13px;font-weight:500;margin-top:8px}
  .stat-sub{display:block;font-size:12px;color:var(--ink-3);margin-top:2px}

  /* ---------- Abweichungs-Liste (letzte 7 Tage) ---------- */
  .dev{display:flex;flex-direction:column}
  .dev-row{display:grid;grid-template-columns:78px 1fr 96px;align-items:center;gap:12px;
    padding:7px 0}
  .dev-row + .dev-row{border-top:1px solid var(--line)}
  .dev-day{font-size:12.5px;color:var(--ink-2)}
  .dev-track{position:relative;height:22px}
  .dev-zero{position:absolute;left:50%;top:0;bottom:0;width:1px;background:var(--line-2)}
  .dev-bar{position:absolute;top:50%;transform:translateY(-50%);height:9px;border-radius:2px;
    min-width:2px;transition:width .5s cubic-bezier(.2,.7,.2,1)}
  .dev-bar.pos{background:var(--pos)} .dev-bar.warn{background:var(--warn)}
  .dev-bar.neg{background:var(--neg)}
  .dev-val{text-align:right;font-size:13px;font-weight:600}
  .dev-val.pos{color:var(--pos)} .dev-val.warn{color:var(--warn)} .dev-val.neg{color:var(--neg)}
  .dev-val small{display:block;font-size:11.5px;font-weight:500;color:var(--ink-3)}
  .dev-flag{color:var(--warn);cursor:help;margin-left:3px}
  .dev-scale{display:grid;grid-template-columns:78px 1fr 96px;gap:12px;
    margin-top:8px;padding-top:8px;border-top:1px solid var(--line)}
  .dev-scale span{grid-column:2;text-align:center;font-size:11.5px;color:var(--ink-3)}
  @media(max-width:520px){
    .dev-row,.dev-scale{grid-template-columns:62px 1fr 74px;gap:8px}
    .dev-day{font-size:12px}
  }

  /* ---------- Balkendiagramm ---------- */
  .chart{margin-top:6px}
  .chart svg{display:block;width:100%;height:auto;overflow:visible}
  .c-grid{stroke:var(--line);stroke-width:1}
  .c-bar{fill:var(--accent-fill)}
  .c-val{fill:var(--ink);font-size:12.5px;font-weight:600;text-anchor:middle;
    font-variant-numeric:tabular-nums}
  .c-goal{stroke:var(--ink-3);stroke-width:1.5;stroke-dasharray:4 4}
  .c-goal-t{fill:var(--ink-3);font-size:11px;font-weight:500}
  .c-labels{display:flex;margin-top:10px}
  .c-label{flex:1;text-align:center;font-size:12px;color:var(--ink-2);min-width:0;padding:0 4px}
  .c-label small{display:block;color:var(--ink-3);font-size:11px}

  /* ---------- Checkpoints ---------- */
  .checks{display:grid;grid-template-columns:repeat(4,1fr)}
  @media(max-width:820px){.checks{grid-template-columns:repeat(2,1fr)}}
  @media(max-width:440px){.checks{grid-template-columns:1fr}}
  .checks{border-top:1px solid var(--line)}
  .check{padding:18px 20px;border-left:1px solid var(--line);text-align:left;width:100%;
    display:flex;flex-direction:column;gap:3px;transition:background .15s}
  .check.c0{border-left:none}          /* erste Spalte */
  .check.rn{border-top:1px solid var(--line)}  /* nicht erste Zeile */
  .check:hover{background:var(--surface-2)}
  .check[aria-expanded="true"]{background:var(--surface-2)}
  .check-top{display:flex;align-items:center;gap:8px}
  .check-name{font-size:12.5px;font-weight:500;color:var(--ink-2)}
  .check-score{margin-left:auto;font-size:11.5px;font-weight:600;color:var(--ink-3)}
  .check-status{font-size:20px;font-weight:600;letter-spacing:-.02em;margin-top:5px}
  .check.pos .check-status{color:var(--pos)} .check.warn .check-status{color:var(--warn)}
  .check.neg .check-status{color:var(--neg)}
  .check-detail{font-size:12.5px;color:var(--ink-2)}
  .check-more{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--ink-3);
    margin-top:auto;padding-top:8px}
  .check-more span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .check-more .caret{flex:none;margin-left:auto;width:6px;height:6px;border-right:1.5px solid currentColor;
    border-bottom:1.5px solid currentColor;transform:rotate(45deg) translate(-1px,-1px);transition:transform .2s}
  .check[aria-expanded="true"] .check-more{color:var(--ink-2)}
  .check[aria-expanded="true"] .check-more .caret{transform:rotate(-135deg) translate(-1px,-1px)}
  .drawer{grid-column:1/-1;border-top:1px solid var(--line);background:var(--surface-2);
    padding:16px 20px}
  .drawer-head{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin-bottom:12px}
  .drawer-head h3{font-size:14px}
  .drawer-head p{font-size:12.5px;color:var(--ink-2)}
  .drawer-cols{display:grid;grid-template-columns:1fr 1fr;gap:22px}
  .drawer-cols[data-single="true"]{grid-template-columns:1fr}
  @media(max-width:520px){.drawer-cols{grid-template-columns:1fr;gap:16px}}
  .drawer-col h4{font-size:11px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;
    margin-bottom:7px}
  .drawer-col.pos h4{color:var(--pos)} .drawer-col.neg h4{color:var(--neg)}
  .drawer-col ul{list-style:none}
  .drawer-col li{display:flex;justify-content:space-between;gap:10px;font-size:13px;
    padding:3px 0;border-bottom:1px solid var(--line)}
  .drawer-col li:last-child{border-bottom:none}
  .drawer-col li span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .drawer-col li em{font-style:normal;color:var(--ink-3);font-size:12px;flex:none}
  .drawer-col .none{font-size:12.5px;color:var(--ink-3)}

  /* ---------- Deckungs-Gauge ---------- */
  .cov{display:flex;align-items:center;gap:20px;padding-bottom:18px;margin-bottom:6px;
    border-bottom:1px solid var(--line)}
  .cov svg{width:84px;height:84px;flex:none}
  .cov-track{fill:none;stroke:var(--surface-3);stroke-width:7}
  .cov-arc{fill:none;stroke-width:7;stroke-linecap:round;transform:rotate(-90deg);
    transform-origin:50% 50%;transition:stroke-dasharray .7s cubic-bezier(.2,.7,.2,1)}
  .cov-num{font-size:19px;font-weight:600;fill:var(--ink);text-anchor:middle;
    dominant-baseline:central;font-variant-numeric:tabular-nums}
  .cov-txt h3{font-size:14px;margin-bottom:3px}
  .cov-txt p{font-size:13px;color:var(--ink-2);line-height:1.55}
  .cov-txt p b{color:var(--ink);font-weight:600}

  /* ---------- Mikronaehrstoff-Balken ---------- */
  .bars{display:flex;flex-direction:column}
  .bar-row{display:grid;grid-template-columns:132px 1fr 46px;align-items:center;gap:14px;
    width:100%;padding:8px 0;text-align:left;transition:background .15s}
  .bars > .bar-row:not(:first-child){border-top:1px solid var(--line)}
  .bar-row:hover{background:var(--surface-2)}
  .bar-name{min-width:0}
  .bar-name b{display:block;font-size:13.5px;font-weight:500;overflow:hidden;
    text-overflow:ellipsis;white-space:nowrap}
  .bar-name small{display:block;font-size:11.5px;color:var(--ink-3)}
  .bar-track{position:relative;height:7px;border-radius:4px;background:var(--surface-3);
    overflow:hidden}
  .bar-fill{position:absolute;left:0;top:0;bottom:0;border-radius:4px;
    transition:width .6s cubic-bezier(.2,.7,.2,1)}
  .bar-fill.pos{background:var(--pos)} .bar-fill.warn{background:var(--warn)}
  .bar-fill.neg{background:var(--neg)}
  .bar-pct{text-align:right;font-size:13px;font-weight:600}
  .bar-pct.pos{color:var(--pos)} .bar-pct.warn{color:var(--warn)} .bar-pct.neg{color:var(--neg)}
  .bar-src{padding:2px 0 12px;font-size:12.5px;color:var(--ink-2);line-height:1.6;
    border-top:1px solid var(--line)}
  .bar-src b{color:var(--ink);font-weight:600}
  .bar-src .lbl{display:block;font-size:11px;font-weight:600;letter-spacing:.08em;
    text-transform:uppercase;color:var(--ink-3);margin:9px 0 3px}
  @media(max-width:520px){.bar-row{grid-template-columns:104px 1fr 40px;gap:10px}}

  /* ---------- Datenqualitaet ---------- */
  .dq summary{display:flex;align-items:center;gap:8px;padding:14px 20px;cursor:pointer;
    font-size:13px;font-weight:500;color:var(--ink-2);list-style:none}
  .dq summary::-webkit-details-marker{display:none}
  .dq summary::after{content:'';margin-left:auto;width:7px;height:7px;border-right:1.6px solid var(--ink-3);
    border-bottom:1.6px solid var(--ink-3);transform:rotate(45deg) translateY(-2px);transition:transform .2s}
  .dq[open] summary::after{transform:rotate(-135deg) translateY(-2px)}
  .dq summary .chip{margin-right:2px}
  .dq-body{padding:0 20px 18px;border-top:1px solid var(--line);margin-top:2px;padding-top:14px}
  .dq-item{font-size:13px;color:var(--ink-2);padding:3px 0}
  .dq-item b{color:var(--ink);font-weight:600}
  .dq-list{margin-top:12px}
  .dq-list h4{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;
    color:var(--ink-3);margin:10px 0 4px}
  .dq-list .row{display:flex;justify-content:space-between;gap:12px;font-size:12.5px;
    padding:2px 0;color:var(--ink-2)}

  /* ---------- Leerzustand ---------- */
  .empty{padding:44px 24px;text-align:center;display:flex;flex-direction:column;
    align-items:center;gap:8px}
  .empty svg{width:30px;height:30px;stroke:var(--ink-3);fill:none;stroke-width:1.5;
    stroke-linecap:round;stroke-linejoin:round;margin-bottom:4px}
  .empty h2{font-size:17px}
  .empty p{font-size:13.5px;color:var(--ink-2);max-width:380px;line-height:1.6}
  .btn{display:inline-flex;align-items:center;gap:7px;margin-top:12px;padding:9px 16px;
    border-radius:9px;font-size:13.5px;font-weight:600;background:var(--accent);
    color:var(--accent-ink);text-decoration:none;transition:filter .15s}
  .btn:hover{filter:brightness(1.08)}
  .btn.ghost{background:var(--surface-2);color:var(--ink);border:1px solid var(--line)}

  footer{margin-top:26px;padding-top:16px;border-top:1px solid var(--line);
    font-size:12px;color:var(--ink-3);text-align:center;line-height:1.6}

  .rise{animation:rise .45s cubic-bezier(.2,.7,.2,1) both}
  @keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
</style>
<script>
/* Laeuft absichtlich vor dem Body: sonst blitzt beim Laden das helle Theme auf. */
(function(){
  var dark = true;                       // Vorgabe: dunkel
  try{
    var stored = localStorage.getItem('brudi-theme');
    if(stored) dark = stored === 'dark';  // manuelle Wahl schlaegt die Vorgabe
  }catch(e){}
  document.documentElement.classList.toggle('dark', dark);
})();
</script>
</head>
<body>
<header class="topbar">
  <div class="topbar-in">
    <span class="mark">kalorien<i id="markWord">brudi</i></span>
    <nav class="tabs" id="tabs" role="tablist">
      <button role="tab" data-pg="kcal" aria-selected="true">Kalorien</button>
      <button role="tab" data-pg="nutri" aria-selected="false">Nährstoffe</button>
    </nav>
    <button class="who-btn" id="whoBtn" type="button">
      <span class="dot"></span><span id="whoCur">Denis</span>
      <svg class="swap" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9h13l-3.5-3.5"/><path d="M20 15H7l3.5 3.5"/></svg>
    </button>
    <button class="icon-btn" id="themeBtn" type="button" aria-pressed="false">
      <svg class="i-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.2A8.2 8.2 0 0 1 9.8 4a8.4 8.4 0 1 0 10.2 10.2z"/></svg>
      <svg class="i-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.6v2M12 19.4v2M4.6 12h-2M21.4 12h-2M6.3 6.3L4.9 4.9M19.1 19.1l-1.4-1.4M17.7 6.3l1.4-1.4M4.9 19.1l1.4-1.4"/></svg>
    </button>
  </div>
</header>

<main class="wrap">
  <div class="pagehead">
    <div>
      <p class="eyebrow" id="eyebrow">Kalorien</p>
      <h1 id="title">Denis</h1>
      <p class="lead" id="lead"></p>
    </div>
    <div class="controls" id="headControls"></div>
  </div>
  <div id="content"></div>
  <footer id="foot"></footer>
</main>

<script>
const DATA_KCAL = __DATA_KCAL__;
const DATA_NUTRI = __DATA_NUTRI__;
const TODAY = "__TODAY_ISO__";
const BUILD = "__BUILD_DATE__";
const NOTION_URL = 'https://www.notion.so/';

let curPage = 'kcal';
/* Zuletzt gewaehlte Person merken. Faellt auf die erste Person zurueck, wenn
   nichts gespeichert ist oder der gespeicherte Name nicht mehr existiert -
   sonst stuende die Seite bei einem umbenannten Eintrag vor leeren Daten. */
let curUser = (function(){
  try{
    const stored = localStorage.getItem('brudi-user');
    if(stored && DATA_KCAL[stored]) return stored;
  }catch(e){}
  return Object.keys(DATA_KCAL)[0];
})();

/* ============================ Helfer ============================ */
const de = n => n.toLocaleString('de-DE');
const WD = ['So','Mo','Di','Mi','Do','Fr','Sa'];
const MONTHS = ['Jan','Feb','Mrz','Apr','Mai','Jun','Jul','Aug','Sep','Okt','Nov','Dez'];
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function fmtDay(iso){
  const dt = new Date(iso+'T00:00');
  return WD[dt.getDay()]+' '+String(dt.getDate()).padStart(2,'0')+'.'+String(dt.getMonth()+1).padStart(2,'0')+'.';
}
function fmtDate(iso){ const p = iso.split('-'); return p[2]+'.'+p[1]+'.'+p[0]; }
function fmtNum(v){
  if(v >= 100) return de(Math.round(v));
  if(v >= 10)  return de(Math.round(v*10)/10);
  return de(Math.round(v*100)/100);
}
function el(id){ return document.getElementById(id); }
const ICON_ADD = '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 8.4v7.2M8.4 12h7.2"/></svg>';
const ICON_CLOCK = '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5.2l3.4 2"/></svg>';

function emptyState(icon, title, msg, action){
  return '<section class="sheet"><div class="empty rise">'+icon
       + '<h2>'+esc(title)+'</h2><p>'+esc(msg)+'</p>'+(action||'')+'</div></section>';
}

/* ============================ Kalorien ============================ */
const RATIO = {p:0.30, f:0.30, c:0.40};
const METRICS = {
  kcal:{label:'Kalorien', unit:'kcal'}, p:{label:'Protein', unit:'g'},
  f:{label:'Fett', unit:'g'}, c:{label:'Carbs', unit:'g'}
};
const PERIODS = {W:'Woche', M:'Monat', J:'Jahr'};
let curMetric = 'kcal', curPeriod = 'W';

const maintenance = u => u.goalIntake + u.deficitTarget;
function classify(u, kcal){
  if(kcal <= u.goalIntake + u.greenBuf) return 'pos';
  if(kcal <= maintenance(u)) return 'warn';
  return 'neg';
}
function targets(u){
  return {kcal:u.goalIntake, p:Math.round(u.goalIntake*RATIO.p/4),
          f:Math.round(u.goalIntake*RATIO.f/9), c:Math.round(u.goalIntake*RATIO.c/4)};
}
function mondayOf(iso){
  const dt = new Date(iso+'T00:00');
  dt.setDate(dt.getDate() - ((dt.getDay()+6)%7));
  return dt;
}
const dm = dt => String(dt.getDate()).padStart(2,'0')+'.'+String(dt.getMonth()+1).padStart(2,'0')+'.';
function periodKey(iso, mode){
  const dt = new Date(iso+'T00:00');
  if(mode === 'J') return String(dt.getFullYear());
  if(mode === 'M') return dt.getFullYear()+'-'+String(dt.getMonth()+1).padStart(2,'0');
  return mondayOf(iso).toISOString().slice(0,10);
}
function periodLabel(k, mode){
  if(mode === 'J') return k;
  if(mode === 'M'){ const p = k.split('-'); return MONTHS[+p[1]-1]+' '+p[0]; }
  const mon = new Date(k+'T00:00'), sun = new Date(mon);
  sun.setDate(sun.getDate()+6);
  return dm(mon)+'–'+dm(sun);
}
function periodAgg(days, mode){
  const g = {};
  days.forEach(x => { const k = periodKey(x.d, mode); (g[k] = g[k] || []).push(x); });
  return Object.keys(g).sort().map(k => {
    const a = g[k], n = a.length;
    const av = key => Math.round(a.reduce((s,x) => s + x[key], 0) / n);
    return {n, range:periodLabel(k, mode), kcal:av('kcal'), p:av('p'), f:av('f'), c:av('c')};
  });
}

function renderKcal(){
  const u = DATA_KCAL[curUser];
  const C = el('content');
  el('headControls').innerHTML = '';

  if(!u.days || !u.days.length){
    C.innerHTML = emptyState(ICON_ADD, 'Noch keine Einträge für '+curUser,
      'Sobald Mahlzeiten in Notion landen, erscheint die Auswertung hier automatisch.',
      '<a class="btn" href="'+NOTION_URL+'" target="_blank" rel="noopener">In Notion eintragen</a>');
    el('lead').textContent = '';
    el('foot').textContent = 'Stand: '+BUILD+' · keine Daten';
    return;
  }

  const t = targets(u), q = u.quality || {};
  const total = u.days.length;
  const counts = {pos:0, warn:0, neg:0};
  u.days.forEach(x => counts[classify(u, x.kcal)]++);
  const pct = n => total ? Math.round(n/total*100) : 0;

  /* Fortschritt = zurueckgelegter Anteil der Strecke Startgewicht -> Zielgewicht.
     Bewusst in Kilo gerechnet, damit die Zahl zur Gewichts-Schiene darunter passt. */
  const sw = u.startWeight, cw = u.weight, gw = u.zielWeight;
  const canProg = sw != null && cw != null && gw != null && sw > gw;
  const doneKg = canProg ? Math.min(sw - cw, sw - gw) : 0;
  const totalKg = canProg ? sw - gw : 0;
  const leftKg = canProg ? Math.max(0, cw - gw) : 0;
  const prog = canProg ? Math.max(0, Math.min(100, doneKg/totalKg*100)) : 0;
  /* Restdauer aus dem geplanten Defizit (Faustregel 7.000 kcal je kg). */
  const daysLeft = canProg ? Math.round(leftKg*7000/u.deficitTarget) : 0;
  /* Zum Vergleich: was das Essens-Log im Schnitt an Defizit hergibt. */
  const avgKcal = u.days.reduce((s,x) => s + x.kcal, 0)/total;
  const avgDeficit = Math.round(maintenance(u) - avgKcal);

  const share = total ? counts.pos/total : 0;
  const cls = share >= 0.5 ? 'pos' : (share >= 0.25 ? 'warn' : 'neg');
  const statusTxt = cls === 'pos' ? 'Auf Kurs' : (cls === 'warn' ? 'Wackelig' : 'Nachschärfen');

  /* Gewichts-Schiene */
  let rail = '';
  if(sw != null && u.weight != null && u.zielWeight != null && sw !== u.zielWeight){
    const p = Math.max(0, Math.min(100, (sw - u.weight)/(sw - u.zielWeight)*100));
    rail = '<div class="rail">'
      + '<div class="rail-top"><span class="num">'+fmtNum(sw)+' kg</span>'
      + '<span class="num">'+fmtNum(u.zielWeight)+' kg</span></div>'
      + '<div class="rail-track"><div class="rail-done" style="width:'+p.toFixed(1)+'%"></div>'
      + '<div class="rail-pin" style="left:'+p.toFixed(1)+'%"></div></div>'
      + '<div class="rail-now">Aktuell <b class="num">'+fmtNum(u.weight)+' kg</b>'
      + (sw > u.weight ? ' · '+fmtNum(Math.round((sw-u.weight)*10)/10)+' kg abgenommen' : '')
      + '</div></div>';
  }

  const est = ok => ok === false ? '<span class="est">Standard</span>' : '';
  const facts = '<dl class="facts">'
    + '<div class="fact"><dt>Kalorienziel</dt><dd class="num">'+de(u.goalIntake)+' <small>kcal</small>'+est(q.goalFromData)+'</dd></div>'
    + '<div class="fact"><dt>Geplantes Defizit</dt><dd class="num">'+de(u.deficitTarget)+' <small>kcal/Tag</small></dd></div>'
    + '<div class="fact"><dt>Erhaltungsbedarf</dt><dd class="num">'+de(maintenance(u))+' <small>kcal</small></dd></div>'
    + '<div class="fact"><dt>Ø Defizit laut Log</dt><dd class="num">'+de(avgDeficit)+' <small>kcal/Tag</small></dd></div>'
    + '<div class="fact"><dt>Makro-Ziel</dt><dd class="num">'+t.p+' P · '+t.f+' F · '+t.c+' C <small>g</small></dd></div>'
    + '</dl>';

  const heroCap = !canProg
    ? 'Für die Quote fehlen Gewichtseinträge (Start, aktuell und Ziel).'
    : (leftKg <= 0
        ? '<b>Zielgewicht erreicht</b> · ' + fmtNum(totalKg) + ' kg geschafft'
        : '<b class="num">' + fmtNum(Math.round(doneKg*10)/10) + '</b> von <span class="num">'
          + fmtNum(totalKg) + '</span> kg geschafft · noch <b class="num">'
          + fmtNum(Math.round(leftKg*10)/10) + ' kg</b>'
          + '<br>Bei ' + de(u.deficitTarget) + ' kcal Defizit pro Tag rechnerisch noch rund <b class="num">'
          + de(daysLeft) + ' Tage</b>.');

  const hero = '<section class="sheet hero rise">'
    + '<div class="hero-main">'
    +   '<p class="eyebrow">Fortschritt zum Zielgewicht</p>'
    +   '<div class="hero-num"><b class="num">'+(canProg ? Math.round(prog) : '–')+'</b><span>%</span></div>'
    +   '<div class="meter"><i style="width:'+prog.toFixed(1)+'%"></i></div>'
    +   '<p class="hero-cap">'+heroCap+'</p>'
    +   rail
    + '</div>'
    + '<div class="hero-side">'
    +   '<span class="chip '+cls+'"><i></i>'+statusTxt+'</span>'
    +   '<p class="hero-cap">'+pct(counts.pos)+' % der '+total+' getrackten Tage lagen im Zielkorridor.</p>'
    +   facts
    + '</div></section>';

  const stat = (k, n, lab, sub) =>
    '<div class="stat '+k+'"><span class="stat-num num">'+n+'</span>'
    + '<span class="stat-lab">'+lab+'</span><span class="stat-sub">'+sub+'</span></div>';
  const stats = '<section class="sheet stats rise">'
    + stat('pos', counts.pos, 'Ziel erreicht', pct(counts.pos)+' % der Tage')
    + stat('warn', counts.warn, 'Im Defizit', pct(counts.warn)+' % der Tage')
    + stat('neg', counts.neg, 'Über Bedarf', pct(counts.neg)+' % der Tage')
    + stat('', total, 'Tage getrackt', 'seit '+fmtDay(u.days[0].d))
    + '</section>';

  /* Letzte 7 Tage: Abweichung vom Tagesziel, divergierend um die Nulllinie */
  const last7 = u.days.slice(-7).reverse();
  const maxAbs = Math.max(...last7.map(x => Math.abs(x.kcal - u.goalIntake)), 300) * 1.05;
  const devRows = last7.map(x => {
    const diff = x.kcal - u.goalIntake, k = classify(u, x.kcal);
    const w = Math.min(Math.abs(diff)/maxAbs*50, 50);
    const pos = diff <= 0 ? 'right:50%' : 'left:50%';
    const flag = x.flag
      ? '<span class="dev-flag" title="Tages-Total weicht von der Einzelposten-Summe ab">▲</span>' : '';
    return '<div class="dev-row"><div class="dev-day">'+fmtDay(x.d)+'</div>'
      + '<div class="dev-track"><div class="dev-zero"></div>'
      + '<div class="dev-bar '+k+'" style="'+pos+';width:'+w.toFixed(1)+'%"></div></div>'
      + '<div class="dev-val '+k+' num">'+(diff > 0 ? '+' : '')+de(diff)+flag
      + '<small>'+de(x.kcal)+' kcal</small></div></div>';
  }).join('');
  const dev = '<section class="sheet rise">'
    + '<div class="sheet-head"><div><h2>Letzte 7 Tage</h2>'
    + '<p class="sub">Abweichung vom Tagesziel von '+de(u.goalIntake)+' kcal</p></div></div>'
    + '<div class="sheet-body"><div class="dev">'+devRows+'</div>'
    + '<div class="dev-scale"><span>← unter Ziel · über Ziel →</span></div></div></section>';

  const trend = '<section class="sheet rise">'
    + '<div class="sheet-head"><div><h2>Durchschnitt pro Tag</h2>'
    + '<p class="sub" id="trendSub"></p></div>'
    + '<div class="controls">'
    +   '<div class="seg" id="segPeriod">'+Object.keys(PERIODS).map(p =>
          '<button data-p="'+p+'" aria-pressed="'+(p === curPeriod)+'" title="'+PERIODS[p]+'">'+p+'</button>').join('')+'</div>'
    +   '<div class="seg" id="segMetric">'+Object.keys(METRICS).map(m =>
          '<button data-m="'+m+'" aria-pressed="'+(m === curMetric)+'">'+METRICS[m].label+'</button>').join('')+'</div>'
    + '</div></div>'
    + '<div class="sheet-body"><div class="chart" id="chart"></div>'
    + '<div class="c-labels" id="chartLabels"></div></div></section>';

  C.innerHTML = hero + stats + dev + trend + dqSection(q);

  el('segPeriod').querySelectorAll('button').forEach(b =>
    b.onclick = () => { curPeriod = b.dataset.p; renderKcal(); });
  el('segMetric').querySelectorAll('button').forEach(b =>
    b.onclick = () => { curMetric = b.dataset.m; renderKcal(); });

  const limit = window.innerWidth < 560 ? 4 : 6;
  drawTrend(periodAgg(u.days, curPeriod).slice(-limit), t);

  el('lead').textContent = fmtDate(u.days[0].d)+' – '+fmtDate(u.days[total-1].d)+' · '+total+' Tage';
  el('foot').textContent = 'Stand: '+BUILD+' · Makro-Verhältnis 30 % Protein / 30 % Fett / 40 % Kohlenhydrate · automatisch generiert';
}

function dqSection(q){
  const items = [];
  if(q.skippedDays)  items.push('<b>'+q.skippedDays+'</b> Tag(e) ohne Kalorien-Eintrag – nicht gewertet');
  if(q.mismatchDays) items.push('<b>'+q.mismatchDays+'</b> Tag(e): Tages-Total weicht von der Einzelposten-Summe ab');
  if(q.goalFromData === false) items.push('Kalorienziel ist ein Standardwert, nicht aus Notion');
  if(q.zielFromData === false) items.push('Zielgewicht ist ein Standardwert, nicht aus Notion');
  if(!items.length) return '';
  let detail = '';
  if((q.mismatchList || []).length){
    detail += '<div class="dq-list"><h4>Abweichende Tage</h4>'
      + q.mismatchList.map(m => '<div class="row"><span>'+fmtDay(m.d)+'</span>'
      + '<span class="num">'+de(m.t)+' statt '+de(m.s)+' kcal</span></div>').join('')+'</div>';
  }
  if((q.skippedList || []).length){
    detail += '<div class="dq-list"><h4>Ohne Kalorien-Eintrag</h4><div class="row"><span>'
      + q.skippedList.map(fmtDay).join(', ')+'</span></div></div>';
  }
  return '<details class="sheet dq rise"><summary><span class="chip warn"><i></i>Datenqualität</span>'
    + items.length+' Hinweis'+(items.length === 1 ? '' : 'e')+'</summary>'
    + '<div class="dq-body">'+items.map(i => '<p class="dq-item">'+i+'</p>').join('')+detail+'</div></details>';
}

function drawTrend(rows, t){
  const box = el('chart'), labels = el('chartLabels');
  if(!rows.length){ box.innerHTML = ''; labels.innerHTML = ''; return; }
  const goal = t[curMetric], unit = METRICS[curMetric].unit;
  const grp = curPeriod === 'W' ? 'Kalenderwoche' : (curPeriod === 'M' ? 'Monat' : 'Jahr');
  const sub = el('trendSub');
  if(sub) sub.textContent = METRICS[curMetric].label+' nach '+grp+' · gestrichelt: Ziel '+de(goal)+' '+unit;

  const W = Math.max(Math.round(box.clientWidth) || 640, 260), H = 190, top = 26, base = H - 10;
  const max = Math.max(...rows.map(r => r[curMetric]), goal) * 1.15 || 1;
  const y = v => base - (v/max)*(base - top);
  const colW = W/rows.length, barW = Math.min(colW*0.34, 52);

  const gy = y(goal);
  const grid = '<line class="c-grid" x1="0" y1="'+base+'" x2="'+W+'" y2="'+base+'"/>';
  const goalLine = '<line class="c-goal" x1="0" y1="'+gy.toFixed(1)+'" x2="'+W+'" y2="'+gy.toFixed(1)+'"/>';

  const bars = rows.map((r,i) => {
    const cx = colW*(i+0.5), v = r[curMetric];
    const by = Math.max(y(v), top), h = Math.max(base - by, 3);
    let ly = Math.max(by - 9, 11);
    return '<rect class="c-bar" x="'+(cx - barW/2).toFixed(1)+'" y="'+by.toFixed(1)
      + '" width="'+barW.toFixed(1)+'" height="'+h.toFixed(1)+'" rx="4"/>'
      + '<text class="c-val" x="'+cx.toFixed(1)+'" y="'+ly.toFixed(1)+'">'+de(v)+'</text>';
  }).join('');

  box.innerHTML = '<svg width="'+W+'" height="'+H+'" viewBox="0 0 '+W+' '+H+'" '
    + 'preserveAspectRatio="xMidYMid meet" role="img" aria-label="'
    + METRICS[curMetric].label+' pro '+grp+'">'+grid+goalLine+bars+'</svg>';
  labels.innerHTML = rows.map(r =>
    '<div class="c-label">'+r.range+'<small>'+r.n+(r.n === 1 ? ' Tag' : ' Tage')+'</small></div>').join('');
}

/* ============================ Nährstoffe ============================ */
const CATS = [
  {key:'Darmgesundheit', help:'Ballaststoffe, Fermentiertes, Vielfalt'},
  {key:'Low FODMAP',     help:'niedrig-FODMAP, gut verträglich'},
  {key:'Säure-Base',     help:'basisch statt säurebildend'}
];
const CHOL_GREEN = 300, CHOL_AMBER = 500;
const CAT_GREEN = 70, CAT_AMBER = 50;
const MIC_GREEN = 90, MIC_AMBER = 50;
const NPERIODS = {'7':'Letzte 7 Tage', '30':'Letzte 30 Tage', 'all':'Gesamter Zeitraum'};
let curNPeriod = '7', curSort = 'worst', openCheck = null;

const splitUnit = k => { const m = k.match(/^(.*) \(([^)]+)\)$/); return m ? [m[1], m[2]] : [k, '']; };
const micColor = p => p >= MIC_GREEN ? 'pos' : (p >= MIC_AMBER ? 'warn' : 'neg');
function shiftISO(iso, d){ const x = new Date(iso+'T00:00'); x.setDate(x.getDate()+d); return x.toISOString().slice(0,10); }
function windowDays(u){
  if(curNPeriod === 'all') return u.days.slice();
  const cut = shiftISO(TODAY, -(parseInt(curNPeriod,10) - 1));
  return u.days.filter(x => x.d >= cut);
}
const SUGGEST = {
  'Ballaststoffe (g)':['Haferflocken','Linsen','Himbeeren','Chiasamen','Vollkornbrot'],
  'Calcium (mg)':['Joghurt','Grünkohl','Mandeln','Käse','Sesam'],
  'Eisen (mg)':['Linsen','Kürbiskerne','Rindfleisch','Haferflocken','Spinat'],
  'Folat (µg)':['Spinat','Kichererbsen','Brokkoli','Linsen','Avocado'],
  'Jod (µg)':['Seelachs','Jodsalz','Milchprodukte','Eier','Nori-Algen'],
  'Kalium (mg)':['Banane','Kartoffeln','Avocado','Spinat','Weiße Bohnen'],
  'Magnesium (mg)':['Kürbiskerne','Vollkornreis','Spinat','Mandeln','Bitterschokolade'],
  'Omega-3 (g)':['Lachs','Walnüsse','Leinsamen','Chiasamen','Rapsöl'],
  'Selen (µg)':['Paranüsse','Thunfisch','Eier','Haferflocken','Champignons'],
  'Vitamin A (µg)':['Süßkartoffel','Karotten','Spinat','Kürbis','Paprika'],
  'Vitamin B12 (µg)':['Lachs','Eier','Käse','Joghurt','Milch'],
  'Vitamin C (mg)':['Paprika','Brokkoli','Orangen','Kiwi','Erdbeeren'],
  'Vitamin D (µg)':['Lachs','Eier','Pilze','Hering','Margarine (angereichert)'],
  'Vitamin E (mg)':['Mandeln','Sonnenblumenkerne','Olivenöl','Haselnüsse','Avocado'],
  'Vitamin K (µg)':['Grünkohl','Spinat','Rucola','Brokkoli','Rosenkohl'],
  'Zink (mg)':['Kürbiskerne','Rindfleisch','Haferflocken','Linsen','Käse']
};
const NICHT_VEGGIE = new Set(['Rindfleisch','Lachs','Thunfisch','Seelachs','Hering','Hähnchen']);

function topFoods(days){
  const out = {};
  CATS.forEach(c => {
    const pos = {}, neg = {};
    days.forEach(day => {
      const f = (day.cf && day.cf[c.key]) || [[],[]];
      f[0].forEach(n => pos[n] = (pos[n]||0)+1);
      f[1].forEach(n => neg[n] = (neg[n]||0)+1);
    });
    const top = o => Object.entries(o).sort((a,b) => b[1]-a[1] || a[0].localeCompare(b[0])).slice(0,5);
    out[c.key] = {pos:top(pos), neg:top(neg)};
  });
  return out;
}
function topChol(days){
  const m = {};
  days.forEach(day => Object.keys(day.chol || {}).forEach(n => m[n] = (m[n]||0) + day.chol[n]));
  return Object.entries(m).sort((a,b) => b[1]-a[1] || a[0].localeCompare(b[0])).slice(0,5);
}

function renderNutri(){
  const u = DATA_NUTRI[curUser];
  const C = el('content');

  if(!u.days.length){
    el('headControls').innerHTML = '';
    C.innerHTML = emptyState(ICON_ADD, 'Noch keine Einträge für '+curUser,
      'Sobald in der Lebensmittel-Analyse Zeilen für '+curUser+' liegen, erscheint die Auswertung hier.',
      '<a class="btn" href="'+NOTION_URL+'" target="_blank" rel="noopener">In Notion eintragen</a>');
    el('lead').textContent = '';
    el('foot').textContent = 'Stand: '+BUILD+' · keine Daten';
    return;
  }

  el('headControls').innerHTML = '<div class="seg" id="segTime">'
    + Object.keys(NPERIODS).map(p => '<button data-p="'+p+'" aria-pressed="'+(p === curNPeriod)+'">'
    + (p === 'all' ? 'Gesamt' : p+' Tage')+'</button>').join('')+'</div>';
  el('segTime').querySelectorAll('button').forEach(b =>
    b.onclick = () => { curNPeriod = b.dataset.p; openCheck = null; renderNutri(); });

  const wd = windowDays(u), n = wd.length;
  if(!n){
    el('lead').textContent = NPERIODS[curNPeriod]+' · keine Daten';
    C.innerHTML = emptyState(ICON_CLOCK, 'Keine Daten im Zeitfenster',
      'Im gewählten Zeitraum wurde nichts getrackt. Wechsle oben das Zeitfenster.',
      '<button class="btn ghost" id="showAll">Gesamten Zeitraum zeigen</button>');
    const s = el('showAll');
    if(s) s.onclick = () => { curNPeriod = 'all'; renderNutri(); };
    el('foot').textContent = 'Stand: '+BUILD;
    return;
  }
  el('lead').textContent = fmtDate(wd[0].d)+' – '+fmtDate(wd[n-1].d)+' · '+n
    + (n === 1 ? ' getrackter Tag' : ' getrackte Tage')+' · Ø pro Tag';

  /* Summen und Kategorie-Stimmen im Fenster */
  const sum = {}; Object.keys(u.ref).forEach(k => sum[k] = 0); sum['Cholesterin (mg)'] = 0;
  const votes = {}; CATS.forEach(c => votes[c.key] = [0,0,0]);
  wd.forEach(day => {
    Object.keys(sum).forEach(k => sum[k] += (day.nut[k] || 0));
    CATS.forEach(c => {
      const v = day.cat[c.key] || [0,0,0];
      votes[c.key][0] += v[0]; votes[c.key][1] += v[1]; votes[c.key][2] += v[2];
    });
  });
  const avg = {}; Object.keys(sum).forEach(k => avg[k] = sum[k]/n);
  const foods = topFoods(wd);

  /* Checkpoints */
  const checks = [];
  CATS.forEach(c => {
    const v = votes[c.key], tot = v[0]+v[1]+v[2];
    if(!tot){
      checks.push({key:c.key, cls:'warn', status:'–', detail:'keine Angaben', score:'', help:c.help,
                   tip:{pos:[], neg:[]}});
    } else {
      const score = (v[0]*100 + v[1]*50)/tot;
      const cls = score >= CAT_GREEN ? 'pos' : (score >= CAT_AMBER ? 'warn' : 'neg');
      checks.push({
        key:c.key, cls,
        status: cls === 'pos' ? 'Gut' : (cls === 'warn' ? 'Okay' : 'Kritisch'),
        detail: v[0]+' gut · '+v[1]+' neutral · '+v[2]+' schlecht',
        score: Math.round(score)+'/100', help:c.help, tip:foods[c.key]
      });
    }
  });
  const ch = avg['Cholesterin (mg)'];
  const chCls = ch <= CHOL_GREEN ? 'pos' : (ch <= CHOL_AMBER ? 'warn' : 'neg');
  checks.push({
    key:'Cholesterin', cls:chCls,
    status: chCls === 'pos' ? 'Gut' : (chCls === 'warn' ? 'Okay' : 'Hoch'),
    detail:'Ø '+de(Math.round(ch))+' mg/Tag · Ziel ≤ '+CHOL_GREEN,
    score:de(Math.round(ch))+' mg', help:'weniger ist besser',
    tip:{pos:[], neg:topChol(wd), unit:'mg'}
  });

  let drawer = '';
  if(openCheck != null && checks[openCheck]){
    const c = checks[openCheck], unit = c.tip.unit;
    const list = (arr, kind) => {
      if(!arr.length) return '<p class="none">Keine Einträge im Zeitfenster.</p>';
      return '<ul>'+arr.map(([nm, v]) => '<li><span>'+esc(nm)+'</span><em class="num">'
        + (unit ? de(Math.round(v))+' '+unit : '×'+v)+'</em></li>').join('')+'</ul>';
    };
    drawer = '<div class="drawer">'
      + '<div class="drawer-head"><h3>'+esc(c.key)+'</h3><p>'+esc(c.help)+'</p></div>'
      + '<div class="drawer-cols" data-single="'+Boolean(unit)+'">'
      + (unit ? '' : '<div class="drawer-col pos"><h4>Häufigste gute Quellen</h4>'+list(c.tip.pos)+'</div>')
      + '<div class="drawer-col neg"><h4>'+(unit ? 'Größte Quellen' : 'Häufigste Problemquellen')+'</h4>'
      + list(c.tip.neg)+'</div></div></div>';
  }

  /* Spaltenzahl exakt wie die Media Queries bestimmen, damit die Schublade
     direkt unter der Zeile der geklickten Kategorie landet - nicht am Ende. */
  const cols = window.matchMedia('(max-width:440px)').matches ? 1
             : (window.matchMedia('(max-width:820px)').matches ? 2 : 4);
  const rowEnd = openCheck == null ? -1
               : Math.min(Math.floor(openCheck/cols)*cols + cols - 1, checks.length - 1);

  const checksHtml = checks.map((c,i) =>
    '<button class="check '+c.cls+(i % cols === 0 ? ' c0' : '')+(i >= cols ? ' rn' : '')
    + '" data-i="'+i+'" aria-expanded="'+(openCheck === i)+'">'
    + '<div class="check-top"><span class="check-name">'+esc(c.key)+'</span>'
    + (c.score ? '<span class="check-score num">'+c.score+'</span>' : '')+'</div>'
    + '<div class="check-status">'+c.status+'</div>'
    + '<div class="check-detail num">'+c.detail+'</div>'
    + '<div class="check-more"><span>'+esc(c.help)+'</span><i class="caret"></i></div></button>'
    + (i === rowEnd ? drawer : '')).join('');

  /* Mikronährstoffe */
  let micros = Object.keys(u.ref).map(k => {
    const [name, unit] = splitUnit(k);
    const a = avg[k] || 0, ref = u.ref[k];
    const raw = ref > 0 ? a/ref*100 : 0, capped = Math.min(100, raw);
    return {key:k, name, unit, avg:a, ref, pct:capped, raw, color:micColor(capped)};
  });
  const cov = micros.length ? micros.reduce((s,m) => s + m.pct, 0)/micros.length : 0;
  const covCls = micColor(cov);
  const r = 34, circ = 2*Math.PI*r, dash = Math.max(0, Math.min(100, cov))/100*circ;
  const gauge = '<div class="cov"><svg viewBox="0 0 80 80" role="img" aria-label="Gesamtdeckung '
    + Math.round(cov)+' Prozent">'
    + '<circle class="cov-track" cx="40" cy="40" r="'+r+'"/>'
    + '<circle class="cov-arc" cx="40" cy="40" r="'+r+'" stroke="var(--'+covCls+')" '
    + 'stroke-dasharray="'+dash.toFixed(1)+' '+circ.toFixed(1)+'"/>'
    + '<text class="cov-num" x="40" y="40">'+Math.round(cov)+'%</text></svg>'
    + '<div class="cov-txt"><h3>Gesamtdeckung</h3><p>Im Schnitt <b>'+Math.round(cov)+' %</b> der '
    + 'DGE-Tagesreferenz über '+micros.length+' Mikronährstoffe · pro Nährstoff bei 100 % gedeckelt.</p></div></div>';

  micros.sort((a,b) => curSort === 'worst' ? a.raw - b.raw : b.raw - a.raw);
  const barsHtml = micros.map(m => {
    const src = (u.nutTop && u.nutTop[m.key]) || [];
    const logged = new Set(src.map(x => x[0].toLowerCase()));
    let sug = (SUGGEST[m.key] || []).filter(x => !logged.has(x.toLowerCase()));
    if(curUser === 'Leni') sug = sug.filter(x => !NICHT_VEGGIE.has(x));
    sug = sug.slice(0,3);
    const srcHtml = (src.length
        ? '<span class="lbl">Aus deinem Log</span>'+src.map(x => '<b>'+esc(x[0])+'</b> (Ø '+fmtNum(x[1])+' '+m.unit+')').join(' · ')
        : '<span class="lbl">Aus deinem Log</span>Noch keine Quelle mit '+esc(m.name)+' erfasst.')
      + (sug.length ? '<span class="lbl">Weitere gute Optionen</span>'+sug.map(x => '<b>'+esc(x)+'</b>').join(' · ') : '');
    return '<button class="bar-row" aria-expanded="false">'
      + '<div class="bar-name"><b>'+esc(m.name)+'</b><small class="num">'+fmtNum(m.avg)+' / '+fmtNum(m.ref)+' '+m.unit+'</small></div>'
      + '<div class="bar-track"><div class="bar-fill '+m.color+'" style="width:'+m.pct.toFixed(1)+'%"></div></div>'
      + '<div class="bar-pct '+m.color+' num">'+Math.round(m.raw)+'%</div></button>'
      + '<div class="bar-src" hidden>'+srcHtml+'</div>';
  }).join('');

  C.innerHTML =
      '<section class="sheet rise">'
    +   '<div class="sheet-head" style="padding-bottom:16px"><div><h2>Gesundheits-Checkpoints</h2>'
    +   '<p class="sub">Ampel im gewählten Zeitfenster · tippen zeigt die Top-Lebensmittel</p></div></div>'
    +   '<div class="checks">'+checksHtml+'</div></section>'
    + '<section class="sheet rise">'
    +   '<div class="sheet-head"><div><h2>Mikronährstoffe</h2>'
    +   '<p class="sub">Ø pro Tag gegen die DGE-Tagesreferenz</p></div>'
    +   '<div class="seg" id="segSort">'
    +     '<button data-s="worst" aria-pressed="'+(curSort === 'worst')+'">Lücken zuerst</button>'
    +     '<button data-s="best" aria-pressed="'+(curSort === 'best')+'">Beste zuerst</button>'
    +   '</div></div>'
    +   '<div class="sheet-body">'+gauge+'<div class="bars">'+barsHtml+'</div></div>'
    + '</section>';

  C.querySelectorAll('.check').forEach(b => b.onclick = () => {
    const i = +b.dataset.i;
    openCheck = (openCheck === i) ? null : i;
    renderNutri();
  });
  el('segSort').querySelectorAll('button').forEach(b =>
    b.onclick = () => { curSort = b.dataset.s; renderNutri(); });
  C.querySelectorAll('.bar-row').forEach(row => row.onclick = () => {
    const src = row.nextElementSibling;
    if(!src || !src.classList.contains('bar-src')) return;
    const wasOpen = !src.hidden;
    C.querySelectorAll('.bar-src').forEach(x => x.hidden = true);
    C.querySelectorAll('.bar-row').forEach(x => x.setAttribute('aria-expanded','false'));
    src.hidden = wasOpen;
    row.setAttribute('aria-expanded', String(!wasOpen));
  });

  el('foot').textContent = 'Stand: '+BUILD+' · '+curUser+' · '+NPERIODS[curNPeriod]
    + ' · Zielwerte: DGE-Tagesreferenz ('+(curUser === 'Denis' ? 'm' : 'w')+') · automatisch generiert';
}

/* ============================ Steuerung ============================ */
function render(){
  const nutri = curPage === 'nutri';
  const src = nutri ? DATA_NUTRI : DATA_KCAL;
  document.documentElement.style.setProperty('--accent-raw', src[curUser].accent);
  document.querySelectorAll('#tabs button').forEach(b =>
    b.setAttribute('aria-selected', String(b.dataset.pg === curPage)));
  const other = nextUser();
  el('whoBtn').title = 'Zu ' + other + ' wechseln';
  el('whoBtn').setAttribute('aria-label', 'Angezeigte Person: ' + curUser + ' – zu ' + other + ' wechseln');
  const kicker = (DATA_KCAL[curUser] || {}).kicker || 'brudi';
  el('markWord').textContent = kicker;
  el('eyebrow').textContent = (nutri ? 'Nährstoff' : 'Kalorien') + kicker;
  /* Auch der Browser-Tab; "Brudi" waere fuer Leni sonst genauso schief. */
  document.title = (nutri ? 'Nährstoff' : 'Kalorien') + kicker;
  el('title').textContent = curUser;
  el('whoCur').textContent = curUser;
  if(nutri) renderNutri(); else renderKcal();
}

el('tabs').querySelectorAll('button').forEach(b =>
  b.onclick = () => { curPage = b.dataset.pg; openCheck = null; render(); });

/* --- Theme-Umschalter --- */
const themeBtn = el('themeBtn');
function syncTheme(){
  const dark = document.documentElement.classList.contains('dark');
  themeBtn.setAttribute('aria-pressed', String(dark));
  themeBtn.setAttribute('aria-label', dark ? 'Zu hellem Design wechseln' : 'Zu dunklem Design wechseln');
  themeBtn.title = dark ? 'Helles Design' : 'Dunkles Design';
}
themeBtn.onclick = () => {
  const dark = !document.documentElement.classList.contains('dark');
  document.documentElement.classList.toggle('dark', dark);
  try{ localStorage.setItem('brudi-theme', dark ? 'dark' : 'light'); }catch(e){}
  syncTheme();
};
syncTheme();

/* --- Personen-Umschalter: ein Klick wechselt direkt --- */
const USERS = Object.keys(DATA_KCAL);
const nextUser = () => USERS[(USERS.indexOf(curUser) + 1) % USERS.length];
el('whoBtn').onclick = () => {
  curUser = nextUser(); curMetric = 'kcal'; openCheck = null;
  try{ localStorage.setItem('brudi-user', curUser); }catch(e){}
  render();
};

/* Das Balkendiagramm skaliert per viewBox mit - nur die Label-Anzahl haengt
   an der Fensterbreite, daher genuegt ein entprellter Re-Render. */
let rz;
window.addEventListener('resize', () => { clearTimeout(rz); rz = setTimeout(render, 200); });

render();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
