# Dashboard-QA (Funktion + UX/Design) — 2026-07-14

**Funktion:** 1 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 0 Charts gerendert

## Funktionale Auffälligkeiten
- 🔴 Keine Charts gerendert

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 5.5/10

Solide Datenstruktur, aber Desktop-Empty-State ist verschwendeter Raum, Monospace-Fließtext wirkt unfertig, und die zwei Screens wirken wie zwei verschiedene Apps (Inkonsistenz Pink/Blau, Layout).

## Konkrete Verbesserungen (priorisiert)

**1. Desktop Empty-State → aktivierbar (HOCH)**
Element: Desktop „Keine Daten im Zeitfenster". Zielzustand: Skeleton-Layout der echten Karten (ausgegraut) statt leerer Box + primärer CTA „Eintrag hinzufügen" + Hinweis „30 Tage/Gesamt hat Daten" als klickbarer Chip. Aktuell führt der Screen in eine Sackgasse.

**2. Monospace-Fließtext eliminieren (HOCH)**
Element: alle Sub-Texte („letzte 7 Tage · keine Daten", „Im letzte 7 Tage wurde nichts getrackt", Datumsangaben, Footer). Zielzustand: Sans-Serif (gleiche Family wie Headlines). Monospace nur für reine Zahlenwerte/kcal. Zusätzlich Grammatik fixen: „In den letzten 7 Tagen".

**3. Kontrast Empty-State-Text (HOCH – A11y)**
Element: Desktop Body-Text auf dunklem BG (~#666 auf #1a1a1a). Zielzustand: min. 4.5:1, Text auf ~#B0B0B0 anheben.

**4. Farb-System vereinheitlichen (MITTEL)**
Element: User-Toggle & Akzentfarbe (Leni=Pink, Denis=Blau). Zielzustand: OK als Personalisierung, aber definierte Semantik-Farben (grün=Ziel, gelb=Defizit, rot=über Bedarf) konsistent auf BEIDEN Profilen. Aktuell nur bei Denis sichtbar.

**5. Mobile: Diff-Chart lesbarer machen (MITTEL)**
Element: „Kaloriendifferenz letzte 7 Tage" Balken. Zielzustand: zentrierte Null-Linie visuell markieren (vertikale Trennlinie), Balken an fixe Achse binden, kcal-Werte rechtsbündig ausrichten. Aktuell schweben Werte ohne klaren Bezug.

**6. Info-Karten (24/24/4/52) → visuelle Hierarchie (MITTEL)**
Element: 2×2 KPI-Grid. Zielzustand: farbige Top-Border ist zu subtil – Icon + größerer farbiger Akzent hinter der Zahl. „46% der Tage" prominenter als eigene Micro-Progress-Bar statt grauer Zeile.

**7. Header-Redundanz reduzieren (NIEDRIG)**
Element: „KALORIEN / NÄHRSTOFFE" + „NÄHRSTOFFBRUDI" + „Dashboard Leni". Zielzustand: Eyebrow-Label „NÄHRSTOFFBRUDI" streichen oder als Logo/Icon; Breadcrumb und H1 reichen. Spart Rauschen.

**8. Whitespace & Karten-Rhythmus (NIEDRIG)**
Element: Zielübersicht-Karte (mobil) mit vielen dünnen Trennlinien. Zielzustand: konsistente 16px vertikale Abstände, Label-Wert-Paare als zwei Spalten mit fixer Baseline statt gepunkteter Linien – wirkt cleaner/moderner.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`