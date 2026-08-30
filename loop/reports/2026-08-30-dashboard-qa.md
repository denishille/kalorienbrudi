# Dashboard-QA (Funktion + UX/Design) — 2026-08-30

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Design/UX-Review · Nährstoff/Kalorien-Dashboard

## Gesamtnote: **6,5 / 10**

Solide Datendichte und funktional durchdacht, aber die visuelle Hierarchie ist flach, Typo-Größen springen inkonsistent, und der Übergang zwischen den Sektionen (v.a. der überlappende Tab-Header auf Desktop) wirkt unfertig. Mit gezielten Fixes schnell auf 8+ hebbar.

---

## Konkrete Verbesserungen (priorisiert)

**1. Überlappenden Tab-Bar / Content-Bruch fixen (Desktop, kritisch)**
Der Segmented-Control „Kalorien/Nährstoffe" + „Denis"-Selector klebt halbtransparent über dem Balkendiagramm (Zeile „2,18 / 20 µg" wird angeschnitten). → Tab-Bar als sticky, opaker Header mit klarer Trennlinie oben auf die Nährstoffkarte setzen; darunter beginnt der Content sauber mit vollem Whitespace.

**2. Balken-Charts: Zielmarke + Klassifizierungsschwellen visualisieren (beide)**
Die Prozent-Balken haben keinen Referenzpunkt. → Vertikale 100%-Ziellinie einziehen und Farbschwellen (rot <50 / gelb 50–99 / grün ≥100) über eine dezente Skala verankern. Aktuell muss man die Zahl rechts lesen, um Farbe zu deuten – redundant und schwer scanbar.

**3. Typografische Hierarchie vereinheitlichen (beide)**
Werte wie „59/100", „289 mg", Prozentzahlen und Nährstoffnamen nutzen zu ähnliche Größen. → 3-stufige Skala definieren: Metrik-Zahl (bold, groß), Label (medium, gedämpft), Einheit (klein, 60% Opacity). Monospace nur für Zahlen-Tabellen konsistent einsetzen (aktuell mal Mono, mal nicht).

**4. Checkpoint-Karten: Farbcodierung an Ampel-Status koppeln (Desktop)**
„Kritisch" (Säure-Base, rot) sieht fast identisch aus wie „Okay"/„Gut". → Linken Card-Border oder Status-Badge kräftig einfärben (rot/gelb/grün), Score-Ring/Bar als Mini-Visual ergänzen. Aktuell trägt nur der Text die Bedeutung.

**5. Whitespace & Card-Konsistenz (beide)**
Padding variiert zwischen Karten (Checkpoints eng, Gesamtdeckung-Block großzügig). → Einheitliches 8pt-Grid, gleiche Innenabstände (24px) und identische Corner-Radii/Border-Opacity für alle Cards.

**6. Mobile: Tages-Balken „Zielerreichung" lesbarer machen (Mobil)**
Die Diverging-Bars (-191, +9…) sind winzig und die Warn-Icons (⚠) unklar. → Bars höher (min. 32px), Nulllinie deutlich markieren, +/- farblich (grün/rot) konsequent, Zahlen außerhalb des Balkens rechtsbündig.

**7. Kontrast der gedämpften Metadaten anheben (beide)**
Fußzeilen und Sub-Labels („Stand…", „Ballaststoffe, Fermentiertes…") liegen unter WCAG-AA. → Sekundärtext auf min. #9AA0A6 (≥4.5:1) anheben.

**8. Akzentfarbe entzerren (beide)**
Blau markiert gleichzeitig aktive Tabs, „Denis" im Titel, Werte und Chart-Balken – Bedeutung verwässert. → Blau nur für interaktive/aktive Elemente reservieren; Datenwerte neutral weiß, Chart in eigener konsistenter Datenfarbe.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`