# Dashboard-QA (Funktion + UX/Design) — 2026-08-03

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# UX/Design-Review – Nährstoff/Kalorien-Dashboard

## Gesamtnote: **6,5 / 10**

Solide Grundstruktur, gutes dunkles Theme, klare Datenlogik. Es fehlt aber Feinschliff bei Ausrichtung, Kontrast, Whitespace und Konsistenz – die App wirkt „gut“, nicht „premium“.

---

## Konkrete Verbesserungen (priorisiert)

**1. Tab-Bar / Nutzer-Switcher (Desktop) – kritischer Layoutfehler**
Der Toggle „Kalorien/Nährstoffe“ + „Denis“ überlappt sichtbar mit dem Content darunter (Header „Spurenelemente…“ ist abgeschnitten, Schatten liegt über Balken). → Als **sticky Sub-Header mit eigener, geschlossener Fläche und ausreichend `padding-bottom` (min. 32px)** verankern, kein Overlay über der Liste.

**2. Kontrast der roten Prozent-/Statuswerte erhöhen**
Rot auf Schwarz (z. B. „17%“, „Kritisch“) unterschreitet WCAG AA. → Rot auf **min. #FF6B6B / helleren Ton** anheben, Werte in **Tabular-Figures + Semibold** setzen. Betrifft alle Balken-%-Werte und Checkpoint-Status.

**3. Balkenliste (Nährstoffe): Ausrichtung & Rhythmus**
Label links, Balken variabel, %-Wert rechts – aktuell ohne feste Spaltenbreiten, Werte „springen“. → **3-Spalten-Grid** mit fixen Breiten (Label 180px / Balken flex / % 60px rechtsbündig). Zeilenhöhe vereinheitlichen, dezente Trennlinie oder Zebra pro Zeile.

**4. Farbskala der Balken vereinheitlichen (Ampel-Logik)**
Grün/Gelb/Rot ok, aber Werte >100% (128–164%) sind grün wie „perfekt 99%“ – Überdosierung sollte differenziert wirken. → **Über 120% eigener Ton (z. B. Türkis/Amber)** einführen, damit „zu viel“ nicht wie „ideal“ aussieht.

**5. Whitespace & Hierarchie der Checkpoint-Cards (Desktop)**
Karten wirken textlastig, „Okay/Kritisch“ konkurriert visuell mit dem Score-Badge. → **Score-Ring/Badge größer als Primär-KPI**, Detailtext (28 gut · 42 neutral) als kleinere Meta-Zeile mit reduzierter Opacity (60–70%). Innenabstand auf 24px vereinheitlichen.

**6. Typografie-System konsolidieren**
Gesperrte Kleinbuchstaben-Labels („ZEITFENSTER“, „AKTUELLES ZIEL“) + Monospace-Werte + Standard-Sans mischen unkontrolliert. → **Max. 2 Schriftgrößen-Rollen pro Ebene** definieren; Monospace nur für Zahlenkolonnen, nicht für Fließtext/Meta.

**7. Mobile: KPI-Kacheln (36/31/5/72) modernisieren**
Große Zahlen gut, aber Karten wirken leer und uneinheitlich hoch. → **Icon oder Mini-Sparkline** ergänzen, gleiche Höhe, konsistenter Punkt-Indikator links. Farbe der Zahl = Statusfarbe (rot bei „Über Bedarf“ bereits gut, konsequent durchziehen).

**8. Wochendurchschnitt-Chart (Mobile): Lesbarkeit**
Ziel-Linie „1900“ überlappt fast mit Balkenwert; nur 3 Balken wirken verloren. → **Ziel-Linie in ruhigem Grau + Label rechts außen**, Balkenwerte oben mit mehr Abstand, Balkenbreite reduzieren für Atmung. Über/Unter-Ziel farblich codieren (Balken rot wenn > Ziel).

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`