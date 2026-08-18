# Dashboard-QA (Funktion + UX/Design) — 2026-08-18

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# UX/Design-Review – Nährstoff/Kalorien-Dashboard

## Gesamtnote: **6,5 / 10**

Solide Datenbasis, gute Farbcodierung und moderne Grundausrichtung (Dark Theme, klare Balken). Es fehlt aber Feinschliff bei Hierarchie, Spacing-Rhythmus und der schwebenden Navi-Leiste, die aktuell Inhalt verdeckt.

---

## Konkrete Verbesserungen (priorisiert)

**1. [KRITISCH] Floating-Tab-Bar (KALORIEN/NÄHRSTOFFE/Denis) – Desktop**
Aktuell überlappt die Leiste die Charts und schneidet die oberste Nährstoffzeile („2,45 / 20 µg“) ab. Zielzustand: als fixierte Bar mit ausreichend `padding-bottom` im Scrollcontainer verankern, plus dezenter Schatten/Blur (`backdrop-blur`), damit sie klar über dem Content „schwebt“ statt ihn zu verdecken.

**2. [HOCH] Typografie-Konsistenz Monospace vs. Sans**
Werte wie „2,45 / 20 µg“, „48/100“ und Datumsangaben nutzen Monospace, Labels Sans – wirkt uneinheitlich. Zielzustand: Monospace **nur** für tabellarische Zahlenspalten (rechtsbündige %-Werte), Labels und Zwischenwerte in derselben Sans wie Überschriften. Einheitliche Zahlengröße.

**3. [HOCH] Prozent-Balken – fehlende Referenzlinie**
Die Balken haben keine sichtbare 100%-Marke, dadurch ist „95%“ vs. „136%“ visuell schwer einzuordnen. Zielzustand: vertikale gestrichelte 100%-Ziellinie über alle Balken, Overflow (>100%) klar abgesetzt (z.B. andere Sättigung/kleiner Marker), damit „genug vs. Überschuss“ sofort lesbar ist.

**4. [HOCH] Checkpoint-Cards – uneinheitliche Ausrichtung**
Die 4 Cards haben unterschiedlich hohe Textblöcke, dadurch „springt“ die Baseline der Fußnoten. Zielzustand: feste Card-Höhe, Fußnote (grauer Hint) bündig am unteren Rand verankern, Score-Badge oben rechts einheitlich (Cholesterin „323 mg“ visuell wie „48/100“ formatieren).

**5. [MITTEL] Spacing-Rhythmus / Whitespace**
Der große leere Bereich im „Gesamtdeckung 61%“-Block (Desktop) wirkt ungenutzt, während Nährstoffliste dicht gedrängt ist. Zielzustand: konsistentes 8px-Grid, Deckungs-Block kompakter oder mit Mini-Legende/Trend füllen; Zeilenhöhe der Nährstoffliste minimal erhöhen (Atmung zwischen Label + Subwert).

**6. [MITTEL] Kontrast grauer Hint-Texte**
„Ballaststoffe, Fermentiertes… = gut“ und Footer-Text liegen unter WCAG AA (zu dunkelgrau auf schwarz). Zielzustand: Grauwert auf min. 4.5:1 anheben (`#9AA0A6`+).

**7. [MITTEL] Mobile – Datenqualitäts-Warnung & „Wackelig“-Badge**
Der gelbe Warnkasten und der Status-Badge konkurrieren farblich mit dem Fortschrittsbalken. Zielzustand: Warnung als eigene, klar abgegrenzte Info-Card mit Icon links; Status-Badge in konsistenter Pill-Form wie die Score-Badges (gleiche Radius/Padding-Tokens).

**8. [NIEDRIG] Bar-Chart Mobil (Wochendurchschnitt)**
Ziel-Linie (grün gestrichelt) und Balkenwerte überlagern sich am linken Rand („Ziel“-Label wird abgeschnitten). Zielzustand: Ziel-Label an Linienende rechts platzieren, Balken einheitlich abrunden (oben), Achsen-Padding erhöhen.

---

**Quick Wins zuerst:** #1 (Overlap fixen), #3 (100%-Linie), #4 (Card-Ausrichtung) → größter visueller Sprung bei geringem Aufwand.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`