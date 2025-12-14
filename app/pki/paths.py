from pathlib import Path

from app.core import DATA_PATH

PKI_DIR = DATA_PATH / "pki"
PKI_DIR.mkdir(parents=True, exist_ok=True)


def get_root_dir() -> Path:
    root_dir = PKI_DIR / "root"
    root_dir.mkdir(parents=True, exist_ok=True)
    return root_dir

def get_root_key_path() -> Path:
    return get_root_dir() / "root_key.pem"

def get_root_cert_path() -> Path:
    return get_root_dir() / "root_cert.pem"

def get_ca_dir(ca_name: str) -> Path:
    ca_dir = PKI_DIR / ca_name.lower()
    ca_dir.mkdir(parents=True, exist_ok=True)
    return ca_dir

def get_ca_key_path(ca_name: str) -> Path:
    return get_ca_dir(ca_name) / f"{ca_name.lower()}_key.pem"

def get_ca_cert_path(ca_name: str) -> Path:
    return get_ca_dir(ca_name) / f"{ca_name.lower()}_cert.pem"

def get_users_dir() -> Path:
    users_dir = PKI_DIR / "users"
    users_dir.mkdir(parents=True, exist_ok=True)
    return users_dir

def get_user_dir(username: str) -> Path:
    user_dir = get_users_dir() / username
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir

def get_user_key_path(username: str) -> Path:
    return get_user_dir(username) / f"{username}_key.pem"

def get_user_cert_path(username: str) -> Path:
    return get_user_dir(username) / f"{username}_cert.pem"