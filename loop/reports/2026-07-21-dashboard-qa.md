# Dashboard-QA (Funktion + UX/Design) — 2026-07-21

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# Bewertung: 6,5 / 10

Solide Datendichte und konsistente Ampel-Logik, aber die Hierarchie franst aus, die Balken-Charts wirken monoton und der Sticky-Tab-Bar auf Desktop überdeckt Inhalt (abgeschnittener Überschriften-Bereich über „Vitamin D“). Guter Ansatz, aber noch nicht „premium“.

---

## Konkrete Verbesserungen (priorisiert)

**1. Sticky-Bar-Overlap fixen (Desktop) — kritisch**
Element: Tab-Leiste „Kalorien/Nährstoffe“ + Profil-Switcher. Zustand: Sie überlagert die Tabellen-Kopfzeile (Text über „Vitamin D“ ist angeschnitten). Ziel: Content-Padding-Top erhöhen bzw. Bar als echten Sticky-Header mit Hintergrund-Blur + Bottom-Border, damit nichts verdeckt wird.

**2. Mikronährstoff-Balken lesbarer & weniger monoton**
Element: 16 horizontale Balken. Zustand: Rot→Gelb→Grün-Verlauf pro Balken erschwert schnelles Scannen. Ziel: Flache Balkenfarbe nach Schwellenwert (rot <50 / gelb 50–79 / grün ≥80), plus dezente 50%- und 100%-Vertikallinien als Referenz. Prozentzahl rechts fett hervorheben.

**3. Zahlen-Typografie vereinheitlichen**
Element: Werte wie „2,85 / 20 µg“ (Monospace) vs. Card-Zahlen (Sans). Zustand: Stilbruch, wirkt technisch/roh. Ziel: Tabular-Figures-Sans durchgängig, Einheiten in gedämpftem Grau (60% Opacity), Nährstoffname 1 Stufe größer als Wert.

**4. KPI-Cards visuell stärker differenzieren (Mobil)**
Element: „30 / 26 / 4 / 60“-Kacheln. Zustand: Nur Farbe der Zahl unterscheidet sie, alle gleich schwer. Ziel: Farb-Akzent auch als dünne Top-Border oder Icon-Badge, damit „Über Bedarf (rot)“ sofort ins Auge fällt. Sekundärtext einheitlich klein/grau.

**5. Card-Backgrounds & Elevation systematisieren**
Element: Alle Panels. Zustand: Fast alle nutzen denselben Fast-Schwarz-Ton → flach, keine Tiefe. Ziel: 2-Stufen-Layer (Surface #16181C / Card #1E2228) + 1px subtile Border (#2A2F36) statt Schatten. Konsistente Border-Radius (12–16px) überall.

**6. „Gesamtdeckung 57%“-Sektion aufwerten**
Element: Donut + Fließtext. Zustand: Viel Leerraum rechts, Donut wirkt isoliert. Ziel: Donut zentrieren oder rechts eine kompakte Legende/Mini-Stats (beste/schlechteste 3 Nährstoffe) ergänzen, um den Whitespace sinnvoll zu füllen.

**7. Farbkontrast der Sekundärtexte erhöhen**
Element: Beschreibungszeilen (z.B. „Ballaststoffe, Fermentiertes, Vielfalt = gut“). Zustand: Zu niedriger Kontrast, an der WCAG-Grenze. Ziel: Mind. 4.5:1 (Grauwert anheben auf ~#9AA0A8).

**8. Chart-Achsen & Nulllinie klarer (Mobil, „Zielerreichung“)**
Element: Diverging-Bar-Chart mit +/− Werten. Zustand: Nulllinie kaum erkennbar, positive/negative Balken schwer zuordenbar. Ziel: Deutliche vertikale 0-Linie, konsistente Balken-Mindestbreite, Vorzeichen-Werte farblich an Balken koppeln (grün = im Defizit/gut, gelb = drüber).

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`