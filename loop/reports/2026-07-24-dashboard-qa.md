# Dashboard-QA (Funktion + UX/Design) — 2026-07-24

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 6.5 / 10

Solide Datenbasis, klares Dark Theme, gute Farb-Semantik (rot→gelb→grün). Aber: inkonsistente Abstände, floating Toolbar überlappt Content, Typo-Hierarchie unscharf, Charts teils unklar. Wirkt „gut“, nicht „premium“.

---

## Konkrete Verbesserungen (priorisiert)

**1. Floating-Toolbar-Overlap beheben (Desktop, kritisch)**
Der `KALORIEN / NÄHRSTOFFE / Denis`-Bar überdeckt die Gesamtdeckungs-Card und Tabellen-Header. Zielzustand: Toolbar als sticky Top-Bar *oberhalb* des Contents oder mit korrektem `padding-top` am Content, kein Overlap, keine abgeschnittenen Header.

**2. Nährstoff-Balken: Zielmarke + Prozent-Ausrichtung (Desktop)**
Balken haben keine visuelle 100%-Referenzlinie; Prozent rechts wirkt losgelöst. Zielzustand: dezente vertikale 100%-Linie im Track, Prozentwert direkt am Balkenende oder in fixer rechter Spalte mit einheitlicher Baseline. Track-Hintergrund minimal aufhellen (aktuell fast unsichtbar).

**3. Typografische Hierarchie schärfen**
`Dashboard Denis` (H1), Section-Titel, Card-Labels und Werte nutzen zu ähnliche Größen/Gewichte. Zielzustand: klare 3-Stufen-Skala (z.B. 28/20/13px), Labels durchgängig `uppercase 11px letter-spacing` grau, Werte bold weiß. Der blaue Name „Denis“ im H1 wirkt zufällig — entweder konsequent als Akzent oder weglassen.

**4. Health-Checkpoint-Cards vereinheitlichen (Desktop)**
Score-Badges (48/100 rot, 68/100 gelb) und Cholesterin (301 mg) haben unterschiedliche Logik/Formate. Zielzustand: einheitliches Badge-System, jede Card mit gleicher vertikaler Struktur (Titel → Score → Status → Detailzeile → Fußnote), gleiche Höhe, gleicher Fußnoten-Kontrast (aktuell zu dunkel/kaum lesbar).

**5. „Zielerreichung – letzte 7 Tage“-Chart lesbarer machen (Mobil)**
Diverging-Bars mit +/− Werten sind ohne Nulllinie/Achse schwer interpretierbar. Zielzustand: sichtbare zentrale Nulllinie, konsistente Bar-Herkunft, Wert-Labels immer außen, einheitliche Farbe (grün=Ziel/Defizit, rot=über). „+104“ gelb neben grünen Bars ist verwirrend.

**6. Kontrast der Sekundärtexte anheben**
Fußnoten („Ballaststoffe… = gut“, Footer, Unterzeilen) liegen bei ~30% Opacity → kaum lesbar, schlechter WCAG-Kontrast. Zielzustand: min. `#8A8A8F` auf dunklem Grund (≥4.5:1 für Fließtext).

**7. Whitespace & Card-Rhythmus harmonisieren**
Uneinheentliche vertikale Abstände zwischen Sektionen (großer Gap nach Checkpoints, enger bei Tabelle). Zielzustand: konsistentes 8px-Grid, einheitliche Card-Radien/Paddings, gleicher Section-Spacing-Token überall.

**8. Toggle-States klarer (Kalorien/Nährstoffe, W/M/J, Makros)**
Aktiv-Zustand (blau gefüllt) gut, aber inaktive Pills sind sehr flau. Zielzustand: inaktive Pills mit dezentem Border/Hover-Feedback, aktive mit klarem Akzent — konsistentes Segment-Control-Pattern über Desktop und Mobil.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`