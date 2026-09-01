# Dashboard-QA (Funktion + UX/Design) — 2026-09-01

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Design/UX-Review – Nährstoff/Kalorien-Dashboard

## Gesamtnote: **6,5 / 10**

Solide Basis, gute Ampel-Logik und lesbare Bar-Charts. Aber: inkonsistente Layers (überlappende Tab-Leiste im Desktop), schwacher Kontrast bei Meta-Text, und die Cards wirken flach/gleichförmig – zu wenig visuelle Hierarchie für ein „Top“-Produkt.

---

## Konkrete Verbesserungen (priorisiert)

**1. [KRITISCH] Überlappende Tab-Leiste (Desktop)**
Die schwebende Leiste „KALORIEN / NÄHRSTOFFE / Denis“ liegt halbtransparent *über* Gesamtdeckung + erster Chart-Zeile → Screenshot 1 wirkt kaputt. Zielzustand: fixe Leiste als eigener Sticky-Header mit vollflächigem Hintergrund + Body-Padding-Top, keine Überdeckung von Content.

**2. [HOCH] Meta-Text-Kontrast erhöhen**
Zeilen wie „25.08.2026 – 31.08.2026 · 7 getrackte Tage“, Footer und Sublabels liegen bei ~2:1 Kontrast. Zielzustand: mind. WCAG AA (4.5:1) → Grauwert von #555 auf ~#9AA0A6 anheben.

**3. [HOCH] Visuelle Hierarchie der Checkpoint-Cards**
Vier Cards sind völlig gleichrangig, obwohl „Kritisch/26“ Aufmerksamkeit braucht. Zielzustand: farbiger linker Border-Akzent oder subtiler Tint pro Status (rot/gelb/grün) + Status-Wort größer als Zahlen-Detail.

**4. [MITTEL] Bar-Charts: Zielmarke + Achsen (Nährstoffe)**
Bars zeigen % ohne visuelle 100%-Referenzlinie. Zielzustand: vertikale gestrichelte Linie bei 100%, damit „Überversorgung“ (147% Selen) sofort erkennbar; Werttext (`984 / 1.000 mg`) rechtsbündig unter Namen für ruhigeres Alignment.

**5. [MITTEL] KPI-Cards Mobil vereinheitlichen (45/47/8/100)**
Riesige Zahlen sind gut, aber Farben (grün/gelb/rot/blau) wirken willkürlich neben identischer Card-Optik. Zielzustand: konsistente Zahlengröße, Farbe nur als kleiner Status-Dot + Prozent, Zahl neutral weiß → weniger „Ampel-Rauschen“.

**6. [MITTEL] Whitespace/Rhythmus im Nährstoff-Listing**
Zeilenhöhen eng, Trennung nur durch Farbe der Bar. Zielzustand: konsistenter 8px-Spacing-Grid, dezente Zeilentrennung (1px, 4% Opacity) und ausgerichtete rechte %-Spalte in Monospace.

**7. [NIEDRIG] Typografie-Konsistenz**
Mischung aus normaler Sans (Headlines) und Monospace-Zahlen mit Letter-Spacing wirkt teils uneinheitlich (Header vs. „ZEITFENSTER“). Zielzustand: max. 2 Schriftrollen definieren – Display für Headline/Werte, ein Mono-Stil *nur* für tabellarische Zahlen.

**8. [NIEDRIG] Wochendurchschnitt-Chart (Mobil)**
Nur 3 Balken mit stark unterschiedlicher Datenbasis (7/7/1 Tag) → „1.055“ vs „2.201“ ist irreführend. Zielzustand: unvollständige Woche visuell markieren (schraffiert/geringere Opacity) + Ziel-Linie beschriften direkt am Wert.

---

**Quick-Win-Reihenfolge:** #1 → #2 → #3 → #4

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`