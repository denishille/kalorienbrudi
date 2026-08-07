# Dashboard-QA (Funktion + UX/Design) — 2026-08-07

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 6.5 / 10

Solide, datenreich, konsistente Farbcodierung. Aber: unruhige Hierarchie, monospace-Zahlen wirken technisch statt premium, sticky-Tab-Leiste überlappt den Chart (Screenshot 1), und Whitespace/Rhythmus sind ungleichmäßig. Nah an „gut“, aber nicht „top“.

---

## Konkrete Verbesserungen (priorisiert)

**1. Sticky Tab-Leiste überlappt Chart (Desktop) — KRITISCH**
Betroffen: „Kalorien/Nährstoffe“-Bar + „Denis“-Dropdown auf Screenshot 1.
Ziel: Bar korrekt als sticky Header oben andocken, nicht mitten über der Nährstoffliste schweben. Erste Chart-Zeile (2,44/20 µg) wird abgeschnitten → oberen Padding-Offset gleich Header-Höhe setzen.

**2. Typografie: Monospace-Zahlen ersetzen**
Betroffen: alle Werte (`22 gut · 38 neutral`, `2,44 / 20 µg`, Prozente).
Ziel: Tabular-Figures einer modernen Sans (Inter, Söhne) statt Courier-artiger Mono. Behält Ausrichtung, wirkt sofort wertiger und weniger „Terminal“.

**3. Balken-Chart: Zielmarke + einheitliche Track-Höhe**
Betroffen: Nährstoff-Balkenliste.
Ziel: Vertikale 100%-Referenzlinie einziehen, damit „105% vs 60%“ visuell ablesbar ist. Balken dünner/gleichmäßiger, mehr vertikaler Abstand zwischen Zeilen (aktuell zu gedrängt).

**4. Checkpoint-Karten: konsistente Höhe & Metrik-Format**
Betroffen: 4 Karten oben (Darmgesundheit … Cholesterin).
Ziel: Cholesterin zeigt `280 mg` statt `x/100` → Bruch in der Zeile. Entweder alle auf Score normalisieren oder einheitliches Badge-Layout mit gleicher vertikaler Achse. Karten auf identische Höhe (Text „schlecht“ bricht unterschiedlich um).

**5. Farb-/Kontrast: Amber-Text auf Dunkel**
Betroffen: „Okay“ (gelb), gelbe Balkenbeschriftung, Datenqualitäts-Box.
Ziel: Gelb-Töne aufhellen/entsättigen für WCAG-AA-Kontrast; „Kritisch“ (rot) ist ok. Prozentzahlen rechts erben Balkenfarbe – bei Rot/Gelb schwer lesbar.

**6. Diverging-Chart Mobil (Zielerreichung): Achsenlinie fixieren**
Betroffen: „-408 / +400“ Balken.
Ziel: Klare zentrierte Null-Achse mit dünner Linie, Labels außerhalb der Balken einheitlich positionieren (aktuell mal innen mal außen). Grün=Defizit/gut, Gelb=Über — kurze Legende ergänzen.

**7. Header-Hierarchie & Whitespace**
Betroffen: „Dashboard Denis“ + Eyebrow-Labels (NÄHRSTOFFBRUDI/KALORIENBRUDI).
Ziel: Eyebrow kleiner + mehr Letter-Spacing-Konsistenz; einheitliche Section-Abstände (32/48px Grid). Aktuell springen die Vertikalabstände (Checkpoints → Donut → Liste).

**8. Donut-Ring „69%“ modernisieren**
Betroffen: Gesamtdeckungs-Ring.
Ziel: Ring dünner, Farbverlauf entlang Fortschritt (rot→gelb→grün) statt Vollgelb, damit Score-Semantik konsistent zur restlichen Ampel ist.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`