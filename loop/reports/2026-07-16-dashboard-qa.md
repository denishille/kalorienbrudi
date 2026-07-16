# Dashboard-QA (Funktion + UX/Design) — 2026-07-16

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 1 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 7/10

Solide Basis, klare Farbcodierung und gute Datenstruktur. Es fehlt jedoch an typografischer Feinabstimmung, konsistentem Rhythmus und visueller Ruhe – aktuell wirkt es an mehreren Stellen technisch statt premium.

---

## Konkrete Verbesserungen (priorisiert)

**1. Mikronährstoff-Werte: Monospace-Font ersetzen** (Desktop)
Die `4,37 / 20 µg`-Zeilen wirken durch Monospace wie Terminal-Output. → Auf dieselbe Sans-Serif wie der Rest umstellen, in gedämpftem Grau (z. B. #8A8A8A), Label fett, Wert regular. Sofort wertiger.

**2. Farbübergang der Balken glätten** (Desktop, Chart)
Rot→Gelb→Grün wechselt hart pro Zeile. → Konsistente, entsättigte Palette mit einheitlicher Sättigung; nur eine Akzentfarbe pro Zustand, kein Gradient innerhalb des Balkens. Prozentwert rechts in gleicher Farbe wie Balken belassen.

**3. Card-Rahmen mit farbigem Border reduzieren** (Desktop, Checkpoints)
Die roten/gelben Vollrahmen um die 4 Cards sind zu laut und konkurrieren mit den Balken. → Border entfernen, stattdessen dünner farbiger Top-Accent (2 px) oder farbiger Status-Dot + neutralem Card-Border (#2A2A2A). Ruhiger, moderner.

**4. Vertikaler Rhythmus & Whitespace vereinheitlichen** (beide)
Abstände zwischen Sektionen variieren (Checkpoints → Gesamtdeckung → Liste). → 8-px-Grid einführen, Sektionsabstände auf konstant 48 px, Card-Innenpadding einheitlich 24 px.

**5. Mobile: Tabellen-Layout auflockern** (Mobil, „Aktuelles Ziel")
Die Ziel/Kalorienziel/Defizit-Liste ist eine dichte Label-Wert-Tabelle mit vielen Trennlinien. → Trennlinien weglassen, Werte in 2er-Grid-Cards gruppieren (Kalorienziel, Defizit, Bedarf visuell zusammen; Gewichte separat). Weniger Zeilenrauschen.

**6. Header-Konsistenz „NÄHRSTOFFBRUDI / KALORIENBRUDI"** (beide)
Zwei verschiedene Klein-Kapitälchen-Labels wirken zufällig. → Ein einheitliches Overline-System (gleiche Größe, gleicher Letter-Spacing, gleiche Farbe), Personen-Akzent nur im H1-Namen.

**7. Datenqualitäts-Warnung visuell definieren** (Mobil)
Der Warnhinweis hat unklaren Border und schwachen CTA. → Als echte Alert-Komponente mit Icon links, gelbem 3-px-Left-Accent, „Details ansehen →" als Button-Link (nicht unterstrichen im Fließtext).

**8. Chart-Achsen & Zielinie kontrastärmer, Bars entsättigen** (Mobil, Wochendurchschnitt)
Blaue Bars sind sehr gesättigt und dominieren. → Bars auf 70 % Sättigung, gestrichelte Ziellinie in dezentem Grün-Grau statt kräftig, Zahlen über Bars in regular statt bold für ruhigeren Eindruck.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`