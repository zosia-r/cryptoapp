from cryptography.hazmat.primitives import serialization
from cryptography import x509

from app.pki.paths import (
    get_ca_key_path,
    get_ca_cert_path,
)
from app.pki import CA_NAMES, CA_PASSWORDS


def select_ca_for_user(username: str) -> str:
    first = username[0].lower()
    if "a" <= first <= "m":
        return "ca1"
    else:
        return "ca2"
    
def load_ca_private_key(ca_name: str):
    key_path = get_ca_key_path(ca_name)

    with open(key_path, "rb") as f:
        key_bytes = f.read()

    private_key = serialization.load_pem_private_key(
        key_bytes,
        password=CA_PASSWORDS[CA_NAMES.index(ca_name.upper())],
    )

    return private_key

def load_ca_certificate(ca_name: str):
    cert_path = get_ca_cert_path(ca_name)

    with open(cert_path, "rb") as f:
        cert_bytes = f.read()

    cert = x509.load_pem_x509_certificate(cert_bytes)

    return cert

