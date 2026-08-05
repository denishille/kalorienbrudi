# Dashboard-QA (Funktion + UX/Design) — 2026-08-05

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 7/10

Solide, moderne Basis mit gutem Dark-Theme und klarer Farb-Ampel-Logik. Es fehlt aber Feinschliff bei Konsistenz, Hierarchie und einigen visuellen Details, die den Unterschied zwischen „gut" und „top" ausmachen.

---

## Konkrete Verbesserungen (priorisiert)

**1. Sticky-Toolbar-Überlappung fixen (Desktop) — KRITISCH**
Element: Kalorien/Nährstoffe-Toggle + Denis-Dropdown liegen halbtransparent über der Nährstoffliste und verdecken die Tabellenkopfzeile.
Ziel: Solide Hintergrundfläche mit Border/Shadow, klare Trennung zur Liste, kein Durchscheinen des Inhalts darunter.

**2. Nährstoff-Balkenliste: Zielmarke + Struktur**
Element: Balkendiagramm Vitamin D–Selen.
Ziel: Vertikale 100%-Referenzlinie einziehen (macht Über-/Unterdeckung sofort lesbar), Zebra-Streifen oder feine Trennlinien für 16 Zeilen, Balkenhöhe leicht reduzieren für ruhigeren Rhythmus. Rechte Prozentspalte rechtsbündig ausrichten.

**3. Checkpoint-Cards vereinheitlichen**
Element: 4 Karten (Darmgesundheit … Cholesterin).
Ziel: Cholesterin bricht das Muster („251 mg" statt „x/100", keine gut/neutral/schlecht-Zeile). Einheitliches Sub-Metrik-Layout einführen, damit alle Karten identische Struktur/Höhe haben. Score-Pills gleich breit.

**4. Typografische Hierarchie schärfen**
Element: Überschriften & Labels durchgehend.
Ziel: Die vielen Grau-in-Grau-Labels (ZEITFENSTER, Sub-Zeilen) haben zu geringen Kontrast (WCAG < 4.5:1). Sekundärtext auf mind. #A0A0A8 anheben, Letter-Spacing bei Caps-Labels reduzieren. Konsistente Font (Monospace-Zahlen wirken uneinheitlich zum Rest).

**5. Donut „Gesamtdeckung" aufwerten**
Element: 63%-Ring.
Ziel: Ring wirkt isoliert im leeren Card-Raum. Farbverlauf passend zum Score (gelb→grün), Center-Zahl kleiner + Label „Ø Deckung" darunter, rechten Whitespace mit Mini-Legende oder Trend füllen.

**6. Mobile: Balken-Chart „Zielerreichung" lesbarer**
Element: Diagonale Balken So–Mo mit +/- Werten.
Ziel: Zentrale 0-Linie visuell markieren (dünne vertikale Linie), Werte-Labels konsistent positionieren (aktuell springen sie links/rechts), einheitliche Balkenhöhe.

**7. Farbsemantik entkoppeln**
Element: Blau wird für Marken-Akzent (Denis), aktive Buttons UND Balken (Wochendurchschnitt) genutzt.
Ziel: Ein dediziertes Akzentblau nur für interaktive/aktive States; Datenvisualisierung in eigener, neutralerer Palette, damit „klickbar" vs. „Datenwert" unterscheidbar bleibt.

**8. Spacing & Abstände (Mobile)**
Element: Stat-Karten (37/31/5/73) und Footer.
Ziel: Einheitliche vertikale Section-Abstände (aktuell ungleich), Footer-Text mittig umbrechend statt gequetscht, konsistente Card-Innenpadding-Werte über alle Blöcke.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`