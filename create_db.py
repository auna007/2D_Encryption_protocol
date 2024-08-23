import sqlite3
import pyotp

# Connect to SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create users table with a column for TOTP secret
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    secret TEXT NOT NULL
)
''')

# Add users with generated TOTP secrets
users = [
    ('user1', 'password1', pyotp.random_base32()),
    ('user2', 'password2', pyotp.random_base32()),
    ('user3', 'password3', pyotp.random_base32())
]

cursor.executemany('INSERT INTO users (username, password, secret) VALUES (?, ?, ?)', users)
conn.commit()
conn.close()

# Print the TOTP secrets (for setting up Google Authenticator)
for user in users:
    print(f"User: {user[0]}, Secret: {user[2]}")
