# Dashboard-QA (Funktion + UX/Design) — 2026-07-15

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 1 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# UX-Review: Kalorien-Tracking-Dashboard

## Gesamtnote: **6,5 / 10**

Solide Datenvisualisierung mit gutem Dark-Theme-Ansatz, aber inkonsistente Typo-Hierarchie, ungenutzter Whitespace (Desktop) und Charts mit schwacher Lesbarkeit ziehen die Note runter. Fühlt sich funktional, aber noch nicht „premium" an.

---

## Konkrete Verbesserungen (priorisiert)

**1. Whitespace-Chaos im Desktop-Balkenchart (KRITISCH)**
Element: Mikronährstoffe-Liste. Die Balken enden bei ~90% Breite, dann kommen die %-Werte weit rechts isoliert. Zustand: Balken auf ~70% Breite begrenzen, %-Wert direkt am Balkenende platzieren (rechtsbündig ausgerichtet in fixer Spalte). Reduziert riesigen Leerraum, verbessert Blickführung.

**2. Farbcodierung Ampel vs. Balken inkonsistent (HOCH)**
Element: Checkpoint-Karten nutzen Rot/Gelb/Grün, Balken haben eigenen Rot-Gold-Grün-Verlauf, Denis-Statuskarten wieder andere Töne. Zustand: EINE definierte Ampelpalette (z.B. #F87171 / #FBBF24 / #4ADE80) systemweit als Design-Token durchziehen.

**3. Typo-Hierarchie „Dashboard Leni/Denis" (HOCH)**
Element: Header. Der Zweifarb-Titel (weiß + pink/blau) plus darüberliegendes „NÄHRSTOFFBRUDI/KALORIENBRUDI" wirkt verspielt und uneindeutig. Zustand: Klare 3-Stufen-Hierarchie – Eyebrow-Label (11px, uppercase, gedämpft), H1 (32px, einfarbig), Nutzer-Toggle rechts. Akzentfarbe nur im aktiven Toggle, nicht im Titel.

**4. Denis-Datenzeilen zu luftig & label-value flach (MITTEL)**
Element: „Ziel / Kalorienziel / Defizit"-Liste (Mobil). Sehr große vertikale Abstände, alle Zeilen gleich gewichtet → keine Hierarchie. Zustand: Wichtigste 2 KPIs (Kalorienziel, Fortschritt) als hervorgehobene Cards, Rest als kompaktere Tabelle mit dezenten Divider-Linien. Zeilenabstand ~30% reduzieren.

**5. Chart-Lesbarkeit „Kaloriendifferenz" (MITTEL)**
Element: Horizontale Balken mit +391 kcal etc. Nulllinie/Referenz fehlt visuell, Balken schweben. Zustand: Vertikale 0-Achse einzeichnen, negative (grün) links / positive (gold/rot) rechts spiegeln. Datumslabels linksbündig ausrichten.

**6. Karten-Border-Akzente wirken beliebig (MITTEL)**
Element: Farbige Top-Border der Checkpoint- & Stat-Cards. Aktuell nur schmaler farbiger Strich oben. Zustand: Entweder konsequent als 2px Top-Accent ODER als dezenter farbiger Glow/Icon – nicht gemischt. Card-Padding vereinheitlichen (aktuell variiert es).

**7. „Datenqualität"-Warnung zu unauffällig / Kontrast (MITTEL)**
Element: Gelber Warnhinweis bei Denis. Text auf dunkelgelbem BG schwer lesbar (Kontrast <4.5:1). Zustand: Kontrast erhöhen (hellerer Text oder dunklerer BG), Warn-Icon prominenter, CTA „Details ansehen" als echter Button-Style.

**8. Zahlenformat & Einheiten inkonsistent (NIEDRIG)**
Element: „3,64 / 20 µg", „58 / 100", „1.900 kcal". Einheiten mal grau/klein, mal inline. Zustand: Durchgehendes Muster – Wert (tabular-nums, gebold) + Einheit (kleiner, gedämpft, konstante Baseline). Tabellenziffern aktivieren für saubere Ausrichtung.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`