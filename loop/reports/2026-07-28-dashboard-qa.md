# Dashboard-QA (Funktion + UX/Design) — 2026-07-28

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 6.5 / 10

Solide Datengrundlage und stimmiges Farbsystem (Ampel), aber visuelle Hierarchie, Whitespace und ein kritischer Overlay-Bug ziehen die Note runter. Wirkt datenlastig statt „premium clean".

---

## Konkrete Verbesserungen (priorisiert)

**1. [KRITISCH] Overlay-Bug beheben — Tab-Bar/Profil-Switcher (Desktop)**
Der schwebende „KALORIEN / NÄHRSTOFFE"-Toggle + Denis-Dropdown überlagert die Nährstoff-Tabelle (abgeschnittener Header „…gedeckt bei 100%").
→ Zielzustand: Toggle als fixierte oder klar abgesetzte Segmented-Control **über** der Tabelle mit eigenem Container + ausreichend Padding-top für die Liste. Keine Überlappung.

**2. Nährstoff-Balken: Ziellinie + Ordnung — Bar-Liste (Desktop)**
16 Balken ohne 100%-Referenzmarke; Sortierung von schlecht→gut ist ok, aber Overachiever (177%) überzeichnen visuell.
→ Zielzustand: Vertikale 100%-Marker-Linie in jeder Bar; Werte >100% clampen/kappen mit Overflow-Indikator. Prozent rechts konsistent rechtsbündig ausrichten.

**3. Header-Wortmarke straffen — „NÄHRSTOFFBRUDI / KALORIENBRUDI"**
Der Kicker wirkt inkonsistent (zwei verschiedene Wortmarken) und billig neben dem großen Titel.
→ Zielzustand: Eine feste Wortmarke, Titel „Dashboard · Denis" mit dezenterem Trenner statt Farbwechsel im Wort. Konsistenter Kicker in beiden Views.

**4. Whitespace & Card-Rhythmus — Gesundheits-Checkpoints (Desktop)**
Karten sind textlich überladen (Score, Label, Zahlen, Fußnote) → dichte, unruhige Blöcke.
→ Zielzustand: Klare 3-Zeilen-Hierarchie: (1) Titel+Badge, (2) großer Status, (3) EIN Detail-Chip. Fußnote als Tooltip auslagern. Mehr vertikaler Innenabstand.

**5. Donut „73%" ausbalancieren — Gesamtdeckung (Desktop)**
Riesiger leerer Raum rechts, Donut wirkt isoliert links.
→ Zielzustand: Donut + Kennzahl links, rechts 2–3 Mini-Stats (bester/schlechtester Nährstoff, Trend) zur Raumfüllung, statt einer einzelnen Textzeile.

**6. Typo-Skala vereinheitlichen — global**
Zu viele Größen/Gewichte (Kicker caps, große Zahlen, graue Mono-Ziffern „3,92 / 20 µg"). Mono-Werte wirken technisch.
→ Zielzustand: Max. 3 Textrollen (Display, Body, Caption), Mikrowerte in derselben Sans wie Rest, Font-Feature „tabular-nums" statt Monospace.

**7. Balkendiagramm-Kontrast — Wochendurchschnitt (Mobil)**
Kräftige Blaubalken vs. blasse gestrichelte Ziellinie → Ziel-Überschreitung schwer erkennbar.
→ Zielzustand: Balken oberhalb Ziel farblich einfärben (rot/gelb), Ziellinie kräftiger + Label als Pill. Direct-Labels dezenter (kleiner, grau).

**8. Ampel-Kontrast prüfen — Gelb-Töne (Beide)**
Mittlere Werte nutzen sehr ähnliche Gelb-/Ockertöne (Vitamin C bis Magnesium) → schwer differenzierbar, WCAG-Kontrast von Gelb auf Dunkel grenzwertig für Text.
→ Zielzustand: 4-Stufen-Palette mit klareren Delta-Sprüngen; Prozent-Text nie in Sättigungsgelb, sondern helle Neutralfarbe + farbiger Balken.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`