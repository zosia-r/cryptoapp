import re
from app.cryptography import pw_management as pw
from app.core.data_storage import ( save_registered_users, load_registered_users, 
                                   create_user_file, create_user_report_directory, 
                                   save_user_keys
                                    )
from app.cryptography import rsa as rsa
from app.pki.user_cert import issue_user_certificate

# REGISTER
def register_user(username, password):
    users = load_registered_users()["users"]
    
    for user in users:
        if user["username"] == username:
            return False
    
    password_data, encryption_salt = pw.create_password_data(password)
    # TODO change "password" to "key" -> change name of field
    users.append({"username": username, "password": 
                  {"password_data": password_data, "encryption_salt": encryption_salt}})

    # Basic RSA
    private_key_pem, public_key_pem = rsa.get_rsa_key_pair_pem(password.encode())
    save_user_keys(username, private_key_pem, public_key_pem)

    # PKI
    issue_user_certificate(username)

    save_registered_users({"users": users})
    create_user_file(username)
    create_user_report_directory(username)
    print(f"Registered users: {users}")
    return True

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
            try:
                scrypt_config = user["password"]["password_data"]
                encryption_salt = user["password"]["encryption_salt"]
                encryption_key = pw.verify_password(password, scrypt_config, encryption_salt)
                return encryption_key
            except Exception:
                return None
    
    return None
