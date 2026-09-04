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
