#!/usr/bin/env python3
"""It inherits from Auth
"""
from api.v1.auth.auth import Auth
from typing import TypeVar
import base64

from models.user import User

class BasicAuth(Auth):
    """It inherits from Auth
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """It returns Base64 part of 
        authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        
        token = authorization_header.split(' ')[-1]
        return token
    
    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """base64_authorization_header (str)
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            item_to_decode = base64_authorization_header.encode('utf-8')
            decoded = base64.b64decode(item_to_decode)
            return decoded.decode('utf-8')
        except Exception:
            return None
    
    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str): # type: ignore
        """Extracts users' credentials
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        email, password = decoded_base64_authorization_header.split(':')
        return (email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """_summary_

        Args:
                        self (_type_): _description_
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'): # type: ignore
        """_summary_
        """
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            token = self.extract_base64_authorization_header(auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, password = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(
                            email, password)

        return