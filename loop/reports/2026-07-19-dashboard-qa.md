# Dashboard-QA (Funktion + UX/Design) — 2026-07-19

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 3 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# UX-Review: Kalorien-Tracking-Dashboard

## Gesamtnote: **6,5 / 10**

Solide, funktionale Datendichte mit klarer Nutzer-Zuordnung über Farbe (Pink/Blau). Aber: inkonsistente Card-Stile, schwache Whitespace-Disziplin, Chart-Lesbarkeit teils mangelhaft, und der User-Switcher hängt visuell zusammenhanglos in der Mitte.

---

## Konkrete Verbesserungen (priorisiert)

**1. User-Switcher fixieren & aus dem Content-Flow lösen** *(Hoch)*
- Element: „Denis / Leni“-Toggle (Desktop mittig überlappend, Mobil im Header)
- Ziel: Als persistente Segmented-Control oben rechts im Header verankern, konsistent auf beiden Views. Aktuell wirkt er wie ein zufälliger Divider zwischen zwei Sektionen.

**2. Card-Rahmen vereinheitlichen** *(Hoch)*
- Element: Health-Checkpoint-Cards (farbige 2px-Borders) vs. dunkle Content-Cards (kein/subtiler Border)
- Ziel: Ein System — dezenter 1px-Border (`rgba(255,255,255,0.08)`) plus farbiger Status nur über einen linken 3px-Accent-Bar oder Dot. Die vollflächigen Neon-Rahmen wirken laut und uneinheitlich.

**3. Balken-Charts: 100%-Marker + Zielsegmentierung** *(Hoch)*
- Element: Nährstoff-Balken (Screenshot 1)
- Ziel: Vertikale 100%-Referenzlinie einziehen, damit „über/unter Ziel“ sofort lesbar ist. Prozente rechtsbündig gleich ausrichten (aktuell OK), aber Rot→Gelb→Grün-Verlauf durch feste Ampel-Stufen ersetzen (Verlauf verwischt die Aussage bei ~50%).

**4. Typo-Hierarchie schärfen** *(Mittel)*
- Element: Werte-Zeilen „3,51 / 20 µg", Datums-/Labelzeilen
- Ziel: Sekundärtext auf einheitliches Grau (`#8A8A8A`), monospace nur für Zahlen. Aktuell konkurrieren Label, Wert und Einheit in ähnlichem Kontrast → alles gleich wichtig = nichts wichtig.

**5. Kalorien-Balkendiagramm (Mobil) lesbar machen** *(Mittel)*
- Element: „Kaloriendifferenz letzte 7 Tage“ (mittiges Diverging-Chart)
- Ziel: Klare Nulllinie sichtbar, Grün (Defizit) / Gelb (Überschuss) mit Baseline-Achse. Aktuell schweben die Balken kontextlos; Zusammenhang Balkenlänge↔kcal ist nicht sofort erkennbar.

**6. Whitespace & Sektionsabstände** *(Mittel)*
- Element: Desktop-Übergang Checkpoints → Gesamtdeckung → Nährstoffe
- Ziel: Konsistentes 48px-Section-Spacing, Gesamtdeckungs-Card wirkt halb-abgeschnitten (großer leerer Raum rechts). Donut + Text linksbündig zentrieren, ungenutzten rechten Whitespace für Mini-Legende/Trend nutzen.

**7. Farb-Overload reduzieren** *(Mittel)*
- Element: Pink „Leni", Blau „Denis", plus Ampel-Rot/Gelb/Grün überall
- Ziel: Nutzerfarbe nur als Akzent (Name, Switcher, 1 Highlight). Statusampel getrennt halten. Aktuell konkurriert Pink-Titel mit rotem Chart-Bereich → visuelles Rauschen.

**8. „Datenqualität“-Warnung als echte Alert-Komponente** *(Niedrig)*
- Element: Warn-Box (Screenshot 2)
- Ziel: Klar abgesetztes Warn-Pattern (Icon links, `#FFB020`-Border, dezenter Fill), „Details ansehen" als sichtbarer Button-Stil statt reiner Textlink.

---

**Quick Win:** Punkte 1–3 heben die App am schnellsten auf „modern & clean" — sie betreffen Konsistenz und Datenklarheit, die aktuell am meisten leiden.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`