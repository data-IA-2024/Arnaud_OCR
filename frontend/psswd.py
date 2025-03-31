import os
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pprint import pprint
import json


# Store user in a non-sql DB
USER_DB = './users_db.json'

# Secret key to hide in production
SECRET_KEY = 'my_strongest_and_secret_password'

# Users dictionnary
users = {}

# Argon2 password hasher
ph = PasswordHasher(
    hash_len=32,
    salt_len=len(SECRET_KEY)
)

#######################################################################
###                    Password Utility functions                   ###
#######################################################################


def encrypt(message: str, key: str = SECRET_KEY):
    """ Password encryption. """
    return ph.hash(message, salt=key.encode('utf8'))


def verify_password(hashed_password, password):
    """ Password verification by using hash comparison. """
    try:
        ph.verify(hashed_password, password)
        return True
    except VerifyMismatchError:
        return False


#######################################################################
###                        User db functions                        ###
#######################################################################


def load_user(user_db_path: str = USER_DB):
    if os.path.isfile(user_db_path):
        with open(user_db_path, 'r') as f:
            return json.load(f)
    return {}


def save_users(user_db_path: str = USER_DB):
    with open(user_db_path, 'w') as f:
        json.dump(users, f)


def register_user(username, password):
    global users
    if username in users.keys():
        print(
            f"User : {username} already registered.\nUpdating password instead.")
    else:
        print(f"User : {username} registered.")
    users[username] = encrypt(password)
    save_users()


def dump_users():
    global users
    print(f"Listing users ...")
    pprint(users)


def verify_credentials(username, password):
    global users

    try:
        return verify_password(users[username], password)
    except KeyError:
        return False


# Loading User DB
users = load_user()

if __name__ == '__main__':
    register_user('a@gmail.com', '1234')
    register_user('steve', '5678')

    dump_users()