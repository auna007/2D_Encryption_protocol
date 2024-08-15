import sqlite3

def create_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create a table for storing users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')

    # Insert sample users
    users = [
        ('user1', 'password1'),
        ('user2', 'password2'),
        ('user3', 'password3')
    ]

    cursor.executemany('INSERT INTO users (username, password) VALUES (?, ?)', users)

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database and table created, and sample users added.")

if __name__ == '__main__':
    create_database()
