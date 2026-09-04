-- Ein Tag, eine Person, eine Zeile - als Regel in der Datenbank.
--
-- Bisher hing die Eindeutigkeit an notion_id. Das trug, solange Notion die
-- Quelle war. Sobald die Eingabe direkt nach Supabase schreibt, gibt es keine
-- Notion-ID mehr, und ein zweiter Eintrag fuer denselben Tag waere moeglich -
-- der Fehler, gegen den Regel 1 des Eingabe-Skills anschreibt. Besser, die
-- Datenbank laesst ihn gar nicht erst zu.
--
-- Der Index macht ausserdem das Fortschreiben einfach: ein
-- "insert ... on conflict (person, datum) do update" trifft immer die richtige
-- Zeile, ohne vorher suchen zu muessen.
--
-- Faellt dieser Lauf mit "could not create unique index" aus, liegen schon
-- doppelte Tage in der Tabelle. Dann zuerst aufraeumen, nicht den Index
-- weglassen.

create unique index if not exists tagesuebersicht_person_datum_uniq
  on public.tagesuebersicht (person, datum);

-- Der alte, nicht eindeutige Index waere jetzt doppelt gemoppelt.
drop index if exists public.tagesuebersicht_person_datum_idx;

-- ------------------------------------------------------------- Aktualisiert am
-- Bisher stand dort nur, wann die Zeile ENTSTANDEN ist: der Default greift
-- beim Einfuegen, ein Update liess ihn stehen. Ein Trigger macht daraus, was
-- der Name verspricht.
create or replace function public.set_aktualisiert_am()
returns trigger
language plpgsql
as $$
begin
  new.aktualisiert_am := now();
  return new;
end;
$$;

drop trigger if exists tagesuebersicht_aktualisiert_am on public.tagesuebersicht;
create trigger tagesuebersicht_aktualisiert_am
  before update on public.tagesuebersicht
  for each row execute function public.set_aktualisiert_am();

drop trigger if exists lebensmittel_analyse_aktualisiert_am on public.lebensmittel_analyse;
create trigger lebensmittel_analyse_aktualisiert_am
  before update on public.lebensmittel_analyse
  for each row execute function public.set_aktualisiert_am();
