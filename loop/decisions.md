
## 2026-07-13 — umgesetzt (✅ Build grün)
- **Total-vs-Analyse-Summen-Konsistenzprüfung im Build** — Über 40 Tage zeigen abweichende Tagessumme vs. Einzelposten-Summe (z.B. Denis 06-13: 2855≠1010); ein Abgleich mit Warn-Flag im Build deckt Erfassungsfehler früh auf und macht Kalorienwerte belastbar. (Aufwand: M; Dateien: build_dashboard.py)
- **Leni: fehlende Kern- und Zielgewicht-Daten erfassen/ableiten** — Viele Leni-Tage haben leere Kalorien-/Makro- und durchgehend leere Zielgewicht-Spalten sowie fehlende Analyse-Trennung; robustes Handling (Fallback/Kennzeichnung statt Absturz) plus Nacherfassung sichert die Abnehm-Auswertung für beide Nutzer. (Aufwand: M; Dateien: build_dashboard.py, Notion-Datenquelle)
