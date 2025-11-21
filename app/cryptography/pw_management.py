import os
import base64
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

length = 32

# Scrypt parameters for the derivition of the encryption key
n_ekay = 2**14
n_r = 8
n_p = 1
     

# Derives the key using Scrypt given parameters
def derive_key(password: str, salt: bytes, n, r, p) -> bytes:

    kdf = Scrypt(
        salt=salt,
        length=length,
        n=n,
        r=r,
        p=p,
        )

    key = kdf.derive(password.encode('utf-8'))

    salt_b64_bytes = base64.b64encode(salt)
    salt_b64_string = salt_b64_bytes.decode('utf-8')
    key_b64_bytes = base64.b16encode(key)
    key_b64_string = key_b64_bytes.decode('utf-8')

    scrypt_configuration = f"§scrypt$ln={n},r={r},p={p}${salt_b64_string}${key_b64_string}"
    return scrypt_configuration

# Parses the cofing string to get necessary parameters
def parse_scrypt_configuration(scrypt_config: str):
    parameters = scrypt_config.split('$')
    scrypt_params = parameters[2]
    scrypt_params_list = scrypt_params.split(',')
    scrypt_config = {}
    for item in scrypt_params_list:
        if '=' in item:
            key, value = item.split('=')
            scrypt_config[key] = value

    salt_string = parameters[3]
    key_string = parameters[4]

    return scrypt_config, salt_string, key_string


# creates the passwort data that must be stored in json
def create_password_data(password: str):
    salt = os.urandom(16)
    scrypt_config = derive_key(password, salt)
    encryption_salt = os.urandom(16)
    return salt, scrypt_config, encryption_salt


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

    pw_b64_bytes = base64.b64encode(password)
    kdf.verify(pw_b64_bytes, key)
