# Dashboard-QA (Funktion + UX/Design) — 2026-08-06

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# UX/Design-Review – Kalorien-Dashboard

## Gesamtnote: **6,5 / 10**

Solide Grundstruktur, gutes Dark-Theme, klare Farbcodierung (Ampel). Aber: schwebende Toolbar zerschneidet den Fluss, inkonsistente Abstände, Chart-Lesbarkeit teils schwach, Hierarchie oben unentschieden.

---

## Konkrete Verbesserungen (priorisiert)

**1. Schwebende Tab-Leiste (Kalorien/Nährstoffe + Denis) — Desktop**
Problem: Der halbtransparente Balken liegt mitten über der Nährstoff-Liste und schneidet Spaltenüberschriften ab (unlesbar, wirkt wie Rendering-Bug).
Ziel: Toolbar sticky an den Seitenkopf ankern (unter Titel), voll deckend, mit klarer Trennlinie. Content-Bereich mit `padding-top` darunterschieben, damit nichts verdeckt wird.

**2. Header-Hierarchie oben**
Problem: „NÄHRSTOFFBRUDI" / „KALORIENBRUDI" als Kicker über „Dashboard Denis" wirkt zufällig und konkurriert mit dem H1.
Ziel: Kicker deutlich kleiner + gedämpfter (z. B. 11px, 60% Opacity, letter-spacing). H1 bleibt dominant. Nutzer-Switch nach rechts oben, konsistent auf beiden Screens.

**3. Nährstoff-Balken: Zielmarkierung fehlt**
Problem: Balken zeigen % aber keine visuelle 100%-Referenzlinie; „108%/137%/144%" sehen aus wie normale volle Balken.
Ziel: Vertikale 100%-Markierung im Track einzeichnen. Überschreitungen visuell abheben (z. B. gedämpftes Grün oder Warn-Ton bei >130%, da „viel" nicht immer „gut" ist).

**4. Karten-Metriken Konsistenz (Checkpoints)**
Problem: „270 mg" (Cholesterin) mischt sich mit „60/100"-Scores in identischer Badge-Optik → semantisch verwirrend.
Ziel: Einheitliches Score-Format (alle /100 ODER Trennung: Score-Badge vs. Wert-Badge klar unterschiedlich stylen). Badges gleich breit/aligned.

**5. Spacing & Alignment**
Problem: Uneinheitliche vertikale Abstände zwischen Sektionen (Checkpoints→Gesamtdeckung großer Gap, dann gedrängt). Prozent-Spalte rechts nicht rechtsbündig sauber.
Ziel: 8px-Grid durchziehen, feste Sektions-Abstände (z. B. 48px). %-Werte rechts numerisch rechtsbündig (tabular-nums).

**6. Chart-Lesbarkeit „Zielerreichung" (Mobil)**
Problem: Divergierendes Balkendiagramm mit Nulllinie ist schwer lesbar; Werte-Labels sitzen mal innen, mal außen; positive (+400 gold) vs. negative (grün) Logik nicht erklärt.
Ziel: Klare Nulllinie beschriften, Legende „unter Ziel = grün / über = gold", Labels konsistent außerhalb des Balkens, gleiche Balkenhöhe.

**7. Whitespace „Gesamtdeckung"-Karte**
Problem: Großer leerer Raum rechts neben dem Donut, Karte wirkt halbleer.
Ziel: Rechts Mini-Zusammenfassung (z. B. „3 kritisch · 4 gut" Chips) oder Sparkline-Trend einfügen. Donut leicht kleiner, Text vertikal zentriert.

**8. Kontrast Sekundärtext**
Problem: Beschreibungszeilen („Ballaststoffe, Fermentiertes…", Footer) sehr dunkelgrau, unter WCAG-Kontrast.
Ziel: Sekundärtext auf min. #9AA0A6 (Kontrast ≥4.5:1) anheben; Monospace-Werte („2,4 / 20 µg") auf konsistente Farbe/Größe.

---

**Quick-Win-Reihenfolge:** 1 → 8 → 3 → 4 (sofort spürbar bei minimalem Aufwand).

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`