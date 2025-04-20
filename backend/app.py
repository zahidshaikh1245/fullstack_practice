from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS  # <--- added
from pymongo import MongoClient
from bson.objectid import ObjectId
from config import MONGO_URI
from utils.auth import generate_token, decode_token

app = Flask(__name__)
CORS(app)  # <--- added
bcrypt = Bcrypt(app)

client = MongoClient(MONGO_URI)
db = client['auth_db']
users = db['users']

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data.get('email') or not data.get('password'):
        return jsonify({'msg': 'Email and password required'}), 400

    if users.find_one({'email': data['email']}):
        return jsonify({'msg': 'Email already exists'}), 400

    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user_id = users.insert_one({'email': data['email'], 'password': hashed_pw}).inserted_id

    token = generate_token(user_id)
    return jsonify({'token': token}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = users.find_one({'email': data.get('email')})
    if user and bcrypt.check_password_hash(user['password'], data.get('password')):
        token = generate_token(user['_id'])
        return jsonify({'token': token})
    return jsonify({'msg': 'Invalid credentials'}), 401

@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'msg': 'Missing token'}), 401

    payload = decode_token(token)
    if not payload:
        return jsonify({'msg': 'Invalid or expired token'}), 401

    return jsonify({'msg': 'Access granted', 'user_id': payload['user_id']})

if __name__ == '__main__':
    app.run(debug=True)
