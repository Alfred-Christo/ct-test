from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

USERS_FILE = 'users_data.json'

if os.path.exists(USERS_FILE):
    try:
        with open(USERS_FILE, 'r') as file:
            users = json.load(file)
    except json.JSONDecodeError:
        users = []
else:
    users = []

def save_users_to_file():
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    
    if not all(key in data for key in ['fcm_token', 'username', 'phone_number', 'date', 'time']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user = {
        'fcm_token': data['fcm_token'],
        'username': data['username'],
        'phone_number': data['phone_number'],
        'date': data['date'],
        'time': data['time']
    }
    
    users.append(user)
    
    save_users_to_file()
    
    return jsonify({'message': 'Done'}), 201

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)