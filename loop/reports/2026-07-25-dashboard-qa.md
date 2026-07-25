# Dashboard-QA (Funktion + UX/Design) — 2026-07-25

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Design/UX Review – Nährstoff-Dashboard

## Gesamtnote: **6.5 / 10**

Solide Basis mit gutem Farbcode-System (Ampel), klarer Datenfokus und ordentlicher mobiler Umsetzung. Es leidet aber an inkonsistenten Abständen, einem überladenen Nährstoff-Screen und einem gravierenden Layout-Bug (überlappender Toggle/Chart). Mit gezielten Fixes schnell auf 8+.

---

## Konkrete Verbesserungen (priorisiert)

**1. [KRITISCH] Overlap-Bug Desktop-Nährstoffliste**
Der Filter-Toggle (`KALORIEN / NÄHRSTOFFE`) und der User-Switch überlagern die Balkenliste + Chart-Header ist abgeschnitten (siehe verschwommener Text hinter Buttons).
→ Ziel: Toggle als sticky Sub-Header über der Liste, mit klarem Abstand (min. 32px) und eigenem Hintergrund-Layer, keine Überlappung mit Content.

**2. [HOCH] Whitespace „Gesamtdeckung"-Karte Desktop**
Der 56%-Donut und Text hängen links oben, rechts riesige leere Fläche.
→ Ziel: Content zentrieren oder rechts eine Mini-Legende/Sparkline platzieren; Kartenhöhe reduzieren.

**3. [HOCH] Checkpoint-Cards konsistent machen**
Die 3. Karte (Säure-Base) hat keinen sichtbaren Border/Hover-State wie Karte 2, Score-Badges unterschiedlich (`47/100` vs `345 mg`).
→ Ziel: Einheitliche Card-Borders, gleiches Badge-Format, Statuszeile („Kritisch/Okay") als farbiges Chip statt loser Text.

**4. [MITTEL] Balkenliste visuell entlasten (Desktop)**
16 Balken untereinander wirken monoton; Prozentzahlen rechts weit entfernt vom Balkenende.
→ Ziel: Prozentwert direkt ans Balkenende oder in den Balken; subtile Zebra-Trennung oder Gruppierung (Vitamine / Mineralstoffe); Zielmarke bei 100% als vertikale Linie einzeichnen.

**5. [MITTEL] Typografie-Hierarchie schärfen**
Label wie „ZEITFENSTER", „NÄHRSTOFFBRUDI" konkurrieren mit echten Headlines; Werte (`2,99 / 20 µg`) sind sehr klein/grau.
→ Ziel: Eyebrow-Labels kleiner + gedämpfter, Einheiten-Werte auf min. 13px mit besserem Kontrast (WCAG AA).

**6. [MITTEL] Kontrast Sekundärtext erhöhen**
Graue Beschreibungstexte („Ballaststoffe, Fermentiertes…", Footer) liegen unter dem Kontrastminimum auf dunklem BG.
→ Ziel: Textfarbe auf mind. #A0A0A8 anheben, Footer als eigener Divider abgesetzt.

**7. [MITTEL] Mobile Stat-Cards vereinheitlichen (31/28/4/63)**
Zahlen top, aber die Einheiten-/Prozentzeilen sind unterschiedlich lang und brechen unruhig.
→ Ziel: Feste Card-Höhe, konsistentes 3-Zeilen-Raster (Zahl / Label / Sub), farbiger Punkt links bündig.

**8. [NIEDRIG] Chart-Politur „Zielerreichung"**
Die horizontalen Bars mit +/- Werten sind schwer als Abweichung um Nulllinie lesbar.
→ Ziel: Klare vertikale Nulllinie, positive Werte rechts / negative links spiegeln, einheitliche Bar-Höhe.

---

**Quick Wins:** Bug (#1) + Whitespace (#2) + Kontrast (#6) → sofort spürbar „professioneller".

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`