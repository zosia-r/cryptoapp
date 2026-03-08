# CryptoApp
## Manage your expenses. Securely.

A Python terminal application for managing encrypted financial transactions and generating digitally signed reports. The project demonstrates secure data handling, public key infrastructure (PKI), and relational database design using SQLite.


### Features
* User authentication with password hashing
* Encrypted storage of financial transactions in SQLite database
* RSA digital signatures for report integrity
* Custom PKI with a Root CA and two intermediate CAs
* Automatic certificate issuance for users
* PDF report generation and signature verification
* Terminal-based interface

### Technologies
* Python
* SQL, SQLite
* Cryptography (RSA, X.509)
* Textual + CSS (terminal UI)
* ReportLab, Matplotlib (PDF generation)

### PKI Structure
The system uses a simple certificate hierarchy:

* **Root CA** – self-signed root certificate
* **CA1** – issues certificates for users with usernames starting with A–M
* **CA2** – issues certificates for users with usernames starting with N–Z

User certificates are signed by the appropriate intermediate CA, forming a verifiable trust chain.

### Database Schema
The application stores users and encrypted transactions in SQLite.

Tables:

* `users` – username, password hash, encryption salt
* `transactions` – encrypted income and expense records

All sensitive financial fields are encrypted before being written to the database.

### Project Structure

```
cryptoapp/
├── main.py
├── README.md
├── requirements.txt
├── app/
│   ├── core/            # authentication, data storage
│   ├── cryptography/    # encryption and signatures
│   ├── db/              # SQLite database management
│   ├── pki/             # certificate management
│   └── views/           # terminal interface
├── data/
│   ├── database.db
│   ├── pki/             # CA keys and certificates
│   └── users/           # user keys and certificates
|       └── reports/     # generated PDF reports
```

### Setting up the environment
```
python -m venv venv

source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

pip install -r requirements.txt

```

### Running the application
```
python main.py
```
