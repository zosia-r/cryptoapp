from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta
from pathlib import Path

from app.pki.ca import load_ca_private_key, load_ca_certificate
from app.pki.ca import select_ca_for_user
from app.pki.paths import get_user_cert_path
from app.cryptography.rsa import load_public_key
    

def issue_user_certificate(username: str) -> Path:
    ca_name = select_ca_for_user(username)

    ca_key = load_ca_private_key(ca_name)
    ca_cert = load_ca_certificate(ca_name)

    user_public_key = load_public_key(username)

    subject = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, username),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "CryptoApp"),
    ])

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)
        .public_key(user_public_key)
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now())
        .not_valid_after(datetime.now() + timedelta(days=365))
        .sign(
            private_key=ca_key,
            algorithm=hashes.SHA256(),
        )
    )

    cert_path = get_user_cert_path(username)
    cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))

    return cert_path