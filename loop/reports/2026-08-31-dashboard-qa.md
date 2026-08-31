# Dashboard-QA (Funktion + UX/Design) — 2026-08-31

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 6,5 / 10

Solide Datenvisualisierung mit gutem Dark-Theme-Ansatz und klarer Farbcodierung (Ampel-Logik funktioniert). Aber: schwacher visueller Rhythmus, inkonsistente Abstände, ein kritischer Layout-Bug und zu geringer Kontrast bei Fließtext. Wirkt „funktional“, nicht „premium“.

---

## Konkrete Verbesserungen (priorisiert)

**1. KRITISCH – Sticky-Toolbar überdeckt Chart (Desktop)**
Element: „Kalorien/Nährstoffe“-Toggle + Denis-Dropdown im Balkendiagramm.
Ziel: Toolbar mit definiertem Hintergrund (solid + Blur, `backdrop-filter`) und `z-index` versehen; darunter `scroll-padding-top` setzen, damit die erste Zeile (Selen/Vitamin D) nicht abgeschnitten wird.

**2. Textkontrast der Sekundärtexte anheben**
Element: Card-Untertexte („Ballaststoffe, Fermentiertes…“, Zahlenwerte „2,18 / 20 µg“, Footer).
Ziel: von aktuell ~#6b6b6b auf min. #9aa0a8 (WCAG AA, 4.5:1). Micro-Werte auf #808690, Labels auf #c4c9d0.

**3. Konsistentes Spacing-System einführen**
Element: Vertikale Abstände zwischen Sektionen (Checkpoints → Gesamtdeckung → Chart) sind unregelmäßig; Card-Innenabstände variieren.
Ziel: 8px-Grid strikt anwenden — Sektionsabstand 48px, Card-Padding 24px, Zeilen-Gap in Listen 16px. Alle Zahlen-Badges gleich hoch (28px).

**4. Balkendiagramm-Zeilen: Ausrichtung & Rhythmus**
Element: Nährstoff-Liste (Desktop).
Ziel: Label-Spalte auf feste Breite (z.B. 160px), Prozentwert rechtsbündig in eigener Spalte, Balken beginnen exakt gleich. Zeilenhöhe konstant 56px mit dezenten Divider-Linien (1px, #ffffff08) statt reinem Whitespace.

**5. Farbverlauf auf Balken reduzieren**
Element: Gradient-Balken (rot→gelb→grün innerhalb eines Balkens).
Ziel: Pro Balken EINE Statusfarbe (basierend auf %-Schwelle). Gradients innerhalb eines Balkens wirken willkürlich und verschlechtern Ablesbarkeit. Optional: Ziel-Marker (100%) als vertikale Linie.

**6. Mobil – KPI-Cards vereinheitlichen**
Element: „44 / 46 / 8 / 98“-Kacheln.
Ziel: Gleiche Höhe, konsistente Zahlengröße, Icon+Label+Sublabel exakt gleich positioniert. Aktuell driften die Baselines. Große Zahl 40px/700, Label 13px/500.

**7. Typo-Hierarchie & Header schärfen**
Element: „Dashboard Denis“, Eyebrow-Labels („NÄHRSTOFFBRUDI“).
Ziel: Eyebrow einheitlich 11px, letter-spacing 0.15em, #7a8290. H1 konsistent 32px/700. Der zweifarbige Titel (weiß+blau) ok, aber Blau (#4a9eff) entspricht der Akzentfarbe — konsequent nur EIN Blau im ganzen UI.

**8. Card-Tiefe & Border modernisieren**
Element: Alle Cards.
Ziel: Statt harter Kanten → subtiler Border (#ffffff0d) + minimaler Schatten für Elevation. Kritische Card („Säure-Base“) mit dünnem roten Left-Accent (3px) statt nur rotem Text hervorheben.

---

**Quick Wins:** #2, #5, #1 zuerst — höchster visueller Effekt bei geringstem Aufwand.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`