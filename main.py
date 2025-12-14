from app import CryptoApp
from app.pki.setup import setup_pki

if __name__ == "__main__":
    setup_pki()
    app = CryptoApp()
    app.run()
