# Dashboard-QA (Funktion + UX/Design) — 2026-08-24

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 6,5 / 10

Solide Datenvisualisierung mit klarer Farb-Semantik (rot→grün), aber es fehlt Feinschliff bei Hierarchie, Konsistenz und Whitespace. Wirkt an mehreren Stellen „selbstgebaut“ statt Produkt-poliert.

---

## Konkrete Verbesserungen (priorisiert)

**1. Tab-Navigation fixieren & Layer-Bug beheben (Desktop)**
Der Tab-Balken (KALORIEN/NÄHRSTOFFE) + Denis-Switcher überlappt den Nährstoff-Chart und schwebt mittendrin. → Als sticky Sub-Header oben unter dem Titel verankern, mit klarer Trennlinie/Backdrop-Blur. Kein Content darf dahinter durchscheinen.

**2. Nährstoff-Bars: Zielmarke & Skalierung**
Die Balken haben keine sichtbare 100%-Referenzlinie; „113/115/120%“ sehen visuell gleich lang aus wie 99%. → Vertikale 100%-Ziellinie einziehen, Balken bis Ziel füllen und Overflow als abgesetztes Segment (z. B. dunkleres Grün) zeigen. Prozentwerte rechtsbündig auf einheitlicher x-Achse.

**3. Checkpoint-Cards vereinheitlichen**
Cholesterin bricht das Muster (kein „x gut/neutral/schlecht“, andere Einheit). Score-Badges (59/100 vs. 192 mg) sind inkonsistent. → Einheitliches Card-Template: Titel + Score-Badge + Status-Wort + 3-teilige Verteilung + Fußnote. Cholesterin auf gleiche Struktur mappen oder optisch als „anderer Typ“ klar markieren.

**4. Typografie-Hierarchie schärfen**
Zu viele ähnliche Graustufen/Größen (Labels, Werte, Fußnoten verschwimmen). → Klare Skala: Label 12px caps muted, Wert 15px weiß, Fußnote 11px 55% Opacity. Zahlen durchgängig tabellarische Ziffern (font-variant-numeric: tabular-nums) für saubere Ausrichtung.

**5. Donut „Gesamtdeckung“ aufwerten & Whitespace fixen**
Der 73%-Donut steht sehr isoliert in einer riesigen halbleeren Card. → Rechts kompakte Legende/Mini-Stats (z. B. „6 unter Ziel · 4 im Ziel“) ergänzen, Card-Höhe reduzieren. Farbe des Rings semantisch an Ampel koppeln.

**6. Mobile: „Datenqualität“-Warnung deutlicher**
18 unbewertete Tage sind kritisch für die Aussagekraft, aber als dezente gelbe Box versteckt. → Als aktionsorientierter Banner mit klarem CTA-Button („Tage nachtragen“) statt Text-Link. Gleiches Thema im Desktop sichtbar machen (fehlt dort).

**7. Balken-Charts Mobile: Achsen & Labels**
„Zielerreichung“ und „Wochendurchschnitt“ haben inkonsistente Wertelabels (mal im Balken, mal daneben, mal überlappend wie „760“). → Werte konsequent außerhalb des Balkens, Nulllinie visuell markieren (Defizit links / Überschuss rechts klar getrennt).

**8. Farb- & Kontrast-Konsistenz**
Die Gelb-/Gold-Töne (Ampel „okay“) sind auf Dark-BG grenzwertig lesbar und variieren leicht zwischen Bars und Text. → Einen definierten Ampel-Token-Satz (red/amber/green mit ≥4.5:1 Kontrast) über alle Komponenten erzwingen.

---

**Quick Wins:** Tabular-Nums, Ziellinie in Bars, Tab-Overlap fixen → hebt die Wahrnehmung sofort spürbar Richtung 8/10.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`