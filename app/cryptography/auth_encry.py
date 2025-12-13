import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


nonce_size = 12

# Todo : not sure what should be used in our case as aad
# key is the user encryption key, HOW DO I GET IT?
def encrypt_data(data, key, aad):
    nonce = os.random(nonce_size)
    chacha = ChaCha20Poly1305(key)
    encrypted = chacha.encrypt(nonce, data, aad)
    ciphertext = nonce + encrypted
    return ciphertext

def decrypt_data(ciphertext, key, aad):
    nonce = ciphertext[:nonce_size]
    encrypted = ciphertext[nonce_size:]

    chacha = ChaCha20Poly1305(key)
    plaintext = chacha.decrypt(nonce, encrypted, aad)

    return plaintext
