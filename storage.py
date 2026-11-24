import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "concrete_tests.json"

def load_records():
    DATA_DIR.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        return {}
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_records(records):
    DATA_DIR.mkdir(exist_ok=True)
    temp = DATA_FILE.with_suffix(".tmp")
    with temp.open("w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
    temp.replace(DATA_FILE)
