"""Agent 3 — Produktkonzept.
Liest die QA-Reports, das Backlog und die Entscheidungshistorie und erzeugt
2–4 konkrete Vorschläge als Markdown mit Freigabe-Checkboxen. Du hakst ab,
die freigegebenen Punkte übernimmt Agent 4 im nächsten Lauf.
"""
import datetime, pathlib
from lib import claude, PROPOSALS, REPORTS, BACKLOG, DECISIONS, TODAY

SYSTEM = """Du bist der Produktmanager für die Kalorien-Tracking-App 'Kalorienbrudi'
(Notion-Daten → build_dashboard.py → statisches HTML-Dashboard auf GitHub Pages;
zwei Nutzer Denis & Leni; Ziel Abnehmen). Du bekommst die heutigen QA-Reports,
das aktuelle Backlog und die Entscheidungshistorie.

Schlage 2–4 konkrete, umsetzbare Verbesserungen/Features vor. Für jeden Vorschlag:
Titel, 1–2 Sätze Nutzen, Aufwand (S/M/L), betroffene Dateien. Priorisiere Bugfixes
aus den QA-Reports vor neuen Features. Schlage nichts vor, was schon in decisions.md
abgelehnt oder im Backlog offen ist. Antworte NUR mit Markdown im vorgegebenen Format,
jede Zeile mit einer '- [ ] '-Checkbox beginnend."""

def read(p):
    p = pathlib.Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else "(leer)"

def main():
    data_qa = read(REPORTS / f"{TODAY}-data-qa.md")
    dash_qa = read(REPORTS / f"{TODAY}-dashboard-qa.md")
    user = f"""## Daten-QA\n{data_qa}\n\n## Dashboard-QA\n{dash_qa}\n\n## Backlog\n{read(BACKLOG)}\n\n## Entscheidungen (Historie)\n{read(DECISIONS)}\n
Erzeuge die heutigen Vorschläge. Format je Zeile:
- [ ] **Titel** — Nutzen (Aufwand: S/M/L; Dateien: ...)"""
    body = claude(SYSTEM, user, max_tokens=1500)
    PROPOSALS.mkdir(parents=True, exist_ok=True)
    out = PROPOSALS / f"{TODAY}.md"
    header = (f"# Vorschläge {TODAY}\n\n"
              "Hake ab, was umgesetzt werden soll (`[x]`), dann committen/pushen.\n"
              "Agent 4 setzt beim nächsten Lauf alle `[x]` um.\n\n")
    out.write_text(header + body.strip() + "\n", encoding="utf-8")
    print(f"Agent3: Vorschläge → {out}")

if __name__ == "__main__":
    main()
