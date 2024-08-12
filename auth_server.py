from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory user database
users = {
    'user1': 'password1',
    'user2': 'password2'
}

@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if users.get(username) == password:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'failure'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
