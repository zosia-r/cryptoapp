from pathlib import Path
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from datetime import datetime, timedelta

from app.pki.paths import (
    PKI_DIR,
    get_root_dir,
    get_root_key_path,
    get_root_cert_path,
    get_ca_dir,
    get_ca_key_path,
    get_ca_cert_path,
    get_users_dir
)
import app.cryptography.rsa as rsa

from app.pki import ROOT_NAME, CA_NAMES, ROOT_PASSWORD, CA_PASSWORDS


def create_self_signed_cert(private_key, subject_name: str, valid_days=3650) -> x509.Certificate:
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, subject_name),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.now()
    ).not_valid_after(
        datetime.now() + timedelta(days=valid_days)
    ).sign(private_key, hashes.SHA256())
    return cert

def create_cert_signed_by_ca(subject_private_key, ca_cert, ca_private_key, subject_name: str, valid_days=1825):
    subject = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, subject_name),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        ca_cert.subject
    ).public_key(
        subject_private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.now()
    ).not_valid_after(
        datetime.now() + timedelta(days=valid_days)
    ).sign(ca_private_key, hashes.SHA256())
    return cert

def write_key_and_cert(key, cert, key_path: Path, cert_path: Path, password: bytes = None):

    private_key_bytes = rsa.serialize_private_key(key, password)
    key_path.write_bytes(private_key_bytes)

    cert_bytes = cert.public_bytes(serialization.Encoding.PEM)
    cert_path.write_bytes(cert_bytes)

def setup_pki(root_name=ROOT_NAME, ca_names=CA_NAMES, root_password=ROOT_PASSWORD, ca_passwords=CA_PASSWORDS):
    # ROOT
    root_key = rsa.generate_rsa_keypair()[0]
    root_cert = create_self_signed_cert(root_key, root_name)
    write_key_and_cert(root_key, root_cert, get_root_key_path(), get_root_cert_path(), root_password)

    # CAs
    for ca_name, ca_password in zip(ca_names, ca_passwords):
        ca_key = rsa.generate_rsa_keypair()[0]
        ca_cert = create_cert_signed_by_ca(ca_key, root_cert, root_key, ca_name)
        write_key_and_cert(ca_key, ca_cert, get_ca_key_path(ca_name), get_ca_cert_path(ca_name), ca_password)

def is_pki_setup() -> bool:
    if not PKI_DIR.exists():
        return False
    if not get_root_key_path().exists() or not get_root_cert_path().exists():
        return False
    for ca_name in CA_NAMES:
        if not get_ca_key_path(ca_name).exists() or not get_ca_cert_path(ca_name).exists():
            return False
    if not get_users_dir().exists():
        return False
    return True

