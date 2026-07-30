# Dashboard-QA (Funktion + UX/Design) — 2026-07-30

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 5 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# UX-Review: Nährstoff/Kalorien-Dashboard

## Gesamtnote: **6,5 / 10**

Solide Datenbasis und moderne dunkle Ästhetik, aber inkonsistente Hierarchie, überladene Header-Zone und ein hartes visuelles Bruch-Problem zwischen den beiden Kartenblöcken auf Desktop.

---

## Konkrete Verbesserungen (priorisiert)

**1. Toggle-/Profil-Leiste (Desktop) — kritischer Layout-Bruch**
Der Balken „KALORIEN / NÄHRSTOFFE / Denis“ überlappt die Nährstoff-Tabelle (abgeschnittene Kopfzeile, Blur-Artefakt oben rechts). → Als **sticky, eigenständige Toolbar** oberhalb der Tabelle fixieren, volle Kartenbreite, klarer 24px-Abstand nach unten. Kein Overlap.

**2. Kontrast der Sekundärwerte**
Werte wie „2,51 / 20 µg“ und Beschreibungstexte (`Ballaststoffe, Fermentiertes…`) liegen bei ~3:1 → unter WCAG AA. → Sekundärtext auf mind. **#9AA0A6 (4.5:1)** anheben, Einheiten in konsistenter Monospace-Größe (aktuell wirken sie technisch/inkonsistent zur Sans).

**3. Farbcodierung der Balken vereinheitlichen & Ziel-Marke setzen**
Rot→Gelb→Grün ist gut, aber >100% (Selen 174%) bleibt sattgrün = signalisiert fälschlich „ideal“. → **Über-Ziel-Werte (>120%) in Amber/Warn-Ton** kippen und eine **vertikale 100%-Ziellinie** über alle Balken legen. Sofort lesbar, was Über-/Unterversorgung ist.

**4. Header-Zone entschlacken (beide Views)**
Doppelte Titel („NÄHRSTOFFBRUDI / Dashboard Denis“ vs. „KALORIENBRUDI…“) plus Zeitfenster plus Profil-Switch konkurrieren. → **Eine Titelzeile**, Zeitfenster-Tabs (7/30/Gesamt) und Profil-Dropdown in **eine flache Kopfleiste** zusammenziehen. Weniger vertikaler Platzverbrauch, klare Ankerpunkte.

**5. Checkpoint-Karten: Score-Badge & Status vereinheitlichen**
„55/100“, „433 mg“, „20/100“ mischen Einheiten/Skalen in identischen Badges. → Einheitliche **Ring-Mini-Gauge + Statuswort** je Karte; „Cholesterin 433mg“ analog auf 0–100-Ampel normalisieren. Konsistente Badge-Höhe und -Padding.

**6. Nährstoff-Tabelle: Zebra & Zeilenrhythmus**
16 Zeilen ohne Trennung ermüden das Auge; Prozentwerte rechts sind visuell isoliert. → **Dezente Zeilenhöhe 44px + subtile Hover-Row**, Prozentzahl in gleicher Farbe wie zugehöriger Balken einfärben (Verknüpfung Wert↔Balken).

**7. Mobile: KPI-Karten & Chart-Achsen**
Die vier KPI-Kacheln (34/29/5/68) sind stark, aber die Diverging-Balken „Zielerreichung“ haben **keine 0-Achsen-Linie** → Richtung unklar. → **Mittelachse (0) als vertikale Linie** einzeichnen, +/- links/rechts konsistent. Balkenminimum sichtbar machen (aktuell verschwinden kleine Werte wie „+1“).

**8. Whitespace & Kartenradien konsistent**
Uneinheitliche Innenabstände (Checkpoint-Karten eng, Gesamtdeckungs-Karte sehr luftig). → **8px-Grid**, einheitliches Card-Padding (20–24px) und ein Border-Radius-Token (z.B. 16px) durchgängig anwenden.

---

**Quick Wins zuerst:** #1 (Overlap) → #2 (Kontrast) → #3 (Farblogik). Das hebt die Note schnell Richtung 8.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`