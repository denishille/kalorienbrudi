# Dashboard-QA (Funktion + UX/Design) — 2026-08-16

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 6.5 / 10

Solide Datendichte und gute Farbcodierung (Ampel), aber inkonsistente Hierarchie, schwaches Grid-Alignment und ein technisch defekter Sticky-Tab-Bereich verhindern einen wirklich modernen, cleanen Eindruck.

---

## Konkrete Verbesserungen (priorisiert)

**1. [KRITISCH] Überlappender Tab-Bar (Desktop, „Kalorien/Nährstoffe“ + „Denis“)**
Der floatende Balken deckt die erste Tabellenzeile ab (Vitamin D/„1,71 / 20 µg“ ist abgeschnitten, „5%“ überlappt). Ziel: Sticky-Bar mit korrektem `scroll-padding-top` / Content-Offset, sodach kein Inhalt verdeckt wird. Bar sauber in den Card-Header integrieren.

**2. [Hoch] Karten-Höhen & Grid angleichen (Health-Checkpoints)**
Die 4 Cards haben unterschiedlich lange Texte → ungleiche visuelle Balance, „Cholesterin“ wirkt leer. Ziel: einheitliche Card-Höhe (`align-items: stretch`), konsistente 4-Zeilen-Struktur (Titel · Score · Detail · Fußnote), gleiche vertikale Rhythmik.

**3. [Hoch] Score-Badges vereinheitlichen**
Mix aus „51/100“, „237 mg“ in unterschiedlichen Farbtönen und der Status-Text („Okay/Kritisch/Gut“) doppelt die Ampel redundant. Ziel: eine einheitliche Badge-Komponente (Pill, gleiche Padding/Radius), Status-Wort in Badge-Farbe statt separater Zeile → weniger visuelles Rauschen.

**4. [Mittel] Typografie-Hierarchie schärfen**
Overline-Labels („ZEITFENSTER“, „NÄHRSTOFFBRUDI“) sind in Letter-Spacing/Größe fast wie Body — wirken zufällig. Ziel: klare Skala definieren (Overline 11px/uppercase/muted, H2 20px/600, Body 14px, Caption 12px) und konsequent anwenden. Monospace-Zahlen für alle Messwerte (tabellarische Ausrichtung).

**5. [Mittel] Balkendiagramm Nährstoffe: Achse & Zielmarke**
Es fehlt eine visuelle 100%-Referenzlinie; Werte >100% (Selen 162%, Calcium 165%) sprengen die Skala ohne Kontext. Ziel: vertikale 100%-Ziellinie einzeichnen, Übererfüllung farblich klar (z.B. gedämpftes Grün/Blau) und Balkenlänge auf sinnvolle Skala cappen.

**6. [Mittel] „Gesamtdeckung 64%“ Donut-Sektion nutzt Whitespace schlecht**
Große leere Fläche rechts, Ring links wirkt isoliert. Ziel: Ring mittiger platzieren oder Sektion mit kompakten Mikro-Metriken (Top 3 Defizite) rechts füllen — sonst Sektionshöhe reduzieren.

**7. [Niedrig] Farbkontrast Muted-Text**
Fußnoten-Grau (z.B. „Ballaststoffe, Fermentiertes…“, Datumszeilen) liegt unter WCAG AA auf dunklem BG. Ziel: mind. `#9BA3AF`+ / Kontrast ≥ 4.5:1 anheben.

**8. [Niedrig] Mobile: „Zielerreichung“-Chart-Nulllinie**
Diverging-Bars (+27, -740) haben unklare Mittelachse; Werte klemmen am Balken. Ziel: sichtbare 0-Achse zentriert, Labels konsistent außerhalb der Balken, Farbe grün=positiv/rot=negativ statt alles grün.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`