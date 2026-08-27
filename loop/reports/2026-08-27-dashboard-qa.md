# Dashboard-QA (Funktion + UX/Design) — 2026-08-27

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# UX-Review: Kalorien-Tracking-Dashboard

## Gesamtnote: **6,5 / 10**

Solide Datenbasis und gute Farbcodierung (Ampel/Grün-Rot), aber inkonsistente Abstände, schwache visuelle Hierarchie bei sekundären Infos und ein gravierender Layout-Bug in Screenshot 1. Wirkt funktional, aber noch nicht „premium".

---

## Konkrete Verbesserungen (priorisiert)

**1. Überlappender Tab-Bar-Bug (Desktop) — KRITISCH**
Betroffen: „KALORIEN/NÄHRSTOFFE"-Umschalter + Nutzer-Dropdown liegen über der Balkenliste, oberster Balken (1,67/20 µg) wird abgeschnitten.
Ziel: Sticky-Header mit eigenem Hintergrund + korrektem `padding-top` auf Content, kein Content-Clipping. Beim Scrollen sauber überlagern (Backdrop-Blur, definierte z-index-Ebene).

**2. Balkenliste: Trennung Label ↔ Wert ↔ Bar schärfen**
Betroffen: Nährstoff-Liste (Desktop).
Ziel: Feste 3-Spalten-Grid (Label links / Bar mittig / % rechts), vertikal zentriert. Grundfarbe des Bar-Tracks minimal aufhellen für sichtbare 100%-Marke. Zielwert-Linie bei 100% als dezente vertikale Guide einziehen.

**3. Farbübergang der Bars zu abrupt**
Betroffen: Rot→Gelb→Grün-Sprünge (49% rot, 58% gelb).
Ziel: Konsistente Schwellen definieren und ggf. weichere Stufung; identische Sättigung/Helligkeit über alle Farben, damit Grün nicht „giftiger" wirkt als Rot. Prozentzahl rechts in gleicher Bar-Farbe = gut, beibehalten.

**4. Checkpoint-Cards: Hierarchie & Höhe angleichen**
Betroffen: 4 Gesundheits-Cards (Desktop).
Ziel: Score-Badge (58/100) und Status-Wort („Okay"/„Kritisch") visuell koppeln — Status kleiner, Score prominenter. Alle 4 Cards gleiche Höhe, Fußnote („Ballaststoffe…=gut") mit gleichem oberen Abstand ausrichten.

**5. Mobile: Zahlen-Kacheln (42/45/8/95) vereinheitlichen**
Betroffen: 4 KPI-Kacheln.
Ziel: Einheitliche Zahlengröße, Label und Sub-Label linksbündig unter der Zahl mit gleichem Baseline-Abstand. Farbige Dots konsistent vor jedem Label. Dezenten Card-Rahmen entfernen oder überall gleich.

**6. Typografie-System vereinheitlichen**
Betroffen: Gesamt (Mix aus Mono-Ziffern, Sans, Letter-Spacing-Labels).
Ziel: Max. 2 Schriftschnitte. Monospace nur für Messwerte/Ziffern, nicht für Fließtext. Uppercase-Labels („ZEITFENSTER", „AKTUELLES ZIEL") konsistent in Größe/Tracking/Farbe (aktuell zu grau, kaum lesbar → Kontrast anheben auf min. 4.5:1).

**7. Whitespace & Sektions-Rhythmus (Desktop)**
Betroffen: Großer Leerraum um „Gesamtdeckung"-Donut, uneinheitliche vertikale Abstände zwischen Sektionen.
Ziel: Einheitliches Spacing-Raster (z.B. 24/32px). Donut-Sektion kompakter oder mit einer zusätzlichen Kern-Info füllen (z.B. Top-3-Defizite als Mini-Liste rechts).

**8. Mobile Wochen-Chart: Zielinie & Achsen klarer**
Betroffen: „Wochendurchschnitt"-Balkendiagramm.
Ziel: Gestrichelte Ziel-Linie (1900) mit klarem Label-Chip am rechten Rand statt überlappend links. Y-Achse mit 2–3 Referenzwerten. Balkenwerte über den Balken beibehalten, aber einheitlich positionieren.

---

**Quick-Wins:** Bug (#1) sofort, dann Grid-Ausrichtung Balkenliste (#2) + Label-Kontraste (#6). Das hebt den Gesamteindruck am schnellsten auf 8/10.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`