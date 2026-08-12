# Dashboard-QA (Funktion + UX/Design) — 2026-08-12

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Gesamtnote: 7/10

Solide, moderne Basis mit klarer Farbcodierung und gutem Dark-Theme. Es fehlt an Feinschliff bei Ausrichtung, Hierarchie und Whitespace-Rhythmus. Der überlappende Tab-Balken im Desktop-Screenshot ist ein echter Bug.

---

## Konkrete Verbesserungen (priorisiert)

**1. [KRITISCH] Sticky Tab-Leiste überlappt Nährstoff-Liste (Desktop)**
Der Balken „KALORIEN/NÄHRSTOFFE + Denis“ liegt halbtransparent über der ersten Tabellenzeile (11%-Wert abgeschnitten). → Sticky-Bar mit vollflächigem Hintergrund + `padding-top` auf dem Content, sodass keine Zeile verdeckt wird. Alternativ Tabs oben fix, Liste darunter mit Offset.

**2. Zahlen-Werte optisch ausrichten (Nährstoff-Liste)**
Prozentwerte rechts sind unterschiedlich weit von der Kante, Sub-Werte („54,3 / 110 mg“) monospace aber unausgerichtet. → Prozente rechtsbündig auf feste Spaltenbreite, tabellarische Ziffern (`font-variant-numeric: tabular-nums`), Balken alle exakt gleiche Startkante.

**3. Checkpoint-Karten: Sekundärtext lesbarer machen**
Die grauen Zeilen („Ballaststoffe, Fermentiertes…“ / „basisch = gut“) haben zu niedrigen Kontrast (~2:1). → Auf mind. WCAG AA (4.5:1) anheben, Trennlinie zur Kartenmitte konsistent auf allen 4 Karten (aktuell fehlt sie bei Karte 3+4 optisch).

**4. Score-Badges vereinheitlichen**
„57/100“, „61/100“ (dezent) vs. „32/100“ rot (auffällig) vs. „292 mg“ – uneinheitliches Padding und Farbgewichtung. → Einheitliche Pill-Komponente, Farbe nur über Textfarbe/ Akzent-Border, gleiche Höhe/Radius. Cholesterin-Einheit als Score-Format angleichen oder klar als Messwert kennzeichnen.

**5. Gesamtdeckungs-Sektion wirkt leer**
73%-Donut + zwei Textzeilen füllen eine riesige Card nur links. → Rechts kompakte Mini-Legende (grün/gelb/rot Verteilung der 16 Nährstoffe) oder Sparkline ergänzen; sonst Card-Höhe reduzieren.

**6. Mobile: Wochendurchschnitt-Chart Achse fixen**
Y-Werte fehlen, „Ziel 2900“-Linie kollidiert mit „2.897“-Label, Balken ohne Baseline-Grid. → Gestrichelte Ziel-Linie hinter Balken legen, Label rechts an Achse ankern, dezentes Y-Grid (2000/2500/3000) für Kontext.

**7. Mobile: Diverging-Bars der Zielerreichung**
Werte wie „108“ und „+40“ überlappen teils die Nulllinie/Balken, Farb-Logik (grün=Defizit, gold=Überschuss) ist ohne Legende unklar. → Werte immer außerhalb des Balkens, klare 0-Achse, Mini-Legende „Defizit / Überschuss“ ergänzen.

**8. Typo-Hierarchie & Spacing-Rhythmus**
Header „Dashboard Denis“ stark, danach flache Hierarchie; Sektionsabstände uneinheitlich (großer Gap vor Deckung, enger bei Checkpoints). → 8pt-Grid durchziehen, Sektions-Header einheitlich (Overline + Titel), konsistente vertikale Rhythmik (z. B. 32/48px).

---

**Quick Wins:** #1 (Bug), #2 (Ausrichtung), #4 (Badges) – höchster Impact bei geringem Aufwand.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`