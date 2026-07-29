# Dashboard-QA (Funktion + UX/Design) — 2026-07-29

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# UX/Design-Review – Nährstoff/Kalorien-Dashboard

## Gesamtnote: **6.5 / 10**

Solide Grundstruktur, gute Farbcodierung (Ampel), klare Datenfülle. Aber: inkonsistente Abstände, schwache Karten-Trennung im Dark-Theme, überladene Header und ein kaputt wirkender Übergang beim Tab-Wechsel (Screenshot 1 zeigt überlappende/abgeschnittene Bereiche).

---

## Konkrete Verbesserungen (priorisiert)

**1. [KRITISCH] Tab-Bar-Positionierung (Desktop, Screenshot 1)**
Der „Kalorien / Nährstoffe“-Toggle + User-Switch schwebt mitten im Content und verdeckt/schneidet den Chart-Header ab.
→ Zielzustand: Toggle als sticky Sub-Header direkt unter dem Titel verankern, klare eigene Zeile, kein Overlap. Content beginnt sauber darunter.

**2. Karten-Kontrast & Elevation (beide)**
Die Cards heben sich kaum vom Hintergrund ab (fast gleiches Schwarz).
→ Zielzustand: Card-Background auf `#1A1C1F`, dezenter 1px-Border `rgba(255,255,255,0.08)` + weicher Shadow. Einheitliches `border-radius: 16px`.

**3. Balkendiagramm-Lesbarkeit Nährstoffe (Screenshot 1)**
Track-Hintergrund der Bars ist unsichtbar, 100%-Referenzlinie fehlt, Prozente rechts wirken losgelöst.
→ Zielzustand: sichtbarer Track (`rgba(255,255,255,0.06)`), vertikale 100%-Ziellinie einzeichnen, Prozentwert direkt am Barende platzieren. Values (`54,3 / 110 µg`) in eigener heller Spalte ausrichten.

**4. Header-Redundanz reduzieren (beide)**
„NÄHRSTOFFBRUDI / KALORIENBRUDI“ + „Dashboard Denis“ + User-Switch = dreifache Namensnennung.
→ Zielzustand: Kicker-Label entfernen oder in eine Zeile mit dem User-Dropdown zusammenfassen. Ein H1 „Dashboard“ + Namens-Pill genügt.

**5. Kennzahlen-Kacheln vereinheitlichen (Screenshot 2)**
„33 / 29 / 5 / 67“ – die riesigen Zahlen haben zu wenig Abstand zum Label, Farbcodierung uneinheitlich (67 ist blau, aber neutral).
→ Zielzustand: konsistentes Kachel-Padding (20px), Zahl → 4px → Label → Sublabel, semantische Farben nur für Status (grün/gelb/rot), neutrale KPIs weiß.

**6. Typografie-Skala festziehen (beide)**
Zu viele Schriftgrößen/Weights (Prozente, Values, Labels wirken beliebig). Monospace-Werte teils sperrig getrackt.
→ Zielzustand: definierte Scale (H1 28 / H2 20 / Body 15 / Caption 12), max. 2 Weights (500/700), Letter-Spacing nur bei Uppercase-Kickern.

**7. Ring-Chart „69%“ Platzierung (Screenshot 1)**
Riesige leere Fläche rechts neben Ring + Text.
→ Zielzustand: Ring zentrieren oder Zusatz-Mini-KPIs (Anzahl gut/neutral/schlecht) rechts einfügen, Whitespace füllen.

**8. Diverging-Chart „Zielerreichung“ (Screenshot 2)**
Balken haben keine gemeinsame Nulllinie / Achse – Vergleich +355 vs -310 schwer lesbar.
→ Zielzustand: sichtbare zentrale 0-Achse, symmetrische Skalierung, Werte konsistent außen am Balkenende.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`