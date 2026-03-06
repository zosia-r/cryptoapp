import sqlite3

from . import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH) 

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create users table
    with open('app/db/create_users.sql', 'r') as f:
        cursor.executescript(f.read())

    # Create transactions table
    with open('app/db/create_transactions.sql', 'r') as f:
        cursor.executescript(f.read())
    
    conn.commit()
    conn.close()



# User management functions

def add_user(username, password_data, encryption_salt):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password_data, encryption_salt) VALUES (?, ?, ?)',
                   (username, password_data, encryption_salt))
    conn.commit()
    conn.close()

def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    users = []
    for row in rows:
        users.append({
            "username": row[0],
            "password": {
                "password_data": row[1],
                "encryption_salt": row[2],
            }
        })

    conn.close()

    return {"users": users}

def add_user(username, password_data, encryption_salt):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password_data, encryption_salt) VALUES (?, ?, ?)',
                   (username, password_data, encryption_salt))
    conn.commit()
    conn.close()

# Transaction management functions
def add_transaction(username, type, amount, category, date, timestamp):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO transactions (username, type, amount, category, date, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
                   (username, type, amount, category, date, timestamp))
    conn.commit()
    conn.close()


def get_transactions(username, type=None):
    conn = get_connection()
    cursor = conn.cursor()
    if type:
        cursor.execute('SELECT * FROM transactions WHERE username = ? AND type = ?', (username, type))
    else:
        cursor.execute('SELECT * FROM transactions WHERE username = ?', (username,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions