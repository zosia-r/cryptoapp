from app import CryptoApp
from app.pki.setup import setup_pki, is_pki_setup
from app.db.db import init_db

if __name__ == "__main__":
    init_db()
    if not is_pki_setup():
        setup_pki()
    app = CryptoApp()
    app.run()
