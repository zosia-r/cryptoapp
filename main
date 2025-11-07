from pathlib import Path
from utils.registration import register_user

if __name__ == "__main__":
    print("Welcome to the registration system.")
    username = input("Please select your username: ")
    password = input("Please select your password: ")
    
    try:
        if register_user(username, password):
            print("You were successfully added as a new user :)")
    except ValueError as e:
        print(e)