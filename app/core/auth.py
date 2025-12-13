import json
import re
from app.core import REGISTERED_USERS_PATH, USERS_DIRECTORY, REPORTS_DIRECTORY
from app.cryptography import pw_management as pw

# REGISTER
def load_registered_users(registered_users_path=REGISTERED_USERS_PATH):
    try:
        with open(registered_users_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": []}
    except json.JSONDecodeError:
        return {"users": []}
    
def register_user(username, password):
    users = load_registered_users()["users"]
    
    for user in users:
        if user["username"] == username:
            return False
    
    password_data, encryption_salt = pw.create_password_data(password)
    # TODO change "password" to "key" -> change name of field
    users.append({"username": username, "password": 
                  {"password_data": password_data, "encryption_salt": encryption_salt}})

    save_registered_users({"users": users})
    create_user_file(username)
    create_user_report_directory(username)
    print(f"Registered users: {users}")
    return True

def save_registered_users(data, registered_users_path=REGISTERED_USERS_PATH):
    with open(registered_users_path, "w") as file:
        json.dump(data, file, indent=4)

def create_user_file(username, users_directory=USERS_DIRECTORY):
    user_file_path = users_directory / f"{username}.json"
    
    if not user_file_path.exists():
        data = {
            "data": {
                "expenses": [],
                "incomes": []
            }
        }
        with open(user_file_path, "w") as file:
            json.dump(data, file, indent=4)

def create_user_report_directory(username, reports_directory=REPORTS_DIRECTORY):
    user_report_dir = reports_directory / username
    user_report_dir.mkdir(parents=True, exist_ok=True)

def is_strong_password(password):
    """
    Minimum 8 characters, maximum 64 characters,
    at least 1 uppercase, 1 lowercase, 1 number, 1 special character
    """
    if len(password) < 8 or len(password) > 64:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True


def is_valid_username(username):
    """
    Username must be alphanumeric and between 3 and 20 characters
    """
    if not re.match(r"^[a-zA-Z0-9]{3,20}$", username):
        return False
    return True


# AUTHENTICATE
def authenticate_user(username, password):

    users = load_registered_users()["users"]

    for user in users:
        if user["username"] == username:
            scrypt_config = user["password"]["password_data"]
            encryption_salt = user["password"]["encryption_salt"]
            encryption_key = pw.verify_password(password, scrypt_config, encryption_salt)
            print("Successfully authenticated!")
            return encryption_key
    
    return None
