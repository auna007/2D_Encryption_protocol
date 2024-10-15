import sqlite3

def view_users():
    # Connect to SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Query to select all users
    cursor.execute('SELECT username, password, secret FROM users')
    users = cursor.fetchall()

    # Check if there are users in the database
    if users:
        print("Existing users:")
        for user in users:
            print(f"Username: {user[0]}, Password: {user[1]}, PK: {user[2]}")  # Be cautious about displaying passwords
    else:
        print("No users found.")

    conn.close()

# Call the view_users function to execute
view_users()
