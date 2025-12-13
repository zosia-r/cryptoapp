import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from app.core import REGISTERED_USERS_PATH
import json


nonce_size = 12

# Todo : not sure what should be used in our case as aad
# key is the user encryption key, HOW DO I GET IT?
def encrypt_data(data, username, aad):
    nonce = os.random(nonce_size)
    chacha = ChaCha20Poly1305(key)
    encrypted = chacha.encrypt(nonce, data, aad)
    ciphertext = nonce + encrypted
    return ciphertext


def decrypt_data(ciphertext, username, aad):
    nonce = ciphertext[:nonce_size]
    encrypted = ciphertext[nonce_size:]

    key = extract_key(username)
    chacha = ChaCha20Poly1305(key)
    plaintext = chacha.decrypt(nonce, encrypted, aad)

    return plaintext



def extract_key(username): 

    with open(REGISTERED_USERS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    encryption_salt = data["users"][username]["password"]["encryption_salt"]
    return encryption_salt
