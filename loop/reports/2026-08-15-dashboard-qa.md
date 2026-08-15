# Dashboard-QA (Funktion + UX/Design) — 2026-08-15

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 6.5 / 10

Solide Datenvisualisierung mit gutem Dark-Theme-Ansatz und starkem Ampel-Farbsystem. Größtes Problem: ein **überlappender, sticky Tab-Bar** (Kalorien/Nährstoffe), der Content abschneidet, plus inkonsistente Typo-Hierarchie und schwacher Whitespace-Rhythmus.

---

## Konkrete Verbesserungen (priorisiert)

**1. [KRITISCH] Sticky-Navbar überlappt Cards**
Element: Kalorien/Nährstoffe-Tab + Denis-Dropdown (Desktop).
Problem: Der Balken liegt über den Checkpoint-Cards und schneidet „24 gut · 53 neutral · 17…" ab.
Ziel: Navbar oben fixieren *oder* Content-Padding-top so setzen, dass keine Card verdeckt wird. Karten müssen vollständig lesbar sein.

**2. [HOCH] Checkpoint-Cards abgeschnitten**
Element: Gesundheits-Checkpoints (Darmgesundheit, Low FODMAP etc.).
Problem: Beschreibungszeile unter „Okay/Kritisch" wird abgeschnitten, Cards wirken unfertig.
Ziel: Feste Card-Höhe mit vollständigem Inhalt, einheitlicher unterer Abstand von 16–24px zum Card-Rand.

**3. [HOCH] Zahlen-Typografie vereinheitlichen**
Element: Werte-Labels (`1,86 / 20 µg`), Prozente, Datumsangaben.
Problem: Monospace-Ziffern gemischt mit unterschiedlichen Größen wirken technisch/inkonsistent; die kleinen grauen Werte sind bei ~11px zu schwach.
Ziel: Eine einzige Tabular-Number-Schrift, min. 13px, Kontrast auf ≥ WCAG AA (aktuell Graustufe ~#8a8a8a zu dunkel).

**4. [MITTEL] Balkendiagramm-Skala + 100%-Marker**
Element: Mikronährstoff-Bars.
Problem: Kein visueller 100%-Referenzstrich; Werte >100% (Selen 170%) sprengen mental die Skala ohne Ankerpunkt.
Ziel: Vertikale gestrichelte 100%-Linie einziehen, Bars ab 100% klar markieren (z.B. gedämpftes Grün + Overflow-Kappe). Prozent-Label linksbündig zum Bar-Ende statt ganz rechts abgesetzt.

**5. [MITTEL] Whitespace-Rhythmus & Card-Abstände**
Element: Gesamt-Layout Desktop.
Problem: Uneinheitliche Abstände (Header eng, Cards weit, Bars dicht). Kein erkennbares 8pt-Grid.
Ziel: Durchgängiges 8px-Spacing-System, Sektionsabstände 48px, Card-Innenpadding 24px – erzeugt ruhigeres, „teureres" Gesamtbild.

**6. [MITTEL] Kreis-Progress (67%) aufwerten**
Element: Gesamtdeckungs-Donut.
Problem: Wirkt flach, dünner Ring, keine visuelle Verbindung zur Farbskala der Bars.
Ziel: Farbverlauf im Ring (rot→gelb→grün analog Bars), dickerer Stroke, dezenter Glow – als Hero-Element inszenieren.

**7. [NIEDRIG] Mobile: Karten-Grid & Ziel-Marker**
Element: Stat-Cards (78/6/0/84) + Wochendurchschnitt-Chart mobil.
Problem: 4 Zahlen-Cards ohne Icons wirken beliebig; Ziel-Linie (2900) im Balkenchart schwer ablesbar.
Ziel: Kleine Icons + einheitliche Card-Höhe; Ziel-Linie mit Label-Chip am rechten Rand fixieren.

**8. [NIEDRIG] Titel-Branding konsistent**
Element: „NÄHRSTOFFBRUDI" / „KALORIENBRUDI" Eyebrow-Labels.
Problem: Zwei Marken-Wordings für dieselbe App verwirren.
Ziel: Ein konsistenter Produktname als Eyebrow; Ansicht per Tab-Zustand differenzieren, nicht per Marke.

---

**Quick Wins zuerst:** #1 + #2 (Overlap/Clipping) sofort fixen – sie ziehen die wahrgenommene Qualität am stärksten runter.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`