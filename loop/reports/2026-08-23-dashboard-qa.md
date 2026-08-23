# Dashboard-QA (Funktion + UX/Design) — 2026-08-23

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 6.5/10

Solide Datenbasis mit gutem Farb-Ampelsystem, aber sichtbare Struktur- und Konsistenzschwächen: schwebende/überlappende Tab-Leiste (Desktop), unruhige Typo-Größen, monospaced Zahlen im Fließtext, und ein Sprung-Chart-Layout mobil.

---

## Konkrete Verbesserungen (priorisiert)

**1. Tab-Leiste „Kalorien/Nährstoffe" — Overlay-Bug beheben (Desktop)**
Aktuell überlappt die Toggle-Leiste + User-Dropdown mit dem darüberliegenden „Gesamtdeckung"-Panel und schneidet die erste Chart-Zeile ab. Ziel: Sticky-Bar mit eigenem Hintergrund (solide, `backdrop-blur`), klarer Abstand nach oben/unten, keine überschnittenen Balken.

**2. Zahlen-Typografie vereinheitlichen**
Werte wie „2,26 / 20 µg" nutzen Monospace mitten im Sans-Serif-Layout → wirkt technisch/inkonsistent. Ziel: Tabellen-Ziffern (`font-variant-numeric: tabular-nums`) in der System-/Sans-Schrift, konsistente Dezimaltrennung (überall Komma), Einheiten in gedämpftem Grau.

**3. Nährstoff-Balkenliste: Prozentwert-Ausrichtung + Ziellinie**
Prozente rechts sind farblich korrekt, aber es fehlt eine visuelle 100%-Markierung. Ziel: vertikale gestrichelte „100%"-Linie im Balkentrack, damit „108% vs. 45%" sofort lesbar sind. Balkenhöhe leicht reduzieren (mehr Zeilen pro Blick, ruhiger).

**4. Checkpoint-Cards: Score-Badge und Farblogik angleichen**
„62/100" gelb, „37/100" rot, aber „Cholesterin 298 mg" hat kein /100-Format → Bruch im Muster. Ziel: einheitliches Badge-Layout (Score ODER Wert konsistent), gleicher Zeilenumbruch bei „15 schlecht" (aktuell umbricht nur eine Card).

**5. Gesamtdeckungs-Ring stärker inszenieren**
76%-Donut steht isoliert in viel Leerraum. Ziel: kompaktere Card, Ring + Text zentriert gruppieren, ggf. Mini-Segmente (grün/gelb/rot-Anteil der 16 Nährstoffe) statt einfarbig — sonst wirkt der Whitespace ungenutzt.

**6. Mobiler Balken-Chart „Zielerreichung" fixen**
Die +/−-Balken (z.B. „+673", „−327") haben inkonsistente Nulllinie und abgeschnittene Werte-Labels. Ziel: zentrierte 0-Achse, Labels immer außerhalb des Balkens, einheitliche Balkenhöhe, grün = Defizit / gelb = Überschuss durchgängig.

**7. Header-Hierarchie schärfen**
„NÄHRSTOFFBRUDI/KALORIENBRUDI" als winziges Label über „Dashboard Denis" wirkt beliebig. Ziel: Eyebrow-Label kleiner + mehr Letter-Spacing weglassen zugunsten klarer H1; der Name „Denis" im Blau ist gut — konsequent als Akzentfarbe nur für interaktive/aktive Elemente nutzen (aktuell auch bei Werten → verwässert).

**8. Datenqualitäts-Warnung prominenter (mobil top, Desktop fehlt sie)**
„20 Tage ohne Kalorien-Eintrag – nicht gewertet" ist kritisch fürs Vertrauen in alle Zahlen. Ziel: konsistent auf beiden Layouts sichtbar, als dezenter Alert-Banner oben, nicht versteckt in einer Card.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`