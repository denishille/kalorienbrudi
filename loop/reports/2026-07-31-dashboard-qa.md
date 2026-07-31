# Dashboard-QA (Funktion + UX/Design) — 2026-07-31

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# UX/Design-Review – Nährstoff/Kalorien-Dashboard

## Gesamtnote: **6,5 / 10**

Solide Datenvisualisierung mit gutem Dark-Theme-Ansatz und klarer Farb-Semantik (rot→grün). Schwächen: inkonsistente Abstände, überladene Header-Zone, schwache Hierarchie im Desktop-Layout und ein sichtbarer Layout-Fehler (überlappende Tab-Leiste über der Nährstoffliste).

---

## Konkrete Verbesserungen (priorisiert)

**1. [KRITISCH] Tab-Leiste „Kalorien/Nährstoffe" – Überlappungs-Bug**
Betroffen: Desktop, schwebende Leiste liegt halbtransparent über der Nährstoffliste („Vitamin D" ist abgeschnitten).
Ziel: Tab-Switch als fixierte, deckende Sub-Nav direkt unter dem Header; Content-Bereich mit korrektem `padding-top`, keine Überlagerung. Toggle + Nutzer-Dropdown gehören logisch nach oben, nicht mittig in den Content.

**2. [HOCH] Header/Zeitfenster – Hierarchie & Ausrichtung**
Betroffen: „NÄHRSTOFFBRUDI / Dashboard Denis" + Zeitfenster-Card.
Ziel: Eyebrow-Label kleiner/dezenter, Titel-Zweifarbigkeit (weiß+blau) beibehalten aber konsistent. Zeitfenster-Toggle (7/30/Gesamt) und Nutzer-Umschalter in EINE obere Toolbar-Zeile zusammenführen → weniger vertikale Streuung.

**3. [HOCH] Checkpoint-Cards – Konsistenz & Ausrichtung**
Betroffen: 4 Karten (Darmgesundheit etc.).
Ziel: Score-Badge einheitlich formatieren (mal „56/100", mal „433 mg" — Einheiten visuell trennen). Statuszeile („19 gut · 41 neutral · 10 schlecht") als Mini-Segmentbalken statt reinem Text → schneller erfassbar. Fußnoten-Text gleiche Zeilenhöhe/vertikal bündig über alle 4 Cards.

**4. [MITTEL] Nährstoff-Balkenliste – Lesbarkeit & Zielmarke**
Betroffen: Bar-Liste Vitamin D…B12.
Ziel: 100%-Zielmarke als vertikale Referenzlinie im Track anzeigen (aktuell nur implizit). Werte-Labels („3,44 / 20 µg") rechtsbündig zur Prozentspalte alignen. Row-Höhe leicht reduzieren + Zebra-Trennung dezenter — Liste wirkt sonst lang und monoton.

**5. [MITTEL] Donut „68% Gesamtdeckung" – Whitespace-Problem**
Betroffen: Card mit Ring-Chart.
Ziel: Riesige leere Fläche rechts nutzen — z.B. 3–4 Mikro-Kennzahlen (bester/schlechtester Nährstoff, Anzahl <50%) daneben platzieren. Aktuell 60% der Card leer.

**6. [MITTEL] Typografie-Skala vereinheitlichen**
Betroffen: durchgängig.
Ziel: Klare Type-Scale definieren (z.B. 32/20/16/13/11). Aktuell mischen sich zu viele ähnliche Größen; Sperrschrift-Labels (LETTER-SPACING) nur für Eyebrows, nicht für Fließtext.

**7. [MITTEL] Mobile – KPI-Kacheln (34/30/5/69) verbessern**
Betroffen: 2×2-Grid Mobile.
Ziel: Einheitliche Kachelhöhe, Icon/Dot links neben Zahl statt darunter, Sekundärzeile („49% der Tage") in gedämpftem Grau. „5 Über Bedarf" in Rot ist gut — Semantik konsistent auf alle Kacheln anwenden.

**8. [NIEDRIG] Kontrast Sekundärtext**
Betroffen: Fußnoten, Datum-Zeilen, „Stand: …".
Ziel: Sehr dunkelgraue Texte auf schwarzem Grund liegen unter WCAG-AA. Mindestens auf #8A8A8A anheben.

---

**Quick-Win-Reihenfolge:** #1 (Bug) → #2/#3 (Hierarchie) → #5 (Whitespace) → Rest.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`