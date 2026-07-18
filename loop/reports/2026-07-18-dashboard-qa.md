# Dashboard-QA (Funktion + UX/Design) — 2026-07-18

**Funktion:** 0 🔴 · 0 🟡

## Funktionale Checks
- ✅ 6 Steuerelemente geklickt
- ✅ 1 Charts gerendert

## Funktionale Auffälligkeiten
- 🟢 keine

## UX-/Design-Bewertung (Claude Vision)

# UX/Design-Review: Kalorien-Tracking-Dashboard

## Gesamtnote: **7 / 10**

Solide, moderne Basis mit gutem Dark-Theme und klarer Farb-Ampellogik. Es fehlt an Feinschliff bei Typo-Hierarchie, Ausrichtung und Chart-Lesbarkeit. Der Balken-Screen (Mikronährstoffe) ist stark, die Header/Nutzer-Umschaltung wirkt inkonsistent.

---

## Konkrete Verbesserungen (priorisiert)

**1. User-Switcher vereinheitlichen (Header, beide Screens)**
Aktuell: Desktop pink-Pill „Leni“ + Bullet „Denis“; Mobil blau-Pill „Denis“. Zwei verschiedene Toggle-Stile.
→ Ziel: Ein konsistenter Segmented-Control (Pill-Container mit aktivem Segment), identisch auf Desktop/Mobil. Aktive Farbe = Nutzerfarbe, inaktives Segment nur Text ohne Bullet.

**2. Farb-Bedeutung der Nutzer entkoppeln von Status-Farben**
Denis = Blau kollidiert visuell mit blauen Balken im Chart; Leni = Pink kollidiert nicht, aber Rot/Grün-Ampel plus Pink/Blau erzeugt Farb-Rauschen.
→ Ziel: Ampelfarben (rot/gelb/grün) exklusiv für Status reservieren. Nutzerakzent nur in Header + Logo, Charts neutral (ein Grau/Akzent).

**3. Chart-Achse & Nullreferenz „Kaloriendifferenz" (Mobil)**
Die Balken schweben ohne sichtbare 0-Linie/Achse; positive/negative Werte schwer ablesbar.
→ Ziel: Vertikale 0-Linie einziehen, Balken links (Defizit, grün) / rechts (Überschuss, gelb/rot) davon ausrichten. Werte konsistent rechtsbündig.

**4. Typo-Hierarchie in Checkpoint-Karten schärfen (Desktop)**
„Okay/Kritisch/Gut" konkurriert mit dem Score-Badge und dem Titel; drei fast gleich große Textebenen.
→ Ziel: Titel klein/uppercase-label, Status-Wort groß+farbig (Primär), Detailzeilen als gedämpftes Grau (60% Opacity). Score-Badge kleiner/dezenter.

**5. Vertikaler Rhythmus & Abstände normieren**
Zeilen-Labels bei Mikronährstoffen (Name + Ø-Wert) haben enges Leading; Sektionsabstände variieren (Header→Zeitfenster→Checkpoints ungleich).
→ Ziel: 8px-Grid konsequent, einheitliche Section-Paddings (z. B. 32px), Label/Sub-Label mit 4px Gap.

**6. Prozent-Balken: Zielmarke & Skala ergänzen (beide)**
Balken zeigen nur Ist-Füllung; die 100%-Deckelung ist nicht visuell markiert.
→ Ziel: Dezente 100%-Ziellinie/Tick im Track, evtl. Skala-Ticks bei 50/100%. Werte >100% (Zink 105%, Selen 126%) klar als „über Ziel" kennzeichnen (Rand/Icon).

**7. „Datenqualität"-Warnbox aufwerten (Mobil)**
Wirkt wie Fließtext, geringe Sichtbarkeit trotz Wichtigkeit.
→ Ziel: Amber-Card mit Icon links, fettem Titel, klarem CTA-Button statt Textlink „Details ansehen".

**8. Footer & Meta-Text Kontrast (beide)**
„Stand: …/automatisch generiert" ist zu dunkelgrau, unter Lesbarkeitsschwelle.
→ Ziel: Kontrast auf min. 4.5:1 anheben, zentriert mit dezentem Divider oben abgrenzen.

---

**Quick Wins:** Nutzer-Toggle vereinheitlichen (1), 0-Linie im Chart (3), Footer-Kontrast (8).

## Screenshots
- `reports/shots/desktop.png`
- `reports/shots/mobile.png`