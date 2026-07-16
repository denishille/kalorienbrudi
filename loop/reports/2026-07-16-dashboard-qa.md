# Dashboard-QA (Funktion + UX/Design) — 2026-07-16

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 1 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 6.5/10

Solide Datenvisualisierung, konsistente Ampel-Logik, gutes Dark-Theme-Fundament. Zieht runter: monospaced Zahlen wirken technisch/unfertig, Kontrastprobleme bei Sekundärtext, Whitespace ungleichmäßig, mobile Chart-Labels kollidieren.

---

## Konkrete Verbesserungen (priorisiert)

**1. Typografie vereinheitlichen (KRITISCH)**
Betroffen: Alle Zahlenwerte (Makros, kcal, µg/mg-Angaben) nutzen Monospace-Font → wirkt wie Terminal.
Ziel: Tabular-Figures einer modernen Sans (z.B. Inter/SF) mit `font-variant-numeric: tabular-nums`. Behält Ausrichtung, wirkt aber premium.

**2. Sekundärtext-Kontrast anheben (KRITISCH)**
Betroffen: Alle grauen Sublabels („4,22 / 20 µg", „Ballaststoffe, Fermentiertes…", Footer). Aktuell teils <3:1.
Ziel: Mindestens 4.5:1 (WCAG AA), grauen Ton von ~#666 auf ~#9CA3AF anheben.

**3. Mobile Chart-Labels entzerren (HOCH)**
Betroffen: Wochendurchschnitt-Chart mobil → „1.842"/„1.900" überlappen (weiß auf gold, unlesbar).
Ziel: Zielwert als dezente Ziellinie mit Label am Achsenrand, Balkenwert oben mittig, ausreichend Padding. Überlappungen algorithmisch verhindern.

**4. Checkpoint-Cards Hierarchie schärfen (HOCH)**
Betroffen: Desktop 4 Karten – Score „57/100" und Makro-Ratio konkurrieren mit Status-Wort.
Ziel: Status-Wort dominant, Score als kleiner Progress-Ring/Chip rechts, Erklärungstext auf max. 1 Zeile kürzen. Farbige Top-Border ist zu dünn/subtil → auf durchgängigen Status-Akzent (Rand + Icon) setzen.

**5. Whitespace & Card-Rhythmus (MITTEL)**
Betroffen: Desktop – großer leerer Bereich links neben „66% Gesamtdeckung"; Cards haben inkonsistente Innen-Paddings.
Ziel: Einheitliches Padding-Token (z.B. 24px), Donut+Text horizontal ausbalancieren oder Donut größer/zentraler nutzen.

**6. Balken-Zeilen in der Mikronährstoff-Liste (MITTEL)**
Betroffen: 16 Zeilen ohne Zebra/Trenner, Label links + Balken + % rechts driften auseinander.
Ziel: Dezente Row-Hover-Highlights, feste Spaltenbreiten, %-Wert vertikal auf Balkenmitte zentriert. Optional 100%-Marker-Linie im Balken-Track.

**7. User-Switcher konsistent machen (MITTEL)**
Betroffen: Denis/Leni-Toggle – Farbe wechselt komplett je Nutzer (Pink vs. Blau), Position mobil vs. desktop unterschiedlich.
Ziel: Neutraler Segmented-Control, aktiver Zustand über Fill; Nutzerfarbe nur als kleiner Akzent-Dot. Reduziert visuelle Unruhe.

**8. Datenqualitäts-Warnung aufwerten (NIEDRIG)**
Betroffen: Mobile Warn-Box wirkt wie Fehler, aber wenig prägnant.
Ziel: Klares Warning-Pattern (Icon + Titel bold + CTA-Button statt Textlink „Details ansehen →").

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`