# Dashboard-QA (Funktion + UX/Design) — 2026-07-17

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 1 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung Kalorien-Tracking-Dashboard

## Gesamtnote: **7 / 10**

Solide, moderne Basis mit klarem Dark-Theme und guter Ampel-Logik. Schwächen bei Konsistenz zwischen den beiden Nutzer-Views, Whitespace-Verteilung und Chart-Lesbarkeit verhindern Top-Wertung.

---

## Konkrete Verbesserungen (priorisiert)

**1. Konsistenz Nutzer-Umschalter (Desktop vs. Mobil) — HOCH**
Element: Denis/Leni-Toggle. Aktuell zwei visuell unterschiedliche Pill-Designs (Position rechts oben vs. links, andere Proportionen). Zielzustand: identische Toggle-Komponente, gleiche Größe/Position, aktive Farbe = Nutzerfarbe (Pink/Blau) durchgängig.

**2. Kontrast der Sub-Labels & Meta-Texte — HOCH (Accessibility)**
Element: graue Fließtexte („Ballaststoffe, Fermentiertes…", „Ø pro Tag vs. Tagesreferenz", Footer). Kontrast unter WCAG AA. Zielzustand: Grauwert von ~#6b6b6b auf min. #9a9a9a anheben, Footer mindestens #808080.

**3. Mikronährstoff-Balken – Prozent & Ziel-Referenz — HOCH**
Element: horizontale Bars mit Prozentzahl. Es fehlt eine sichtbare 100%-Ziellinie; Balken über 100% (Selen 128%) laufen visuell identisch aus. Zielzustand: vertikale gestrichelte 100%-Marke einfügen, Werte >100% farblich/visuell (z. B. leichter Overflow-Indikator) abheben. Prozent-Labels rechtsbündig auf feste Spalte ausrichten.

**4. Whitespace Desktop – große Leerfläche unter Donut — MITTEL**
Element: Bereich „Gesamtdeckung" (66%-Ring). Viel ungenutzter Platz rechts. Zielzustand: Donut kleiner + Kennzahl-Kacheln (Top/Flop-Nährstoffe, Trend) rechts daneben, um Fläche zu füllen und Informationsdichte zu erhöhen.

**5. Typo-Hierarchie Zahlen (Mobil) — MITTEL**
Element: KPI-Kacheln „25 / 26 / 4 / 55". Große Zahlen konkurrieren mit den Ziel-Zeilen darüber (1.900 kcal etc.), keine klare erste Ebene. Zielzustand: einheitliche numerische Schrift (tabular figures), konsistente Zahlengrößen pro Ebene, Labels darunter kleiner + uppercase-tracking reduzieren.

**6. Checkpoint-Cards – Score-Badge & Farb-Semantik — MITTEL**
Element: „59/100", „47/100" Badges. Farbcodierung der Badge entspricht nicht immer dem Card-Rahmen (gelb vs. rot). Zielzustand: Badge-Farbe = Ampelstatus konsequent, Rahmen dezenter (1px statt farbig-glow), Status-Wort („Kritisch") als primärer Blickfang beibehalten.

**7. Balkendiagramm „Kaloriendifferenz" – Nulllinie — MITTEL**
Element: Mini-Bars pro Tag (Mobil). Positive/negative Werte nicht klar an gemeinsamer Nulllinie ausgerichtet, Balkenlängen wirken beliebig. Zielzustand: zentrale vertikale Nulllinie, grün links (Defizit) / gelb rechts (Überschuss), proportionale Länge.

**8. Ausrichtung Nährstoff-Liste (Desktop) — NIEDRIG**
Element: Name + Wert-Zeile links. „14,7 / 30 g" Werte unterschiedlich formatiert (Kommazeichen, Einheiten). Zielzustand: monospace/tabular für alle Zahlenpaare, einheitliche Einheiten-Platzierung, konsistenter vertikaler Rhythmus (gleicher Zeilenabstand).

---

**Quick Wins:** Kontrast erhöhen (2), 100%-Ziellinie (3), Toggle vereinheitlichen (1).

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`