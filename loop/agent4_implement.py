"""Agent 4 — Umsetzung.
Sammelt alle freigegebenen ([x]) Vorschläge aus loop/proposals/, übergibt sie
an Claude Code (headless) zur Umsetzung im Repo, baut das Dashboard testweise
und verschiebt erledigte Punkte ins decisions.md. Bei fehlendem Claude Code wird
ein Aufgaben-Branch mit TODO-Datei erstellt (Fallback).
"""
import subprocess, datetime, re, pathlib, shutil
from lib import PROPOSALS, DECISIONS, BACKLOG, ROOT, TODAY

REPO = ROOT.parent  # loop/ liegt im Repo-Root

def approved_items():
    items = []
    for f in sorted(PROPOSALS.glob("*.md")):
        for line in f.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\s*-\s*\[[xX]\]\s*(.+)", line)
            if m:
                items.append((f.name, m.group(1).strip()))
    return items

def run(cmd, **kw):
    return subprocess.run(cmd, cwd=REPO, text=True, capture_output=True, **kw)

def build_ok():
    """Testbuild des Dashboards; grün = Erfolg."""
    r = run(["python", "build_dashboard.py"])
    return r.returncode == 0, (r.stderr or r.stdout)[-1000:]

def main():
    items = approved_items()
    if not items:
        print("Agent4: keine freigegebenen Punkte."); return
    task = "\n".join(f"- {t}" for _, t in items)
    print(f"Agent4: {len(items)} freigegebene Punkte")

    if shutil.which("claude"):
        prompt = (
            "Setze folgende freigegebene Aufgaben in diesem Repo um. Ändere das Dashboard "
            "ausschließlich über build_dashboard.py (HTML_TEMPLATE bzw. Python-Teil), "
            "committe NICHT die index.html. Halte dich an die bestehende Architektur. "
            "Nach der Umsetzung muss `python build_dashboard.py` fehlerfrei durchlaufen.\n\n"
            f"Aufgaben:\n{task}")
        run(["claude", "-p", prompt, "--permission-mode", "acceptEdits"])
    else:
        # Fallback: Aufgabenliste als Datei ablegen
        (REPO / "loop" / f"TODO-{TODAY}.md").write_text(
            f"# Umzusetzen {TODAY}\n\n{task}\n", encoding="utf-8")
        print("Agent4: Claude Code nicht gefunden – TODO-Datei geschrieben.")

    ok, log = build_ok()
    status = "✅ Build grün" if ok else f"❌ Build rot:\n{log}"
    with open(DECISIONS, "a", encoding="utf-8") as fh:
        fh.write(f"\n## {TODAY} — umgesetzt ({status})\n" + task + "\n")
    print("Agent4:", status)

if __name__ == "__main__":
    main()
