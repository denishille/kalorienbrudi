"""Gemeinsame Helfer für den Kalorienbrudi-Agenten-Loop."""
import os, json, time, urllib.request, urllib.error, datetime, pathlib

# --- Config -----------------------------------------------------------------
NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
NOTION_VERSION = "2025-09-03"
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-8")

DS_TAGES = "a748d265-3bbe-448b-b4e8-c8111c208c46"      # Tagesübersicht
DS_ANALYSE = "be09a702-364a-4f0f-9548-5f4f32092dee"    # Lebensmittel-Analyse / Nährstoffbrudi
DASHBOARD_URL = "https://denishille.github.io/kalorienbrudi/"

ROOT = pathlib.Path(__file__).resolve().parent
REPORTS = ROOT / "reports"
PROPOSALS = ROOT / "proposals"
BACKLOG = ROOT / "backlog.md"
DECISIONS = ROOT / "decisions.md"
STATE = ROOT / "state.json"

TODAY = datetime.date.today().isoformat()
WD_DE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

# --- Notion -----------------------------------------------------------------
def _post(url, payload):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {NOTION_TOKEN}",
                 "Notion-Version": NOTION_VERSION,
                 "Content-Type": "application/json"}, method="POST")
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:            # Rate limit → warten
                time.sleep(35); continue
            raise
    raise RuntimeError("Notion: zu viele Rate-Limits")

def query_all(ds_id):
    """Alle Seiten einer Data Source (mit Pagination)."""
    out, cursor = [], None
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        data = _post(f"https://api.notion.com/v1/data_sources/{ds_id}/query", body)
        out.extend(data.get("results", []))
        if not data.get("has_more"):
            return out
        cursor = data["next_cursor"]

def prop(page, name):
    """Wert einer Property typunabhängig extrahieren."""
    p = page.get("properties", {}).get(name)
    if not p:
        return None
    t = p["type"]
    v = p[t]
    if t == "number":       return v
    if t == "checkbox":     return v
    if t == "select":       return v["name"] if v else None
    if t == "date":         return v["start"] if v else None
    if t in ("title", "rich_text"):
        return "".join(x["plain_text"] for x in v) if v else ""
    return v

# --- Reports / State --------------------------------------------------------
def write_report(kind, text):
    REPORTS.mkdir(parents=True, exist_ok=True)
    path = REPORTS / f"{TODAY}-{kind}.md"
    path.write_text(text, encoding="utf-8")
    return path

def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"last_run": None, "history": []}

def save_state(state):
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

# --- Anthropic --------------------------------------------------------------
def _messages(payload):
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages", data=json.dumps(payload).encode(),
        headers={"x-api-key": ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01",
                 "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print("Anthropic API error", e.code, e.read().decode())
        raise
    return "".join(b["text"] for b in data["content"] if b["type"] == "text")

def claude(system, user, max_tokens=4000):
    return _messages({"model": ANTHROPIC_MODEL, "max_tokens": max_tokens,
                      "system": system, "messages": [{"role": "user", "content": user}]})

def claude_vision(system, user, image_paths, max_tokens=4000):
    """Design-/UX-Bewertung: ein oder mehrere Screenshots an Claude schicken."""
    import base64
    content = []
    for p in image_paths:
        b64 = base64.b64encode(pathlib.Path(p).read_bytes()).decode()
        content.append({"type": "image", "source": {"type": "base64",
                        "media_type": "image/png", "data": b64}})
    content.append({"type": "text", "text": user})
    return _messages({"model": ANTHROPIC_MODEL, "max_tokens": max_tokens,
                      "system": system, "messages": [{"role": "user", "content": content}]})
