import json
from pathlib import Path

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
            raise ValueError("Username is already taken.")
        
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


# AUTHENTICATE
def authenticate_user(username, password):

    users = load_registered_users()["users"]
    
    for user in users:
        if user["username"] == username and user["password"] == password:
            print("Successfully authenticated!")
            return True
    
    return False
