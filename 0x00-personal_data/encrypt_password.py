#!/usr/bin/python3
"""password encryption and validation module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """function that expects one string argument 
    name password and returns a salted, hashed 
    password, which is a byte string.
    """

    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode(), salt)

    return hashed_pwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if password matches
    """

    valid = False
    
    if bcrypt.checkpw(password.encode(), hashed_password):
        valid = True
    
    return valid




