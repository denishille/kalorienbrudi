# Dashboard-QA (Funktion + UX/Design) — 2026-08-19

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 6.5/10

Solide Datenvisualisierung mit gutem Dark-Theme-Ansatz und klarer Ampel-Logik. Aber: uneinheitliche Typo-Hierarchie, sticky Nav-Bug im Desktop-Screenshot, zu viel visuelles Rauschen bei den Balken und fehlender Whitespace bremsen den „premium“-Eindruck.

---

## Konkrete Verbesserungen (priorisiert)

**1. Sticky-Toolbar-Overlap fixen (Desktop) — KRITISCH**
Die „Kalorien/Nährstoffe“-Tab-Leiste + „Denis“-Selector überlappt den Nährstoff-Chart und verdeckt die erste Zeile (2,56/20 µg). → Toolbar mit korrektem `z-index` + `scroll-margin`/Padding-Offset, Chart-Content darunter mit Top-Padding = Toolbar-Höhe.

**2. Nährstoff-Balken: einheitliches Farbsystem statt 3-Stufen-Rot/Gelb/Grün-Chaos**
Aktuell wirken die vielen roten Balken alarmierend-monoton. → Definiere 3 klare Tokens (rot <50%, amber 50–99%, grün ≥100%) mit *einheitlicher* Sättigung, dezenter Track-Hintergrund (`#ffffff08`), Prozent-Label rechts vertikal zentriert und in gleicher Textfarbe wie Balken. Balkenhöhe reduzieren (aktuell zu klobig).

**3. Typografie-Hierarchie vereinheitlichen**
Überschriften mischen Letter-Spacing-Caps („NÄHRSTOFFBRUDI“), Bold + Blau-Accent inkonsistent. → Ein Type-Scale festlegen: Kicker (11px, uppercase, muted), H1 (28px), Card-Title (16px semibold). Blau-Akzent nur für *einen* Zweck (aktiver State), nicht gleichzeitig für „Denis“ + Werte + Buttons.

**4. Checkpoint-Cards: Status-Wort visuell an Ampel koppeln**
„Kritisch“ in Rot ist ok, aber Score-Badge (40/100), Punkt und Wort konkurrieren. → Score-Badge dezenter (outline statt fill), „Kritisch“ als kleiner Pill-Tag mit gedämpftem Hintergrund. „6 gut · 13 neutral · 12 schlecht“ als Mini-Segmented-Bar visualisieren statt reinem Text.

**5. Gesamtdeckungs-Ring: Kontext + Größe**
Der 55%-Ring steht isoliert mit viel leerer Fläche rechts. → Segmentierte Sub-Metriken daneben (z.B. Mini-Legende „5 kritisch / 6 mittel / 5 gut“) oder Card verkleinern. Ring-Track sichtbar machen (aktuell verschwindet er im BG).

**6. Mobile: Zahlen-Kacheln (39/39/8/86) — Einheit + Farbcodierung**
Riesige Zahlen ohne klaren Bezug wirken plakativ. → Farbe der Zahl an Bedeutung koppeln (grün=gut, rot=schlecht ist ok), aber Kontext-Label größer/lesbarer. „39 Tage“ statt nur „39“ zur Verständlichkeit.

**7. Whitespace & Card-Radien konsistent**
Desktop hat großzügige Cards, Mobile enger — Radien und Paddings variieren. → Globales Spacing-Token (16/24/32) und einheitlicher Border-Radius (12–16px). Card-Borders dezenter (`#ffffff0d`), Elevation über subtilen Gradient statt harter Kante.

**8. Datenqualitäts-Warnung als Action, nicht als Fußnote**
„24 Tage ohne Kalorien-Eintrag“ ist verstreut zwischen Werten. → Als eine klare Warn-Card oben mit CTA-Button „Einträge ergänzen“, damit Datenlücke handlungsleitend statt beiläufig ist.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`