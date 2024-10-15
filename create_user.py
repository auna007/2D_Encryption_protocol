import sqlite3
import pyotp
from DNA_functions import dna_encrypt, dna_decrypt

def create_user():
    # Connect to SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Prompt for username and password
    username = input("Enter username (email): ")
    password = input("Enter password: ")
    secret = pyotp.random_base32()  # Generate a new TOTP secret
    secret_code = dna_encrypt(username, secret)

    try:
        cursor.execute('INSERT INTO users (username, password, secret) VALUES (?, ?, ?)', (username, password, secret_code))
        conn.commit()
        print(f"User {username} created successfully! Your TOTP secret is: {secret_code}")
    except sqlite3.IntegrityError:
        print(f"User {username} already exists. Please choose a different username.")
    
    conn.close()

# Call the create_user function to execute
create_user()
