# Dashboard-QA (Funktion + UX/Design) — 2026-07-26

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# UX/Design-Review – Nährstoff/Kalorien-Dashboard

## Gesamtnote: **6,5 / 10**

Solide, funktional dichte Datenvisualisierung mit gutem Dark-Theme-Ansatz und schöner Farbcodierung (Rot→Gelb→Grün). Es fehlt aber Feinschliff bei Ausrichtung, Whitespace-Rhythmus, Typo-Konsistenz und einem kritischen Layout-Bug im Desktop-View.

---

## Konkrete Verbesserungen (priorisiert)

**1. Layout-Bug: Überlappender Tab-Bar Desktop** *(kritisch)*
Betroffen: Sticky-Leiste „KALORIEN / NÄHRSTOFFE / Denis“ auf dem Gesamtdeckungs-Ring/Chart-Header.
→ Zustand: Sticky-Bar mit eigenem `padding` + `background` als abgesetzte Zeile, kein Überdecken von Content. Erste Chart-Zeile (Vitamin D) hat aktuell abgeschnittenen Header darüber – muss vollständig sichtbar sein.

**2. Monospace-Font für Werte entfernen** *(hoch)*
Betroffen: Alle Nährstoff-Zahlen („2,82 / 20 µg“), Sublabels, Datumszeilen.
→ Zustand: Einheitliche Sans (z. B. Inter) mit `tabular-nums` für Zahlen-Alignment. Monospace wirkt technisch/dev-lastig und bricht die moderne Anmutung.

**3. Prozent-Labels im Balkendiagramm ausrichten & einbetten** *(hoch)*
Betroffen: Rechte %-Spalte (14 %, 30 % … 129 %).
→ Zustand: Feste rechtsbündige Zahlenspalte mit konstanter Breite; 100 %-Referenzlinie visuell markieren (dünne vertikale Linie). Overflow-Werte (110 %, 129 %) durch dezenten Marker statt gleichem Balkenstil kennzeichnen.

**4. Whitespace-Rhythmus & Card-Konsistenz** *(mittel)*
Betroffen: Checkpoint-Cards vs. Gesamtdeckungs-Card vs. Chart-Container.
→ Zustand: Einheitliches Spacing-System (8-px-Grid), gleiche `border-radius` und `border`-Behandlung auf allen Cards. Aktuell haben Checkpoint-Cards sichtbare Border, der Ring-Container fast keine – vereinheitlichen.

**5. Header-Hierarchie „Dashboard Denis“ + Nutzerwahl zusammenführen** *(mittel)*
Betroffen: Titel oben links + „Denis“-Dropdown rechts (redundant).
→ Zustand: Nutzername nur an einer Stelle. Titel z. B. „Dashboard“ + Nutzer-Switcher als klarer Toggle rechts. „NÄHRSTOFFBRUDI/KALORIENBRUDI“-Eyebrow tonaler/kleiner setzen.

**6. Status-Badges & Farbsemantik verstärken** *(mittel)*
Betroffen: „Kritisch/Okay“ (Desktop), „Wackelig · 48 %“ (Mobil).
→ Zustand: Badges mit gefülltem, farbcodiertem Chip-Hintergrund (rot/gelb/grün, niedrige Opazität) statt reiner Textfarbe. Erhöht Scanbarkeit und Kontrast.

**7. Mobile KPI-Kacheln typografisch entzerren** *(mittel)*
Betroffen: „31 / 28 / 5 / 64“-Kacheln.
→ Zustand: Große Zahl + Label brauchen mehr vertikalen Abstand; Zusatzzeile („48 % der Tage“) als dezentes Sub-Label (kleiner, gedimmt). Einheitliche Zahlenfarbe-Logik dokumentieren (warum 64 blau, 31 grün).

**8. Chart-Kontrast Balkendiagramm mobil erhöhen** *(niedrig)*
Betroffen: Wochendurchschnitt-Bars (alle gleiches Blau) + Ziel-Linie.
→ Zustand: Bars je nach Ziel-Über/Unterschreitung einfärben (rot über Ziel, grün darunter) – aktuell alle blau, obwohl 2 von 3 über Ziel liegen. Ziel-Linie kräftiger/gelabelt.

---

**Quick-Wins zuerst:** #1 (Bug), #2 (Font), #3 (Chart-Alignment) bringen den größten optischen Sprung.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`