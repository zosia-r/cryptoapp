from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data"
REGISTERED_USERS_PATH = DATA_PATH / "registered.json"
USERS_DIRECTORY = DATA_PATH / "users"

DATA_PATH.mkdir(parents=True, exist_ok=True)
USERS_DIRECTORY.mkdir(parents=True, exist_ok=True)

if not REGISTERED_USERS_PATH.exists():
    REGISTERED_USERS_PATH.write_text("{ \"users\": []}", encoding="utf-8")
