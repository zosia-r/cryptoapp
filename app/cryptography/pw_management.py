import os
import base64
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

length = 32

# Scrypt parameters for the derivition of the encryption key
n_ekay = 2**14
n_r = 8
n_p = 1
     

# Derives the key using Scrypt given parameters
def derive_key(password: str, salt: bytes, n= n_ekay, r = n_r, p = n_p) -> bytes:

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
    key_b64_bytes = base64.b64encode(key)
    key_b64_string = key_b64_bytes.decode('utf-8')

    scrypt_configuration = f"$scrypt$ln={n},r={r},p={p}${salt_b64_string}${key_b64_string}"
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
    print(type(scrypt_config))
    print(type(encryption_salt))
    #scrypt_config_string = scrypt_config.decode('utf-8')
    encryption_salt_string = base64.b64encode(encryption_salt).decode('utf-8')
    return scrypt_config, encryption_salt_string

def verify_password(password, scrypt_config):
    # Structure of the s_c: $scrypt$ln={n},r={r},p={p}${salt_b64_string}${key_b64_string}
    parameters = scrypt_config.split('$')
    for item in parameters[2].split(","):
        var, value = item.split("=")
        if var == "ln":
            n = int(value)
        if var == "r":
            r = int(value)
        if var == "p":
            p = int(value)
    salt = parameters[3]
    key = parameters[4]
    salt = base64.b64decode(salt)
    key = base64.b64decode(key)
    verify_key(password, key, n, r, p, salt)
    


def verify_key(password: str, key: bytes, n, r, p, salt: bytes):
    
    kdf = Scrypt(
        salt=salt,
        length=length,
        n=n,
        r=r,
        p=p,
    )

    pw_bytes = password.encode("utf-8")
    kdf.verify(pw_bytes, key)
