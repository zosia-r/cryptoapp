import json
from datetime import datetime
from app.core import USERS_DIRECTORY


def load_user_data(username: str) -> dict:
    user_file = USERS_DIRECTORY / f"{username}.json"

    with open(user_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_user_data(username: str, data: dict) -> None:
    user_file = USERS_DIRECTORY / f"{username}.json"

    with open(user_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def add_income(username: str, amount: float, category: str, date_str: str) -> None:
    data = load_user_data(username)["data"]

    data["incomes"].append({
        "amount": float(amount),
        "category": category,
        "date": date_str,
        "timestamp": datetime.now().isoformat()
    })

    save_user_data(username, {"data": data})


def add_expense(username: str, amount: float, category: str, date_str: str) -> None:
    data = load_user_data(username)["data"]

    data["expenses"].append({
        "amount": float(amount),
        "category": category,
        "date": date_str,
        "timestamp": datetime.now().isoformat()
    })

    save_user_data(username, {"data": data})
