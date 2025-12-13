import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from app.core import REGISTERED_USERS_PATH
import json


nonce_size = 12


def encrypt_data(key:bytes , data, aad):

    if isinstance(key, str):
        raise TypeError("Key is str. ChaCha20Poly1305 needs raw 32-byte bytes (not base64 text).")
    if not isinstance(key, (bytes, bytearray)):
        raise TypeError(f"Key must be bytes/bytearray, got {type(key)}")
    if len(key) != 32:
        raise ValueError(f"ChaCha20Poly1305 key must be 32 bytes, got {len(key)}")
    
    if isinstance(data, str):
        data = data.encode("utf-8")
    if isinstance(aad, str):
        aad = aad.encode("utf-8")

    nonce = os.urandom(nonce_size)
    chacha = ChaCha20Poly1305(key)
    encrypted = chacha.encrypt(nonce, data, aad)
    ciphertext = nonce + encrypted

    
    if isinstance(ciphertext, bytes):
        ciphertext =  base64.b64encode(ciphertext).decode("utf-8")
    if not isinstance(ciphertext, str):
        raise TypeError(f"ciphertext must be base64 str, got {type(ciphertext)}")
    

    # to be able to store it in json
    #ciphertext = base64.b64encode(ciphertext).decode("utf-8")

   
    return ciphertext


def decrypt_data(key: bytes, ciphertext, aad):
    ciphertext = base64.b64decode(ciphertext)

    nonce = ciphertext[:nonce_size]
    encrypted = ciphertext[nonce_size:]

    
    chacha = ChaCha20Poly1305(key)
    plaintext = chacha.decrypt(nonce, encrypted, aad)

    return plaintext
