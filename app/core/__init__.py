from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data"
REGISTERED_USERS_PATH = DATA_PATH / "registered.json"
USERS_DIRECTORY = DATA_PATH / "users"
REPORTS_DIRECTORY = DATA_PATH / "reports"

DATA_PATH.mkdir(parents=True, exist_ok=True)
USERS_DIRECTORY.mkdir(parents=True, exist_ok=True)
REPORTS_DIRECTORY.mkdir(parents=True, exist_ok=True)

if not REGISTERED_USERS_PATH.exists():
    REGISTERED_USERS_PATH.write_text("{ \"users\": []}", encoding="utf-8")
