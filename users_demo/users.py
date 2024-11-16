from flask import Flask, request, jsonify
import argparse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import uuid
import hashlib


app = Flask(__name__)


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


@app.route('/create', methods=['POST'])
def handle_create():
    email = request.json.get('email')
    password = request.json.get('password')
    col = connect_to_database("users")

    if col.find_one({"email": email}):
        return jsonify({"error": "Email already exists."}), 400

    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])

    user = {"email": email, "password": password_db_string}
    col.insert_one(user)
    return jsonify({"message": f"Successfully created an account with email: {email}"}), 201


@app.route('/login', methods=['POST'])
def handle_login():
    email = request.json.get('email')
    password = request.json.get('password')
    col = connect_to_database("users")

    user = col.find_one({"email": email})
    if not user:
        return jsonify({"error": "Invalid email."}), 400

    stored_password = user['password']
    algorithm, salt, stored_hash = stored_password.split('$')
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()

    if password_hash != stored_hash:
        return jsonify({"error": "Invalid password."}), 400

    return jsonify({"message": f"Successfully logged in with email: {email}"}), 200


@app.route('/delete', methods=['DELETE'])
def handle_delete():
    email = request.json.get('email')
    password = request.json.get('password')
    col = connect_to_database("users")

    # Verify the login before deleting
    user = col.find_one({"email": email})
    if not user:
        return jsonify({"error": "Invalid email."}), 400

    stored_password = user['password']
    algorithm, salt, stored_hash = stored_password.split('$')
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()

    if password_hash != stored_hash:
        return jsonify({"error": "Invalid password."}), 400

    result = col.delete_one({"email": email})
    if result.deleted_count > 0:
        return jsonify({"message": f"User with email {email} has been deleted."}), 200
    return jsonify({"error": "No user found."}), 404


# def main():
#     parser = argparse.ArgumentParser(description="User information demo.")
#     parser.add_argument("-o", "--operation", type=str, required=True, help="Operation (create, login, delete).")
#     parser.add_argument("-e", "--email", type=str, required=True, help="Email.")
#     parser.add_argument("-p", "--password", type=str, required=True, help="Password.")
#     args = parser.parse_args()
    
#     operation = args.operation
#     email = args.email
#     password = args.password
#     print(f"Operation: {operation} Email: {email} Password: {password}")
    
#     col = connect_to_database("users")

#     if operation == 'create':
#         handle_create(email, password, col)
#     elif operation == 'login':
#         handle_login(email, password, col)
#     elif operation == 'delete':
#         handle_delete(email, password, col)
#     else:
#         print("Invalid operation. Operations: create, login, delete")


if __name__ == '__main__':
    # main()
    app.run(debug=True)