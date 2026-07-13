"""Agent 1 — Datenprüfer (streng).
Ziel: eine *perfekte* Datenquelle. Prüft, dass in BEIDEN Notion-DBs wirklich
JEDE Spalte befüllt ist, dass jedes Lebensmittel sauber als eigene Zeile
getrennt ist (zusammengesetzte Gerichte aufgeteilt, Markenprodukte einzeln),
dass Summen zusammenpassen, Datum/Wochentag stimmen, keine Duplikate und keine
Namens-Inkonsistenzen existieren. Nur lesend — schlägt Fixes vor.
"""
import datetime, collections, re
from lib import query_all, prop, write_report, DS_TAGES, DS_ANALYSE, WD_DE

TOL = 0.05

# --- Vollständige Spaltenlisten (jede muss befüllt sein) --------------------
TAGES_COLS = ["Tag", "Datum", "Person", "Kalorien (kcal)", "Protein (g)",
              "Kohlenhydrate (g)", "Fett (g)", "Kalorienziel (kcal)",
              "Gewicht (kg)", "Zielgewicht", "Ziel"]
ANALYSE_COLS = ["Lebensmittel", "Person", "Datum", "Kalorien (kcal)", "Eiweiß (g)",
                "Kohlenhydrate (g)", "Fett (g)", "Zucker (g)", "Ballaststoffe (g)",
                "Cholesterin (mg)", "Omega-3 (g)", "Calcium (mg)", "Eisen (mg)",
                "Folat (µg)", "Jod (µg)", "Kalium (mg)", "Magnesium (mg)",
                "Selen (µg)", "Zink (mg)", "Vitamin A (µg)", "Vitamin B12 (µg)",
                "Vitamin C (mg)", "Vitamin D (µg)", "Vitamin E (mg)", "Vitamin K (µg)",
                "Darmgesundheit", "Low FODMAP", "Säure-Base"]

# Marken/Fertigprodukte bleiben EINE Zeile (kein Splitten erwartet)
BRANDS = ["rewe", "ehrmann", "gustavo", "nuii", "ben & jerry", "kölln", "kellogg",
          "biscoff", "finello", "buko", "billie green", "billy green", "arla",
          "oakberry", "rich & greens", "esn", "clearwhey", "clear whey", "fritz",
          "toblerone", "langnese", "mälzer", "prep my meal", "kinder", "oreo",
          "taifun", "mühlen", "bonduelle", "miracel", "harry", "koro", "ppura",
          "grünländer", "skyr", "quäse", "harzer", "proteinriegel", "riegel",
          "eis", "cookie", "smoothie", "wrap", "brötchen", "porridge", "mousse"]
# Wörter, die auf ein zusammengesetztes (aufzuteilendes) Gericht hindeuten
COMPOSITE = [" mit ", " + ", " und ", " auf ", "bowl", "gratin", "auflauf",
             "pfanne", "salat mit", "teller"]

def _num(x): return x if isinstance(x, (int, float)) else 0
def _empty(v): return v is None or v == ""

def check():
    tages = query_all(DS_TAGES)
    analyse = query_all(DS_ANALYSE)
    issues = []

    by_day = collections.defaultdict(lambda: {"kcal": 0, "rows": 0})
    for a in analyse:
        if prop(a, "Duplikat"):
            continue
        name = prop(a, "Lebensmittel") or "(ohne Name)"
        person, datum = prop(a, "Person"), prop(a, "Datum")
        # JEDE Spalte befüllt?
        empties = [c for c in ANALYSE_COLS if _empty(prop(a, c))]
        if empties:
            sev = "🔴" if any(c in ("Lebensmittel", "Person", "Datum") for c in empties) else "🟡"
            issues.append((sev, f"Analyse '{name}' ({datum}): leere Spalten: {', '.join(empties)}"))
        # Trennung: sieht der Name nach zusammengesetztem Gericht aus?
        low = name.lower()
        looks_composite = any(k in low for k in COMPOSITE) or low.count(",") >= 1
        is_brand = any(b in low for b in BRANDS)
        if looks_composite and not is_brand:
            issues.append(("🟡", f"Analyse '{name}' ({datum}): evtl. nicht getrennt – "
                                 f"in Einzel-Zutaten aufteilen?"))
        if person and datum:
            d = by_day[(person, datum)]
            d["kcal"] += _num(prop(a, "Kalorien (kcal)")); d["rows"] += 1

    # Namens-Konsistenz
    ALIAS = {"skier": "Skyr", "mühle hack": "Mühlen Hack", "jakitori": "Yakitori",
             "kellox": "Kellogg's", "gustavo augusto": "Gustavo Gusto"}
    for a in analyse:
        raw = prop(a, "Lebensmittel") or ""
        for bad, good in ALIAS.items():
            if bad in raw.lower():
                issues.append(("🟡", f"Namens-Normalisierung: '{raw}' → '{good}'"))

    # Tagesübersicht
    seen = collections.Counter()
    for t in tages:
        person, datum, tag = prop(t, "Person"), prop(t, "Datum"), prop(t, "Tag")
        seen[(person, datum)] += 1
        label = f"{person} {datum}"
        empties = [c for c in TAGES_COLS if _empty(prop(t, c))]
        if empties:
            issues.append(("🔴", f"Tag {label}: leere Spalten: {', '.join(empties)}"))
        if datum and tag:
            try:
                wd = WD_DE[datetime.date.fromisoformat(datum).weekday()]
                if not tag.startswith(wd):
                    issues.append(("🔴", f"Tag {label}: Wochentag '{tag}' ≠ {datum} ({wd})"))
            except ValueError:
                issues.append(("🟡", f"Tag {label}: Datum nicht parsebar"))
        if datum and datum > datetime.date.today().isoformat():
            issues.append(("🟡", f"Tag {label}: Datum in der Zukunft"))
        kcal = _num(prop(t, "Kalorien (kcal)"))
        mk = _num(prop(t, "Protein (g)"))*4 + _num(prop(t, "Kohlenhydrate (g)"))*4 + _num(prop(t, "Fett (g)"))*9
        if kcal and not (0 <= kcal <= 8000):
            issues.append(("🔴", f"Tag {label}: kcal={kcal} unplausibel"))
        if kcal and mk and abs(mk-kcal)/max(kcal,1) > 0.25:
            issues.append(("🟡", f"Tag {label}: Makro-Gegenrechnung {mk:.0f} ≠ {kcal:.0f} kcal"))
        key = (person, datum)
        if kcal and key in by_day:
            asum = by_day[key]["kcal"]
            if asum and abs(asum-kcal)/max(kcal,1) > TOL:
                issues.append(("🔴", f"Tag {label}: Total {kcal:.0f} ≠ Analyse-Summe {asum:.0f} kcal"))
        elif kcal and key not in by_day:
            issues.append(("🔴", f"Tag {label}: KEINE Lebensmittel-Analyse-Zeilen (Trennung fehlt)"))

    for key, n in seen.items():
        if n > 1:
            issues.append(("🔴", f"Doppelter Tageseintrag: {key[0]} {key[1]} ({n}×)"))

    return issues, len(tages), len(analyse)

def main():
    issues, n_t, n_a = check()
    order = {"🔴": 0, "🟡": 1}
    issues.sort(key=lambda x: order.get(x[0], 9))
    crit = sum(1 for s, _ in issues if s == "🔴")
    perfect = "✅ Datenquelle perfekt." if not issues else ""
    lines = [f"# Daten-QA (streng) — {datetime.date.today().isoformat()}", "",
             f"Tagesübersicht: {n_t} · Lebensmittel-Analyse: {n_a}",
             f"**Befunde:** {crit} 🔴 · {len(issues)-crit} 🟡  {perfect}", ""]
    lines += [f"- {s} {t}" for s, t in issues]
    write_report("data-qa", "\n".join(lines))
    print(f"Agent1: {crit} kritisch, {len(issues)-crit} Hinweise")
    return crit

if __name__ == "__main__":
    main()
