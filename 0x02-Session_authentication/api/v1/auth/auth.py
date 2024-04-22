#!/usr/bin/env python3
"""It manages API authentication
"""

from typing import List, TypeVar
from flask import request
import os


class Auth():
    """Authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if authentication is required
        """
        
        if path is None:
            return None
        if excluded_paths is None or []:
            return True
        if path in excluded_paths:
            return False
        for ex_path in excluded_paths:
            if ex_path.startswith(path):
                return False
            if path.startswith(ex_path):
                return False
            elif ex_path[-1] == '*':
                if path.startswith(ex_path[:-1]):
                    return False
        return True
        
    
    def authorization_header(self, request=None) -> str:
        """Gets authorization header from request
        """
        if request is None:
            return None
        header = request.headers.get('Auhorization')

        if header is None:
            return None
        return header
    
    def current_user(self, request=None) -> TypeVar('User'):
        """It returns current user
        """

        return None
    def session_cookie(self, request=None):
        """It returns a cookie value from request
        """

        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
        
    

