import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Execute SQL command to delete all rows from the users table
cursor.execute('DELETE FROM users')

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

print("All rows have been deleted from the 'users' table.")
