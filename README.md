# Kalorienbrudi

Ein statisches Dashboard für das Kalorien- und Nährstofftracking von Denis und
Leni. Ein Python-Skript liest Supabase und schreibt eine einzelne `index.html`,
die auf Cloudflare Pages liegt. Kein Server, keine Datenbank im Browser.

## Wie die Daten fließen

```
Chat (/brudi-Skill)  ──►  Supabase  ──►  build_dashboard.py  ──►  Cloudflare Pages
                            ▲
                            └── sync_supabase.py (Notion, Übergang)
```

Eingetragen wird im Chat über den `/brudi`-Skill, der direkt nach Supabase
schreibt. Gebaut wird in GitHub Actions: bei jedem Push und zusätzlich zweimal
täglich (13:00 und 19:00 UTC), damit die Zahlen auch ohne Code-Änderung frisch
bleiben. Deshalb liegt der Build in Actions und nicht in der Git-Anbindung von
Cloudflare Pages — die kennt keine geplanten Builds.

`sync_supabase.py` ist der Rest des Umzugs von Notion und die einzige
verbliebene Notion-Abhängigkeit. Sobald die Eingabe vollständig über Supabase
läuft, können die Datei, `supabase-sync.yml` und das Secret `NOTION_TOKEN`
ersatzlos weg.

## Die Datenbank

Das Supabase-Projekt ist **gemeinsam mit Malena Cosmetics** genutzt. Im Schema
`public` liegen deshalb drei Tabellen aus zwei Vorhaben:

| Tabelle | Gehört zu | Inhalt |
|---|---|---|
| `tagesuebersicht` | Kalorienbrudi | eine Zeile pro Person und Tag |
| `lebensmittel_analyse` | Kalorienbrudi | eine Zeile pro erfasstem Lebensmittel |
| `termine` | **Malena Cosmetics** | Termine aus Treatwell — nicht anfassen |

Jede Tabelle trägt eine Beschreibung in der Datenbank selbst (`comment on
table`), damit die Zuordnung auch in der Supabase-Oberfläche sichtbar ist und
nicht nur hier steht.

Was das praktisch heißt: Der `service_role`-Key dieses Projekts kommt an
**alle drei** Tabellen. Er liegt ausschließlich in GitHub Actions, nie im
ausgelieferten Dashboard. Der `/brudi`-Skill grenzt sich in seiner Regel 0
selbst auf die zwei Kalorienbrudi-Tabellen ein — das ist eine Selbstverpflich-
tung, keine technische Sperre.

**Zugriff:** Auf beiden Kalorienbrudi-Tabellen ist RLS aktiv, bewusst **ohne**
Policy. Damit kommt der `anon`-Key nicht an die Daten; gelesen wird nur mit dem
`service_role`-Key in Actions. Der Supabase-Linter meldet das als Hinweis
(`rls_enabled_no_policy`) — hier ist es Absicht, nicht ein Versäumnis.

## Migrationen

Die Dateien in `supabase/` sind die Wahrheit; angewendet werden sie auf zwei
Wegen, die zum selben Ergebnis führen:

- über den **Supabase-Connector** (MCP), wenn er in der Sitzung verfügbar ist —
  dann landen sie zusätzlich in Supabases eigener Migrationshistorie
  (`list_migrations`), die dieselben Namen trägt wie die Dateien hier;
- über den Workflow **„Supabase-Migration ausführen"** (`supabase-migrate.yml`),
  der eine Datei aus `supabase/` per `psql` ausführt. Den braucht es, weil die
  Sandbox ohne Connector `supabase.co` nicht erreicht (der Egress-Proxy lehnt
  CONNECT ab).

Beide Wege sind nachvollziehbar — anders als Copy-Paste im SQL-Editor.

| Datei | Zweck |
|---|---|
| `001_schema.sql` | Stand für eine leere Datenbank |
| `002_fehlende_felder.sql` | Notizen, Ziel, Sport, Bauch/Stuhlgang/Symptome; Makros je Lebensmittel |
| `003_tagesschluessel.sql` | `(person, datum)` eindeutig; Trigger für `aktualisiert_am` |
| `004_aufraeumen.sql` | Beschreibungen aller Tabellen und Spalten; `search_path` der Trigger-Funktion |
| `pruefung.sql` | liest nur — zeigt Zeilenzahlen, Füllstände und doppelte Tage |

`001_schema.sql` ist der Stand für eine **leere** Datenbank, keine Historie.
`create table if not exists` ergänzt keine Spalten an bestehenden Tabellen —
eine Änderung muss deshalb in einer neuen, durchnummerierten Migration **und**
in `001_schema.sql` stehen.

## Secrets

| Secret | Wofür |
|---|---|
| `SUPABASE_URL` | Build und Sync |
| `SUPABASE_SERVICE_KEY` | Build und Sync (umgeht RLS) |
| `SUPABASE_DB_URL` | nur Migrationen (Direktverbindung/Session Pooler, Port 5432) |
| `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` | Veröffentlichen |
| `NOTION_TOKEN` | nur noch für `sync_supabase.py` |

## Dateien

| Datei | Zweck |
|---|---|
| `build_dashboard.py` | liest Supabase, schreibt `index.html` (stdlib only) |
| `sync_supabase.py` | spiegelt Notion nach Supabase (Übergang) |
| `skills/brudi/SKILL.md` | der Eingabe-Skill; liegt hier, weil er zum Schema gehört |
| `supabase/` | Schema, Migrationen, Prüfung |

`index.html` ist **nicht** eingecheckt — sie entsteht bei jedem Build neu.
