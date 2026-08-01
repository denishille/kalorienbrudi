# Dashboard-QA (Funktion + UX/Design) — 2026-08-01

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 6.5 / 10

Solide Datenvisualisierung mit klarem Konzept, aber inkonsistente Abstände, ein kaputter Layout-Bereich (Desktop) und mangelnde visuelle Hierarchie halten es vom Top-Niveau ab.

---

## Konkrete Verbesserungen (priorisiert)

**1. KRITISCH – Desktop-Toggle-Bereich reparieren**
Der KALORIEN/NÄHRSTOFFE-Umschalter + „Denis"-Selektor überlappen die Donut-Karte und die Balkenliste (abgeschnittener Header „...gedeckt bei 100%"). → Toggle als eigene, saubere Zeile mit definiertem Abstand über die Balkenliste setzen; Überlappung/Blur entfernen.

**2. HOCH – Farbcodierung der Checkpoints vereinheitlichen**
Darmgesundheit 60/100 = gelb „Okay", Cholesterin 396mg = gelb „Okay" trotz Zielverfehlung (>300). → Konsistente Schwellenlogik: Cholesterin über Ziel muss orange/rot sein. Ampelfarbe + Status-Label immer synchron.

**3. HOCH – Typografie-Hierarchie stärken**
Werte-Zeilen („27 gut · 42 neutral · 11 schlecht") sind zu klein/grau und schlecht lesbar. → Zahlen fett + heller (mind. 14px, Kontrast ≥4.5:1), Einheiten/Labels dezent. Sekundärtext (z.B. „Ballaststoffe, Fermentiertes...") auf einheitliche 12px setzen.

**4. HOCH – Balkenliste: Zielmarke + Ausrichtung**
100%-Referenz ist nicht sichtbar markiert; Werte >100% (Selen 164%) sprengen visuell die Skala unklar. → Vertikale 100%-Ziellinie einziehen, Balken darüber klar überlaufend darstellen. Prozent-Spalte rechtsbündig fix ausrichten.

**5. MITTEL – Whitespace & Kartenrhythmus vereinheitlichen**
Uneinheitliche vertikale Abstände zwischen Sektionen (Checkpoints ↔ Donut ↔ Liste). → Einheitliches 8px-Grid, konsistente Card-Paddings (24px) und Sektionsabstände (48px).

**6. MITTEL – Mobile: KPI-Zahlen-Kontrast & Konsistenz**
„5 Über Bedarf" in Rot wirkt wie Fehler, Farbsemantik der 4 KPI-Kacheln uneinheitlich (grün/gelb/rot/blau). → Farben nur semantisch (rot = negativ), neutrale Metriken (71 Tage) in Weiß/Grau statt Blau.

**7. MITTEL – Waterfall-Chart (Zielerreichung) lesbarer machen**
Werte wie „+525 / -310" ohne Achsen-Nulllinie schwer einzuordnen. → Klare zentrierte Nulllinie, konsistente Balkenhöhe, Datum linksbündig, Wert am Balkenende einheitlich positionieren.

**8. NIEDRIG – Branding-Konsistenz**
„NÄHRSTOFFBRUDI" (Desktop) vs. „KALORIENBRUDI" (Mobile) als Eyebrow wirkt zufällig. → Einheitlicher Markenname, Ansicht separat über Toggle kommunizieren.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`