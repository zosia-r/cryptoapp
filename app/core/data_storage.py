import json
from datetime import datetime
import sqlite3
from app.core import USERS_DIRECTORY, REGISTERED_USERS_PATH
from app.cryptography import auth_encry
import app.db.db as db

# USER DATA STORAGE
def load_user_data(username: str) -> dict:    
    transactions = db.get_transactions(username)
    return {"data": transactions}

# REGISTERED USERS STORAGE
def load_registered_users(registered_users_path=REGISTERED_USERS_PATH):
    return db.get_all_users()

def save_user(username, password_data, encryption_salt):
    db.add_user(username, password_data, encryption_salt)

# USER SETUP
def create_user_report_directory(username, users_directory=USERS_DIRECTORY):
    user_report_dir = users_directory / username / "reports"
    user_report_dir.mkdir(parents=True, exist_ok=True)

# USER DATA MANAGEMENT
def add_income(username: str, encryption_key, amount: float, category: str, date_str: str) -> None:
    type = "income"

    # todo: fix datatypes to bytes
    amount_encry = auth_encry.encrypt_data(encryption_key, str(amount).encode('utf-8'), (username + type).encode('utf-8'))
    category_encry = auth_encry.encrypt_data(encryption_key, category.encode('utf-8'), (username + type).encode('utf-8'))
    date_encry = auth_encry.encrypt_data(encryption_key, date_str.encode('utf-8'), (username + type).encode('utf-8'))
    timestamp_encry = auth_encry.encrypt_data(encryption_key, datetime.now().isoformat().encode('utf-8'), (username + type).encode('utf-8'))

    db.add_transaction(username, type, amount_encry, category_encry, date_encry, timestamp_encry)


def add_expense(username: str, encryption_key, amount: float, category: str, date_str: str) -> None:
    type = "expense"

    # todo: fix datatypes to bytes
    amount_encry = auth_encry.encrypt_data(encryption_key, str(amount).encode('utf-8'), (username + type).encode('utf-8'))
    category_encry = auth_encry.encrypt_data(encryption_key, category.encode('utf-8'), (username + type).encode('utf-8'))
    date_encry = auth_encry.encrypt_data(encryption_key, date_str.encode('utf-8'), (username + type).encode('utf-8'))
    timestamp_encry = auth_encry.encrypt_data(encryption_key, datetime.now().isoformat().encode('utf-8'), (username + type).encode('utf-8'))

    db.add_transaction(username, type, amount_encry, category_encry, date_encry, timestamp_encry)

# REPORT STORAGE
def get_reports_dir(username: str) -> str:
    user_report_dir = USERS_DIRECTORY / username / "reports"
    user_report_dir.mkdir(parents=True, exist_ok=True)
    return user_report_dir

# KEY STORAGE
def save_user_keys(username: str, private_key_pem: bytes, public_key_pem: bytes) -> None:
    user_directory = USERS_DIRECTORY / username
    user_directory.mkdir(parents=True, exist_ok=True)

    private_key_path = user_directory / "private_key.pem"
    public_key_path = user_directory / "public_key.pem"

    with open(private_key_path, "wb") as f:
        f.write(private_key_pem)

    with open(public_key_path, "wb") as f:
        f.write(public_key_pem)

def get_user_keys_path(username: str) -> tuple:
    user_directory = USERS_DIRECTORY / username
    private_key_path = user_directory / "private_key.pem"
    public_key_path = user_directory / "public_key.pem"
    return private_key_path, public_key_path
