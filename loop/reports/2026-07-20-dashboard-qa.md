# Dashboard-QA (Funktion + UX/Design) — 2026-07-20

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 3 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 6,5 / 10

Solide Datenvisualisierung mit klarem Konzept, aber inkonsistente Abstände, überladene Cards und unruhige Farbführung verhindern den „Premium“-Eindruck. Die Nährstoff-Balkenliste ist stark, der Rest wirkt zusammengesetzt statt aus einem Guss.

---

## Konkrete Verbesserungen (priorisiert)

**1. Sticky-Header-Überlappung fixen (Desktop, kritisch)**
Der `KALORIEN / NÄHRSTOFFE`-Tab-Balken schneidet die „Gesamtdeckung“-Card ab (Donut wird verdeckt). → Sticky-Bar mit korrektem `padding-top`/`scroll-margin` versehen, sodass darunterliegende Cards vollständig sichtbar bleiben. Klarer visueller Abstand (min. 24px) zwischen Bar und Content.

**2. Farbchaos reduzieren (global)**
Pink (Leni), Blau (Denis), Rot/Gelb/Grün (Ampel) + gelber Donut konkurrieren. → Ampelfarben nur für Status/Balken, ein neutrales Akzentsystem pro Nutzer. Donut „Gesamtdeckung“ soll die reale Wertfarbe tragen (63% = gelb ist ok), aber Titel/Zahlen in Weiß statt weiterer Farbe.

**3. Checkpoint-Cards vereinheitlichen (Desktop)**
Score-Pill, Statuswort in Farbe, 3 Textzeilen → dicht und ungleich lang. → Feste Card-Höhe, konsistente vertikale Rhythmik (Titel → Score → Statuswort → Metrik-Zeile → Hinweis). Statuswort kleiner (aktuell zu dominant ggü. Titel), Score-Pill als Hauptindikator.

**4. Typo-Hierarchie schärfen (global)**
Zu viele Gewichte/Größen ähnlich stark. → Klare Skala: H1 32px, Section-Titel 20px semibold, Card-Titel 15px medium, Meta 12px muted (#8A8A8A). Letterspaced-Uppercase-Labels („ZEITFENSTER“, „AKTUELLES ZIEL“) auf 11px + einheitliches Grau.

**5. Nährstoff-Balken: Zielmarke ergänzen (Desktop)**
Balken zeigen %, aber 100%-Linie fehlt visuell. → Vertikale 100%-Referenzlinie im Track einzeichnen; Werte >100% dürfen sichtbar überstehen. Rechtsbündige %-Zahl in gleicher Farbe wie Balken beibehalten – gut.

**6. Card-Radius & Border vereinheitlichen (global)**
Mix aus scharfen Score-Pills, runden Toggles, verschiedenen Card-Radii. → Ein Radius-System: Cards 16px, Pills/Buttons 10px, Toggles voll rund. Border einheitlich 1px `rgba(255,255,255,0.06)`.

**7. Mobil: Stat-Cards & KPI-Zahlen (Mobil)**
Die 4 KPI-Cards (28/26/4/58) haben farbige Oberkante + Riesenzahl – wirken plakativ. → Zahl 40px, Label darunter konsistent, farbige Kante durch dezenten farbigen Icon-Dot ersetzen. Einheitliches Grid-Gap (16px).

**8. Balkendiagramm „Kaloriendifferenz“ lesbarer (Mobil)**
Mini-Balken um Nulllinie sind zu klein/unklar. → Nulllinie klar markieren, Balken höher, +/− farbcodiert (rot/grün) mit Wert direkt am Balkenende statt separater Spalte.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`