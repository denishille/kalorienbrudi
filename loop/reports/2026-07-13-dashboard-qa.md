# Dashboard-QA (Funktion + UX/Design) — 2026-07-13

**Funktion:** 1 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 0 Charts gerendert

## Funktionale Auffälligkeiten
- 🔴 Keine Charts gerendert

## UX-/Design-Bewertung (Claude Vision)

# UX-Review: Kalorien-Dashboard

## Gesamtnote: **6/10**

Solide Basis mit modernem Dark-Theme und guter Akzentfarben-Logik (Blau=Denis, Pink=Leni). Aber: massive Whitespace-Verschwendung im Empty-State, inkonsistente Typografie (Monospace-Fließtext), und der Empty-State wirkt tot statt einladend.

---

## Konkrete Verbesserungen (priorisiert)

**1. Empty-State (Desktop) — HÖCHSTE PRIO**
Aktuell: 70% leerer schwarzer Screen unter der Card. → Card zentriert vertikal im Viewport, Illustration/Icon (z.B. leeres Tellersymbol) + primärer CTA-Button „Ersten Eintrag hinzufügen". Kein toter Scrollraum.

**2. Typografie-Systemfehler — Monospace raus**
Aktuell: Body-Text („Im letzte 7 Tage wurde nichts getrackt", „Stand:", Card-Texte) in Monospace → wirkt wie Terminal/Prototyp. → Durchgängig eine moderne Sans (Inter/Geist). Monospace nur für Zahlenwerte, wenn überhaupt.

**3. Grammatik/Copy-Fehler**
„Im letzte 7 Tage" → „In den letzten 7 Tagen". „ueber", „gruenen" (Umlaut-Ersatz) → korrekte Umlaute. Wirkt sonst unfertig.

**4. Kontrast Empty-State-Text**
Aktuell: Sekundärtext auf dunklem BG kaum lesbar (~2:1). → Mindestens `#A0A0A8` auf `#1A1A1D`, Ziel WCAG AA (4.5:1).

**5. Farbkodierte Stat-Cards vereinheitlichen (Mobil)**
Aktuell: Grün/Gelb/Rot/Blau-Topbalken gut, aber „24 / 24" (Grün & Gelb identische Zahl) verwirrt. → Kontext-Label prominenter, evtl. Prozent-Badge oben rechts in Card statt in Fließtext.

**6. User-Switch als echter Toggle**
Aktuell: Zwei Pill-Buttons ohne klare Toggle-Semantik. → Segmented Control mit klarem aktiv/inaktiv-State (Fill vs. Ghost), Avatar-Initialen statt nur Dot.

**7. Chart-Lesbarkeit „Kaloriendifferenz" (Mobil)**
Aktuell: Zentrierte Bars mit Nulllinie sind clever, aber Nulllinie unsichtbar → dünne vertikale Referenzlinie einzeichnen, Achsenlabel „Ziel" mittig. Werte-Farbe an Bar-Farbe koppeln.

**8. Card-Spacing & Radius-Konsistenz**
Aktuell: Unterschiedliche vertikale Abstände zwischen Zeilen im Detail-Block. → Einheitliches 8px-Grid, konsistente Border-Radien (aktuell mischen Cards/Buttons). „Datenqualität"-Warnung als eigenes Alert-Element mit Icon absetzen.

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`