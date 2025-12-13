import json
from datetime import datetime
from app.core import USERS_DIRECTORY, REGISTERED_USERS_PATH
from app.cryptography import auth_encry


def load_user_data(username: str) -> dict:
    user_directory = USERS_DIRECTORY / username
    user_directory.mkdir(parents=True, exist_ok=True)
    user_file = user_directory / "data.json"

    with open(user_file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_user_data(username: str, data: dict) -> None:
    user_directory = USERS_DIRECTORY / username
    user_directory.mkdir(parents=True, exist_ok=True)
    user_file = user_directory / "data.json"

    with open(user_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_registered_users(registered_users_path=REGISTERED_USERS_PATH):
    try:
        with open(registered_users_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": []}
    except json.JSONDecodeError:
        return {"users": []}
    
def save_registered_users(data, registered_users_path=REGISTERED_USERS_PATH):
    with open(registered_users_path, "w") as file:
        json.dump(data, file, indent=4)

def create_user_file(username, users_directory=USERS_DIRECTORY):
    user_directory = users_directory / username
    user_directory.mkdir(parents=True, exist_ok=True)
    user_file_path = user_directory / "data.json"
    
    if not user_file_path.exists():
        data = {
            "data": {
                "expenses": [],
                "incomes": []
            }
        }
        with open(user_file_path, "w") as file:
            json.dump(data, file, indent=4)

def create_user_report_directory(username, users_directory=USERS_DIRECTORY):
    user_report_dir = users_directory / username / "reports"
    user_report_dir.mkdir(parents=True, exist_ok=True)

def add_income(username: str, encryption_key, amount: float, category: str, date_str: str) -> None:
    type = "income"
    data = load_user_data(username)["data"]

    # todo: fix datatypes to bytes
    amount_encry = auth_encry.encrypt_data(encryption_key, str(amount).encode('utf-8'), (username + type).encode('utf-8'))
    category_encry = auth_encry.encrypt_data(encryption_key, category.encode('utf-8'), (username + type).encode('utf-8'))
    date_encry = auth_encry.encrypt_data(encryption_key, date_str.encode('utf-8'), (username + type).encode('utf-8'))
    timestamp_encry = auth_encry.encrypt_data(encryption_key, datetime.now().isoformat().encode('utf-8'), (username + type).encode('utf-8'))


    data["incomes"].append({
        "amount": amount_encry,
        "category": category_encry,
        "date": date_encry,
        "timestamp": timestamp_encry
    })

    save_user_data(username, {"data": data})


def add_expense(username: str, encryption_key, amount: float, category: str, date_str: str) -> None:
    type = "expense"
    data = load_user_data(username)["data"]

    if len(encryption_key) != 32:
        raise ValueError(f"Add expense key must be 32 bytes, got {len(encryption_key)}")

    # todo: fix datatypes to bytes
    amount_encry = auth_encry.encrypt_data(encryption_key, str(amount).encode('utf-8'), (username + type).encode('utf-8'))
    category_encry = auth_encry.encrypt_data(encryption_key, category.encode('utf-8'), (username + type).encode('utf-8'))
    date_encry = auth_encry.encrypt_data(encryption_key, date_str.encode('utf-8'), (username + type).encode('utf-8'))
    timestamp_encry = auth_encry.encrypt_data(encryption_key, datetime.now().isoformat().encode('utf-8'), (username + type).encode('utf-8'))

    data["expenses"].append({
        "amount": amount_encry,
        "category": category_encry,
        "date": date_encry,
        "timestamp": timestamp_encry
    })

    save_user_data(username, {"data": data})
