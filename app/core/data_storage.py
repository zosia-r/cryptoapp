import json
from datetime import datetime
from app.core import USERS_DIRECTORY
from app.cryptography import auth_encry


def load_user_data(username: str) -> dict:
    user_file = USERS_DIRECTORY / f"{username}.json"

    with open(user_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_user_data(username: str, data: dict) -> None:
    user_file = USERS_DIRECTORY / f"{username}.json"

    with open(user_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


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
