# Dashboard-QA (Funktion + UX/Design) — 2026-08-09

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 6.5/10

Solide Datenbasis, gute Ampel-Logik und schöne Grün-Gelb-Rot-Skala. Es wirkt aber noch „funktional-generisch" statt premium: inkonsistente Typo-Casing, schwache Sekundärkontraste, gequetschter Tab-Switcher und ein Desktop-Layout, das nach unten verläuft.

---

## Konkrete Verbesserungen (priorisiert)

**1. Tab-Switcher „Kalorien/Nährstoffe" (Desktop) — schwebt frei & bricht Layout**
Aktuell überlagert der Switcher die Nährstoffliste (halbtransparente Box dahinter sichtbar). → Als fixierter Segmented-Control oben unter dem Titel platzieren, volle Deckkraft, klare Card-Grenze. Kein Überlappen mit Content.

**2. Typo-Casing vereinheitlichen — inkonsistent**
Mix aus `ALL-CAPS gesperrt` (Labels), Title-Case und Satzfall. → Ein System: Section-Labels durchgehend `ALL-CAPS 11px letter-spacing`, Werte-Labels Satzfall. Monospace-Zahlen (`1,92 / 20 µg`) nur für Werte, nicht mischen.

**3. Sekundärtext-Kontrast zu niedrig (WCAG-Fail)**
Graue Beschreibungen (`Ballaststoffe, Fermentiertes…`, Footer, Achsenbeschriftung) liegen unter 4.5:1. → Sekundärtext von ~#6b6b6b auf mind. #9a9a9a anheben, Footer auf #8a8a8a.

**4. Nährstoff-Balken: Zielmarke fehlt**
Balken laufen bis 195% ohne visuelle 100%-Referenzlinie. → Vertikale gestrichelte „100%"-Marker-Linie einziehen, damit Über-/Unterversorgung sofort lesbar ist. Prozent-Labels rechtsbündig ausrichten (aktuell leicht schwankend).

**5. Health-Checkpoint-Cards — Whitespace & Alignment**
Text `29 gut · 42 neutral · 13 schlecht` bricht unschön 2-zeilig, Beschreibung klebt unten. → Feste Card-Höhe, Score-Badge und Status vertikal rhythmisieren (8pt-Grid), Zeilenumbruch durch kürzere Labels oder Icons ersetzen.

**6. Donut „71%" — visuell zu leicht**
Dünner Ring, viel Leerraum rechts daneben. → Ring dicker, im Zentrum Prozent + kleiner Label „Ø Deckung"; Beschreibungstext links vom Ring in eine zweispaltige Balance bringen statt langer Fließtext.

**7. Mobile: Zahlen-Karten (72/6/0/78) zu nackt**
Große Zahlen ohne Card-Kontrast, wirken flach. → Dezente farbige Akzentkante links (grün/gelb/rot/blau) passend zum Status, konsistente Icon-Position, gleiche Höhe für 2×2-Grid.

**8. Datenqualität-Hinweis prominenter nutzen**
`27 Tage ohne Eintrag` ist wichtig, aber versteckt in gelber Box unten. → Als klarer inline-Warnstreifen mit CTA-Button-Stil statt Unterstreichungs-Link; Farbe konsistent zur Ampel (Amber).

**Quick Wins:** Zahlen-Kommastellen vereinheitlichen (`5,38` vs `191`), Header-Overline (`NÄHRSTOFFBRUDI`/`KALORIENBRUDI`) — Wording wirkt unfertig, ersetzen.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`