import os
import sys
from flask import Flask, request, jsonify, session
from flask_session import Session
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import uuid
import hashlib
# from datetime import timedelta


app = Flask(__name__)
app.secret_key = 'aVeryLongAndComplexSecretKey12345!'

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_FILE_DIR'] = './flask_sessions'
app.config['SESSION_COOKIE_DOMAIN'] = 'localhost'
app.config['SESSION_COOKIE_PATH'] = '/'
Session(app)
CORS(app, supports_credentials=True)


def connect_to_database(db_name):
    db_url = "mongodb+srv://tzb:123qweasdzxc@cluster0.ly0rn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(db_url, server_api=ServerApi('1'))
    db = client["449project"]
    col = db[db_name]
    # try:
    #     client.admin.command('ping')
    #     print("Pinged your deployment. You successfully connected to MongoDB!")
    # except Exception as e:
    #     print(e)
    return col


def hash_password(password, salt=None, algorithm='sha512'):
    if not salt:
        salt = uuid.uuid4().hex  # Generate a new salt for hashing new password.
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    return salt, password_hash


@app.route('/auth', methods=['GET'])
def auth():
    print(session, file=sys.stderr)
    if 'username' in session:
        return {'username': session['username']}
    return {}


@app.route('/create', methods=['POST'])
def handle_create():
    username = request.json.get('username')
    password = request.json.get('password')
    col = connect_to_database("users")

    if col.find_one({"username": username}):
        return jsonify({"error": "Username already exists."}), 400

    salt, password_hash = hash_password(password)
    password_db_string = "$".join(['sha512', salt, password_hash])

    user = {"username": username, "password": password_db_string}
    col.insert_one(user)
    return jsonify({"message": "Successfully created an account."}), 201


@app.route('/login', methods=['POST'])
def handle_login():
    print(111, file=sys.stderr)
    username = request.json.get('username')
    password = request.json.get('password')
    col = connect_to_database("users")

    user = col.find_one({"username": username})
    if not user:
        return jsonify({"error": "Invalid username."}), 400

    stored_password = user['password']
    algorithm, salt, stored_hash = stored_password.split('$')

    _, password_hash = hash_password(password, salt, algorithm)
    
    if password_hash != stored_hash:
        return jsonify({"error": "Your password is incorrect."}), 400

    session['username'] = username
    session.modified = True
    print(session, file=sys.stderr)
    
    if not session['username']:
        return jsonify({"error": "No session."}), 400

    return jsonify({"message": "Successfully logged in. Redirecting"}), 200


@app.route('/logout', methods=['POST'])
def handle_logout():
    print(session, file=sys.stderr)
    session.pop('username', None)
    session.modified = True
    return jsonify({"message": "Successfully logged out."}), 200


@app.route('/change_password', methods=['POST'])
def handle_change_password():
    print(session, file=sys.stderr)
    if not session.get('username'):
        return jsonify({"error": "User not logged in."}), 401
    username = session.get('username')
    print(session.get('username'))
    password = request.json.get('password')
    new_password = request.json.get('new_password')
    col = connect_to_database("users")

    # Verify the login before allowing password change
    user = col.find_one({"username": username})
    if not user:
        return jsonify({"error": "Invalid username."}), 400

    stored_password = user['password']
    algorithm, salt, stored_hash = stored_password.split('$')
    
    # Verify the current password
    _, password_hash = hash_password(password, salt, algorithm)

    if password_hash != stored_hash:
        return jsonify({"error": "Your current password is incorrect."}), 400

    # Hash the new password
    new_salt, new_password_hash = hash_password(new_password)
    new_password_db_string = "$".join([algorithm, new_salt, new_password_hash])

    # Update the password in the database
    col.update_one({"username": username}, {"$set": {"password": new_password_db_string}})

    return jsonify({"message": "Password successfully changed."}), 200


@app.route('/delete', methods=['DELETE'])
def handle_delete():
    username = request.json.get('username')
    password = request.json.get('password')
    col = connect_to_database("users")

    # Verify the login before deleting
    user = col.find_one({"username": username})
    if not user:
        return jsonify({"error": "Invalid username."}), 400

    stored_password = user['password']
    algorithm, salt, stored_hash = stored_password.split('$')
    _, password_hash = hash_password(password, salt, algorithm)

    if password_hash != stored_hash:
        return jsonify({"error": "Your password is incorrect."}), 400

    result = col.delete_one({"username": username})
    if result.deleted_count > 0:
        return jsonify({"message": "User successfully deleted."}), 200
    return jsonify({"message": "No user found."}), 500


if __name__ == '__main__':
    # main()
    app.run(debug=True, port=5000)