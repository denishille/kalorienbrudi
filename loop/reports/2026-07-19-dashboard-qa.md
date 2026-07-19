# Dashboard-QA (Funktion + UX/Design) — 2026-07-19

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 1 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Design/UX Review – Kalorien-Dashboard

## Gesamtnote: **7 / 10**

Solide, moderne Basis mit gutem Dark-Theme und klarer Farbsemantik (Ampel). Schwächen liegen in Detail-Konsistenz, Whitespace-Rhythmus und Chart-Lesbarkeit. Mit gezieltem Feinschliff sehr nah an Top-Niveau.

---

## Konkrete Verbesserungen (priorisiert)

**1. User-Switch vereinheitlichen (Desktop vs. Mobil)**
Element: Denis/Leni-Toggle. Aktuell auf Desktop Pill-rechts, auf Mobil Pill-links + andere Höhe → wirkt inkonsistent. Zielzustand: identische Segmented-Control-Komponente, gleiche Höhe/Radius/Padding auf beiden Breakpoints, aktiver Nutzer immer links.

**2. Balken-Prozentwerte hierarchisch entkoppeln**
Element: Mikronährstoff-Liste (Vitamin D 18% … Selen 127%). Die grauen `x / y`-Rohwerte konkurrieren mit dem farbigen %. Zielzustand: %-Wert als dominante Zahl (semibold, 16px, farbcodiert), Rohwerte kleiner (11px, 40% Opacity). Zusätzlich subtile 50%- und 100%-Markierungslinien im Balken-Track zur schnelleren Einordnung.

**3. Whitespace-Rhythmus & Card-Padding vereinheitlichen**
Element: Alle Cards. Padding variiert (Checkpoint-Cards eng, Gesamtdeckung-Card sehr luftig). Zielzustand: konsistentes 8pt-Grid, Card-Padding 24px, Sektionsabstand 32px. Der große Leerraum rechts neben „Gesamtdeckung 67%" strukturiert füllen (z.B. 2–3 Micro-KPIs).

**4. Kalorien-Wasserfall-Chart lesbarer machen (Mobil)**
Element: „Kaloriendifferenz – letzte 7 Tage". Balken sind winzig, Nulllinie unklar, grün/gold-Logik nicht erklärt. Zielzustand: zentrierte Nulllinie sichtbar markieren, Balken min. 20px hoch, kcal-Wert rechtsbündig ausgerichtet, kurze Legende (grün = Defizit / gold = Überschuss).

**5. Kontrast der Meta-/Sekundärtexte anheben**
Element: Kleine Graubeschriftungen (Zeitfenster, Fußzeilen, „Ø pro Tag vs…"). Kontrast teils <3:1 → WCAG-kritisch. Zielzustand: Sekundärtext auf min. #9AA0A6 (≥4.5:1 gegen Hintergrund) anheben.

**6. Typografie-Konsistenz Überschriften**
Element: „Dashboard Leni/Denis" nutzt Mixed-Case-Highlight in Pink/Blau – gut. Aber Section-Header („Gesundheits-Checkpoints", „Mikronährstoffe") variieren in Gewicht/Größe. Zielzustand: klare Type-Scale definieren (H1 32, H2 20 semibold, Label 12 uppercase tracked) und durchziehen.

**7. Status-Badges & Ampel-Punkte vereinheitlichen**
Element: „Okay/Kritisch/Gut"-Zustände + Score-Badges (60/100). Zielzustand: einheitliche Pill-Badges mit gefülltem Farbhintergrund (10% Opacity) statt gemischt aus Text-Farbe + Border-Cards. Der Score sollte visuell an den Status gekoppelt sein (gleiche Akzentfarbe).

**8. KPI-Karten Mobil (27/26/4/57) angleichen**
Element: 2×2 KPI-Grid. Farbige Topline nur teilweise, unterschiedliche Zahlengrößen wirken. Zielzustand: einheitliche Card-Struktur (Topline-Akzent 3px in Statusfarbe für alle), gleiche Zahlengröße, Label-Zeile immer 2-zeilig gleich ausgerichtet.

---

**Quick Wins zuerst:** #2, #5, #7 (hoher Impact, geringer Aufwand).

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`