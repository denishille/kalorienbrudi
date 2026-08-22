# Dashboard-QA (Funktion + UX/Design) — 2026-08-22

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 6.5/10

Solide Datendarstellung mit gutem Ampel-System und klarer Farbcodierung. Größte Schwächen: schwebender Tab-Bar mit Überlappungsbug, inkonsistente Kartenränder und uneinheitliche Typo-Hierarchie. Wirkt eher „Dashboard-Tool“ als „Premium-App“.

---

## Konkrete Verbesserungen (priorisiert)

**1. [KRITISCH] Sticky Tab-Bar-Überlappung (Desktop)**
Der „Kalorien/Nährstoffe“-Tab + Profil-Dropdown überlagert im Screenshot 1 die Gesamtdeckungs-Karte und schneidet die erste Nährstoffzeile ab. → Tab-Bar als saubere Sticky-Leiste mit definiertem Padding oben, Content darunter mit `scroll-padding-top` versetzen. Kein Overlap, keine abgeschnittenen Werte.

**2. Karten-Konsistenz (Checkpoints)**
Die 4 Checkpoint-Karten haben unterschiedliche/teils fehlende Border-Radien und ungleiche Innenhöhen (Cholesterin-Karte wirkt luftiger). → Einheitliche Card-Komponente: gleicher `radius: 16px`, gleiche `min-height`, identisches Padding (24px), 1px Border `rgba(255,255,255,0.06)`.

**3. Nährstoff-Balken: Ausrichtung & Track**
Balken starten unterschiedlich, Prozent-Labels rechts sind schwach kontrastiert, Track kaum sichtbar. → Alle Balken auf gemeinsame Baseline, konsistente Balkenhöhe (10px), sichtbarer Track (`rgba(255,255,255,0.05)`), Zielmarke bei 100% als vertikale Linie. Prozentwerte rechtsbündig in Tabellenspalte ausrichten.

**4. Typografie-Hierarchie vereinheitlichen**
„Dashboard Denis“ mischt Weiß+Blau, Section-Header („Gesundheits-Checkpoints“) und Karten-Titel liegen zu nah beieinander im Gewicht. → Klare Skala definieren: H1 28px/700, Section 18px/600, Card-Title 15px/600, Label 12px/500 uppercase. Nur EIN Akzentblau, konsistent eingesetzt.

**5. Whitespace & Zahlenformat**
Werte wie „2,25 / 20 µg“ in Monospace-Optik mit inkonsistenten Abständen; Metrik-Zeilen (Ziel/Kalorienziel etc. mobil) zu eng. → Tabular-Nums-Font für alle Zahlen, konsistente Zeilenhöhe (min 44px touch-target mobil), Trennlinien dezenter (`0.04` alpha).

**6. Farbkontrast Sekundärtext**
Beschreibungstexte („Ballaststoffe, Fermentiertes…“, „weniger ist besser“) liegen unter WCAG-Kontrast. → Sekundärtext auf mind. `#8A8F98` (4.5:1) anheben.

**7. Mobile Stat-Cards (40/42/8/90)**
Große Zahlen gut, aber Karten wirken flach und uneinheitlich zum Rest. → Subtiler Gradient/Glow in Statusfarbe am oberen Rand, gleiche Höhe, Icon-Dot vor Label vergrößern für schnellere Scanbarkeit.

**8. Donut & Balken-Charts modernisieren**
75%-Donut und Wochenbalken wirken generisch. → Donut mit weicherem Verlauf + Center-Label kleiner sekundär beschriften; Balken mit abgerundeten Kappen und gestrichelter Ziel-Linie klar labeln (aktuell „Ziel“ überlappt Balken).

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`