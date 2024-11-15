import argparse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import uuid
import hashlib


def connect_to_database(db_name):
    db_url = "mongodb+srv://tzb:123qweasdzxc@cluster0.ly0rn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(db_url, server_api=ServerApi('1'))
    db = client["449project"]
    col = db[db_name]
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return col


def handle_create(email, password, col):
    # Check if email already exists.
    if col.find_one({"email": email}):
        print("email already exists.")
        return

    # Hash the password.
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])

    # Create the initial user info.
    user = {
        "email": email,
        "password": password_db_string
    }

    # Insert the new user to MongoDB.
    col.insert_one(user)
    print(f"Successfully create an account with email: {email}")


def handle_login(email, password, col):
    # Check if email is valid.
    user = col.find_one({"email": email})
    if not user:
        print("Invalid email.")
        return
    
    # Hash the password.
    stored_password = user['password']
    algorithm, salt, stored_hash = stored_password.split('$')
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()

    # Compare hased password.
    if password_hash != stored_hash:
        print("Invalid password.")
        return

    print(f"Successfully login with email: {email}")
    return


def handle_delete(email, password, col):
    # First login the account.
    handle_login(email, password, col)

    # Remove the user from mongoDB.
    result = col.delete_one({"email": email})

    # Check if a document was deleted, for debug.
    if result.deleted_count > 0:
        print(f"User with email {email} has been deleted.")
    else:
        print(f"No user found with email {email}.")


def main():
    parser = argparse.ArgumentParser(description="User information demo.")
    parser.add_argument("-o", "--operation", type=str, required=True, help="Operation (create, login, delete).")
    parser.add_argument("-e", "--email", type=str, required=True, help="Email.")
    parser.add_argument("-p", "--password", type=str, required=True, help="Password.")
    args = parser.parse_args()
    
    operation = args.operation
    email = args.email
    password = args.password
    print(f"Operation: {operation} Email: {email} Password: {password}")
    
    col = connect_to_database("users")

    if operation == 'create':
        handle_create(email, password, col)
    elif operation == 'login':
        handle_login(email, password, col)
    elif operation == 'delete':
        handle_delete(email, password, col)
    else:
        print("Invalid operation. Operations: create, login, delete")


if __name__ == '__main__':
    main()
