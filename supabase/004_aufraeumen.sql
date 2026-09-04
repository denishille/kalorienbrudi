-- Aufraeumen im gemeinsamen Projekt.
--
-- In dieser Datenbank liegen ZWEI Vorhaben nebeneinander: Kalorienbrudi
-- (tagesuebersicht, lebensmittel_analyse) und Malena Cosmetics (termine).
-- Wer die Tabellenliste aufmacht, soll ohne Nachfragen sehen, was wozu
-- gehoert - deshalb bekommt jede Tabelle und jede nicht offensichtliche
-- Spalte eine Beschreibung. Kommentare sind reine Metadaten: kein Code liest
-- sie, es kann daran nichts brechen.

-- ------------------------------------------------------- search_path festnageln
-- Der Supabase-Linter meldet die Trigger-Funktion zu Recht: ohne festes
-- search_path entscheidet die aufrufende Rolle, wo Namen aufgeloest werden.
-- Bei dieser Funktion ist das harmlos, aber es kostet nichts, es zu schliessen.
-- Leeres search_path heisst: nur pg_catalog, alles andere muss qualifiziert
-- werden. Der Rumpf braucht nur now() - das steht in pg_catalog.
create or replace function public.set_aktualisiert_am()
returns trigger
language plpgsql
security invoker
set search_path = ''
as $$
begin
  new.aktualisiert_am := now();
  return new;
end;
$$;

comment on function public.set_aktualisiert_am() is
  'Setzt aktualisiert_am bei jedem UPDATE. Haengt an tagesuebersicht und lebensmittel_analyse.';

-- ------------------------------------------------------------------ Kalorienbrudi
comment on table public.tagesuebersicht is
  'Kalorienbrudi: eine Zeile pro Person und Tag. Quelle des Dashboards. Repo: github.com/denishille/kalorienbrudi';
comment on table public.lebensmittel_analyse is
  'Kalorienbrudi: eine Zeile pro erfasstem Lebensmittel. Quelle des Dashboards. Repo: github.com/denishille/kalorienbrudi';

comment on column public.tagesuebersicht.notion_id is
  'Herkunft aus der alten Notion-Datenbank. Zeilen, die direkt hier entstehen, lassen sie leer. Faellt weg, sobald Notion abgeschaltet ist.';
comment on column public.tagesuebersicht.person is 'Denis oder Leni.';
comment on column public.tagesuebersicht.tag is 'Anzeigetitel, Format "Freitag, 29.05.26".';
comment on column public.tagesuebersicht.kalorienverbrauch_kcal is
  'Durch Sport verbraucht. Wird nur festgehalten, nicht gegen die Aufnahme verrechnet.';
comment on column public.tagesuebersicht.symptome is
  'Freitext. Auch Angaben zur Atmung gehoeren hierher.';
comment on column public.tagesuebersicht.aktualisiert_am is
  'Letzte Aenderung, per Trigger gesetzt.';

comment on column public.lebensmittel_analyse.notion_id is
  'Herkunft aus der alten Notion-Datenbank. Siehe tagesuebersicht.notion_id.';
comment on column public.lebensmittel_analyse.lebensmittel is
  'Titel im Format "Name (Menge)", z. B. "Milch 1,8% (250ml)".';
comment on column public.lebensmittel_analyse.duplikat is
  'Markiert versehentliche Doppelerfassungen. Die Auswertung rechnet sie heraus, geloescht wird nichts.';
comment on column public.lebensmittel_analyse.eiweiss_g is
  'Heisst in der Tagestabelle protein_g - die Namen folgen der jeweiligen Quelle.';
comment on column public.lebensmittel_analyse.darmgesundheit is 'Ampel: gut | neutral | schlecht.';
comment on column public.lebensmittel_analyse.low_fodmap is 'Ampel: gut | neutral | schlecht.';
comment on column public.lebensmittel_analyse.saeure_base is 'Ampel: gut | neutral | schlecht.';

-- --------------------------------------------------------------- Malena Cosmetics
-- Fremde Tabelle, deshalb nur beschriftet und sonst nicht angefasst. Ohne
-- diese Zeile steht sie unerklaert zwischen den Kalorienbrudi-Tabellen.
comment on table public.termine is
  'Malena Cosmetics: Termine aus dem Treatwell-Partnerkalender. Gehoert NICHT zum Kalorienbrudi-Dashboard.';
