#!/usr/bin/env python3
"""password hashing and user authentication module
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4

from typing import Union


def _hash_password(password: str) -> bytes:
    """This method takes in a password string 
    arguments and returns bytes.
    """

    salt = bcrypt.gensalt(rounds=16)
    encoded_pwd = password.encode('utf-8')
    hashed_pwd = bcrypt.hashpw(encoded_pwd, salt)
    return hashed_pwd


def _generate_uuid() -> str:
        """it generates a uuid (unique id)
        """
        id = str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """it initializes the Auth class
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[None, User]:
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


    def valid_login(self, email: str, password: str) -> bool:
        """it validates user credentials
        """

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password) 

    
        return id
    def create_session(self, email: str) -> str:
        """It takes an email string argument 
        and returns the session ID as a string.
        It finds the user corresponding to the email, 
        generate a new UUID and store it in the database 
        as the user’s session_id, then return the session ID.
        """

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            user.session_id = _generate_uuid()
            return user.session_id
        
    def get_user_from_session_id(self, session_id: str) -> User:
        """ It takes a single session_id string argument and 
        returns the corresponding User or None.
        If the session ID is None or no user is found, return None. 
        Otherwise return the corresponding user.
        """
        if session_id is None:
            return None
        user = self._db.find_user_by(session_id=session_id)
        if user is None:
            return None
        return user
    def destroy_session(self, user_id: int) -> None:
        """The method takes a single user_id integer 
        argument and returns None.
        It updates the corresponding user’s session ID to None.
        """

        try:
            user = self._db.find_user_by(user_id=user_id)
        except NoResultFound:
            return None
        else:
            user.session_id = None
            return None
    def get_reset_password_token(self, email: str) -> str:
        """Find the user corresponding to the email. 
        If the user does not exist, raise a ValueError 
        exception. If it exists, generate a UUID 
        and update the user’s reset_token database field. 
        Return the token."""

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        else:
            user.reset_token = _generate_uuid()
            return user.reset_token
   
   
    def update_password(self, reset_token: str, password: str) -> None:
        """Use the reset_token to find the corresponding user. If it does 
        not exist, raise a ValueError exception.
        Otherwise, hash the password and update the user’s hashed_password 
        field with the new hashed password and the reset_token field to None.
        """

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        else:
            user.hashed_password = _hash_password(password)
            user.reset_token = None
            return None