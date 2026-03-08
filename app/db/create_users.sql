CREATE TABLE IF NOT EXISTS users
(
    username TEXT PRIMARY KEY,
    password_data TEXT NOT NULL,
    encryption_salt TEXT NOT NULL
);