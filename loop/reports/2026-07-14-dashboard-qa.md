# Dashboard-QA (Funktion + UX/Design) — 2026-07-14

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 2 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# UX-Review: Kalorien-Tracking-Dashboard

## Gesamtnote: **6,5 / 10**

Solide Basis mit gutem Dark-Theme und klarer Nutzer-Umschaltung. Der Mobile-View (Denis) ist deutlich stärker als der Desktop-Empty-State. Es fehlt an Konsistenz, Whitespace-Disziplin und Chart-Feinschliff für einen echten „TOP"-Eindruck.

---

## Konkrete Verbesserungen (priorisiert)

**1. Desktop Empty-State – Whitespace-Verschwendung (HOCH)**
Element: Leere Card „Keine Daten im Zeitfenster" (Screenshot 1). Riesige leere Fläche wirkt ungenutzt und unfertig. Zielzustand: Card auf max. 50 % Höhe reduzieren, Icon+Text+CTA vertikal enger zentrieren; darunter optional 2–3 „Skeleton"-Vorschau-Kacheln des künftigen Dashboards (ausgegraut) zeigen.

**2. Zwei Nutzer, zwei Design-Sprachen (HOCH)**
Element: Leni = Pink-Akzent, Denis = Blau-Akzent. Aktuell ändert sich die komplette Farbwelt inkl. Header-Gradient. Zielzustand: Akzentfarbe pro User beibehalten, aber Layout, Kartenstruktur und Typo-Hierarchie identisch halten – Empty-State (Leni) muss dieselbe Card-Systematik wie Denis nutzen.

**3. Header-Typografie überladen (MITTEL)**
Element: „NÄHRSTOFFBRUDI" / „KALORIENBRUDI" Overline + „Dashboard Leni/Denis". Zwei konkurrierende Beschriftungen. Zielzustand: Overline entfernen oder auf Nav-Breadcrumb reduzieren; „Dashboard" kleiner setzen, Username als visuellen Anker (kein gemischtes Farb-Wort mitten im Titel).

**4. Chart-Lesbarkeit „Kaloriendifferenz" (MITTEL)**
Element: Horizontale Bar-Chart mit +391/+510 etc. (Screenshot 2). Balken sind schwer als Skala lesbar, Mittellinie unklar. Zielzustand: klare vertikale 0-kcal-Referenzlinie einzeichnen, Balken links/rechts symmetrisch, dezente Achsen-Gridlines, negative Werte grün / positive gold konsequent mit Legende.

**5. KPI-Kacheln – Zahlenausrichtung & Farbcodierung (MITTEL)**
Element: 24 / 25 / 4 / 53 Kacheln. Große Zahlen top, aber uneinheitliche Sekundärtexte („45 % der Tage" vs. „seit Fr 22.05."). Zielzustand: einheitliches 3-Zeilen-Raster (Zahl → Label → Kontext), gleiche Baseline, farbiger Top-Border nur als Status-Signal mit Tooltip-Erklärung.

**6. Datenqualitäts-Warnung zu unauffällig (MITTEL)**
Element: „⚠ 15 Tage: Total weicht von Einzelposten-Summe ab". Wichtige Info, aber grau und übersehbar. Zielzustand: dezente Warn-Card mit amber-Hintergrund (10 % opacity) + „Details ansehen"-Link statt reinem Fließtext.

**7. Zeitfenster-Toggle vs. Kalender-Angaben inkonsistent (NIEDRIG)**
Element: „7 Tage" gewählt, Chart zeigt aber Wochen 29.06–19.07 und „1 Tag" in letzter Spalte. Zielzustand: Filter-Zustand und Chart-Range synchronisieren; fehlerhafte „1 Tag"-Spalte prüfen.

**8. Spacing- & Trennlinien-Feinschliff (NIEDRIG)**
Element: „Aktuelles Ziel"-Card mit gepunkteten Trennern. Zeilen zu eng, Punkt-Linien wirken retro. Zielzustand: durchgehende 1px-Linien bei 8 % Opacity, Zeilen-Padding von ~12px auf 16px, konsistente Label-links / Wert-rechts-Ausrichtung.

---
**Quick Wins:** #1, #6, #7 sofort umsetzbar mit größtem visuellen Effekt.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`