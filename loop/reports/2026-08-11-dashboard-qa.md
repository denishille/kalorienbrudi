# Dashboard-QA (Funktion + UX/Design) — 2026-08-11

**Funktion:** 1 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🔴 JS-Konsolenfehler: Failed to load resource: the server responded with a status of 404 ()

## UX-/Design-Bewertung (Claude Vision)

# Gesamtnote: 6.5 / 10

Solide Datenvisualisierung mit gutem Dark-Theme-Ansatz, aber inkonsistente Typografie, Ausrichtungsfehler und ein kaputter Layout-Zustand im Desktop-Screenshot ziehen die Note runter.

---

## Konkrete Verbesserungen (priorisiert)

**1. Sticky-Tab-Bar-Overlap fixen (Desktop) — KRITISCH**
Betroffen: KALORIEN/NÄHRSTOFFE-Toggle über der Nährstoffliste. Ziel: Die Tab-Leiste überlappt aktuell den Donut-Chart-Bereich und wirkt wie ein Rendering-Bug. Toggle als eigenständige, korrekt umflossene Zeile mit klarem Abstand (min. 24px) oberhalb der Liste platzieren, kein Overlay.

**2. Monospace-Sekundärtext ersetzen**
Betroffen: Alle Werte wie „2,16 / 20 µg", „ZEITFENSTER", „28 gut · 43 neutral". Ziel: Die Mono-Font wirkt technisch/roh. Auf eine tabellarische Variante der Haupt-Sans (`font-variant-numeric: tabular-nums`) umstellen — behält Ausrichtung, wirkt moderner und konsistenter.

**3. Prozent-Labels an Balken vertikal zentrieren & vereinheitlichen**
Betroffen: Nährstoffliste, rechte %-Spalte. Ziel: Prozente konsistent rechtsbündig ausrichten, gleiche Baseline wie Balken. Farbcodierung der %-Zahl aktuell redundant zum Balken — stattdessen %-Text neutral (weiß) und nur Balkenfarbe als Status nutzen, reduziert visuelle Unruhe.

**4. Checkpoint-Karten: Hierarchie schärfen**
Betroffen: 4 Health-Checkpoint-Karten (Darmgesundheit etc.). Ziel: Score-Badge (61/100) ist gleich stark wie Titel. Score größer und als Primärelement setzen, Statuswort („Okay") mit definierter Farbskala, Detailzeile in gedämpftem Grau kleiner. Einheitliche Kartenhöhe erzwingen (aktuell brechen Zeilen unterschiedlich).

**5. Farbskala Ampel konsistent definieren**
Betroffen: Gelb/Grün/Rot über Donut, Balken, Badges, Bar-Chart. Ziel: Aktuell mehrere Gelb-/Grüntöne. Ein Design-Token-Set festlegen (z.B. success/warning/critical), überall identisch. Das Kritisch-Rot (35/100) sollte kräftiger/gesättigter als das Warning-Gelb sein.

**6. Whitespace & Ausrichtung Kennzahl-Tabelle (Mobil)**
Betroffen: „Ziel / Kalorienziel / Startgewicht…" Zeilen. Ziel: Label links, Wert rechts mit klarer Baseline. Einheiten (kcal, kg) konsistent kleiner & gedämpft neben dem Wert. Trennlinien dünner (0.5px, niedrigerer Kontrast) für cleaneren Look.

**7. Bar-Chart „Zielerreichung" lesbarer machen**
Betroffen: Mobil, Diverging-Balken pro Tag. Ziel: Nulllinie visuell als vertikale Referenzlinie markieren, Werte (+400/-128) konsistent außerhalb der Balken, gleiche Balkenhöhe. Aktuell schwer erkennbar, was positiv/negativ bedeutet — kurze Legende oder Achsenbeschriftung ergänzen.

**8. Datenqualitäts-Hinweis prominenter, aber ruhiger**
Betroffen: „27 Tage ohne Kalorien-Eintrag"-Box. Ziel: Warngelb ist ok, aber Box wirkt textlastig. Icon + kompakte Warnung, „Details ansehen" als klarer sekundärer Button-Style statt Textlink mit Pfeil.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`