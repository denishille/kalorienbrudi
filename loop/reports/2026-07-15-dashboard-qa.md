# Dashboard-QA (Funktion + UX/Design) — 2026-07-15

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 1 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# UX-Review: Kalorien-Tracking-Dashboard

## Gesamtnote: **6,5 / 10**

Solide Datendichte, funktionale Balken, gute Farbcodierung (Ampel). Aber: schwache Typo-Hierarchie, inkonsistente Abstände, zu viel gleichförmiger Dark-on-Dark-Kontrast und ein wenig durchdachtes Chart auf Mobil. Wirkt „Dashboard-Template“, nicht „Premium-Produkt“.

---

## Konkrete Verbesserungen (priorisiert)

**1. Kontrast der Fließtexte anheben (Desktop + Mobil)**
Betroffen: alle grauen Sublabels („5 getrackte Tage“, „4,97 / 20 µg“, Footer).
Ziel: Sekundärtext von ~#666 auf min. #9A9A9A (WCAG AA ≥ 4.5:1). Aktuell teils kaum lesbar.

**2. User-Switch vereinheitlichen**
Betroffen: Toggle „Denis / Leni“ (pink vs. blau, unterschiedliche Position/Größe je Screen).
Ziel: Identische Komponente, aktive Farbe = jeweilige User-Akzentfarbe, gleiche Höhe/Padding auf beiden Plattformen. Inaktiver Zustand als Outline-Pill, nicht als voller Button.

**3. Balkenliste: Prozent + Label-Ausrichtung fixieren**
Betroffen: Mikronährstoff-Liste.
Ziel: Prozentwerte rechtsbündig in fester Spalte, Balken links auf gleicher X-Achse starten, Wert-Sublabel (z. B. „42,3 / 95 mg“) rechtsbündig zum Nährstoffnamen. Aktuell wirkt die linke Spalte visuell zerfranst.

**4. Chart-Achse auf Mobil (Kaloriendifferenz) neu denken**
Betroffen: horizontale Mini-Balken „letzte 7 Tage“.
Ziel: Nulllinie visuell markieren (vertikale Achse), grüne/goldene Balken beidseitig davon; aktuell sind alle Balken quasi bündig und die +/- Logik nicht ablesbar. Werte konsistent rechts.

**5. Karten-Radius & Border-Stil konsistent machen**
Betroffen: Checkpoint-Karten (farbige Top-Border) vs. große Container (kein Akzent) vs. Mobil-Stat-Karten (dicke farbige Top-Border).
Ziel: Ein Border-System – z. B. 1px subtiler Rand + 3px farbiger Top-Accent nur bei Status-Karten. Radius global auf 16px vereinheitlichen.

**6. Typo-Hierarchie schärfen**
Betroffen: Überschriften „Dashboard Leni“, „Mikronährstoffe“, Werte wie „71%“.
Ziel: Klarere Skala (H1 32/40, Section 20/28, Wert-Zahlen tabular-nums). Letter-Spacing der Uppercase-Kicker („ZEITFENSTER“, „NÄHRSTOFFBRUDI“) reduzieren – aktuell zu breit gesperrt und billig wirkend. „Brudi“-Kicker wirkt unprofessionell → entfernen oder ersetzen.

**7. Vertikaler Rhythmus / Whitespace**
Betroffen: Abstände zwischen Gesamtdeckung → Mikronährstoffe (zu eng) und großzügige Leerräume oben.
Ziel: Konsistentes 8pt-Spacing-Grid; Section-Abstände einheitlich 40px, Karten-Innenpadding 24px.

**8. Status-Badges & Datenqualität-Hinweis aufwerten**
Betroffen: „Wackelig · 45%“, „14 Tage weicht ab“-Box.
Ziel: Icon + klare Farbfläche (Amber-Chip mit dunklem Text statt dünner Border), CTA „Details ansehen“ als echter Link-Button mit Hover-State.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`