# Dashboard-QA (Funktion + UX/Design) — 2026-07-27

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# UX-Review: Nährstoff-/Kalorien-Dashboard

## Gesamtnote: **6,5 / 10**

Solide Grundstruktur, gute Datenvisualisierung (Balken-Ranking, Ampellogik). Aber: inkonsistente Hierarchie, ein gebrochenes Overlay-Element im Desktop-Screenshot, zu wenig Farbdisziplin und schwache Kontraste bei Metadaten. Wirkt „funktional-dashboardig“, noch nicht „premium“.

---

## Konkrete Verbesserungen (priorisiert)

**1. Toggle/Sticky-Bar-Overlap fixen (Desktop) — KRITISCH**
Betroffen: „KALORIEN/NÄHRSTOFFE“-Toggle + „Denis“-Dropdown liegen halbtransparent über der Nährstoffliste (Blur-Artefakt, Header „…gruppiert nach…“ wird abgeschnitten).
Ziel: Toggle als echte Sticky-Bar mit deckendem Hintergrund + eigenem `z-index`; Content darunter mit `padding-top`. Kein Durchscheinen der Liste.

**2. Farbpalette entsättigen & vereinheitlichen — HOCH**
Betroffen: Balken-Ranking, KPI-Zahlen (33/28/5/66), Ampel-Badges.
Ziel: Ein einziges Ampel-Token-Set (rot/gelb/grün) mit reduzierter Sättigung (z. B. `#E5484D / #E0B341 / #46A758`). Aktuell zu grell/gesättigt → wirkt „bootstrap-bunt“. Grün/Blau/Gelb als Akzentfarben strikt semantisch trennen.

**3. Typo-Hierarchie & Metadaten-Kontrast — HOCH**
Betroffen: Sublabels wie „3,35 / 20 µg“, „ZEITFENSTER“, Footer-Zeilen (Grau auf Dunkel).
Ziel: Werte in Monospace-Tabular-Figures für saubere Ausrichtung; Metadaten-Kontrast auf min. 4.5:1 anheben. Prozent-Spalte rechtsbündig mit fester Spaltenbreite ausrichten (aktuell leicht schwankend).

**4. Ampel-Karten (Health-Checkpoints) klarer strukturieren — MITTEL**
Betroffen: 4 Karten „Darmgesundheit / Low FODMAP / …“.
Ziel: Score-Badge (48/100) und Status („Kritisch“) visuell koppeln — Status als farbiges Pill statt loser roter Text. „14 gut · 33 neutral · 17 schlecht“ als Mini-Stacked-Bar statt Fließtext. Fußnote in einheitliche, gedämpfte Caption-Farbe.

**5. Whitespace & Karten-Rhythmus vereinheitlichen — MITTEL**
Betroffen: Abstand Header→Zeitfenster→Checkpoints→Gesamtdeckung (Desktop wirkt oben luftig, Liste unten gedrängt).
Ziel: Konsistentes 8px-Grid, gleiche vertikale Section-Gaps (z. B. 48px), einheitliche Card-Paddings (24px). Balkenzeilen mit min. 12px vertikalem Rhythmus.

**6. Balken-Ranking lesbarer machen — MITTEL**
Betroffen: 16-Zeilen-Nährstoffliste.
Ziel: 100%-Referenzlinie als vertikale gestrichelte Marke einzeichnen (Overachiever wie Selen 151% brauchen Kontext). Track-Hintergrund dezenter, Balken mit 4px Radius, Zebra-Grouping nach Ampelbereich.

**7. Mobile: KPI-Kacheln & Diagramm-Achsen — MITTEL**
Betroffen: 33/28/5/66-Kacheln + „Zielerreichung letzte 7 Tage“.
Ziel: Riesige Zahlen (28/33) etwas kleiner, Label größer → bessere Balance. Im 7-Tage-Chart Nulllinie + Achsenbeschriftung ergänzen; die dünnen grünen Balken (-48, -100) sind kaum sichtbar → Mindest-Balkenbreite/Textlabel-Farbe konsistent zur Richtung.

**8. Brand-Konsistenz Header — NIEDRIG**
Betroffen: „NÄHRSTOFFBRUDI“ vs. „KALORIENBRUDI“ (Kaps, Tracking) + „Dashboard Denis“ mit blauem Namen.
Ziel: Ein Logo-Lockup, konsistentes Letter-Spacing, Namensfarbe als definiertes Accent-Token statt Hardcode-Blau.

---

**Quick-Wins zuerst:** #1 (Overlap), #2 (Farbe), #3 (Kontrast) → heben den „Premium“-Eindruck sof

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`