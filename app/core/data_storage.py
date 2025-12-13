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


def add_income(username: str, amount: float, category: str, date_str: str) -> None:
    type = "income"
    data = load_user_data(username)["data"]

    # todo: fix datatypes to bytes
    amount_encry = auth_encry.encrypt_data(amount.encode('utf-8'), username, (username + type).encode('utf-8'))
    category_encry = auth_encry.encrypt_data(category.encode('utf-8'), username, (username + type).encode('utf-8'))
    date_encry = auth_encry.encrypt_data(date_str.encode('utf-8'), username, (username + type).encode('utf-8'))
    timestamp_encry = auth_encry.encrypt_data(datetime.now().isoformat().encode('utf-8'), username, (username + type).encode('utf-8'))


    data["incomes"].append({
        "amount": amount_encry,
        "category": category_encry,
        "date": date_encry,
        "timestamp": timestamp_encry
    })

    save_user_data(username, {"data": data})


def add_expense(username: str, amount: float, category: str, date_str: str) -> None:
    type = "expense"
    data = load_user_data(username)["data"]

    # todo: fix datatypes to bytes
    amount_encry = auth_encry.encrypt_data(amount.encode('utf-8'), username, (username + type).encode('utf-8'))
    category_encry = auth_encry.encrypt_data(category.encode('utf-8'), username, (username + type).encode('utf-8'))
    date_encry = auth_encry.encrypt_data(date_str.encode('utf-8'), username, (username + type).encode('utf-8'))
    timestamp_encry = auth_encry.encrypt_data(datetime.now().isoformat().encode('utf-8'), username, (username + type).encode('utf-8'))

    data["expenses"].append({
        "amount": amount_encry,
        "category": category_encry,
        "date": date_encry,
        "timestamp": timestamp_encry
    })

    save_user_data(username, {"data": data})
