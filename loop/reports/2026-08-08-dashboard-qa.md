# Dashboard-QA (Funktion + UX/Design) — 2026-08-08

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Gesamtnote: 6.5 / 10

Solide Datenvisualisierung mit gutem Ampel-System, aber inkonsistente Abstände, schwache visuelle Hierarchie bei den Karten und Kontrastprobleme trüben den modernen Eindruck.

---

## Konkrete Verbesserungen (priorisiert)

**1. Sticky-Toolbar-Überlappung (Desktop, kritisch)**
Betroffen: `KALORIEN / NÄHRSTOFFE`-Tab-Leiste überlagert die Nährstoff-Liste (obere Zeile abgeschnitten, „2,35 / 20 µg"-Balken halb verdeckt).
Ziel: Toolbar als echtes Sticky-Element mit `padding-top` im Content-Bereich, damit kein Balken je verdeckt wird. Höchste Priorität – aktuell Datenverlust.

**2. Kontrast Sekundärtext**
Betroffen: Graue Unter-Labels („28 gut · 43 neutral · 13 schlecht", Achsenbeschriftungen, Footer).
Ziel: Text von ~#6b6b6b auf min. #9aa0a6 anheben (WCAG AA, ≥4.5:1). Footer nicht kleiner als 12px.

**3. Visuelle Hierarchie der Checkpoint-Karten**
Betroffen: 4 Karten „Gesundheits-Checkpoints" – Status-Wort („Okay/Kritisch") konkurriert mit Score-Badge, wirkt flach.
Ziel: Score-Badge als dominantes Element (größer, farbcodierter Rand), Status-Wort kleiner darunter. Karten gleiche Höhe erzwingen (aktuell brechen Texte unterschiedlich um → ungleiche Baseline).

**4. Balkendiagramm-Skala vereinheitlichen (Desktop)**
Betroffen: Nährstoff-Balken – 100%-Marke ist nicht visuell markiert, Werte >100% (168%) und <100% teilen dieselbe Trackbreite ohne Referenzlinie.
Ziel: Vertikale 100%-Ziellinie einziehen, Prozent rechtsbündig in fester Spalte. Rot→Gelb→Grün-Verlauf durch klare Schwellen (Kategoriewechsel sichtbar), nicht kontinuierlicher Gradient.

**5. Typografie / Zahlenformat**
Betroffen: Werte wie „2.437 / 4.000 mg", „0,62 / 1,6 g" in Monospace-artiger, sehr kleiner Schrift.
Ziel: Tabellen-Zahlen mit `font-variant-numeric: tabular-nums`, konsistente Ausrichtung, IST-Wert fett / SOLL-Wert gedimmt. Einheiten kleiner & gedimmt.

**6. Abstände & Whitespace (Desktop)**
Betroffen: Riesige Leerräume oben (Header→Toolbar) und um Donut-Chart „69% Gesamtdeckung", während Karten gedrängt wirken.
Ziel: Einheitliches 8px-Spacing-Grid. Donut-Sektion kompakter, gewonnene Fläche für Chart-Breite nutzen.

**7. Mobile: Datenqualitäts-Hinweis stört Flow**
Betroffen: Gelbe „27 Tag(e) ohne Kalorien-Eintrag"-Box mitten in Kern-KPIs.
Ziel: Als dezente Info-Zeile unter den Zielwerten oder einklappbar. Nicht als Warn-farbige Box, die mit echten Status-Ampeln konkurriert.

**8. KPI-Kacheln modernisieren (Mobile)**
Betroffen: „71 / 6 / 0 / 77"-Kacheln – große Zahl, aber flacher Hintergrund, kein Icon-Anker.
Ziel: Dezenter farbiger Akzent-Rand/Glow passend zum Status (grün/gelb/rot/blau), Icon links oben, mehr `border-radius`-Konsistenz mit anderen Karten.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`