# Dashboard-QA (Funktion + UX/Design) — 2026-08-26

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung Nährstoffbrudi Dashboard

## Gesamtnote: **6,5 / 10**

Solide Datenvisualisierung mit gutem dunklem Theme und klarer Farbcodierung (Ampel). Es fehlt jedoch an konsistenter vertikaler Rhythmik, einheitlicher Typo-Skala und Polish im Detail. Der Header-Bereich wirkt hochwertig, die Listenbereiche eher generisch.

---

## Konkrete Verbesserungen (priorisiert)

**1. Sticky-Tab-Bar (Desktop) reparieren — HOCH**
Element: „Kalorien / Nährstoffe“-Toggle + „Denis“-Selector überlappen halbtransparent den Gesamtdeckungs-Chart und die Nährstoffliste. Ziel: Als eigenständige, undurchsichtige Sticky-Leiste mit klarer Trennlinie/Shadow oben fixieren, kein Content-Overlay.

**2. Typo-Skala vereinheitlichen — HOCH**
Element: Karten-Werte (61/100, 153 mg), Sektions-Header, Balken-Labels nutzen zu viele Größen/Weights. Ziel: 4-stufige Skala definieren (Display 32/H2 20/Body 14/Caption 12), Werte durchgängig `tabular-nums` für saubere Zahlen-Ausrichtung.

**3. Balkenliste: Grid-Ausrichtung + Zebra/Zeilenhöhe — HOCH**
Element: Nährstoff-Balken (Jod, Vitamin C …). Labels links, Balken mittig, %-Wert rechts stehen unsauber im Verhältnis. Ziel: festes 3-Spalten-Grid (200px / 1fr / 60px), einheitliche Zeilenhöhe 56px, dezente Ziel-100%-Markierungslinie in jeder Bar für Kontext.

**4. Kontrast der Sekundärtexte erhöhen — MITTEL**
Element: graue Metadaten („6 getrackte Tage“, „Ballaststoffe, Fermentiertes…“, Footer). Aktuell unter WCAG-AA. Ziel: von ~#6b7280 auf mind. #9ca3af anheben (Kontrast ≥ 4,5:1).

**5. Karten-Konsistenz Checkpoints — MITTEL**
Element: 4 Gesundheits-Checkpoint-Karten. Text „Okay/Kritisch/Gut“ + Zahlenblöcke unterschiedlich lang → uneinheitliche Höhen. Ziel: gleiche Kartenhöhe, Statuswort als farbiges Badge (statt reiner Textfarbe), Icon oben links konsistent platzieren.

**6. Gesamtdeckungs-Ring aufwerten — MITTEL**
Element: 73%-Donut. Wirkt isoliert und flach. Ziel: dünnerer Ring, Gradient (rot→gelb→grün entlang Fortschritt), Mini-Legende/Sub-Value darunter, Karte mittig statt linksbündig-leer.

**7. Mobile: Stat-Cards & Chart-Spacing — MITTEL**
Element: 41/44/8/93-Kacheln + Balkencharts. Große Zahlen dominieren, Labels zu klein; Balkenchart „Zielerreichung“ hat inkonsistente Bar-Radien/Abstände. Ziel: einheitliche Card-Paddings (16px), Label 13px/medium, alle Bars gleiche corner-radius (6px) und Baseline-Grid.

**8. Farbsystem tokenisieren — NIEDRIG**
Element: Grün/Gelb/Rot in Badges, Bars, Text variieren leicht in Sättigung. Ziel: 3 semantische Tokens (success/warning/danger) je in Text-, Fill-, Bg-Variante definieren und überall referenzieren.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`