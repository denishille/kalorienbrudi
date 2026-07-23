# Dashboard-QA (Funktion + UX/Design) — 2026-07-23

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 6.5/10

Solide Datendichte, gutes Farbcoding (Ampel-Logik), aber inkonsistente Ausrichtung, schwache Hierarchie und ein kaputter Layout-Übergang (schwebende Tab-Leiste über Chart) ziehen die Note runter.

---

## Konkrete Verbesserungen (priorisiert)

**1. Schwebende Tab-/User-Leiste fixieren (Desktop, kritisch)**
Betroffen: `KALORIEN/NÄHRSTOFFE`-Toggle + `Denis`-Selector im Screenshot 1.
Problem: Die Leiste liegt halbtransparent MITTEN über der Nährstoff-Tabelle und verdeckt die Spaltenüberschrift („Vitamin D“ ist abgeschnitten). Zielzustand: Sticky-Header oben fixiert ODER als eigenständige Toolbar unter dem H1 platziert – niemals über Content-Zeilen liegend.

**2. Tab-Navigation an feste Position (beide Screens)**
Betroffen: Segment-Control `KALORIEN | NÄHRSTOFFE`.
Zielzustand: Direkt unter der Überschrift verankern, gleiche vertikale Position auf Desktop wie Mobil. Aktuell ist die Hierarchie unklar (Toggle taucht mitten im Scroll auf).

**3. Prozent-Balken linksbündig mit einheitlicher Track-Breite (Desktop)**
Betroffen: Mikronährstoff-Bars.
Zielzustand: Balken-Track-Ende und %-Werte an fester rechter Kante ausrichten (Grid). Aktuell wirken die %-Zahlen ungleichmäßig, Track-Enden variieren optisch. Fügt eine dezente 100%-Marker-Linie ein.

**4. Farbverlauf der Balken vereinheitlichen (Desktop)**
Betroffen: Bar-Fills (rot→gelb→grün).
Problem: Jeder Balken hat internen Verlauf → unruhig, Werte schwer vergleichbar. Zielzustand: Einfarbige Fills pro Ampelstufe (klare 3 Töne), kein Gradient innerhalb eines Balkens.

**5. Hero-Progress „54%“-Ring erhält Kontext (Desktop)**
Betroffen: „Gesamtdeckung 54%“.
Zielzustand: Ring-Trackfarbe (dunkelgrau) sichtbar machen, damit der Fortschritt lesbar ist; Label-Typo verkleinern zugunsten der Zahl. Card ist aktuell sehr leer → Whitespace nutzen für Mini-Legende (rot/gelb/grün Schwellen).

**6. Typografie-Hierarchie schärfen (beide)**
Betroffen: Section-Labels wie `ZEITFENSTER`, `AKTUELLES ZIEL`.
Zielzustand: Letter-Spacing beibehalten, aber Kontrast erhöhen (aktuell fast unsichtbar auf Dunkelgrau). Sub-Labels min. #8A8A8A statt aktuellem Low-Contrast-Grau (WCAG-Fail).

**7. KPI-Kacheln vereinheitlichen (Mobil)**
Betroffen: `31 / 27 / 4 / 62`-Kacheln.
Zielzustand: Gleiche Höhe, identische Icon-Position, Zahlen optisch zentriert. Große Zahlen etwas kleiner, damit „62 Tage getrackt“ nicht zweizeilig bricht.

**8. Balkendiagramm „Zielerreichung“ mit Nulllinie (Mobil)**
Betroffen: Diff-Balken (-144, +4 …).
Zielzustand: Vertikale 0-Achse einzeichnen, Balken links/rechts davon (negativ = grün links, positiv = rot rechts). Aktuell startet alles rechts → Defizit/Überschuss nicht auf einen Blick erkennbar.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`