import os
import base64
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

length = 32
#TODO somewhere convert string to bytes

def registration_derivition(password:str):
     salt = os.urandom(16)
     derive_key(password, salt)


def derive_key(password: str, salt: bytes) -> bytes:

    n=2**14,
    r=8,
    p=1,

    kdf = Scrypt(
        salt=salt,
        length=length,
        n=n,
        r=r,
        p=p,
        )

    # password has to be bytes here
    key = kdf.derive(password)

    salt_b64_bytes = base64.b64encode(salt)
    salt_b64_string = salt_b64_bytes.decode('utf-8')
    key_b64_bytes = base64.b16encode(key)
    key_b64_string = key_b64_bytes.decode('utf-8')

    scrypt_configuration = f"§scrypt$ln={n},r={r},p={p}${salt_b64_string}${key_b64_string}"
    return scrypt_configuration


def get_scrypt_configuration(scrypt_config: str):
    pass

# not sure if key input is tring or bytes
def verify_key(password: str, key: str, scrypt_config:str):
    # salt, n, r, and p are derived from scrypt config
    #TODO: what ablut length?
    
    kdf = Scrypt(
        salt=salt,
        length=length,
        n=2**14,
        r=8,
        p=1,
    )

    #password probably also has additional information
    # TODO filter only to pw that has to be checked
    # password has to be bytes
    kdf.verify(password, key)
