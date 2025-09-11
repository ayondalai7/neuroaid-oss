import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
JOURNAL_PATH = DATA_DIR / "journal.json"

def append_journal(entry: dict):
    existing = []
    if JOURNAL_PATH.exists():
        try:
            existing = json.loads(JOURNAL_PATH.read_text(encoding="utf-8"))
        except Exception:
            existing = []
    existing.append(entry)
    JOURNAL_PATH.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    return JOURNAL_PATH

def load_journal():
    if JOURNAL_PATH.exists():
        try:
            return json.loads(JOURNAL_PATH.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []
