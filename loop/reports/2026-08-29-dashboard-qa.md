# Dashboard-QA (Funktion + UX/Design) — 2026-08-29

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung

**Gesamtnote: 6.5 / 10**

Solide Datenvisualisierung mit klarem Dark-Theme und gutem Farb-Coding (rot/gelb/grün). Aber: inkonsistente Abstände, schwache Kontraste bei Meta-Text, uneinheitliche Card-Stile und ein gravierender Layout-Bug (überlappender Sticky-Bar). Das verhindert den „premium" Eindruck.

---

## Konkrete Verbesserungen (priorisiert)

**1. [KRITISCH] Sticky-Bar-Überlappung (Desktop)**
Der „Kalorien/Nährstoffe"-Toggle + Denis-Dropdown überlagert die Gesamtdeckungs-Card und schneidet den ersten Nährstoff-Balken ab. → Sticky-Bar mit solidem Hintergrund + Schatten versehen und ausreichend `scroll-padding-top` setzen, damit kein Content darunter verschwindet.

**2. [HOCH] Kontrast der Meta-/Label-Texte erhöhen**
Grau-auf-Schwarz-Beschriftungen (z. B. „27 gut · 26 neutral · 15 schlecht", „2,18 / 20 µg") liegen unter WCAG AA. → Sekundärtext von ~#6B7280 auf mind. #9CA3AF anheben, tertiäre Hinweiszeilen einheitlich 13px.

**3. [HOCH] Typografie-Konsistenz Zahlen**
Mix aus Monospace (Nährstoffwerte, Chart-Labels) und Proportional-Font wirkt uneinheitlich. → EINE tabellarische Ziffern-Variante (`font-variant-numeric: tabular-nums`) durchgängig für alle KPI-Zahlen und Balken-Werte verwenden.

**4. [MITTEL] Checkpoint-Cards vereinheitlichen**
Cards haben unterschiedliche Höhen/Beschreibungslängen → unruhige Baseline. → Feste Card-Höhe, Beschreibungszeile immer 2-zeilig reservieren, Score-Badge und Titel auf gemeinsame Grid-Baseline ausrichten.

**5. [MITTEL] Nährstoff-Balken lesbarer machen**
Prozentwerte rechts stehen zu weit isoliert, Balken haben keine Zielmarke. → Prozent-Label direkt an Balkenende oder in feste Spalte mit Trennlinie; 100%-Referenzlinie (gestrichelt) einzeichnen, damit Über-/Untererfüllung sofort erkennbar.

**6. [MITTEL] Whitespace/Rhythmus vereinheitlichen**
Vertikale Abstände zwischen Sektionen springen (großer Gap vor „Gesamtdeckung", enge Balkenliste). → 8pt-Spacing-System durchziehen, Sektionsabstand konstant (z. B. 48px), Card-Padding einheitlich 24px.

**7. [MITTEL] Mobile KPI-Kacheln (43/45/8/96) aufwerten**
Riesige Zahlen ohne Einheit-Bezug wirken beliebig; „8 Über Bedarf" in Rot ohne Kontext alarmierend. → Kleine Sparkline oder Icon je Kachel, Einheit/Sub-Label typografisch abstufen, gleiche Farb-Semantik wie Ampel oben.

**8. [NIEDRIG] Chart „Zielerreichung" aufräumen (Mobil)**
Divergierende Balken um Null-Achse ohne sichtbare Mittellinie, Warn-Icon (△) schlecht platziert. → Klare vertikale 0-Achse, +/- Werte konsistent außerhalb der Balken, Nulllinie hervorheben.

---
**Quick-Win:** Punkte 1–3 lösen ~70 % des „nicht-fertig"-Eindrucks.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`