-- Nachtrag: Felder, die Notion haelt, das Schema aber nicht hatte.
--
-- Das erste Schema war aus dem abgeleitet, was das Dashboard LIEST. Notion
-- hielt aber mehr - eine Bestandsaufnahme aller Notion-Properties hat die
-- Luecke gezeigt. Ohne diese Spalten waeren die Felder beim Umzug der
-- Eingabe dauerhaft weg gewesen.
--
-- Bewusst NICHT uebernommen sind die Notion-Formeln "Differenz",
-- "Kaloriendefizit", "Ziel erreicht" und "Ziel nicht erreicht": sie sind
-- restlos aus Kalorien und Kalorienziel ausgerechnet. Abgeleitetes gehoert
-- nicht in die Ablage - es wuerde beim naechsten Schreiben veralten.
--
-- Mehrfaches Ausfuehren ist unschaedlich (IF NOT EXISTS).

-- ---------------------------------------------------------------- Tagesuebersicht
alter table public.tagesuebersicht
  add column if not exists ziel                   text,     -- Notion: Ziel (select)
  add column if not exists notizen                text,     -- Notion: Notizen
  add column if not exists kalorienverbrauch_kcal numeric,  -- Notion: Kalorienverbrauch (Sport)
  add column if not exists bauch                  text,
  add column if not exists stuhlgang              text,
  add column if not exists symptome               text;

-- ------------------------------------------------------------ Lebensmittel-Analyse
-- Die Makros je Lebensmittel. Die Tagestabelle hat sie als Summe, hier fehlten
-- sie je Eintrag. "Eiweiss" heisst in Notion so, in der Tagestabelle "Protein" -
-- die Namen bleiben wie in der Quelle, damit die Zuordnung eindeutig bleibt.
alter table public.lebensmittel_analyse
  add column if not exists eiweiss_g       numeric,
  add column if not exists fett_g          numeric,
  add column if not exists kohlenhydrate_g numeric,
  add column if not exists zucker_g        numeric;
