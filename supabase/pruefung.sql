-- Nur lesen: zeigt, ob in Supabase wirklich das steht, was in Notion stand.
-- Ueber den Workflow "Supabase-Migration ausfuehren" mit datei=pruefung.sql.
-- Aendert nichts und kann jederzeit laufen.

\echo '--- Zeilen je Person ---'
select person, count(*) as tage, min(datum) as von, max(datum) as bis
from public.tagesuebersicht group by person order by person;

\echo '--- Tagesuebersicht: wie viele Zeilen haben welchen Wert? ---'
select count(*)                            as zeilen,
       count(kalorien_kcal)                as kalorien,
       count(gewicht_kg)                   as gewicht,
       count(zielgewicht)                  as zielgewicht,
       count(ziel)                         as ziel,
       count(notizen)                      as notizen,
       count(kalorienverbrauch_kcal)       as sport,
       count(bauch)                        as bauch,
       count(stuhlgang)                    as stuhlgang,
       count(symptome)                     as symptome
from public.tagesuebersicht;

\echo '--- Lebensmittel-Analyse: Makros je Eintrag ---'
select count(*)                as zeilen,
       count(kalorien_kcal)    as kalorien,
       count(eiweiss_g)        as eiweiss,
       count(kohlenhydrate_g)  as kohlenhydrate,
       count(fett_g)           as fett,
       count(zucker_g)         as zucker
from public.lebensmittel_analyse;

\echo '--- Doppelte Tage (muss leer sein) ---'
select person, datum, count(*)
from public.tagesuebersicht group by person, datum having count(*) > 1;

\echo '--- Letzte drei Tage je Person ---'
select person, datum, tag, kalorien_kcal, gewicht_kg, ziel,
       left(coalesce(notizen, ''), 60) as notizen_anfang
from (select *, row_number() over (partition by person order by datum desc) as r
      from public.tagesuebersicht) t
where r <= 3 order by person, datum desc;

\echo '--- Offene Nachtraege: Zeilen mit Makros, aber ohne Mikronaehrstoffe ---'
-- Der Eingabe-Skill schreibt in zwei Zuegen: erst Kalorien und Makros, damit
-- die Antwort sofort dasteht, danach die Mikronaehrstoffe. Bricht der zweite
-- Zug ab, bleibt eine halbe Zeile stehen. Der Skill holt Nachzuegler der
-- letzten 14 Tage selbst nach - was hier auftaucht, ist aelter und braucht
-- einen Anstoss von Hand.
--
-- Zwei Gruppen sind ausgenommen, weil sie hier nur Rauschen waeren:
-- die Ausgleichszeilen (tragen absichtlich keine Kategorien) und Zeilen aus
-- dem Notion-Altbestand (33 Stueck, Mai bis Juli 2026) - die hatten schon
-- dort keine Kategorien und stammen nicht aus dem zweistufigen Verfahren.
select person, datum, lebensmittel, kalorien_kcal
from public.lebensmittel_analyse
where darmgesundheit is null
  and notion_id is null
  and lebensmittel not like 'Ausgleich Schätzdifferenz%'
order by datum desc, person, lebensmittel;
