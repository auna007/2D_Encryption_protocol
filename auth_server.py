import sqlite3
import pyotp
from flask import Flask, request, jsonify

app = Flask(__name__)

def check_credentials(username, password):
    #decrypt the username and password before comparing - 2D_Decryption_protocol (parameter)

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def get_user_secret(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT secret FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    username = data.get('username') #2D_ENCRYPTION_PROTOCOL (data.get('username'));
    password = data.get('password') #2D_ENCRYPTION_PROTOCOL (data.get('password'));
    totp_code = data.get('totp_code')   #2D_ENCRYPTION_PROTOCOL (data.get('totp_code'));


#ALTERNATIVELY YOU CAN USE THIS
#encrpted_data = 2D_ENCRYPTION_PROTOCOL(USERNAME, PASSWORD) - FUNCTION 
#ucrpyt = encrpted_data['0];
#pcrpyt = encrpted_data['1'];

    if check_credentials(username, password):
        # Fetch the TOTP secret for the user
        secret = get_user_secret(username)
        totp = pyotp.TOTP(secret)
        # print(totp)
        if totp.verify(totp_code):
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'failure', 'message': 'Invalid TOTP code'}), 401
    else:

        return jsonify({'status': 'failure', 'message': 'Invalid username or password'}), 402

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
