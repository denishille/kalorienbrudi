# Dashboard-QA (Funktion + UX/Design) — 2026-08-04

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 6.5/10

Solide Datengrundlage und funktionierendes dunkles Theme, aber inkonsistente Abstände, ein schwebendes Menü ohne Bezug und ein grob wirkendes Balkendiagramm ziehen das Niveau runter. Mit gezielten Fixes schnell auf 8+.

---

## Konkrete Verbesserungen (priorisiert)

**1. Schwebendes Tab/User-Menü fixen (Desktop, kritisch)**
Element: „KALORIEN / NÄHRSTOFFE / Denis"-Leiste über der Nährstoffliste.
Zielzustand: Als klar abgesetzte Sub-Nav mit eigenem Hintergrund, Rahmen und definiertem Abstand oben/unten platzieren. Aktuell überlappt/schwebt sie ohne visuelle Verankerung und wirkt wie ein Render-Fehler. Sticky-Header mit Blur-Backdrop.

**2. Nährstoff-Balkenliste als Chart lesbarer machen (Desktop)**
Element: Vitamin-D-bis-B12-Balken.
Zielzustand: 100%-Referenzlinie/Marker einzeichnen (Werte >100% sind sonst nicht ablesbar), Track-Hintergrund heller kontrastieren, Prozent-Label rechtsbündig in einer festen Spalte ausrichten. Farbverlauf pro Balken entfernen → flache Semantik-Farbe (rot/gelb/grün) für schnelleren Scan.

**3. Karten-Höhen & Textumbrüche vereinheitlichen (Checkpoints)**
Element: 4 Gesundheits-Checkpoint-Karten.
Zielzustand: Gleiche Kartenhöhe, „26 gut · 34 neutral · 11 schlecht" nicht umbrechen lassen (feste Baseline). Aktuell springen die Zeilen unterschiedlich → optisch unruhig. Fußnoten-Text auf einheitliche Y-Position setzen.

**4. Typo-Hierarchie schärfen**
Element: Section-Header („Gesundheits-Checkpoints", „Gesamtdeckung") vs. Body.
Zielzustand: Klarere Größenstufen (H2 > Label > Body), Sekundärtext auf einheitliches Grau (#8A8A8A). Die tabellarischen Nährwerte in Monospace-Ziffern (tabular-nums) für saubere Ausrichtung von „3,11 / 20 µg".

**5. Farbsystem für Prozent/Ampel konsolidieren**
Element: Prozent-Badges, Status-Farben, Chart-Farben.
Zielzustand: Ein definiertes Set (z.B. rot <40, gelb 40–75, grün >75) app-weit identisch. Cholesterin-Badge (grau/grün) und Score-Badges (gelb/rot) folgen aktuell unterschiedlicher Logik – vereinheitlichen.

**6. Mobiles Balkendiagramm „Zielerreichung" verfeinern**
Element: 7-Tage-Diverging-Bars mit Werten.
Zielzustand: Zentrierte Nulllinie sichtbar machen, Werte-Labels konsistent außen platzieren, Bar-Höhe reduzieren + mehr Whitespace. Wirkt derzeit gedrängt und klobig.

**7. Weekly-Chart-Referenzlinie & Achsen (Mobil)**
Element: Wochendurchschnitt-Balken mit „Ziel 1900".
Zielzustand: Y-Achse mit 2–3 Gridlines, Ziel-Linie durchgehend über alle Balken, Werte-Labels kleiner. Balken schmaler mit abgerundeten Ecken für modernen Look.

**8. Whitespace & Grid-Rhythmus (Desktop)**
Element: Abstände zwischen Sektionen.
Zielzustand: Einheitliches 8px-Spacing-System, größerer, konsistenter Vertikalabstand zwischen Blöcken. Der große leere „Gesamtdeckung"-Bereich rechts vom Donut sinnvoll füllen (z.B. Mini-Legende der 16 Nährstoffe) oder Karte kompakter.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`