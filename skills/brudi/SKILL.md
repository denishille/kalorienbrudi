---
name: brudi
description: "Kalorien- und Nährstofftracking für das Kalorienbrudi-Projekt (Denis & Leni, zwei Supabase-Tabellen: tagesuebersicht + lebensmittel_analyse). Dieser Skill MUSS bei jedem Tracking-Vorgang verwendet werden: immer wenn der Nutzer /brudi schreibt oder Claude als \"Brudi\", \"Rudi\" oder \"Bruder\" anspricht – z. B. Nachrichten, die mit \"hi/hallo/hey brudi\" oder ähnlich beginnen, sowie jede sonstige Anrede, und IMMER automatisch, wenn in den Chats \"Kalorienrechner Denis\" oder \"Kalorienrechner Leni\" Essen, Mahlzeiten, Getränke, Snacks, Mengen oder Marken genannt werden (\"ich habe ... gegessen/getrunken\", \"noch ein/e ...\", \"trag ... ein/nach\", \"heute gab es ...\"), ebenso bei Angaben zu Gewicht, Kalorienziel, Sport/Kalorienverbrauch, Bauch, Stuhlgang oder Atmung, bei Korrekturen (\"nicht X sondern Y\", \"das war für gestern\") und beim Nachtragen vergangener Tage. Auch bei beiläufigen oder per Spracheingabe diktierten Meldungen ohne explizite Aufforderung triggern. Läuft IMMER kombiniert mit dem ponytail-Skill (full)."
---

# Brudi

Tracking-Workflow für die Kalorienbrudi-Datenbank. Nicht moralisieren – nur
Werte erfassen und übertragen. Wird immer ausgelöst, wenn in den Chats
"Kalorienrechner Denis" oder "Kalorienrechner Leni" Lebensmittel oder
Mahlzeiten eingetragen werden. Wird auch ausgelöst, wenn im Chat mit
"Hey Brudi", "Hey Rudi", "Hey Bruder" angesprochen.

**Immer zuerst:** den ponytail-Skill laden und in Stufe **full** anwenden
(minimale Tool-Calls, kürzester funktionierender Weg).

## Datenbank

Die Daten liegen in **Supabase** (Projekt Kalorienbrudi), Schema `public`.
Zugriff über den Supabase-Connector, SQL per `execute_sql`.

| Tabelle | Zweck |
|---|---|
| `public.tagesuebersicht` | 1 Zeile pro Tag und Person |
| `public.lebensmittel_analyse` | 1 Zeile pro Lebensmittel |

Das Dashboard liest genau diese beiden Tabellen. Was hier steht, steht dort.

### ⚠️ Regel 0: Was dieser Skill an der Datenbank darf

Erlaubt sind **ausschließlich** `select`, `insert` und `update` auf
`public.tagesuebersicht` und `public.lebensmittel_analyse`.

Nicht erlaubt – auch nicht, wenn es der kürzere Weg wäre:

- **Kein DDL**: kein `create`, `alter`, `drop`, `truncate`. Fehlt eine Spalte,
  ist das eine Schema-Änderung im Repo (`supabase/`), keine Sache dieses Skills.
- **Kein `delete` ohne Rückfrage.** Falsches wird korrigiert, nicht gelöscht.
  Muss doch eine Zeile weg (echter Doppeleintrag), vorher die betroffene Zeile
  zeigen und bestätigen lassen.
- **Kein `update` ohne `where`** und kein `where`, das mehr als den
  bearbeiteten Tag trifft. Immer `person` UND `datum` einschränken.
- **Keine anderen Tabellen**, keine Systemkataloge, keine Rollen/Policies.

Der Connector selbst schränkt nichts ein – diese Regel ist die einzige Bremse.
Im Zweifel: erst `select`, Ergebnis zeigen, dann schreiben.

### Spalten

`tagesuebersicht`:

| Spalte | Typ | Inhalt |
|---|---|---|
| `person` | text | `Denis` / `Leni` |
| `datum` | date | `YYYY-MM-DD` |
| `tag` | text | Titel, Format *Freitag, 29.05.26* |
| `kalorien_kcal` | numeric | Tagessumme |
| `protein_g`, `kohlenhydrate_g`, `fett_g` | numeric | Tagessummen |
| `kalorienziel_kcal` | numeric | Pflicht (Carry-Forward) |
| `gewicht_kg` | numeric | Pflicht (Carry-Forward) |
| `zielgewicht` | numeric | Pflicht (Carry-Forward) |
| `ziel` | text | Pflicht (Carry-Forward) |
| `notizen` | text | Auflistung der Speisen |
| `kalorienverbrauch_kcal` | numeric | Sport, nur eintragen, nicht verrechnen |
| `bauch`, `stuhlgang`, `symptome` | text | optional; **Atmung gehört in `symptome`** |

`lebensmittel_analyse`:

| Spalte | Typ | Inhalt |
|---|---|---|
| `person`, `datum` | text, date | wie oben |
| `lebensmittel` | text | Titel, Format `Name (Menge)` |
| `duplikat` | boolean | Default `false`, normalerweise nicht setzen |
| `kalorien_kcal` | numeric | Pflicht |
| `eiweiss_g`, `kohlenhydrate_g`, `fett_g` | numeric | Pflicht |
| `zucker_g`, `ballaststoffe_g`, `cholesterin_mg`, `omega3_g` | numeric | schätzen |
| `calcium_mg`, `eisen_mg`, `folat_ug`, `jod_ug`, `kalium_mg`, `magnesium_mg`, `selen_ug`, `zink_mg` | numeric | schätzen |
| `vitamin_a_ug`, `vitamin_b12_ug`, `vitamin_c_mg`, `vitamin_d_ug`, `vitamin_e_mg`, `vitamin_k_ug` | numeric | schätzen |
| `darmgesundheit`, `low_fodmap`, `saeure_base` | text | `gut` / `neutral` / `schlecht` |

`notion_id` bleibt bei neuen Zeilen leer – die stammt aus der alten Quelle.
Differenz und Kaloriendefizit stehen **nicht** in der Datenbank: das rechnet
das Dashboard aus Kalorien und Kalorienziel selbst aus.

## ⚠️ Regel 1: Datum IMMER aus externer Quelle ziehen

Das heutige Datum wird bei JEDEM Tracking-Vorgang per Tool-Call aus einer
robusten Quelle geholt – NIEMALS aus dem Gesprächsverlauf, dem Gefühl oder
einer früheren Antwort übernommen (häufige Fehlerquelle: gestriger Tag wird
weiterverwendet):

1. **Pflicht-Schritt:** `https://worldtimeapi.org/api/timezone/Europe/Berlin`
   per web_fetch abrufen und das Feld `datetime` lesen (Datum + Wochentag für
   Zeitzone Berlin). Fallback bei Nichterreichbarkeit: Web-Suche nach
   "aktuelles datum deutschland" (z. B. timeanddate.de / zeitzonen.de).
2. Dieses externe Datum oben in der Antwort nennen ("Heutiges Datum: …").
3. Essen nach Mitternacht: gehört im Zweifel zum noch laufenden Vortag –
   kurz nachfragen.

Ein Suchen nach dem bestehenden Tageseintrag ist nicht mehr nötig: `(person,
datum)` ist eindeutig, der Upsert in Regel 2 trifft immer die richtige Zeile.

## ⚠️ Regel 2: KEIN Pflichtfeld darf leer bleiben (Carry-Forward-Prozedur)

1. **Vortagswerte laden** (Pflicht-Query vor dem Schreiben):

   ```sql
   select gewicht_kg, zielgewicht, ziel, kalorienziel_kcal
   from public.tagesuebersicht
   where person = 'Denis' and datum < date '2026-05-29'
   order by datum desc limit 1;
   ```

2. **Übernehmen, was nicht neu genannt wurde:** Gewicht, Zielgewicht, Ziel
   und Kalorienziel werden 1:1 aus diesem letzten Eintrag übernommen, außer
   im Chat wird explizit ein neuer Wert genannt (z. B. "wiege heute 61,8").
   Diese vier Felder dürfen unter KEINEN Umständen leer bleiben.

3. **Schreiben als Upsert** – legt an oder schreibt fort, nie doppelt:

   ```sql
   insert into public.tagesuebersicht
     (person, datum, tag, kalorien_kcal, protein_g, kohlenhydrate_g, fett_g,
      kalorienziel_kcal, gewicht_kg, zielgewicht, ziel, notizen)
   values
     ('Denis', date '2026-05-29', 'Freitag, 29.05.26', 1840, 112, 180, 62,
      1900, 79.4, 80, 'Abnehmen', 'Haferflocken, Skyr, Bowl, Riegel')
   on conflict (person, datum) do update set
     tag               = excluded.tag,
     kalorien_kcal     = excluded.kalorien_kcal,
     protein_g         = excluded.protein_g,
     kohlenhydrate_g   = excluded.kohlenhydrate_g,
     fett_g            = excluded.fett_g,
     kalorienziel_kcal = excluded.kalorienziel_kcal,
     gewicht_kg        = excluded.gewicht_kg,
     zielgewicht       = excluded.zielgewicht,
     ziel              = excluded.ziel,
     notizen           = excluded.notizen;
   ```

   **Wichtig:** Der Upsert überschreibt die genannten Spalten vollständig.
   Deshalb erst die vorhandene Zeile lesen, die Summen und Notizen
   fortschreiben, und den vollständigen neuen Stand schreiben. Spalten, die
   nicht in der Liste stehen (`bauch`, `stuhlgang`, `symptome`,
   `kalorienverbrauch_kcal`), bleiben unangetastet – sie nur aufnehmen, wenn
   im Chat etwas dazu gesagt wurde.

4. **Abhak-Check vor dem Absenden:** Sind Ziel, Zielgewicht, Gewicht und
   Kalorienziel gefüllt? Ein leeres davon ist ein Fehler und muss vor dem
   Antworten korrigiert werden.

## ⚠️ Regel 3: Titel-Format der Lebensmittel-Zeilen (STRIKT)

Format: **`Name (Menge)`** – z. B. "Milch 1,8% (250ml)", "Ei (2)".

- Menge NIE vorne ("100ml Milch" ❌ → "Milch 1,8% (100ml)" ✅)
- Keine Kommas, kein " mit ", " und ", " + ", " auf " außerhalb von Klammern.
  Zusätze in Klammern: "Flat White (Hafermilch)" ✅, "Flat White mit
  Hafermilch" ❌
- Basisnamen verwenden: "Ei" statt Spiegelei/Rührei/gekochtes Ei; konkrete
  Sorte statt Sammelbegriff, wenn bekannt (Zucchini statt "Gemüse")
- Marken-/Produktnamen bleiben vollständig ("Kellogg's Tresor (40g)")

## ⚠️ Regel 4: Splitten – auch Bowls

Zusammengesetzte Gerichte IMMER in Einzelzutaten-Zeilen trennen, auch kleine
Zutaten (Öl, Soße, Honig). **Bowls (auch Restaurant/Fertigbowls) werden in
ihre Komponenten gesplittet** (Basis, Protein, Gemüse, Sauce/Topping).
Einzige Ausnahme: einfache Markenprodukte ohne trennbare Komponenten
(Riegel, Eis, Schokolade).

## ⚠️ Regel 5: Duplikat-Schutz

Anders als die Tagesübersicht hat die Analyse **keinen** eindeutigen
Schlüssel – mehrere gleiche Zeilen pro Tag sind fachlich erlaubt (zweimal
derselbe Kaffee). Der Schutz liegt deshalb beim Skill:

```sql
select lebensmittel, kalorien_kcal
from public.lebensmittel_analyse
where person = 'Denis' and datum = date '2026-05-29'
order by lebensmittel;
```

Liegen dort schon Zeilen → nur die NEUEN Lebensmittel per `insert` ergänzen,
niemals den Tag komplett neu schreiben. Bricht ein Schreibvorgang mit einem
Fehler ab, IMMER erst mit dieser Query prüfen, ob er doch durchging, bevor er
wiederholt wird.

Mehrere Lebensmittel gehen in **einem** `insert ... values (...), (...)` –
ein Call statt zehn.

## ⚠️ Regel 6: Summen-Abgleich nach jedem Eintrag

Nach jedem Schreiben:

```sql
select coalesce(sum(kalorien_kcal), 0) as analyse,
       (select kalorien_kcal from public.tagesuebersicht
        where person = 'Denis' and datum = date '2026-05-29') as tag
from public.lebensmittel_analyse
where person = 'Denis' and datum = date '2026-05-29' and not duplikat;
```

Die Tagesübersicht ist IMMER die Baseline. Weicht die Summe ab → vorhandene
Zeile "Ausgleich Schätzdifferenz (±X kcal)" des Tages auf die neue Differenz
anpassen (`update ... where person = … and datum = … and lebensmittel like
'Ausgleich Schätzdifferenz%'`), sonst eine anlegen (nur `kalorien_kcal`;
Makros 0; keine Kategorien, keine Mikronährstoffe).
Ziel: Beide Tabellen stimmen nach jeder Antwort exakt überein.

## ⚠️ Regel 7: Mengen IMMER schätzen – NIEMALS nachfragen

Bei ungenauen Mengenangaben ("zwei Hände voll", "ein bisschen", "so'n
halbes Glas") wird **nie** nachgefragt. Es wird geschätzt, die Annahme wird
in der Antwort genannt, und der Nutzer korrigiert bei Bedarf von selbst.
Eine Rückfrage zur Menge ist ein Fehler.

**Schätz-Reihenfolge (erste passende Quelle gewinnt):**

1. **Alte Einträge derselben Person**: gleiches Lebensmittel schon mal
   getrackt? → identische Menge/Werte übernehmen.

   ```sql
   select lebensmittel, kalorien_kcal, eiweiss_g, kohlenhydrate_g, fett_g
   from public.lebensmittel_analyse
   where person = 'Denis' and lebensmittel ilike '%Skyr%'
   order by datum desc limit 3;
   ```

2. **Standard-/Packungsportion** des konkreten Produkts (z. B. Riegel,
   Fertigsalat, Becher).
3. **Referenztabelle** unten.

**Referenzmengen (Default bei fehlender Angabe):**

| Formulierung | Ansatz |
|---|---|
| eine Handvoll (Nüsse, Chips, Cerealien) | 30 g |
| zwei Hände voll | 55 g |
| ein bisschen / etwas (Käse, Belag, Streusel) | 15 g |
| ein Klecks (Soße, Dressing, Quark) | 20 g |
| ein Schuss (Öl, Sahne) | 10 ml |
| TL / EL | 5 g / 15 g |
| ein Glas / eine Tasse (Getränk) | 200 ml |
| eine Scheibe Brot / Toast | 40 g / 25 g |
| ein Becher Joghurt/Skyr | 150 g |
| eine Portion Gemüse / Salat | 150 g / 60 g |
| ein Teller Pasta/Reis (gekocht) | 250 g |
| ein Stück Kuchen | 80 g |
| ein Riegel | 25 g |
| ein Ei (M) | 55 g |

Bei "wenig/klein" −30 %, bei "viel/groß/ordentlich" +50 % auf den Default.

**Kennzeichnung:** Geschätzte Mengen in der Chat-Tabelle mit `~` markieren
(z. B. `~55 g`) und am Ende der Antwort ein Einzeiler: "Geschätzt: Choco
Chips ~55 g, Gouda ~15 g – sag Bescheid, wenn's daneben liegt." Damit bleibt
die Korrektur möglich, ohne den Eintrag zu blockieren.

Nachgefragt wird ausschließlich noch bei: unklarer **Tageszuordnung**
(Regel 1, Punkt 3) und wenn ein genanntes Lebensmittel gar nicht
identifizierbar ist (z. B. unverständliche Spracheingabe) – nie bei Mengen.

## Workflow bei neuen Mahlzeiten – in ZWEI Zügen

Das Schätzen der gut zwanzig Mikronährstoffe je Lebensmittel dauert länger als
alles andere zusammen. Es kommt deshalb **nach** der Antwort, nicht davor: was
interessiert (Kalorien, Makroverteilung, Ampel), steht sofort da, der Rest
läuft still nach. Beide Züge gehören zum selben Durchgang – Zug 2 wird nicht
auf später vertagt und nicht angekündigt und dann vergessen.

### Zug 1 – bis zur Antwort

1. Datum prüfen (Regel 1).
2. Mengen schätzen (Regel 7), dann **nur** Kalorien und die drei Makros
   (Eiweiß, Kohlenhydrate, Fett). Gleiche Lebensmittel wie an Vortagen =
   gleiche Werte.
3. Bestehende Analyse-Zeilen des Tages lesen (Regel 5) – in derselben Query
   gleich die Nachzügler aus abgebrochenen Durchgängen mitnehmen, das spart
   einen Aufruf:

   ```sql
   select id, datum, lebensmittel, kalorien_kcal,
          (darmgesundheit is null) as nachtrag_offen
   from public.lebensmittel_analyse
   where person = 'Denis'
     and (datum = date '2026-09-06'
          or (datum > current_date - 14
              and darmgesundheit is null
              and lebensmittel not like 'Ausgleich Schätzdifferenz%'))
   order by datum desc, lebensmittel;
   ```

   Was mit `nachtrag_offen` zurückkommt, wird in Zug 2 mitversorgt.
4. Neue Zeilen per **einem** Sammel-`insert` anlegen – Pflichtfelder und sonst
   nichts. Das `returning` liefert die `id`s, die Zug 2 braucht:

   ```sql
   insert into public.lebensmittel_analyse
     (person, datum, lebensmittel, kalorien_kcal, eiweiss_g, kohlenhydrate_g, fett_g)
   values
     ('Denis', date '2026-09-06', 'Skyr 0,2% (150g)', 97, 17, 6, 0.3),
     ('Denis', date '2026-09-06', 'Blaubeeren (80g)', 46, 0.6, 9.8, 0.3)
   returning id, lebensmittel;
   ```

5. Tagesübersicht per Upsert fortschreiben (Regel 2).
6. Summen-Abgleich (Regel 6).
7. **Antworten** – Tabelle, Summe, Ampel (siehe Antwort-Format).

Schritt 4 vor Schritt 5, damit die Tagessumme aus dem tatsächlich
geschriebenen Stand entsteht.

### Zug 2 – nach der Antwort, still

8. Mikronährstoffe und die drei Kategorien für **genau die `id`s aus Schritt 4**
   nachtragen. Ein `update` für alle Zeilen, nicht eines pro Zeile:

   ```sql
   update public.lebensmittel_analyse t set
     zucker_g = v.zucker, ballaststoffe_g = v.ballast, cholesterin_mg = v.chol,
     omega3_g = v.omega3, calcium_mg = v.calcium, eisen_mg = v.eisen,
     folat_ug = v.folat, jod_ug = v.jod, kalium_mg = v.kalium,
     magnesium_mg = v.magnesium, selen_ug = v.selen, zink_mg = v.zink,
     vitamin_a_ug = v.vit_a, vitamin_b12_ug = v.vit_b12, vitamin_c_mg = v.vit_c,
     vitamin_d_ug = v.vit_d, vitamin_e_mg = v.vit_e, vitamin_k_ug = v.vit_k,
     darmgesundheit = v.darm, low_fodmap = v.fodmap, saeure_base = v.saeure
   from (values
     ('<id-1>'::uuid, 4.0, 0.0, 8, 0.0, 180, 0.1, 12, 9, 230, 15, 5, 0.6,
      2, 0.8, 1, 0.1, 0.1, 0.2, 'gut', 'gut', 'neutral'),
     ('<id-2>'::uuid, 8.0, 1.9, 0, 0.1,   5, 0.2, 5, 1,  62,  5, 0, 0.1,
      2, 0.0, 8, 0.0, 0.4, 15.6, 'gut', 'gut', 'gut')
   ) as v(id, zucker, ballast, chol, omega3, calcium, eisen, folat, jod, kalium,
          magnesium, selen, zink, vit_a, vit_b12, vit_c, vit_d, vit_e, vit_k,
          darm, fodmap, saeure)
   where t.id = v.id;
   ```

9. Ein Satz zum Abschluss, mehr nicht: "Nährstoffe ergänzt."

### Wenn Zug 2 ausfällt

Bricht der Durchgang zwischen den Zügen ab, bleiben Zeilen mit Kalorien und
Makros zurück, denen die Mikronährstoffe fehlen. Die Teilung kauft
Geschwindigkeit gegen dieses Risiko – deshalb holt Schritt 3 die Nachzügler
der letzten 14 Tage jedes Mal mit ein, und Zug 2 versorgt sie zusammen mit den
neuen Zeilen. Ein verpasster Nachtrag heilt damit beim nächsten Eintrag von
selbst.

`darmgesundheit` ist der Marker: in Zug 1 nie gesetzt, in Zug 2 immer. Die
Ausgleichszeilen aus Regel 6 tragen absichtlich keine Kategorien und sind
deshalb ausgenommen.

Fällt beim Nachtragen auf, dass eine Zeile älter als 14 Tage ist und noch
offen: `pruefung.sql` im Repo zeigt offene Nachträge ohne Zeitgrenze.

## Tageszuordnung & Korrekturen

"gestern" = heute−1, "vorgestern" = heute−2, Wochentag/Datum explizit =
dieser Tag.

Korrekturen: betroffene Positionen in BEIDEN Tabellen anpassen bzw.
verschieben, danach Summen-Abgleich. Verschieben heißt `update ... set datum
= …` mit `where person = … and datum = … and lebensmittel = …` – nicht
löschen und neu anlegen. Im Zweifel nachfragen – aber nur zur
Tageszuordnung, nie zu Mengen (Regel 7).

## Antwort-Format

Die Antwort kommt in zwei Teilen, passend zu den zwei Zügen.

**Nach Zug 1** – das ist die eigentliche Antwort: heutiges Datum oben,
kompakte Tabelle (Positionen mit kcal und den drei Makros + Summe), Ampel
(🟢 Denis ≤1995 / Leni ≤~1575 · 🟡 · 🔴), knapper Kommentar ohne
Moralisieren. Geschätzte Mengen mit `~` markieren + Einzeiler am Ende
(Regel 7). Zum Schluss ein Halbsatz, dass die Nährstoffe noch nachlaufen.

**Nach Zug 2** – eine Zeile, mehr nicht: "Nährstoffe ergänzt."

Der Sinn der Teilung: die Tabelle steht sofort da. Nicht erst alles rechnen
und dann in einem Block antworten – dann wartet man auf das Uninteressante.

Das Dashboard aktualisiert sich nicht sofort: es wird zweimal täglich neu
gebaut (13:00 und 19:00 UTC). Frisch Eingetragenes ist dort also erst beim
nächsten Lauf zu sehen.
