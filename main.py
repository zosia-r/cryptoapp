from app import CryptoApp
from app.pki.setup import setup_pki, is_pki_setup

if __name__ == "__main__":
    if not is_pki_setup():
        setup_pki()
    app = CryptoApp()
    app.run()
