# Dashboard-QA (Funktion + UX/Design) — 2026-08-28

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 6.5/10

Solide Datenvisualisierung mit gutem Dark-Theme-Ansatz, aber inkonsistente Abstände, schwache Typo-Hierarchie und ein gravierender Layout-Bug (überlappender Tab-Bar) verhindern einen Premium-Eindruck.

---

## Konkrete Verbesserungen (priorisiert)

**1. [KRITISCH] Sticky-Tab-Bar überlappt Content (Desktop)**
Der „Kalorien/Nährstoffe“-Toggle liegt halbtransparent über der Nährstoffliste und dem Gesamtdeckungs-Ring. → Tab-Bar als klar abgesetzte Sticky-Leiste mit vollem Hintergrund (opak, Blur), definierter Höhe und `scroll-padding-top` für die Liste darunter. Kein Overlap.

**2. Nährstoffliste: fehlende Achse & Referenzlinie**
Die Balken haben keine 100%-Markierung. Werte wie 154% vs. 37% sind nicht schnell einzuordnen. → Vertikale gestrichelte 100%-Ziellinie einziehen, Balken darüber visuell abschneiden/markieren („Overshoot“). %-Werte rechtsbündig auf feste Spaltenbreite ausrichten.

**3. Typografische Hierarchie der Checkpoint-Cards**
„Okay/Kritisch/Gut“ konkurriert farblich mit dem Score-Badge; Fließtext (21 gut · 23 neutral) ist zu klein und blass (Kontrast < AA). → Score-Badge als primäres Element (größer), Status-Wort kleiner darunter, Detailtext auf min. `#A0A0A8` anheben. Einheitliche Card-Innenabstände (aktuell variieren sie).

**4. Farbsystem konsolidieren (Ampel)**
Gelb/Orange-Töne der Bars, Badges und des Rings sind leicht unterschiedlich → wirkt zufällig. → 3-4 feste semantische Tokens definieren (rot/gelb/grün/blau) und überall identisch nutzen. Gelb dunkler abstufen für Kontrast auf hellen Balken (%-Text auf Gelb ist grenzwertig lesbar).

**5. Whitespace & Grid-Konsistenz (Desktop)**
Große leere Fläche im Gesamtdeckungs-Block (rechts vom Text), während Checkpoint-Cards eng wirken. → 8px-Grid durchziehen, Ring-Sektion mit ergänzendem Inhalt füllen (z. B. Top-3-Defizite als Mini-Liste) oder Sektion vertikal kompakter.

**6. Mobile: „Wackelig“-Statusbadge & Datenqualitäts-Box aufwerten**
Der Warn-Block ist textlastig und die Statuspill „44% im grünen Bereich“ liest sich unklar. → Statuspill mit Mini-Progress oder Icon-System, Datenqualitäts-Box als aufklappbares Accordion (nicht default offen), spart Höhe.

**7. Mobile Balkendiagramm „Zielerreichung“**
Werte (+9, +801) kleben an Balkenenden, „-48“ mit Warn-Icon schlecht ausgerichtet. → Konsistente Label-Position (immer außen, feste Baseline in der Mitte für +/-), einheitliche Balkenhöhe, Nulllinie klar markieren.

**8. Header-Redundanz**
„NÄHRSTOFFBRUDI / KALORIENBRUDI“ + „Dashboard Denis“ + User-Switcher „Denis“ = dreifache Namensnennung. → Eyebrow-Label entfernen oder zu dezenter Wortmarke reduzieren; User-Switcher als einzige Personen-Angabe.

---

**Quick Wins:** Overlap-Bug fixen (1), 100%-Referenzlinie (2), Kontraste anheben (3/4). Damit → 8/10 erreichbar.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`