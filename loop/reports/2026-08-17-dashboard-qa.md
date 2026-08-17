# Dashboard-QA (Funktion + UX/Design) — 2026-08-17

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 6.5/10

Solide Datenvisualisierung mit gutem Farbcode (Ampel), aber inkonsistente Typografie (Mono vs. Sans-Mix), unruhige Abstände und ein floatendes Tab-Menü, das den Nährstoff-Chart oben abschneidet. Wirkt funktional, aber nicht „premium".

---

## Konkrete Verbesserungen (priorisiert)

**1. Floating-Tab-Bar (Desktop) — kritisch**
Betroffen: `KALORIEN/NÄHRSTOFFE`-Toggle + `Denis`-Dropdown, das über der Liste schwebt und die erste Zeile (Vitamin D?) abschneidet.
Ziel: In den Header verankern (sticky top), Chart erhält vollständigen oberen Rand mit ≥24px Abstand. Kein Überlappen von Content.

**2. Typografie-Konsistenz — hoch**
Betroffen: Mono-Font für Werte (`13,7 / 30 g`, `52/100`) vs. Sans für Labels.
Ziel: Ein Font-System. Mono nur für tabellarische Zahlen-Spalten, Labels durchgehend Sans. Einheitliche Größen-Skala (z.B. 12/14/16/24/32).

**3. Progress-Bar-Labels Nährstoffe — hoch**
Betroffen: Balkenliste, Prozente stehen weit rechts isoliert, Name/Ist-Ziel links — Auge muss weit springen.
Ziel: Prozent direkt am Balkenende oder Ist-Wert-Label kompakter gruppieren. Alternierender Row-Hintergrund oder feine Trennlinien für Scanbarkeit.

**4. Card-Abstände & Ausrichtung Checkpoints — mittel**
Betroffen: 4 Gesundheits-Cards, Textblöcke unterschiedlich hoch, untere Kante flattert.
Ziel: Gleiche Card-Höhe, Baseline-Grid für „Okay/Kritisch"-Zeile, Fußnoten-Text auf einheitlicher Y-Position.

**5. Kontrast Grautöne — mittel**
Betroffen: Sekundärtext (`Ballaststoffe, Fermentiertes...`, `weniger ist besser...`) zu dunkel, unter WCAG AA.
Ziel: Sekundärtext auf min. #9CA3AF (4.5:1), Labels wie `ZEITFENSTER` etwas heller.

**6. Donut-Chart Gesamtdeckung — mittel**
Betroffen: 63%-Ring wirkt leer/unausbalanciert im breiten Container, viel toter Whitespace rechts.
Ziel: Ring verkleinern + Mini-Legende/Sparkline oder Top-3-Defizite daneben platzieren, um Fläche zu nutzen.

**7. Datenqualität-Warnung (Mobil) — mittel**
Betroffen: Gelbe Warn-Box „26 Tage ohne Eintrag" — wichtige Info, aber optisch schwach zwischen Zahlen versteckt.
Ziel: Klarere Iconografie + Button-Style für „Details ansehen", konsistente Warn-Farbe zur Ampel.

**8. Balken-Chart Zielerreichung (Mobil) — niedrig**
Betroffen: Winzige grüne Balken um Nulllinie, Werte teils außerhalb.
Ziel: Nulllinie mittig fixieren, symmetrische Skala, Werte-Labels konsistent innen/außen je nach Balkenlänge.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`