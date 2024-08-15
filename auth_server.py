import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def check_credentials(username, password):
    # Connect to SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Check if the username and password match
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()

    # Close the connection
    conn.close()

    # Return True if user is found, else False
    return user is not None

@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if check_credentials(username, password):
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'failure'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
