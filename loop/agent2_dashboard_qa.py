"""Agent 2 — Dashboard-Tester (Funktion + UX/Design).
1) Funktional: klickt alle Toggles/Wege durch, prüft Rendering, NaN/undefined,
   JS-Fehler und ob der neueste Notion-Eintrag sichtbar ist.
2) UX/Design: macht Screenshots (Desktop + Mobil) und lässt Claude Vision
   bewerten, ob alles clean, modern und top aussieht — mit konkreten
   Design-Verbesserungen, die als Bugs/Vorschläge weiterfließen.

Benötigt: playwright (+ chromium)
"""
import datetime, pathlib
from lib import (query_all, prop, write_report, claude_vision,
                 DASHBOARD_URL, DS_TAGES, REPORTS)

SHOTS = REPORTS / "shots"

DESIGN_SYSTEM = """Du bist Senior Product-Designer und UX-Reviewer. Du bewertest
Screenshots eines Kalorien-Tracking-Dashboards (dunkles Theme, zwei Nutzer).
Bewerte streng auf: visuelle Hierarchie, Typografie, Abstände/Ausrichtung,
Farb- & Kontrastqualität, Konsistenz, Whitespace, Moderne/Cleanliness,
Lesbarkeit von Charts, mobile Tauglichkeit. Ziel ist eine TOP aussehende,
moderne App. Gib eine Gesamtnote (1–10) und danach 4–8 KONKRETE, umsetzbare
Design-Verbesserungen (jede mit betroffenem Element + gewünschtem Zielzustand).
Kurz, priorisiert, keine Floskeln."""

def functional(page, body):
    issues, checks = [], []
    clicked = 0
    for sel in ["#pt button", "#mt button", ".user-toggle button", "button", "[role=tab]"]:
        for el in page.query_selector_all(sel):
            try:
                el.click(timeout=2000); clicked += 1; page.wait_for_timeout(150)
            except Exception:
                pass
    checks.append(f"{clicked} Steuerelemente geklickt")
    charts = len(page.query_selector_all("svg, canvas"))
    checks.append(f"{charts} Charts gerendert")
    if charts == 0:
        issues.append(("🔴", "Keine Charts gerendert"))
    for bad in ["NaN", "undefined", "null kcal"]:
        if bad in body:
            issues.append(("🟡", f"Verdächtiger Wert im DOM: '{bad}'"))
    dates = [prop(t, "Datum") for t in query_all(DS_TAGES) if prop(t, "Datum")]
    nd = max(dates) if dates else None
    if nd:
        de = datetime.date.fromisoformat(nd).strftime("%d.%m")
        if de not in body and nd not in body:
            issues.append(("🟡", f"Neuester Eintrag ({nd}) nicht im Dashboard sichtbar"))
    return issues, checks

def run():
    from playwright.sync_api import sync_playwright
    SHOTS.mkdir(parents=True, exist_ok=True)
    issues, checks, errs, shots = [], [], [], []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        # Desktop
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errs.append(str(e)))
        page.goto(DASHBOARD_URL, wait_until="networkidle", timeout=60000)
        body = page.content()
        i, c = functional(page, body); issues += i; checks += c
        p1 = SHOTS / "desktop.png"; page.screenshot(path=str(p1), full_page=True); shots.append(p1)
        # Mobil
        mob = browser.new_page(viewport={"width": 390, "height": 844})
        mob.goto(DASHBOARD_URL, wait_until="networkidle", timeout=60000)
        p2 = SHOTS / "mobile.png"; mob.screenshot(path=str(p2), full_page=True); shots.append(p2)
        browser.close()
    for e in errs[:10]:
        issues.append(("🔴", f"JS-Konsolenfehler: {e[:160]}"))
    return issues, checks, shots

def main():
    try:
        issues, checks, shots = run()
        design = claude_vision(DESIGN_SYSTEM,
            "Screenshot 1 = Desktop, Screenshot 2 = Mobil. Bewerte Design/UX und "
            "liste konkrete Verbesserungen für ein top, modernes Aussehen.",
            [str(s) for s in shots], max_tokens=1800)
    except Exception as e:
        issues, checks, shots, design = [("🔴", f"Test-Fehler: {e}")], [], [], "(keine Design-Bewertung)"
    crit = sum(1 for s, _ in issues if s == "🔴")
    lines = [f"# Dashboard-QA (Funktion + UX/Design) — {datetime.date.today().isoformat()}", "",
             f"**Funktion:** {crit} 🔴 · {len(issues)-crit} 🟡", "",
             "## Funktionale Checks"] + [f"- ✅ {c}" for c in checks]
    lines += ["", "## Funktionale Auffälligkeiten"] + ([f"- {s} {t}" for s, t in issues] or ["- 🟢 keine"])
    lines += ["", "## UX-/Design-Bewertung (Claude Vision)", "", design.strip()]
    lines += ["", "## Screenshots"] + [f"- `{s.relative_to(REPORTS.parent)}`" for s in shots]
    write_report("dashboard-qa", "\n".join(lines))
    print(f"Agent2: {crit} kritisch + Design-Bewertung erstellt")
    return crit

if __name__ == "__main__":
    main()
