# Dashboard-QA (Funktion + UX/Design) — 2026-08-10

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Design/UX Review – Nährstoff-/Kalorien-Dashboard

## Gesamtnote: **6.5 / 10**

Solide Datenvisualisierung mit gutem Dark-Theme-Ansatz, aber inkonsistente Typo-Hierarchie, verschenkter Whitespace, ungleiche Card-Höhen und ein kaputter Tab-/Sticky-Übergang (Desktop) verhindern den „Top“-Eindruck.

---

## Konkrete Verbesserungen (priorisiert)

**1. Sticky-Tab-Bar Überlappung fixen (Desktop, kritisch)**
Element: „Kalorien/Nährstoffe“-Toggle + „Denis“-Dropdown, das mitten über der Gesamtdeckungs-Card klebt.
Ziel: Bar als saubere Sticky-Leiste mit eigenem Hintergrund + Schatten oben fixieren; darunterliegender Content erhält Padding-Top, keine visuelle Überlappung/abgeschnittene Zeile („2,2 / 20 µg“).

**2. Card-Höhen der 4 Checkpoints angleichen**
Element: Darmgesundheit / Low FODMAP / Säure-Base / Cholesterin.
Ziel: Einheitliche Mindesthöhe, vertikal ausgerichtete Baseline-Grid für Titel, Score-Badge, „Okay/Gut“-Label und Fußnote. Aktuell springen Zeilenumbrüche (28 gut · 40 neutral · 13) und erzeugen Ungleichheit.

**3. Balkenliste (Nährstoffe) lesbarer strukturieren**
Element: Mikronährstoff-Balken mit %-Werten rechts.
Ziel: Zebra-Striping oder feine Divider zwischen Zeilen; Ist/Ziel-Werte (z.B. „59,7 / 110 mg“) tabellarisch rechtsbündig ausrichten; Ziel-100%-Linie als vertikale Referenzlinie einzeichnen, damit Über-/Unterdeckung sofort erkennbar.

**4. Farbcodierung vereinheitlichen & Kontrast erhöhen**
Element: Gelb-Töne (Amber) in Balken, Scores und Donut.
Ziel: Ein konsistentes 3-Stufen-Ampelsystem (rot/amber/grün) mit exakt gleichen Hex-Werten in Donut, Badges, Balken und Stat-Cards. Aktuelles Gelb auf dunklem BG ist grenzwertig – auf WCAG AA (≥4.5:1) anheben.

**5. Typo-Hierarchie schärfen**
Element: Überschriften „Dashboard Denis“, Section-Titel, Labels.
Ziel: Klares Type-Scale (z.B. 32/24/18/14/12) mit definierten Weights. Monospace-Zahlen (2,2 / 20 µg) nur für Datenwerte konsistent, nicht mischen. Labels wie „ZEITFENSTER“ / „AKTUELLES ZIEL“ mit einheitlichem Letterspacing.

**6. Whitespace & Sektions-Rhythmus (Desktop)**
Element: Großer Leerraum oben + zwischen Header und Content.
Ziel: Content-Max-Width beibehalten, aber Top-Padding reduzieren; gleichmäßige vertikale Sektionsabstände (z.B. 48px) statt großer Sprünge.

**7. Donut „Gesamtdeckung“ aufwerten**
Element: 75%-Ring-Chart.
Ziel: Zentrierte Prozentzahl mit Sub-Label („Ø Deckung“) im Ring; Ring-Farbe an Score koppeln; rechts danebenstehenden Text vertikal mittig zum Ring ausrichten.

**8. Mobile Stat-Cards (72/6/0/78) veredeln**
Element: 2×2 Grid der KPI-Kacheln.
Ziel: Einheitliche Icon-Position, Zahl-Baseline und Sub-Text-Zeilen; farbige Akzentleiste oder dezenter farbiger Rand pro Status statt nur farbiger Punkt – erhöht Scanbarkeit deutlich.

---

**Quick Wins:** Sticky-Bar-Fix (#1) + Card-Höhen (#2) + Referenzlinie in Balken (#3) heben die App bereits sichtbar Richtung 8/10.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`