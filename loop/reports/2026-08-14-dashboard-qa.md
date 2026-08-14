# Dashboard-QA (Funktion + UX/Design) — 2026-08-14

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# UX-Review: Nährstoff-/Kalorien-Dashboard

## Gesamtnote: **6,5 / 10**

Solide Datenvisualisierung mit klarem Ampelsystem, aber inkonsistente Typografie (Mix Monospace/Sans), schwache Tab-Navigation und ein kritischer Layout-Bruch beim Overlay-Panel (Desktop) ziehen die Wertung runter.

---

## Konkrete Verbesserungen (priorisiert)

**1. Schwebendes Tab-Panel „Kalorien/Nährstoffe" (Desktop) — kritisch**
Der Toggle liegt als halbtransparenter Overlay-Streifen über der Nährstoffliste und verdeckt den ersten Balken (Vitamin D, „18%" abgeschnitten). → Panel als fixe Kopfzeile *oberhalb* der Liste verankern, voll deckend, mit klarem Abstand zum ersten Listeneintrag.

**2. Typografie vereinheitlichen**
Werte wie „2,05 / 20 µg", „57/100" nutzen Monospace, Labels dagegen Sans — wirkt technisch/inkonsistent. → Monospace nur für tabellarisch alignierte Zahlenkolonnen (Prozent-Spalte rechts). Alles andere in *eine* Sans-Familie mit klarer Skala (z. B. 3–4 Stufen).

**3. Prozent-Farbcodierung an Balken koppeln**
Rechte Prozentwerte sind farbig (rot/gelb/grün), Balken auch — aber Werte wie „106%/183%" bleiben grün, obwohl Überschuss (z. B. Calcium 183%) ggf. warnwürdig ist. → Dritte Kategorie „Überschuss" einführen (z. B. Türkis/Blau), damit „gut gedeckt" ≠ „stark über Referenz".

**4. Karten-Kontrast & Abgrenzung (Checkpoints)**
Die 4 Checkpoint-Karten haben kaum sichtbare Ränder/Erhöhung auf dem dunklen BG → schwache Gruppierung. → Subtile 1px-Border (rgba weiß 8%) + minimale Elevation/Innenschatten, einheitliche Innenabstände (aktuell wirken Texte unterschiedlich weit vom Rand).

**5. Donut „70%" — Beschriftung integrieren**
Der Ring links steht optisch isoliert neben viel Text. → Restsegment dezenter (nicht schwarz, sondern dunkelgrau), Legende/Skala näher an den Ring, oder Mikro-Label „16 Nährstoffe" direkt unter der 70%-Zahl.

**6. Balkenliste: Zebra/Trennung & Alignment**
15+ Balken ohne visuelle Rhythmisierung → ermüdend. → Dezente Zeilen-Hover/alternierender Hintergrund, Labels linksbündig auf feste Spaltenbreite fixieren (aktuell „Vitamin B12" vs „Jod" leicht unruhig), Referenzlinie bei 100% als vertikaler Marker einblenden.

**7. Mobile: „Zielerreichung"-Chart lesbarkeit**
Die grünen Mini-Balken mit „-132/-117" sind zu schmal, Werte kleben am Balken, der Nullpunkt ist unklar. → Zentrierte Nulllinie mit Achsenbeschriftung, Balken höher, positive/negative Seite klar spiegeln.

**8. Header-Konsistenz zwischen Views**
„NÄHRSTOFFBRUDI" vs „KALORIENBRUDI" als Kicker wirkt unseriös/verspielt gegenüber sonst sachlichem Ton. → Einheitlichen, ruhigen Marken-Kicker wählen; Blau-Akzent im Titel („Denis") ist gut, konsistent halten.

---

**Quick Wins:** #1 (Overlay-Bug), #2 (Font-Konsistenz), #4 (Karten-Border) — höchster Wirkung-zu-Aufwand-Faktor.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`