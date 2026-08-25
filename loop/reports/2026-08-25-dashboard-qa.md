# Dashboard-QA (Funktion + UX/Design) — 2026-08-25

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Gesamtnote: 6.5/10

Solide Datenvisualisierung mit klarer Farblogik (Ampel), aber uneinheitliche Hierarchie, schwache Kontraste in Metatexten und ein kaputter Übergang zwischen Sektionen ziehen die Note runter.

---

## Konkrete Verbesserungen (priorisiert)

**1. Sticky-Tab-Bar-Überlappung fixen (Desktop)**
Betroffen: Tab-Leiste „KALORIEN/NÄHRSTOFFE" schneidet die Gesamtdeckungs-Karte und die erste Nährstoffzeile ab (1,44/20 µg halb verdeckt).
→ Ziel: Tab-Bar als echtes Sticky-Element mit Hintergrund + Schatten, klarer Content-Padding-Offset (mind. 24 px), keine Überlappung mit Cards.

**2. Kontrast der Metatexte anheben**
Betroffen: Beschreibungszeilen („Ballaststoffe, Fermentiertes…", „weniger ist besser…", Werte „35 / 200 µg").
→ Ziel: von ~#6B7280 auf mind. #9CA3AF (WCAG AA), Mono-Werte in konsistenter Farbe statt fast-unsichtbarem Grau.

**3. Bar-Chart-Achse & Zielmarkierung sichtbar machen**
Betroffen: Nährstoff-Balken haben keine 100%-Referenzlinie; man erkennt „gedeckelt bei 100%" nicht visuell.
→ Ziel: dünne vertikale 100%-Linie + Ziel-Tick, Balken >100% klar abgesetzt (z.B. gestrichelter Überhang statt gleiche Fläche).

**4. Card-Typografie vereinheitlichen (Checkpoints)**
Betroffen: „Okay/Kritisch/Gut" konkurrieren farblich mit Score-Badges; Score-Badge, Titel und Statuswort haben keine klare Rangfolge.
→ Ziel: Titel = weiß/medium, Score-Badge = sekundär, Statuswort als kleines Label unter dem Score; einheitliche vertikale Struktur pro Card.

**5. Whitespace-Rhythmus & Card-Höhen angleichen**
Betroffen: Checkpoint-Cards haben ungleiche Textlängen → unruhige Unterkanten. Große leere Fläche unter Gesamtdeckungs-Donut.
→ Ziel: gleiche Card-Höhe (min-height), Donut vertikal zentriert, Padding-System auf 8px-Grid normalisieren.

**6. Prozent-Labels rechtsbündig ausrichten (Chart)**
Betroffen: „7%/50%/52%…" rechts stehen optisch flatternd, Farbe springt (rot/gelb/grün) ohne Ausrichtung.
→ Ziel: feste Label-Spalte rechts, rechtsbündig, tabellarische Ziffern (font-variant-numeric: tabular-nums).

**7. Mobile Balkendiagramm „Zielerreichung" lesbarer**
Betroffen: Balken laufen aus dem Container (+673, +450 rechts abgeschnitten), Werte kleben am Rand.
→ Ziel: Balken skalieren auf Container-Breite mit Innen-Padding, Werte innerhalb oder klar abgesetzt, keine Clipping-Kante.

**8. „Dashboard Denis"-Titel + Kicker konsistent branden**
Betroffen: Zwei verschiedene Kicker („NÄHRSTOFFBRUDI" vs „KALORIENBRUDI") wirken inkonsistent; blauer Name kollidiert leicht mit Tab-Blau.
→ Ziel: einheitlicher Brand-Kicker, Namen-Akzent in eigenem Accent-Ton oder als Chip, damit Tab-Blau die primäre Interaktionsfarbe bleibt.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`