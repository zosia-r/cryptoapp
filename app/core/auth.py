import json
from pathlib import Path
import re

DATA_PATH = Path(__file__).resolve().parent.parent / "data"
REGISTERED_USERS_PATH = DATA_PATH / "registered_users.json"
USERS_DIRECTORY = DATA_PATH / "users"

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
        
    users.append({"username": username, "password": password})

    save_registered_users({"users": users})
    create_user_file(username)
    print(f"Registered users: {users}")
    return True

def save_registered_users(data, registered_users_path=REGISTERED_USERS_PATH):
    with open(registered_users_path, "w") as file:
        json.dump(data, file, indent=4)

def create_user_file(username, users_directory=USERS_DIRECTORY):
    user_file_path = users_directory / f"{username}.json"
    
    if not user_file_path.exists():
        with open(user_file_path, "w") as file:
            json.dump({"data": []}, file, indent=4)


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
        if user["username"] == username and user["password"] == password:
            print("Successfully authenticated!")
            return True
    
    return False
