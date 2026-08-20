# Dashboard-QA (Funktion + UX/Design) — 2026-08-20

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Gesamtnote: 6.5/10

Solide Datendichte und gute Farb-Semantik (Ampel), aber inkonsistente Ausrichtung, schwache Hierarchie in Karten und ein kaputt wirkender Sticky-Nav-Übergang ziehen die Note runter.

---

## Konkrete Verbesserungen (priorisiert)

**1. Sticky-Bar / Overlap-Bug fixen (Desktop, kritisch)**
Die Tab-Leiste „KALORIEN/NÄHRSTOFFE + Denis" liegt halbtransparent über der Nährstoffliste und schneidet Zeile „…2,81/20 µg / 14%" ab. → Sticky-Header mit vollflächigem Hintergrund (kein Alpha), sauberem `padding-top` am Content, damit keine Zeile verdeckt wird.

**2. Nährstoff-Balken: Skala & Ausrichtung vereinheitlichen (Desktop)**
Balken enden willkürlich, Prozent-Spalte rechts ist optisch entkoppelt. → Feste 100%-Track-Breite mit sichtbarem Rest-Track (schon vorhanden), Label + Wert linksbündig in fixer Spaltenbreite (z.B. 160px), Prozent rechtsbündig in eigener Spalte. Werte „41,8 / 110 µg" typografisch in gedämpftem Grau, Nährstoffname als Medium-Weight.

**3. Checkpoint-Karten: Hierarchie & Status-Chip (Desktop)**
„Kritisch/Okay" konkurriert farblich mit Score-Chip; Detailzeilen wirken gequetscht. → Status als klarer Badge unter dem Titel, Score-Chip einheitlich (alle als „/100" ODER Einheit, aktuell Bruch: Cholesterin „364 mg" ohne Skala). Zeilenabstand der „11 gut · 14 neutral" erhöhen, Fußnote optisch als Caption abtrennen (Divider oder mehr Whitespace).

**4. Donut „64% Gesamtdeckung" ausbalancieren (Desktop)**
Riesiger Leerraum rechts, Donut alleinstehend. → Sektion mit 2–3 Kern-KPIs neben dem Donut füllen (z.B. „16 Mikronährstoffe · 3 im grünen Bereich"), oder Donut kleiner + Mini-Legende. Card-Höhe an Inhalt anpassen.

**5. Typografie-System konsolidieren (beide)**
Mix aus Monospace (Zahlen), Sans, unterschiedlichen Tracking-Werten wirkt uneinheitlich. → Ein Zahlen-/Label-System: Monospace nur für tabellarische Werte, Überschriften einheitlich (Dashboard-Titel, Sektionstitel, Card-Titel = 3 klare Stufen). Uppercase-Labels („ZEITFENSTER", „NÄHRSTOFFBRUDI") mit konsistentem letter-spacing.

**6. Mobile Charts – abgeschnittene Werte (Mobil)**
„Zielerreichung" zeigt „+1…" und „+86…" abgeschnitten am rechten Rand. → Balken-Container-Padding rechts erhöhen oder Labels ins Balkeninnere/über den Balken setzen, damit keine Zahl clippt.

**7. Mobile Balkendiagramm „Wochendurchschnitt" (Mobil)**
Ziellinie („Ziel") überlappt Balken, Balken zu wuchtig/rund. → Gestrichelte Ziellinie durchgehend über volle Breite mit Label rechts außen, Balken schmaler mit dezenteren Ecken, Werte oberhalb konsistent positioniert.

**8. Kontrast der Caption-/Meta-Texte anheben (beide)**
Fußzeilen und Sekundärtexte („Stand: 19.08…", Sub-Labels) sind grenzwertig lesbar (unter WCAG AA). → Sekundärtext auf min. 4.5:1 anheben (helleres Grau), Tertiär nur für echte Randinfos.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`