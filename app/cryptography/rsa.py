from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature
from pathlib import Path

from app.core.data_storage import get_user_keys_path

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

def load_private_key(username: str, password: str):
    key_path = get_user_keys_path(username)[0]
    with open(key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=password.encode() if password else None,
        )
    return private_key

def load_public_key(username: str):
    key_path = get_user_keys_path(username)[1]
    with open(key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
        )
    return public_key

def get_rsa_key_pair_pem(password=None):
    private_key, public_key = _generate_rsa_keypair()
    private_key_pem = _serialize_private_key(private_key, password)
    public_key_pem = serialize_public_key(public_key)
    return private_key_pem, public_key_pem

def sign_pdf(username: str, 
             pdf_path: str, 
             password=None
             ) -> Path:
    private_key_path = get_user_keys_path(username)[0]

    pdf_path = Path(pdf_path)
    # Load PDF bytes
    pdf_bytes = pdf_path.read_bytes()

    # Load private key
    private_key = load_private_key(username, password)

    # Sign PDF bytes
    signature = private_key.sign(
        pdf_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )

    # Store signature
    sig_path = pdf_path.with_name(pdf_path.name + ".sig")
    sig_path.write_bytes(signature)

    return sig_path


def verify_pdf_signature(
        username: str,
        pdf_path: str,
        sig_path: str,
        ) -> bool:

    pdf_bytes = Path(pdf_path).read_bytes()
    signature = Path(sig_path).read_bytes()

    public_key = load_public_key(username)

    try:
        public_key.verify(
            signature,
            pdf_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        return False