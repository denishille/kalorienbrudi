# Dashboard-QA (Funktion + UX/Design) — 2026-08-13

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Gesamtnote: 7 / 10

Solide, moderne Basis mit gutem Dark-Theme und klarer Datenlogik. Es gibt aber klare Schwächen bei Ausrichtung, Whitespace-Balance und einem gravierenden Overlay-Bug im Desktop-Screenshot.

---

## Kritische Verbesserungen (priorisiert)

**1. Sticky-Bar Overlay-Bug (Desktop) — HÖCHSTE PRIO**
Die Tab-Leiste „KALORIEN / NÄHRSTOFFE / Denis" überlagert das Gesamtdeckungs-Chart und schneidet die erste Nährstoff-Zeile (2,03/20 µg) ab.
→ Ziel: Sticky-Bar mit vollem Hintergrund-Blur + `padding-top` am Content, sodass keine Zeile verdeckt wird. Klare z-Index- und Scroll-Offset-Regel.

**2. Nährstoff-Balken: Zielmarkierung fehlt**
Balken zeigen nur Ist-Wert; die 100%-Referenz ist nur implizit über Farbe erkennbar.
→ Ziel: vertikale 100%-Ziellinie in jeder Balkenzeile einziehen. Werte über 100% klar visuell „kappen" oder überlaufen lassen — aktuell wirken 190% Calcium wie ein neutraler Vollbalken.

**3. Checkpoint-Cards: 4. Card bricht Muster**
„Cholesterin" zeigt „262 mg" statt Score/100 und hat keinen unteren Erklärungs-Divider wie die anderen. Inkonsistente Höhe/Struktur.
→ Ziel: einheitliches Card-Template (Titel · Badge · Status · Aufschlüsselung · Footnote mit Divider) für alle 4 Cards.

**4. Typografie-Hierarchie schärfen**
Zu viele fast gleich große Labels (Sektionstitel „Gesundheits-Checkpoints" vs. Card-Titel konkurrieren). Monospace-Zahlen (2,03 / 20 µg) wirken technisch/inkonsistent zur restlichen Sans-Serif.
→ Ziel: 3 klare Text-Level (Section 20px bold, Card-Title 15px medium, Meta 12px muted). Monospace nur für Prozentwerte rechts, nicht für Nährstoff-Ist/Soll.

**5. Whitespace-Balance (Desktop)**
Die Gesamtdeckungs-Card (70%-Ring) hat massiv leeren Raum rechts; wirkt unfertig.
→ Ziel: Raum nutzen — Mini-Legende, Top-3-Defizite oder Trend-Sparkline rechts neben dem Ring platzieren.

**6. Farb-/Kontrast bei Statusfarben**
Gelb-Töne (Okay/Warnung) und Prozentzahlen in Gelb auf Dunkelgrau liegen teils unter WCAG-AA. Rot „Kritisch" und Grün sind ok.
→ Ziel: Gelb auf min. #E5B800 anheben, Prozent-Labels min. 4.5:1 Kontrast. Nicht Farbe allein als Bedeutungsträger (Icon/Label ergänzen).

**7. Mobile: Datenqualitäts-Warnung besser integrieren**
Der Hinweis „27 Tage ohne Eintrag" sitzt unauffällig in der Ziel-Card, obwohl er die 99%-Aussage stark relativiert.
→ Ziel: als eigene, dezent umrandete Info-Zeile direkt unter der 99%-Progressbar — Vertrauens-Transparenz.

**8. Mobile Chart „Zielerreichung": Achsen-Lesbarkeit**
Die kleinen Balken mit -132/-117 etc. sind schwer als Skala lesbar; keine 0-Linie sichtbar betont.
→ Ziel: klare Null-Achse (heller), symmetrische Skalierung, Balkenwerte rechtsbündig konsistent.

---

**Quick Wins:** Overlay-Fix (#1), Ziellinie in Balken (#2), Card-4-Vereinheitlichung (#3) bringen den größten sichtbaren Sprung Richtung „premium & clean".

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`