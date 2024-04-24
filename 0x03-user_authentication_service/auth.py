#!/usr/bin/env python3
"""password hashing module
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """This method takes in a password string 
    arguments and returns bytes.
    """

    salt = bcrypt.gensalt(rounds=16)
    encoded_pwd = password.encode('utf-8')
    hashed_pwd = bcrypt.hashpw(encoded_pwd, salt)
    return hashed_pwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """take mandatory email and password string arguments 
        and return a User object.
        If a user already exist with the passed email, raise a 
        ValueError with the message User <user's email> already exists
        If not, hash the password with _hash_password, save the user 
        to the database using self._db and return the User object.
        """

        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError('User {} already exists'.format(email))
