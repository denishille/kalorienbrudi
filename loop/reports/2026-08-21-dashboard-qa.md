# Dashboard-QA (Funktion + UX/Design) — 2026-08-21

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 6.5/10

Solide Datenvisualisierung mit klarer Farb-Logik (Ampel), aber technische Schwächen bei Layering, Ausrichtung und Typo-Hierarchie verhindern den „Top“-Eindruck. Das dunkle Theme wirkt an Stellen flach und inkonsistent.

---

## Konkrete Verbesserungen (priorisiert)

**1. Tab-Leiste (KALORIEN/NÄHRSTOFFE) – kritischer Bug [Desktop]**
Die Tab-Leiste + Profil-Dropdown liegen als Sticky-Bar **mitten über der Nährstoff-Liste** und verdecken die oberste Zeile (Vitamin D o.ä. abgeschnitten, „13%“ hängt frei). → Sticky-Bar oben fixieren mit korrektem `padding-top` auf dem Content, sodass keine Zeile überlappt.

**2. Balken-Chart-Ausrichtung [Mobil, Zielerreichung]**
Werte „+673 / +866 / +1…“ werden rechts abgeschnitten, Balken laufen aus dem Container. → Chart-Breite begrenzen, Labels innerhalb des Viewports platzieren; bei Überlauf Wert links vom Balken oder mit fixem Rand rendern.

**3. Checkpoint-Cards – uneinheitliche Höhe & Textumbruch [Desktop]**
„10 gut · 12 neutral · 9 schlecht“ bricht unschön um, Cards wirken unruhig. → Feste Card-Höhe, Zahlen-Chips statt Fließtext (z.B. 3 kleine Pills grün/gelb/rot), einheitlicher Untertext-Bereich mit fixer Zeilenzahl.

**4. Typo-Hierarchie „Dashboard Denis“ [beide]**
Zweifarbiger Titel (weiß+blau) plus Eyebrow „NÄHRSTOFFBRUDI“/„KALORIENBRUDI“ wirkt inkonsistent zwischen den Views. → Ein einheitliches Titelsystem: Eyebrow uppercase klein grau, Titel einfarbig, aktiver Kontext (Kalorien/Nährstoffe) nur über den Tab kennzeichnen, nicht über Titelfarbe.

**5. Nährstoff-Liste: Kontrast & Whitespace [Desktop]**
Sekundärwerte „50,3 / 110 µg“ sind sehr dunkel/schwer lesbar; Zeilen ohne Trennung wirken gedrängt. → Sekundärtext auf min. #8A8A8A anheben, Zeilenhöhe +8px, dezente Hover-Row-Highlight für Scanbarkeit.

**6. Donut „71%“ – zu leer [Desktop]**
Der Ring steht isoliert mit viel toter Fläche rechts. → Ring verkleinern, daneben Mini-Legende (beste/schlechteste 3 Nährstoffe) einsetzen, um Whitespace zu füllen und Kontext zu geben.

**7. Datenqualitäts-Box [Mobil]**
Warnhinweis-Box („23 Tage ohne Eintrag“) hat gleiche Optik wie Info – zu unauffällig für die Datenrelevanz. → Klare Warn-Farbe (amber Border + Icon), CTA „Details ansehen“ als echter Button statt Unterstrich-Link.

**8. Konsistenz Zahlenformat & Einheiten [beide]**
Mischung aus „452 mg“, „1.900 kcal“, „µg“ in unterschiedlicher Ausrichtung. → Einheiten durchgängig gleich stylen (kleiner, gedimmt, fixe Ausrichtung rechtsbündig), Tausenderpunkte konsistent.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`