
## 2026-07-13 — umgesetzt (✅ Build grün)
- **Total-vs-Analyse-Summen-Konsistenzprüfung im Build** — Über 40 Tage zeigen abweichende Tagessumme vs. Einzelposten-Summe (z.B. Denis 06-13: 2855≠1010); ein Abgleich mit Warn-Flag im Build deckt Erfassungsfehler früh auf und macht Kalorienwerte belastbar. (Aufwand: M; Dateien: build_dashboard.py)
- **Leni: fehlende Kern- und Zielgewicht-Daten erfassen/ableiten** — Viele Leni-Tage haben leere Kalorien-/Makro- und durchgehend leere Zielgewicht-Spalten sowie fehlende Analyse-Trennung; robustes Handling (Fallback/Kennzeichnung statt Absturz) plus Nacherfassung sichert die Abnehm-Auswertung für beide Nutzer. (Aufwand: M; Dateien: build_dashboard.py, Notion-Datenquelle)

## 2026-07-14 — umgesetzt (✅ Build grün)
- **Chart-Rendering-Bug beheben (0 Charts gerendert)** — Der Funktions-QA meldet 🔴 „Keine Charts gerendert"; ohne Charts ist das Dashboard funktionslos, daher höchste Prio für die Kernauswertung beider Nutzer. (Aufwand: M; Dateien: build_dashboard.py)
- **Wochentag-Konsistenzprüfung im Build** — Leni 2026-05-21 hat 'Mittwoch, 21.05.26' ≠ tatsächlich Donnerstag; ein Datum-vs-Wochentag-Abgleich mit Warn-Flag deckt Erfassungsfehler auf und verhindert falsche Zeitachsen. (Aufwand: S; Dateien: build_dashboard.py)
- **Empty-State neu gestalten mit CTA statt toter Leerfläche** — Aktuell 70% leerer Screen wirkt kaputt; zentrierte Card mit Icon + Button „Ersten Eintrag hinzufügen" macht den Zustand einladend und nutzbar. (Aufwand: M; Dateien: build_dashboard.py)
- **Typografie & Copy bereinigen (Sans statt Monospace, Umlaute/Grammatik)** — Monospace-Fließtext und Fehler wie „Im letzte 7 Tage", „ueber", „gruenen" wirken unfertig; einheitliche Sans-Schrift und korrekte Umlaute steigern Vertrauen und Lesbarkeit. (Aufwand: S; Dateien: build_dashboard.py)
