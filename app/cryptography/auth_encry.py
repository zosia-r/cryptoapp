import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from app.core import REGISTERED_USERS_PATH
import json


nonce_size = 12

# Todo : not sure what should be used in our case as aad
# key is the user encryption key, HOW DO I GET IT?
def encrypt_data(key:bytes , data, aad):

    if isinstance(key, str):
        raise TypeError("Key is str. ChaCha20Poly1305 needs raw 32-byte bytes (not base64 text).")
    if not isinstance(key, (bytes, bytearray)):
        raise TypeError(f"Key must be bytes/bytearray, got {type(key)}")
    if len(key) != 32:
        raise ValueError(f"ChaCha20Poly1305 key must be 32 bytes, got {len(key)}")

    nonce = os.urandom(nonce_size)
    chacha = ChaCha20Poly1305(key)
    encrypted = chacha.encrypt(nonce, data, aad)
    ciphertext = nonce + encrypted
    return ciphertext


def decrypt_data(key: bytes, ciphertext, aad):
    nonce = ciphertext[:nonce_size]
    encrypted = ciphertext[nonce_size:]

    chacha = ChaCha20Poly1305(key)
    plaintext = chacha.decrypt(nonce, encrypted, aad)

    return plaintext
