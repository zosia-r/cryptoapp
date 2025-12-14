from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

from app.pki.ca import select_ca_for_user
from app.pki.paths import get_user_cert_path, get_ca_cert_path, get_root_cert_path


def verify_user_certificate_by_username(username: str) -> str:
    try:
        user_cert = load_certificate(get_user_cert_path(username))
        ca_cert = load_certificate(get_ca_cert_path(select_ca_for_user(username)))
        root_cert = load_certificate(get_root_cert_path())

        return verify_certificate_chain(user_cert, ca_cert, root_cert)
    
    except Exception as e:
        return (f"Error verifying certificate for {username}: {e}")    


def verify_certificate_chain(user_cert, ca_cert, root_cert) -> str:
    if not verify_root_certificate(root_cert):
        return "ROOT"

    if not verify_ca_certificate(ca_cert, root_cert):
        return "CA"

    if not verify_user_certificate(user_cert, ca_cert):
        return "USER"

    return "VALID"

def verify_certificate_signature(cert, issuer_cert) -> bool:
    """
    Verifies that `cert` was signed by `issuer_cert`
    """
    issuer_public_key = issuer_cert.public_key()

    try:
        issuer_public_key.verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            padding.PKCS1v15(),
            cert.signature_hash_algorithm,
        )
        return True
    except Exception:
        return False
    
def verify_root_certificate(root_cert) -> bool:
    return verify_certificate_signature(root_cert, root_cert)

def verify_ca_certificate(ca_cert, root_cert) -> bool:
    if ca_cert.issuer != root_cert.subject:
        return False

    return verify_certificate_signature(ca_cert, root_cert)

def verify_user_certificate(user_cert, ca_cert) -> bool:
    if user_cert.issuer != ca_cert.subject:
        return False

    return verify_certificate_signature(user_cert, ca_cert)

def load_certificate(path):
    with open(path, "rb") as f:
        return x509.load_pem_x509_certificate(f.read())



