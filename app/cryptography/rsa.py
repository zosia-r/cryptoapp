from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def _generate_rsa_keypair(key_size=2048, public_exponent=65537):
    private_key = rsa.generate_private_key(
        public_exponent=public_exponent,
        key_size=key_size,
    )
    public_key = private_key.public_key()
    return private_key, public_key

def serialize_public_key(public_key):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem

def _serialize_private_key(private_key, password=None):
    if password:
        encryption_algorithm = serialization.BestAvailableEncryption(password)
    else:
        encryption_algorithm = serialization.NoEncryption()

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=encryption_algorithm
    )
    return pem

def get_rsa_key_pair_pem(password=None):
    private_key, public_key = _generate_rsa_keypair()
    private_key_pem = _serialize_private_key(private_key, password)
    public_key_pem = serialize_public_key(public_key)
    return private_key_pem, public_key_pem