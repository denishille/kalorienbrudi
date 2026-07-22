# Dashboard-QA (Funktion + UX/Design) — 2026-07-22

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Gesamtnote: 6.5/10

Solide Datendichte und funktionierendes Dark-Theme, aber inkonsistente Abstände, schwache visuelle Hierarchie im Header/Nav und Kontrast-/Farbprobleme mindern die Premium-Wirkung.

---

## Konkrete Verbesserungen (priorisiert)

**1. Sticky-Tab-Leiste (KALORIEN/NÄHRSTOFFE + Denis) — Desktop**
Aktuell schwebt sie mitten im Content und überdeckt die Chart-Überschrift (Zeile „…gedeckt bei 100%“ wird angeschnitten). → Als echte fixierte Top-Navigation oberhalb des Contents verankern, mit klarer Trennlinie/Backdrop-Blur und Padding zum darunterliegenden Chart (min. 32px). Kein Content darf überlappt werden.

**2. Kontrast der roten Balken & Prozentwerte**
Rote Bars (Vitamin D–Omega-3) + rote Prozentzahlen auf dunklem BG liegen nahe der WCAG-Grenze und wirken „alarmig-billig“. → Prozentwerte in neutralem Weiß/Grau setzen, nur Balkenfarbe kodiert Status. Rot entsättigen (#E5484D → weicher), Track-Hintergrund der Bars leicht aufhellen für definierten Kontrast.

**3. Header-Hierarchie & Eyebrow-Label**
„NÄHRSTOFFBRUDI“/„KALORIENBRUDI“ als Eyebrow ist verspielt und lenkt ab; „Dashboard Denis“ dominiert unnötig. → Eyebrow kleiner/dezenter (oder als Logo), Nutzername konsistent — er erscheint 3× (Titel, Nav-Switch, Footer). Redundanz reduzieren: Name nur im Nav-Switcher + Titel.

**4. Karten-Konsistenz Gesundheits-Checkpoints**
Score-Badges (47/100, 64/100) haben uneinheitliche Farblogik, und „Cholesterin 263 mg“ nutzt eine andere Werteinheit-Darstellung als die /100-Scores. → Einheitliches Badge-System: gleiche Pill-Größe, gleiche Radius, konsistente Ampellogik. Statustext („Kritisch“, „Gut“) farblich an Badge koppeln.

**5. Gesamtdeckungs-Ring (55%)**
Der einsame große Ring links wirkt unbalanciert, rechts viel Leerraum. → Ring verkleinern und Content zentrieren, ODER rechts Mini-Stats (z.B. „X von 16 Nährstoffen ≥100%“) ergänzen. Whitespace gezielt nutzen statt Leerlauf.

**6. Balken-Chart Lesbarkeit (Nährstoffliste)**
16 Zeilen ohne Gruppierung/Zebra sind ermüdend; Zielmarkierung (100%) fehlt visuell im Track. → Vertikale 100%-Referenzlinie einziehen, subtile Zeilentrennung (alternierender BG 3–5% Opacity), Werte (2,92 / 20 µg) rechtsbündig ausrichten für Scanbarkeit.

**7. Mobil: Bar-Chart „Zielerreichung“**
Labels „06“ und „+250“ überlappen die Balken, Nulllinie unklar, Farbkodierung (grün=gut?) ohne Legende. → Zentrale Nulllinie klar zeichnen, Werte außerhalb der Balken platzieren, kurze Legende (grün = im Defizit / gelb = drüber).

**8. Typografie-Rhythmus & Spacing (beide)**
Monospace-Ziffern gut, aber Abstände zwischen Sektionen variieren stark (Header→Zeitfenster eng, Ring-Sektion sehr luftig). → Konsistentes 8px-Grid, einheitliche Section-Gaps (z.B. 48px Desktop / 24px Mobil), gleiche Card-Innenpaddings überall.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`