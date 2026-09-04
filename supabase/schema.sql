-- Kalorienbrudi: Schema fuer den Umzug von Notion nach Supabase.
-- Ueber den Workflow "Supabase-Migration ausfuehren" laufen lassen.
-- Mehrfaches Ausfuehren ist unschaedlich (IF NOT EXISTS).
--
-- Achtung: "create table if not exists" ergaenzt KEINE Spalten an bestehenden
-- Tabellen. Diese Datei ist der Stand fuer eine leere Datenbank; nachtraegliche
-- Aenderungen liegen als eigene Migration daneben (002_fehlende_felder.sql)
-- und muessen dort UND hier stehen.
--
-- Schluessel-Entwurf: eine eigene UUID ist der Primaerschluessel, die
-- Notion-Seiten-ID steht daneben und ist eindeutig. Damit ist der Sync ein
-- sauberer Upsert, und Zeilen, die spaeter direkt in Supabase entstehen,
-- brauchen keine Notion-ID mehr. Sobald Notion abgeschaltet ist, kann die
-- Spalte ersatzlos entfallen.

create extension if not exists pgcrypto;

-- ---------------------------------------------------------------- Tagesuebersicht
-- Eine Zeile pro Person und Tag: die Tages-Summen und die Zielwerte.
create table if not exists public.tagesuebersicht (
  id                uuid primary key default gen_random_uuid(),
  notion_id         text unique,
  person            text not null,
  datum             date not null,
  tag               text,
  kalorien_kcal     numeric,
  protein_g         numeric,
  kohlenhydrate_g   numeric,
  fett_g            numeric,
  kalorienziel_kcal numeric,
  gewicht_kg        numeric,
  zielgewicht       numeric,

  ziel                   text,     -- Tagesziel, in Notion ein select
  notizen                text,
  kalorienverbrauch_kcal numeric,  -- durch Sport verbraucht
  bauch                  text,
  stuhlgang              text,
  symptome               text,

  aktualisiert_am   timestamptz not null default now()
);

create index if not exists tagesuebersicht_person_datum_idx
  on public.tagesuebersicht (person, datum);

-- ------------------------------------------------------------ Lebensmittel-Analyse
-- Eine Zeile pro erfasstem Lebensmittel. Mehrere Eintraege pro Person und Tag
-- sind der Normalfall, deshalb gibt es hier keinen fachlichen Schluessel.
create table if not exists public.lebensmittel_analyse (
  id              uuid primary key default gen_random_uuid(),
  notion_id       text unique,
  person          text not null,
  datum           date not null,
  lebensmittel    text,
  duplikat        boolean not null default false,
  kalorien_kcal   numeric,

  -- Makros je Eintrag. "Eiweiss" heisst in Notion so, in der Tagestabelle
  -- "Protein" - die Namen bleiben wie in der Quelle.
  eiweiss_g       numeric,
  fett_g          numeric,
  kohlenhydrate_g numeric,
  zucker_g        numeric,

  ballaststoffe_g numeric,
  calcium_mg      numeric,
  eisen_mg        numeric,
  folat_ug        numeric,
  jod_ug          numeric,
  kalium_mg       numeric,
  magnesium_mg    numeric,
  omega3_g        numeric,
  selen_ug        numeric,
  vitamin_a_ug    numeric,
  vitamin_b12_ug  numeric,
  vitamin_c_mg    numeric,
  vitamin_d_ug    numeric,
  vitamin_e_mg    numeric,
  vitamin_k_ug    numeric,
  zink_mg         numeric,
  cholesterin_mg  numeric,

  -- Ampel-Kategorien aus der Analyse: 'gut' | 'neutral' | 'schlecht'
  darmgesundheit  text,
  low_fodmap      text,
  saeure_base     text,

  aktualisiert_am timestamptz not null default now()
);

create index if not exists lebensmittel_analyse_person_datum_idx
  on public.lebensmittel_analyse (person, datum);

-- ---------------------------------------------------------------------- Zugriff
-- RLS an, aber bewusst KEINE Policy: damit kommt der anon-Key nicht an die
-- Daten. Der Build liest mit dem service_role-Key, der RLS umgeht und
-- ausschliesslich in GitHub Actions liegt - nie im ausgelieferten Dashboard.
alter table public.tagesuebersicht     enable row level security;
alter table public.lebensmittel_analyse enable row level security;
