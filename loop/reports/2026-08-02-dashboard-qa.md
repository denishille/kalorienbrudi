# Dashboard-QA (Funktion + UX/Design) — 2026-08-02

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Design/UX-Review – Nährstoff/Kalorien-Dashboard

## Gesamtnote: **6,5 / 10**

Solide, funktionale Basis mit gutem Ampel-Farbsystem und ordentlicher Datendichte. Aber: schwacher Tab-Wechsel-Zustand, inkonsistente Abstände, überladenes Desktop-Layout und ein kaputt wirkender Übergang (Screenshot 1 zeigt den Tab-Header mitten über der Chart-Liste). Das kostet den „premium“ Eindruck.

---

## Konkrete Verbesserungen (priorisiert)

**1. Tab-/Sticky-Header-Bug beheben (Desktop) – KRITISCH**
Element: „Kalorien / Nährstoffe“-Toggle + „Denis“-Dropdown.
Zielzustand: Der Toggle darf nicht als milchiger Overlay-Balken die Chart-Liste überlappen (aktuell verdeckt er die Spaltenüberschrift „µg / %“). Als klar abgesetzten Sticky-Header mit voller Hintergrundfarbe (kein Blur-Fragment) und definiertem oberen Abstand zur Liste fixieren.

**2. Chart-Liste braucht Achsen-Kontext & Ziel-Marker**
Element: Nährstoff-Balken (Vitamin D … B12).
Zielzustand: Vertikale 100 %-Referenzlinie einziehen, damit „unter/über Bedarf“ sofort lesbar ist. Header-Zeile fixieren („Nährstoff · Ist / Ziel · %“). %-Werte rechtsbündig auf gleicher X-Achse ausrichten (aktuell optisch leicht schwankend).

**3. Card-Werte-Badges konsistent machen**
Element: Checkpoint-Cards (59/100, 66/100, 27/100, 247 mg).
Zielzustand: Einheitliches Badge-Format – „247 mg“ bricht das 100er-Skalensystem. Entweder alle als Score anzeigen oder Cholesterin visuell klar als eigenen Typ (z. B. andere Badge-Form). Statustext („Okay/Kritisch/Gut“) einheitlich positionieren und in gleicher Größe.

**4. Visuelle Hierarchie oben verdichten**
Element: Header „Dashboard Denis“ + Zeitfenster-Card.
Zielzustand: Zu viel Leerraum über dem Titel (Desktop). Titel enger an Nav rücken, Zeitfenster-Toggle als Segmented Control mit sichtbarem aktivem State (aktuell fast randlos). Gesamt-Whitespace oben um ~40 % reduzieren.

**5. Donut „62 %“ integrieren statt isoliert**
Element: Gesamtdeckung-Ring.
Zielzustand: Ring wirkt verloren in großer leerer Card. Card-Höhe reduzieren, Ring + Text vertikal zentrieren, Mini-Legende (dicht/offen) ergänzen. Farbe des Rings (Gelb) sollte den Score-Zustand widerspiegeln (62 % = mittel, ok).

**6. Typografie-Skala & Zahlen-Alignment (Mobil)**
Element: Kennzahl-Cards (36 / 31 / 5 / 72).
Zielzustand: Große Zahlen sind gut, aber Label-Zeilen unterschiedlich lang → Baseline vereinheitlichen. Tabellarische Ziffern (`font-variant-numeric: tabular-nums`) für alle kcal-/%-Werte, damit Werte nicht „springen“.

**7. Waterfall-Chart lesbarer machen (Mobil)**
Element: „Zielerreichung – letzte 7 Tage“.
Zielzustand: Balken sind sehr dünn und Werte (+525, -310) uneinheitlich platziert (mal innen, mal außen). Einheitliche Label-Position, Nulllinie klar markieren, Balkenhöhe erhöhen für Touch-Lesbarkeit.

**8. Farbkontrast der Sekundärtexte**
Element: Meta-Zeilen (grau auf schwarz, „weniger ist besser · Ziel …“, Footer).
Zielzustand: Grauton ist zu dunkel (unter WCAG AA). Auf mind. #A0A0A0 anheben. Footer zentriert + mehr Abstand zur letzten Card.

---

**Quick Wins:** Punkte 1, 3, 8 → sofort größter Qualitätssprung.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`