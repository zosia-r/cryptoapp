import json
from pathlib import Path

data_path = Path(__file__).resolve().parent.parent / "data"
registered_users_path = data_path / "registered_users.json"
users_directory = data_path / "users"

def load_registered_users(registered_users_path=registered_users_path):
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

def save_registered_users(data, registered_users_path=registered_users_path):
    with open(registered_users_path, "w") as file:
        json.dump(data, file, indent=4)

def create_user_file(username, users_directory=users_directory):
    user_file_path = users_directory / f"{username}.json"
    
    if not user_file_path.exists():
        with open(user_file_path, "w") as file:
            json.dump({"data": []}, file, indent=4)



