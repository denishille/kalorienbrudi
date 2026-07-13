# Kalorienbrudi Agent-Loop — Setup & Betrieb

Täglicher, vollautomatischer Loop in GitHub Actions. Zustand versioniert im Repo.

## Dateien
```
loop/
  lib.py                 gemeinsame Helfer (Config, Notion, Anthropic)
  agent1_data_qa.py      Datenprüfer STRENG: jede Spalte befüllt, jedes
                         Lebensmittel getrennt, Summen/Datum/Duplikate/Namen
  agent2_dashboard_qa.py Dashboard-Tester: Funktion + UX/Design-Bewertung
                         (Screenshots Desktop+Mobil → Claude Vision)
  agent3_product.py      Produktkonzept (Claude) → Vorschläge mit Checkboxen
  agent4_implement.py    Umsetzung (Claude Code headless) → Code + Build
  run_loop.py            Orchestrator
  backlog.md / decisions.md / state.json
  proposals/YYYY-MM-DD.md   tägliche Vorschläge (Freigabe hier)
  reports/YYYY-MM-DD-*.md   QA-Reports
.github/workflows/agent-loop.yml   täglicher Cron
```

## Einrichtung (einmalig)
1. Ordner `loop/` und die Workflow-Datei ins Repo `denishille/kalorienbrudi` legen.
2. GitHub → Settings → Secrets and variables → Actions → **New repository secret**:
   - `NOTION_TOKEN` (bereits vorhanden für den Dashboard-Build)
   - `ANTHROPIC_API_KEY` (neu)
3. Settings → Actions → General → Workflow permissions → **Read and write** aktivieren.
4. Fertig. Der Loop läuft täglich 05:00 UTC oder manuell über „Run workflow".

## Täglicher Ablauf
1. Agent 1 prüft die Daten → `reports/<datum>-data-qa.md`
2. Agent 2 testet das Dashboard → `reports/<datum>-dashboard-qa.md`
3. Agent 4 setzt um, was du **seit gestern freigegeben** hast
4. Agent 3 legt **neue Vorschläge** ab → `proposals/<datum>.md`
5. Zustand wird zurück ins Repo committed

## Dein Freigabe-Gate
Öffne `loop/proposals/<datum>.md`, ändere bei gewünschten Punkten `- [ ]` in `- [x]`
und committe/pushe (geht auch direkt in der GitHub-Weboberfläche). Beim nächsten
Lauf setzt Agent 4 alle `[x]` um.

## Gewählte Defaults (jederzeit änderbar)
- **Frequenz:** täglich 05:00 UTC (`cron` in der Workflow-Datei anpassbar).
- **Agent 4 committet direkt auf `main`** (Feature vorher per Gate freigegeben; der
  Testbuild ist die Absicherung). Für PR-Review stattdessen einen Branch + `peter-evans/create-pull-request` einsetzen.
- **Agent 1 ist nur lesend** — er schlägt Daten-Fixes vor, ändert aber nichts selbst
  (bewusst konservativ, da Datums-/Duplikat-Themen heikel sind). Auto-Fix kann später
  gezielt für sichere Fälle (z. B. `Duplikat` bei exakten Dubletten) freigeschaltet werden.

## Lokal testen
```
pip install playwright && playwright install chromium
export NOTION_TOKEN=... ANTHROPIC_API_KEY=...
python loop/run_loop.py
```
